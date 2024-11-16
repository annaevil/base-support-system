<script setup lang="ts">
import { reactive, computed } from "vue"

import InputControl from "@/components/template/InputControl.vue"
import SubmitControl from "@/components/template/SubmitControl.vue"
import axios from "axios"

const { toggleVisibility, inputType } = usePasswordVisibility()

const regForm = reactive({
  loginReg: "",
  passwordReg: "",
  confirmPassword: "",
})

const latinLetters = helpers.withMessage(
  "Пароль должен содержать только латинские буквы, цифры и символы",
  (value: unknown): value is string =>
    typeof value === "string" && /^[a-zA-Z0-9@._-]*$/.test(value)
)

// const checkPassword = helpers.withMessage(
//   "Пароли не совпадают",
//   () => form.confirmPassword === form.password
// )

const rules = computed(() => ({
  loginReg: {
    required: requiredRule(),
    email: emailRule()
  },
  passwordReg: {
    required: requiredRule(),
    latinLetters,
    minLength: minLengthRule(3),
  },
}))

const v$ = useVuelidate(rules, regForm)

const formSubmitReg = async () => {
  try {
    v$.value.$touch()
    if (!v$.value.$invalid) { 
    
    const response = await axios.post(
      'http://localhost:8888/api/v1/auth/register',
      {
        email: regForm.loginReg,
        password: regForm.passwordReg,
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      }
    );
  
    console.log('Ответ от сервера:', response.data); 
  }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error("Ошибка при регистрации:", error.response?.data || error.message);
      alert("Произошла ошибка. Попробуйте еще раз");
    } else {
      console.error("Неизвестная ошибка:", error);
    }
  }
};


// const formSubmitReg = async () => {
//   try {
//     v$.value.$touch()

//     const data = {
//       email: v$.value.loginReg.$model,
//       password: v$.value.password.$model,
//     }

//     const response = await axios.post("http://localhost:8888/api/v1/auth/register", data, {
//       headers: {
//         'Content-Type': 'application/json',
//         'Accept': 'application/json',
//       },
//     })

//     console.log("Успех:", response.data)

//   } catch (error: unknown) {
//     if (axios.isAxiosError(error)) {
//       console.error("Ошибка при регистрации:", error.response?.data || error.message)
//       alert("Произошла ошибка. Попробуйте еще раз")
//     } else {
//       console.error("Неизвестная ошибка:", error)
//     }
//   }
// }

</script>

<template>
  <form @submit.prevent="formSubmitReg">
    <InputControl
      :type="'email'"
      :name="'loginReg'"
      :label="'Почта'"
      :prop="'loginReg'"
      :required="true"
      :error="v$.loginReg.$error"
      :errors="v$.$errors"
      v-model="v$.loginReg.$model"
    />
    <InputControl
      :type="inputType('password')"
      :name="'passwordReg'"
      :label="'Пароль'"
      :prop="'passwordReg'"
      :icon="'password'"
      :required="true"
      :error="v$.passwordReg.$error"
      :errors="v$.$errors"
      v-model="v$.passwordReg.$model"
      @password-visible="toggleVisibility('password')"
    ></InputControl>
    <InputControl
      v-if="false"
      :type="inputType('confirmPassword')"
      :name="'confirmPassword'"
      :label="'Повторите пароль'"
      :placeholder="''"
      :prop="'confirmPassword'"
      :icon="'password'"
      :required="false"
      v-model="regForm.confirmPassword"
      @password-visible="toggleVisibility('confirmPassword')"
    ></InputControl>
    <div class="wrapper__error"></div>
    <SubmitControl
      :cancel="false"
      :labelSend="'Зарегистрироваться'"
      :buttonFullWidth="true"
      :disabled="v$.$silentErrors.length !== 0"
    />
  </form>
  <!-- <div v-if="false">
        <h1>Пароль успешно изменен!</h1>
        <button class="btn_gray">В профиль</button>
      </div> -->
      
</template>
