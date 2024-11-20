<script setup lang="ts">
import { ref, computed } from 'vue';
import Modal from "@/components/template/Modal.vue";
import ExitButton from "@/components/ExitButton.vue"

interface Ticket {
  id: number;
  title: string;
  status: 'Ожидает назначения' | 'В обработке' | 'Завершено';
  comments: string[];
}

const tickets = ref<Ticket[]>([
  { id: 1, title: 'Ошибка в системе', status: 'В обработке', comments: [] },
  { id: 2, title: 'Не работает кнопка', status: 'В обработке', comments: [] },
  { id: 3, title: 'Проблемы с сервером', status: 'Завершено', comments: [] }
]);

const selectedFilter = ref('all')
const showModal = ref(false);
const comment = ref('');
const selectedTicketId = ref<number | null>(null);


const filteredTickets = computed(() => {
  if (selectedFilter.value === 'all') {
    return tickets.value
  }
  return tickets.value.filter(ticket => ticket.status === selectedFilter.value)
})

const addComment = (ticketId: number) => {
  showModal.value = true;
  selectedTicketId.value = ticketId
}

const saveComment = () => {
  if (selectedTicketId.value !== null) {
    const ticket = tickets.value.find(ticket => ticket.id === selectedTicketId.value);
    if (ticket && comment.value) {
      ticket.comments.push(comment.value)
      comment.value = ''
      showModal.value = false
    }
  }
};

const completeTicket = (ticketId: number) => {
  const ticket = tickets.value.find(ticket => ticket.id === ticketId)
  if (ticket) {
    ticket.status = 'Завершено'
  }
}
</script>
<template>
  <div class="wrapper">
    <ExitButton class="exit__btn"/>
    <div class="wrapper__container">
      <div class="avatar">
        <div class="avatar__photo">M</div>
        <div class="avatar__name">
            <p>Михаил Фролов</p>
          <p class="avatar__name-status">Технический специалист</p>
        </div>
      </div>
      <div class="support-manager-dashboard mt-5">      
        <div class="tickets-section">
          <div class="tickets-header">
            <h2 class="section-title pb-3">Заявки на обработку</h2>
            <div class="filter-container">
              <select v-model="selectedFilter" class="form-select mb-3">
                <option value="all">Все заявки</option>
                <option value="В обработке">В обработке</option>
                <option value="Завершено">Завершенные</option>
              </select>
            </div>
          </div>
      
          <div class="tickets-list">
            <div 
              class="ticket-card" 
              v-for="ticket in filteredTickets" 
              :key="ticket.id" 
              :data-status="ticket.status"
              :class="{'ticket-processing': ticket.status === 'В обработке', 'ticket-completed': ticket.status === 'Завершено'}"
            >
              <div class="ticket-info">
                <p class="ticket-id">Заявка #{{ ticket.id }}</p>
                <p class="ticket-title bold">Тема обращения: {{ ticket.title }}</p>
                <p class="ticket-status" :class="ticket.status.toLowerCase()">
                  {{ ticket.status }}
                </p>
                <div v-if="ticket.comments.length > 0" class="ticket-comments">
                  <p><strong>Комментарии:</strong></p>
                  <ul style="padding-left: 15px;">
                    <li v-for="(comment, index) in ticket.comments" :key="index">{{ comment }}</li>
                  </ul>
                </div>
              </div>
      
              <div class="ticket-actions">
                <button 
                  v-if="ticket.status === 'В обработке'" 
                  class="btn btn-success" 
                  @click="completeTicket(ticket.id)"
                >
                  Завершить
                </button>
                <button 
                  class="btn btn-comment" 
                  @click="addComment(ticket.id)"
                >
                  Комментарий
                </button>
              </div>
            </div>
          </div>
        </div>
      
        <Modal v-model="showModal" :overlayClick="false" :showCloseButton="true" :header="'Комментарий'">
          <template #body>
            <textarea v-model="comment" placeholder="Напишите ваш комментарий..."></textarea>
            <button @click="saveComment" class="btn btn-primary">Сохранить</button>
          </template>
        </Modal>
      </div>    

    </div>

  </div>
</template>

<style scoped lang="scss">
.dashboard-title {
  font-size: 24px;
  font-weight: bold;
  opacity: 60%;
  text-align: end;
}
.tickets-list {
  display: flex;
    flex-direction: column;
    gap: 20px;
}
.ticket-actions {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.ticket-processing {
  background-color: #f0f8ff; 
}

.ticket-completed {
  background-color: #d4edda; 
}

.ticket-card {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.ticket-actions button {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-comment {
  background-color: #ffc107;
  color: white;
}

textarea {
  width: 100%;
  height: 100px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.avatar {
  width: 100%;
  display: flex;
  column-gap: 10px;
  position: fixed;
  align-items: center;
  top: 30px;
  left: 30px;
  &__photo {
    width: 50px;
    height: 50px;
    border-radius: 8px;
    background-color: #2e0ae4;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 20px;
    color: #fff;

  }
  &__name {
    &-status {
      color: #989898;
      font-size: 14px;
    }
  }
}
</style>
