<script setup lang="ts">
import axios from "axios"
import { useRouter } from "vue-router"
import InputControl from "@/components/template/InputControl.vue"
import SubmitControl from "@/components/template/SubmitControl.vue"
import { reactive, computed } from "vue"

const router = useRouter()

const { toggleVisibility, inputType } = usePasswordVisibility()

const form = reactive({
  login: "",
  password: "",
})

const latinLetters = helpers.withMessage(
  "Пароль должен содержать только латинские буквы, цифры и символы",
  (value: unknown): value is string =>
    typeof value === "string" && /^[a-zA-Z0-9@._-]*$/.test(value)
)

const rules = computed(() => ({
  login: {
    required: requiredRule(),
  },
  password: {
    required: requiredRule(),
    latinLetters,
    minLength: minLengthRule(3),
  },
}))

const v$ = useVuelidate(rules, form)

const formSubmitLogin = async () => {
  try {
    v$.value.$touch();
    if (!v$.value.$invalid) {
      const data = new URLSearchParams();
      data.append("username", form.login);
      data.append("password", form.password);

      const response = await axios.post("http://localhost:8888/api/v1/auth/jwt/login", data, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          Accept: "application/json",
        },
        withCredentials: true,
      });

      if (response.status === 200) {
        console.log('response',response.data.access_token)
        document.cookie = `token=${response.data.access_token}; path=/; samesite=strict`

        console.log("Успешный вход:", response.data);
        if(form.login === 'user') {
          router.push("/")
        } else if (form.login === 'editor') {
          router.push("/manager")
        } else if (form.login === 'tech') {
          router.push("/specialist")
        } else {
          router.push("/auth")
        }
      } else {
        console.error("Ошибка ответа сервера:", response.data);
      }
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error("Ошибка при входе:", error.response?.data || error.message);
      alert("Произошла ошибка. Проверьте учетные данные и повторите попытку.");
    } else {
      console.error("Неизвестная ошибка:", error);
    }
  }
}
</script>
<template>
    <form @submit.prevent="formSubmitLogin">
        <InputControl
        :type="'text'"
        :name="'login'"
        :label="'Логин'"
        :prop="'login'"
        :required="true"
        :error="v$.login.$error"
        :errors="v$.$errors"
        v-model="v$.login.$model"
        />
        <InputControl
        :type="inputType('password')"
        :name="'password'"
        :label="'Пароль'"
        :prop="'password'"
        :icon="'password'"
        :required="true"
        :error="v$.password.$error"
        :errors="v$.$errors"
        v-model="v$.password.$model"
        @password-visible="toggleVisibility('password')"
        >
          <template #faggotPass v-if="false">
            <a class="form__link" href="/change-password">Забыли пароль?</a>
          </template>
        </InputControl>
        <SubmitControl
          :cancel="false"
          :labelSend="'Войти'"
          :buttonFullWidth="true"
          :disabled="v$.$silentErrors.length !== 0"
        />
      </form>
</template>