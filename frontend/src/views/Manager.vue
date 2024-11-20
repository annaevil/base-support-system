<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Modal from "@/components/template/Modal.vue"
import axios from 'axios'
import ExitButton from "@/components/ExitButton.vue"

const selectedFilter = ref('all')
const showModal = ref(false)
const comment = ref('')
const selectedTicketId = ref<number | null>(null)
const tickets = ref([])


const filteredTickets = computed(() => {
  if (selectedFilter.value === 'all') {
    return tickets.value
  }
  return tickets.value.filter(ticket => ticket.status === selectedFilter.value)
})


const loadTasks = async () => {
  try {
    const token = getAuthToken() 
    const response = await axios.get('http://localhost:8888/api/v1/task/load_tasks', {
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
        'Accept': 'application/json'
      },
      withCredentials: true
    })

    tickets.value = response.data
    console.log('Задачи:', tickets.value)
  } catch (error) {
    console.error('Ошибка при загрузке задач:', error)
    alert('Ошибка при загрузке задач. Попробуйте еще раз.')
  }
}

const saveComment = () => {
  showModal.value = false
}

const addComment = (ticketId: number) => {
  showModal.value = true;
  selectedTicketId.value = ticketId
}


const startProcessing = (ticketId: number) => {
  const ticket = tickets.value.find(ticket => ticket.id === ticketId)
  if (ticket) {
    ticket.status = 'work'
  }
}

onMounted(() => {
  loadTasks()
})
</script>

<template>
  <div class="wrapper">
    <ExitButton class="exit__btn"/>
    <div class="wrapper__container">
      <div class="support-manager-dashboard">
        <div class="avatar">
          <div class="avatar__photo">Н</div>
          <div class="avatar__name">
            <p>Надежда Краснова</p>
            <p class="avatar__name-status">Менеджер</p>
          </div>
        </div>

        <div class="tickets-section">
          <div class="tickets-header">
            <h2 class="section-title pb-3">Заявки на обработку</h2>
            <div class="filter-container">
              <select v-model="selectedFilter" class="form-select mb-3">
                <option value="all">Все заявки</option>
                <option value="Ожидает назначения">Ожидает назначения</option>
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
            >
              <div class="ticket-info">
                <p class="ticket-id">Заявка #{{ ticket.id.slice(0, 3) }}</p>
                <div class="history-item__date pb-3">Дата: {{ new Date(ticket.created_at).toLocaleDateString() }}</div>
                <p class="fw-bold">Тема: {{ticket.header}}</p>
                <div class="history-item__title pb-2">Текст обращения: {{ ticket.description }}</div>
                <p class="ticket-status" :class="ticket.status.toLowerCase()">
                  Статус: {{ ticket.status }} 
                </p>
                <p class="mt-2" v-if="ticket.status === 'Завершено'">Tехнический специалист: <b>Михаил Фролов</b></p>
                <div v-if="ticket.comments?.length > 0" class="ticket-comments">
                  <p><strong>Комментарии:</strong></p>
                  <ul>
                    <li v-for="(comment, index) in ticket.comments" :key="index">{{ comment }}</li>
                  </ul>
                </div>
              </div>

              <div class="ticket-actions">
                <button class="btn btn-primary" v-if="ticket.status === 'new'" @click="startProcessing(ticket.id)">
                  Взять в работу
                </button>
                <button class="btn btn-success" v-if="ticket.status === 'dev'" @click="assignTicket(ticket.id)">
                  Назначить
                </button>
                <button class="btn btn-comment" v-if="ticket.status !== 'compled'" @click="addComment(ticket.id)">
                  Комментарий 
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.83341 6.83366V11.8337H5.16675V6.83366H0.166748V5.16699H5.16675V0.166992H6.83341V5.16699H11.8334V6.83366H6.83341Z" fill="#000"/>
                  </svg>
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
.support-manager-dashboard {
  padding: 20px;
  width: 100%;
}

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

.ticket-card {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.ticket-info {
  display: flex;
  flex-direction: column;
}

.ticket-id {
  font-weight: bold;
}

.ticket-status {
  font-style: italic;
  color: #28a745;
}

.ticket-card[data-status="Ожидает назначения"] {
  background-color: #f2f2f2;
}

.ticket-card[data-status="work"] {
  background-color: #06ff7d1a;

}

.ticket-card[data-status="Завершено"] {
  background-color: #bfffce; 
}

.ticket-actions {
    display: flex;
    flex-direction: column;
    gap: 15px;
    button {
        padding: 8px 15px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
}

.assign-btn {
  background-color: #28a745;
  color: white;
}

.process-btn {
  background-color: #007bff;
  color: white;
}

.comment-btn {
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

.ticket-comments {
  margin-top: 10px;
}

.ticket-comments ul {
  list-style-type: none;
  padding-left: 0;
}

.ticket-comments li {
  padding: 5px 0;
}

.btn-comment {
    background-color: #fff;
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
    background-color: #f16eff;
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

.btn-comment {
  background-color: #bbf5c1;
}
</style>
