<script setup lang="ts">
import { storeToRefs } from "pinia"
import { useUserStore } from "@/store/userData"
import InputControl from "@/components/template/InputControl.vue"
import SubmitControl from "@/components/template/SubmitControl.vue"
import UserTicketsList from "@/components/UserTicketsList.vue"

import { onMounted, ref, reactive, computed } from "vue"

// import axios from "axios"

const userStore = useUserStore()

const { avatarColor, initial } = storeToRefs(userStore)

const tabs = computed(() => [
  { label: "Профиль", key: "profile" },
  { label: "Мои обращения", key: "tickets" },
])

const tab = ref("profile")
const userId = 1

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
      const response = await fetch(
          `/api/v3/users/${userId}/profile`,
          {
              method: 'POST',
              headers: {
                  Authorization: `Bearer ${getAuthToken()}`,
                  'Content-Type': 'application/x-www-form-urlencoded',
              },
              body: new URLSearchParams({
                  first_name: form.name,
                  last_name: form.surname,
                  email: form.email,
                  phone: form.phone,
              }),
          }
      )
      v$.value.$touch()
      userStore.setUserData(
          form.name,
          form.surname,
          form.email,
      )
      if (!v$.value.$invalid) {
          await handleResponse(response, 'Изменения сохранены')
      } else if (!response.ok) {
          const errorMessage =
              response.status === 404
                  ? 'Профиль не найден'
                  : 'Что-то пошло не так, попробуйте позднее'
          await handleResponse(response, errorMessage)
          return
      }
  } catch (error) {
      console.error('Ошибка:', error)
  }
}
</script>

<template>
  <div class="wrapper">
    <div class="wrapper__container">
      <div class="profile-body">
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
        <div class="profile__tabs">
          <div class="profile__tabs-btns">
            <button
              v-for="tabItem in tabs"
              class="tab"
              :key="tabItem.key"
              :class="{ active: tab === tabItem.key }"
              @click="tab = tabItem.key"
            >
              {{ tabItem.label }}
            </button>
          </div>
          <div class="profile-content" v-show="tab === 'profile'">
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
          <div class="profile-content" v-show="tab === 'tickets'">
            <UserTicketsList />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 45px;
}

.profile-body {
  &__info {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
  }

  &__avatar {
    border-radius: 20px;
    width: 96px;
    height: 96px;
    color: #fff;
    font-size: 35px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-shrink: 0;
    @media (max-width: 450px) {
      width: 70px;
      height: 70px;
      border-radius: 5px;
    }
  }

  &__text {
    padding-left: 25px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    @media (max-width: 450px) {
      padding-left: 15px;
    }
  }

  &__name {
    font-weight: 700;
    font-size: 28px;
    line-height: 114%;
    max-width: min-content;
    @media (max-width: 450px) {
      font-size: 18px;
      text-wrap: wrap;
    }
  }

  &__email {
    font-weight: 500;
    line-height: 154%;
  }
  .profile-content {
    width: 100%;
  }
}

.profile-form {
  display: flex;
  flex-direction: column;

  &__input {
    margin-bottom: 20px;
    flex: 1;
  }

  &__row {
    display: flex;
    gap: 20px;
    &:last-child {
      border-bottom: 1px solid var(--btn-gray-color);
      width: 100%;
      padding-bottom: 20px;
    }
    @media (max-width: 1080px) {
      flex-direction: column;
    }
    @media (max-width: 720px) {
      gap: 0;
    }
  }
  &__change {
    padding-bottom: 25px;
    border-bottom: 1px solid var(--btn-gray-color);
  }

  &__change-btn {
    background: none;
    border: 1px solid var(--btn-gray-color);
    border-radius: 8px;
    color: var(--white-text-color);
    margin-top: 25px;
    &:hover {
      background-color: var(--btn-gray2-color);
      color: var(--text-color-headers);
    }
  }

  &__select {
    width: 100%;
    @media (max-width: 720px) {
      margin-bottom: 20px;
    }
  }
}

.profile-tabs__list {
  margin-bottom: 30px;
}

.profile-form__submit {
  width: 100%;
  border-radius: 8px;
  margin-top: 25px;
  width: fit-content;
  &:hover {
    background: var(--btn-gray-color);
  }
}

.profile-sessions {
  &__current,
  &__other {
    padding-bottom: 20px;
    h5 {
      padding-bottom: 15px;
      font-weight: 700;
    }
  }
  &__title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    &-btn {
      background: none;
      border: none;
      padding: 0;
      color: var(--default-svg-color);
      cursor: pointer;
      margin-bottom: 10px;
      &:hover {
        color: var(--default-svg-color-hover);
        transition: 0.3s;
      }
    }
  }
}

.session-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 15px 10px 10px;
  border: 1px solid var(--btn-gray-color);
  border-radius: 8px;
  margin-bottom: 10px;

  &__ip {
    font-size: 14px;
    color: var(--default-svg-color);
    padding: 3px 0 10px 0;
  }

  &__activity {
    padding-bottom: 3px;
  }

  &__activity,
  &__authorization {
    font-size: 12px;
  }

  &__close-btn {
    cursor: pointer;
    fill: var(--default-svg-color);
    &:hover {
      fill: var(--default-svg-color-hover);
    }
  }
}

.profile-public-links {
  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 15px;
  }

  &__close-all {
    background: none;
    border: none;
    color: var(--default-svg-color);
    display: flex;
    align-items: center;
    cursor: pointer;
    padding: 0;
    &:hover {
      color: var(--default-svg-color-hover);
    }
    svg {
      margin-left: 5px;
    }
  }

  &__list {
    display: flex;
    flex-direction: column;
  }
}

.link-item {
  display: flex;
  flex-direction: column;
  padding: 10px 15px 10px 10px;
  border: 1px solid var(--btn-gray-color);
  border-radius: 8px;
  margin-bottom: 10px;

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  &__title {
    display: flex;
    align-items: center;
  }

  &__text {
    color: var(--main-color);
    margin-left: 5px;
    font-weight: 700;
  }

  &__btn {
    cursor: pointer;
    &:hover {
      fill: var(--default-svg-color-hover);
    }
  }
  &__buttons {
    display: flex;
    align-items: center;
    column-gap: 10px;
  }
  &__tags {
    display: flex;
    align-items: center;
    column-gap: 5px;
    padding: 5px 0;
    color: var(--default-svg-color);
  }

  &__tags-more {
    background: none;
    border: none;
    color: var(--default-svg-color);
    display: flex;
    align-items: center;
    cursor: pointer;
    padding: 0;
    &:hover {
      color: var(--default-svg-color-hover);
    }

    .link-item__tags-more-icon {
      margin-left: 5px;
    }
  }

  &__date {
    display: flex;
    gap: 20px;
    &-item {
      display: flex;
      column-gap: 5px;
    }
  }

  &__date-item p {
    font-size: 14px;
    color: var(--default-svg-color);
  }
}

.profile-tokens {
  &__header {
    padding: 20px 0 10px 0;
  }

  .token-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 15px 10px 10px;
    border: 1px solid var(--btn-gray-color);
    border-radius: 8px;
    margin-bottom: 13px;

    &__info {
      display: flex;
      flex-direction: column;
    }

    &__name {
      font-weight: 700;
      padding-bottom: 3px;
    }

    &__description {
      font-size: 12px;
      color: var(--default-svg-color);
    }

    &__close-btn {
      cursor: pointer;
      &:hover {
        fill: var(--default-svg-color-hover);
      }
    }
  }
}

.profile__info__pushes {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.flex_direction {
  flex-direction: column;
}

.switch_control_wrapper {
  width: 100%;
}

.margin_top {
  margin-top: 0;
}

.profile__tabs-btns {
  margin-bottom: 30px;
  display: flex;
  gap: 10px;
  .tab {
    background: none;
    border-bottom: 2px solid #fff;
    font-size: 16px;
  }
  .tab.active {
    border-bottom: 2px solid var(--main-color);
  }
}
</style>
