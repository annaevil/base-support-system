<script setup lang="ts">
import { storeToRefs } from "pinia"
import { useUserStore } from "@/store/userData"
import InputControl from "@/components/template/InputControl.vue"
import SubmitControl from "@/components/template/SubmitControl.vue"
import Modal from "@/components/template/Modal.vue"
import NewTicket from "@/components/NewTicket.vue"

import { onMounted, reactive, computed, ref } from "vue"

// import axios from "axios"

const userStore = useUserStore()

const { avatarColor, initial } = storeToRefs(userStore)

const tabs = computed(() => [
  { label: "Профиль", key: "profile" },
  { label: "История обращений", key: "history" },
  { label: "Обратная связь", key: "support" },
  { label: "Полезные ссылки", key: "links" },
  { label: "Настройки уведомлений", key: "pushes" },
  { label: "Информация о подписке", key: "subscription" },
  { label: "Часто задаваемые вопросы", key: "faq" },
])

const tab = ref("profile")
const userId = 1
const openModal = ref(false)

const emit = defineEmits(["update:modelValue", "loaded"])

const form = reactive({
  name: "",
  surname: "",
  email: "",
  phone: "",
})

const rules = computed(() => ({
  name: {
    required: requiredRule(),
  },
  surname: {
    required: requiredRule(),
  },
  email: {
    required: requiredRule(),
    email: emailRule(),
  },
}))

const faqs = [
  {
    question: "Как отменить подписку?",
    answer: 'Для того, чтобы подробнее узнать о текущем тарифе или отмене подписки, перейдите в раздел "Информация о подписке" в настройках.',
  },
  {
    question: "Как изменить данные профиля?",
    answer: 'Вы можете изменить ваши данные в разделе "Профиль" в удобном меню, которое находится слева',
  },
  {
    question: "Когда служба поддержки ответит на мое обращение?",
    answer:
      'Мы передадим вашу заявку первому свободному оператору. Обычно ответ не занимает больше, чем 2 рабочих дня',
  },
  {
    question: "Что делать, если приложение не работает?",
    answer: "Попробуйте перезапустить приложение или проверьте ваше интернет-соединение. Если проблема сохраняется, то вы можете связаться с нами любым удобным для вас сопособом. контакты находятся в меню слева <--" ,
  },
  {
    question: "Как обновить приложение?",
    answer: "Обновления выходят автоматически. Мы уведомляем обо всех изменениях, если вы не хотите пропустить важные новости, то проверьте разрешение в 'Настроках уведомлений'",
  },
]

const isOpen = ref<number>(0)

const toggleAnswer = (index: number): void => {
  isOpen.value = isOpen.value === index ? -1 : index
}

const v$ = useVuelidate(rules, form)

const loadProfileData = async () => {
  // try {
  //     const response = await axios.get(
  //         `${getOrigin()}/api/v3/users/${userId}/profile`,
  //         {
  //             headers: {
  //                 Authorization: `Bearer ${getAuthToken()}`,
  //             },
  //         }
  //     )
  //     form.name = response.data.first_name || ''
  //     form.surname = response.data.last_name || ''
  //     form.email = response.data.email || ''
  //     form.phone = response.data.phone || ''
  //     const userStore = useUserStore()
  //     userStore.setUserData(
  //         response.data.first_name,
  //         response.data.last_name,
  //         response.data.email
  //     )
  // } catch (error) {
  //     console.error('Ошибка при получении данных профиля:', error)
  // }
}

onMounted(() => {
  loadProfileData()
})

const saveProfile = async () => {
  try {
    const response = await fetch(`/api/v3/users/${userId}/profile`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${getAuthToken()}`,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        first_name: form.name,
        last_name: form.surname,
        email: form.email,
        phone: form.phone,
      }),
    })
    v$.value.$touch()
    userStore.setUserData(form.name, form.surname, form.email)
    if (!v$.value.$invalid) {
      await handleResponse(response, "Изменения сохранены")
    } else if (!response.ok) {
      const errorMessage =
        response.status === 404
          ? "Профиль не найден"
          : "Что-то пошло не так, попробуйте позднее"
      await handleResponse(response, errorMessage)
      return
    }
  } catch (error) {
    console.error("Ошибка:", error)
  }
}
</script>
<template>
  <div class="wrapper">
    <div class="wrapper__container">
      <div class="sidebar">
        <div class="sidebar__section">
          <div class="sidebar__link">
            <h2 class="sidebar__title">Base Support</h2>
            <button
              class="sidebar__link-item"
              v-for="tabItem in tabs"
              :key="tabItem.key"
              :class="{ active: tab === tabItem.key }"
              @click="tab = tabItem.key"
            >
              {{ tabItem.label }}
            </button>
          </div>
          <div class="">
              <button class="sidebar__btn" @click.prevent="openModal = true">
                Новое обращение
                <svg
                  width="12"
                  height="12"
                  viewBox="0 0 12 12"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M6.83341 6.83366V11.8337H5.16675V6.83366H0.166748V5.16699H5.16675V0.166992H6.83341V5.16699H11.8334V6.83366H6.83341Z"
                    fill="#00b46d"
                  />
                </svg>
              </button>
              <div class="class__icons d-flex justify-content-evenly align-items-center mt-4">
               
                <a href=""><i class="bi bi-whatsapp"></i></a>
                <a href="tel:+49999999999"><svg class="svg" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                    width="40px" height="40px" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">
               <g>
                   <path d="M256,32c123.5,0,224,100.5,224,224S379.5,480,256,480S32,379.5,32,256S132.5,32,256,32 M256,0C114.625,0,0,114.625,0,256
                       s114.625,256,256,256s256-114.625,256-256S397.375,0,256,0L256,0z M398.719,341.594l-1.438-4.375
                       c-3.375-10.062-14.5-20.562-24.75-23.375L334.688,303.5c-10.25-2.781-24.875,0.969-32.405,8.5l-13.688,13.688
                       c-49.75-13.469-88.781-52.5-102.219-102.25l13.688-13.688c7.5-7.5,11.25-22.125,8.469-32.406L198.219,139.5
                       c-2.781-10.25-13.344-21.375-23.406-24.75l-4.313-1.438c-10.094-3.375-24.5,0.031-32,7.563l-20.5,20.5
                       c-3.656,3.625-6,14.031-6,14.063c-0.688,65.063,24.813,127.719,70.813,173.75c45.875,45.875,108.313,71.345,173.156,70.781
                       c0.344,0,11.063-2.281,14.719-5.938l20.5-20.5C398.688,366.062,402.062,351.656,398.719,341.594z"/>
               </g>
               
               </svg></a>
               <a href="" style="margin-left: 10px"><i class="bi bi-telegram"></i></a>
              </div>

          </div>
        </div>
      </div>

      <div class="content">
        <div class="profile-body">
          <div class="profile__tabs" v-show="tab === 'profile'">
            <div class="profile-body__info">
              <div class="profile-body__avatar" :style="{ backgroundColor: avatarColor }">
                {{ initial }}
              </div>
              <div class="profile-body__text">
                <div class="profile-body__name">
                  {{ userStore.fullName }}
                </div>
                <div class="profile-body__email">
                  {{ userStore.email }}
                </div>
              </div>
            </div>
            <div class="profile-content">
              <form class="profile-form" @submit.prevent="saveProfile">
                <InputControl
                  :type="'text'"
                  :name="'name'"
                  :label="'Имя'"
                  :class="'profile-form__input'"
                  :placeholder="''"
                  :prop="'name'"
                  :required="true"
                  :error="v$.name.$error"
                  :errors="v$.$errors"
                  v-model="v$.name.$model"
                />
                <InputControl
                  :type="'text'"
                  :name="'surname'"
                  :label="'Фамилия'"
                  :class="'profile-form__input'"
                  :placeholder="''"
                  :prop="'surname'"
                  :required="true"
                  :error="v$.surname.$error"
                  :errors="v$.$errors"
                  v-model="v$.surname.$model"
                />
                <div class="profile-form__row">
                  <InputControl
                    :type="'text'"
                    :name="'email'"
                    :label="'E-mail'"
                    :class="'profile-form__input'"
                    :placeholder="''"
                    :prop="'email'"
                    :required="true"
                    :error="v$.email.$error"
                    :errors="v$.$errors"
                    v-model="v$.email.$model"
                  />
                  <InputControl
                    :type="'text'"
                    :name="'phone'"
                    :label="'Телефон'"
                    :class="'profile-form__input'"
                    :placeholder="''"
                    :prop="'phone'"
                    :mask="{
                      mask: '+9{11,14}',
                      showMaskOnHover: false,
                    }"
                    :required="false"
                    v-model="form.phone"
                  />
                </div>

                <SubmitControl
                  :ring="false"
                  :processing="false"
                  :labelSend="'Сохранить'"
                  :disabled="v$.$silentErrors.length !== 0"
                  class="profile-form__submit"
                />
              </form>
            </div>
          </div>

          <div v-show="tab === 'history'">
            <h2 class="pb-4">История обращений</h2>
            <ul class="history-list">
              <li class="history-item">
                <div class="history-item__title">Обращение №1</div>
                <div class="history-item__status">Статус: Ожидает ответа</div>
                <div class="history-item__date">Дата: 12 Октября 2024</div>
              </li>
              <li class="history-item">
                <div class="history-item__title">Обращение №2</div>
                <div class="history-item__status">Статус: Закрыто</div>
                <div class="history-item__date">Дата: 1 Октября 2024</div>
              </li>
            </ul>
          </div>

          <div v-show="tab === 'support'">
            <h2 class="pb-4">Обратная связь с поддержкой</h2>
            <div class="ticket-item">
              <div class="ticket-info">
                <span class="ticket-status">Ожидает ответа</span>
                <div class="ticket-description">
                  <strong>Тема:</strong> Проблемы с подключением
                </div>
              </div>
              <button class="btn btn-primary">Просмотреть</button>
            </div>
            <div class="ticket-item">
              <div class="ticket-info">
                <span class="ticket-status">Закрыт</span>
                <div class="ticket-description">
                  <strong>Тема:</strong> Ошибка в аккаунте
                </div>
              </div>
              <button class="btn btn-secondary">Просмотреть</button>
            </div>
          </div>

          <div v-show="tab === 'links'">
            <h2 class="pb-4">Полезные ссылки</h2>
            <ul class="links__list">
              <li class="links__list-item">
                <a href="#"><span>✓</span> Документация</a>
              </li>
              <li class="links__list-item">
                <a href="#"><span>✓</span> С чего начать?</a>
              </li>
              <li class="links__list-item">
                <a href="#"><span>✓</span> Руководство пользователя</a>
              </li>
              <li class="links__list-item">
                <a href="#"><span>✓</span> Контакты для связи</a>
              </li>
              <li class="links__list-item">
                <a href="#"><span>✓</span> Сообщество пользователей</a>
              </li>
              <li class="links__list-item">
                <a href="#"><span>✓</span> Политика конфиденциальности</a>
              </li>
              <li class="links__list-item">
                <a href="#"><span>✓</span> Обновления и новости</a>
              </li>
              <li class="links__list-item">
                <a href="#"><span>✓</span> Отзывы и предложения</a>
              </li>
            </ul>
          </div>

          <div v-show="tab === 'pushes'">
            <h2 class="pb-4">Настройки уведомлений</h2>
            <label for="flexCheckDefault" class="form-check-label pb-3">
              <input
                type="checkbox"
                class="form-check-input"
                id="flexCheckDefault"
                checked
              />
              Получать уведомления о новых ответах
            </label>
            <label for="flexCheckDefault" class="form-check-label pb-3">
              <input
                type="checkbox"
                class="form-check-input"
                id="flexCheckDefault"
                checked
              />
              Получать уведомления о статусах обращения
            </label>
            <label for="flexCheckDefault" class="form-check-label">
              <input
                type="checkbox"
                class="form-check-input"
                id="flexCheckDefault"
                checked
              />
              Получать уведомления о новостях и предложениях
            </label>
          </div>

          <div v-show="tab === 'subscription'">
            <h2 class="pb-4">Информация о подписке</h2>
            <div class="subscription-info">
              <b>Текущий тариф:</b> Стандартный
              <div class="subscription-details pt-2">
                <span>Дата окончания: 30 ноября 2025</span>
              </div>
              <div class="mt-3"><i class="bi bi-info-circle"></i>За месяц до окончания срока, мы напомним вам об оплате. Для большего удобства вы можете подключить автоплатеж. </div>
            </div>
            <button class="btn btn-secondary mt-5">Изменить тариф</button>
          </div>

          <div v-show="tab === 'faq'">
            <h2 class="pb-4">Часто задаваемые вопросы</h2>
            <ul class="faq-list">
              <li v-for="(faq, index) in faqs" :key="index" class="faq-item">
                <div
                  class="faq-question"
                  @click="toggleAnswer(index)"
                  :class="{ 'is-open': isOpen === index }"
                >
                  {{ faq.question }}
                  <span class="faq-toggle-icon">{{ isOpen === index ? "‒" : "+" }}</span>
                </div>

                <div
                  v-show="isOpen === index"
                  class="faq-answer"
                  :style="{
                    height: isOpen === index ? 'auto' : '0',
                    opacity: isOpen === index ? 1 : 0,
                  }"
                >
                  {{ faq.answer }}
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
  <Modal
    v-model="openModal"
    :overlayClick="false"
    :showCloseButton="true"
    :header="'Новое обращение в поддержку'"
  >
    <template #body>
      <NewTicket />
    </template>
  </Modal>
</template>

<style scoped lang="scss">
.wrapper {
  display: flex;
  justify-content: flex-start;
  &__container {
    margin-left: 100px;
  }
}
.sidebar {
  width: 250px;
  background-color: #fff;
  position: fixed;
  height: 100%;
  top: 0;
  left: 0;
  border-right: 1px solid #dbe8ff;
  &__section {
    margin-bottom: 30px;
    display: flex;
    justify-content: space-between;
    flex-direction: column;
    height: 100%;
    padding-bottom: 70px;
  }
  &__title {
    font-size: 18px;
    padding-left: 20px;
    margin-bottom: 50px;
    background: linear-gradient(to right, #004ca3 0%, #00d4e0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 30px;
    font-weight: normal;
  }
  &__link {
    display: flex;
    flex-direction: column;
    &-item {
      color: #007bff;
      text-decoration: none;
      padding: 10px 0 10px 20px;
      transition: 0.2s;
      font-size: 16px;
      background: none;
      text-align: left;
      &:hover {
        background-color: #eaf2ff;
      }
    }
  }
  &__btn {
    width: fit-content;
    margin-left: auto;
    margin-right: auto;
    padding: 13px 37px;
    background: none;
    color: var(--green-color);
    border: 1px solid var(--green-color);
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 16px;
    &:hover {
      background-color: #00b46c33;
    }
  }
}
.sidebar__link-item.active {
  background-color: #eaf2ff;
}

.content {
  margin-left: 250px;
  width: 100%;
}

.profile-body__info {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.profile-body__avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #007bff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 20px;
  margin-right: 20px;
}

.profile-body__text {
  display: flex;
  flex-direction: column;
}

h2 {
  margin-top: 30px;
  font-size: 24px;
  font-weight: bold;
}

.ticket-item,
.history-item {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 10px;
}

.ticket-status {
  color: #28a745;
}

.btn {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-secondary {
  background-color: #007bff;
  &:hover {
    background-color: #1f8afc;
  }
}

label {
  font-size: 20px;
}

.subscription-info {
  background-color: #e9fff6;
  border-radius: 7px;
  padding: 15px 10px;
}

.links__list {
  list-style: none;
  &-item {
    font-size: 20px;
    a:hover {
      color: var(--link-color-hover);
    }
    span {
      font-size: 25px;
    }
  }
}
.faq-list {
  list-style: none;
}
.faq-question {
  cursor: pointer;
  font-weight: normal;
  transition: all 0.3s ease;
  padding: 15px;
  font-size: 20px;
  color: var(--text-color-headers);
  background-color: #00b46c14;
  border-radius: 7px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.faq-question.is-open {
  background-color: #00b46c33;
}

.faq-toggle-icon {
  font-size: 20px;
  transition: transform 0.3s ease;
}

.faq-answer {
  height: 0;
  opacity: 0;
  overflow: hidden;
  transition: all 0.3s ease;
  padding: 0 15px;
}

.faq-answer[style*="height: auto"] {
  max-height: 500px;
  opacity: 1;
  padding: 15px;
}
i {
    font-size: 40px;
    color: transparent;
    margin-right: 10px;
    overflow: hidden;
    width: min-content;
    transition: all .3s;
}
.bi-telegram {
    color: #007bff;
    &:hover {
        color: #14d8ff;
    }
}
.bi-whatsapp {
    color: var(--green-color);
    &:hover {
        color: #14ea86;
    }
}
.svg:hover {
    fill: #5e5e5e;
}
.class__icons {
    margin-left: 10px;
}

.bi-info-circle {
color: var(--text-color);
font-size: 16px;
}
</style>
