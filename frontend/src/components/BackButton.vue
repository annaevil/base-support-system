<script setup lang="ts">
import { useRouter } from 'vue-router'
import BackIcon from '#/back.svg'

const router = useRouter()

function goBack() {
    router.back()
}
</script>
<template>
    <div>
        <button class="btn__back" @click="goBack">
            <BackIcon class="btn__back-icon" />
            Назад
        </button>
    </div>
</template>
<style scoped lang="scss">
.btn__back {
    color: var(--default-svg-color);
    font-family: 'SfProDisplay', sans-serif;
    display: flex;
    align-items: center;
    column-gap: 3px;
    font-weight: 500;
    padding: 0;
    background: none;
    font-size: 13px;
    margin-bottom: 40px;
    &:hover {
        color: var(--default-svg-color-hover);
        transition: 0.3s;
        .btn__back-icon {
            fill: var(--default-svg-color-hover);
            transition: 0.3s;
        }
    }
    &-icon {
        fill: var(--default-svg-color);
    }
}
</style>
