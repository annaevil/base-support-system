<script setup lang="ts">
import { useRoute } from 'vue-router'
import { watch } from 'vue'

const route = useRoute()

watch(
  () => route.meta.title,
  (newTitle) => {
    document.title = (newTitle as string)
  }
)
</script>

<template>
  <router-view></router-view>
</template>

<style scoped lang="scss">
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

</style>
