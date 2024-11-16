<script setup lang="ts">
import Registration from "@/components/Registration.vue"
import Login from "@/components/Login.vue"

import { ref } from "vue"

const tabs = ref([
  { label: "Вход", key: "entrance" },
  { label: "Регистрация", key: "registration" },
])

const tab = ref("entrance")
</script>
<template>
  <div class="wrapper">
    <div class="wrapper__container">
      <!-- <BackButton /> -->
      <div class="tab__header">
        <button
          v-for="tabItem in tabs"
          :key="tabItem.key"
          :class="{ active: tab === tabItem.key }"
          @click="tab = tabItem.key"
        >
          {{ tabItem.label }}
        </button>
      </div>
      <div class="tab__content" v-show="tab === 'entrance'">
        <Login />
      </div>
      <div class="tab__content" v-show="tab === 'registration'">
        <Registration />
      </div>
    </div>
  </div>
</template>
<style scoped lang="scss">
.wrapper {
  height: 100vh;
  align-items: center;
  background: #d0d0d0;
  &__container {
    background: #fff;
    padding: 40px 15px;
    border-radius: 15px;
    height: fit-content;
    box-shadow: 0 3px 15px #00000026;
  }
}
.registration__title {
  text-align: center;
  padding-top: 18px;
}
</style>
