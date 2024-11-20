<template>
  <div class="new-ticket">
    <form @submit.prevent="submitTicket" class="ticket-form">
      <div class="form-group">
        <label for="formFile" class="form-label">Категория обращения</label>
        <select v-model="ticket.category" class="form-select" required>
          <option value="" disabled selected>Выберите категорию</option>
          <option value="technical">Техническая проблема</option>
          <option value="account">Вопрос по аккаунту</option>
          <option value="billing">Вопрос по платежам</option>
          <option value="other">Другое</option>
        </select>
      </div>

      <div class="form-group">
        <label for="description">Описание проблемы</label>
        <textarea
          v-model="ticket.description"
          id="description"
          class="form-control"
          rows="6"
          placeholder="Подробно опишите вашу проблему..."
          required
        ></textarea>
      </div>

      <div class="form-group">
        <label for="attachment">Прикрепить файл (не обязательно)</label>
        <input
          type="file"
          id="attachment"
          @change="handleFileUpload"
          class="form-control"
        />
        <span v-if="fileName" class="file-name">{{ fileName }}</span>
      </div>

      <div class="form-group">
        <button type="submit" :disabled="isSubmitting" class="btn btn-primary">
          {{ isSubmitting ? "Отправка..." : "Отправить" }}
        </button>
      </div>
    </form>

    <div
      v-if="submissionStatus"
      :class="submissionStatus.success ? 'success' : 'error'"
      class="submission-status"
    >
      {{ submissionStatus.message }}
    </div>
  </div>
</template>

<script setup lang="ts">
import axios from "axios";
import { ref } from "vue"

const emit = defineEmits(["success"])

const ticket = ref({
  category: "",
  description: "",
})

const file = ref(null)
const fileName = ref("")
const isSubmitting = ref(false)
const submissionStatus = ref(null)

const handleFileUpload = (event) => {
  const uploadedFile = event.target.files[0]
  if (uploadedFile) {
    file.value = uploadedFile
    fileName.value = uploadedFile.name
  }
}

const submitTicket = async () => {
  isSubmitting.value = true;

  try {
    const response = await axios.post("http://localhost:8888/api/v1/task/create-task",
    {
        header: ticket.value.category,
        description: ticket.value.description,
      },
    {
        headers: {
          "Content-Type": "application/json",
          'Authorization': `Bearer ${getAuthToken()}`,
          Accept: "application/json",
        },
        withCredentials: true,
    })

    console.log('Response:', response.data)
    emit('success')

  } catch (error) {
    alert('Произошла ошибка при отправке обращения. Попробуйте еще раз')
    console.error(error)
  } finally {
    isSubmitting.value = false
  }
};


</script>

<style scoped lang="scss">
.new-ticket {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin: 0 auto;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.form-group .form-control {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.form-group .file-name {
  display: block;
  margin-top: 10px;
  font-size: 14px;
  color: #666;
}

.btn {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:disabled {
  background-color: #ccc;
}

.submission-status {
  margin-top: 20px;
  padding: 10px;
  font-size: 16px;
  border-radius: 4px;
  text-align: center;
}

.success {
  background-color: #d4edda;
  color: #155724;
}

.error {
  background-color: #f8d7da;
  color: #721c24;
}

textarea {
  resize: vertical;
  &::placeholder {
    font-size: 16px;
    font-family: sans-serif;
  }
  &:focus {
    border: 1px solid var(--border-color);
    outline: none !important;
    &::placeholder {
      color: transparent;
    }
  }
}
</style>
