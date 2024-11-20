<script setup lang="ts">
import { useRouter } from 'vue-router'
import exitIcon from '#/exit.svg'

function logout() {
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT;'
}
</script>
<template>
    <router-link :to="{ name: 'Auth' }">
        <button class="exit__button" @click="logout">
            Выйти
            <exitIcon class="exit__button-icon" />
        </button>
    </router-link>
</template>
<style scoped lang="scss">
.exit__button {
    color: var(--default-svg-color);
    font-family: 'SfProDisplay', sans-serif;
    display: flex;
    align-items: center;
    column-gap: 3px;
    font-weight: 500;
    padding: 0;
    background: none;
    font-size: 13px;
    &:hover {
        color: var(--default-svg-color-hover);
        transition: 0.3s;
        .exit__button-icon {
            fill: var(--default-svg-color-hover);
            transition: 0.3s;
        }
    }
    &-icon {
        fill: var(--default-svg-color);
    }
}
</style>
