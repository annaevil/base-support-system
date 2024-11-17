<script setup lang="ts">
import { defineProps, defineEmits, computed } from 'vue'
import buttonClose from '#/close.svg'

interface ModalProps {
    modelValue: boolean
    customClass?: string
    showCloseButton?: boolean
    overlayClick?: boolean
    header?: string
}

const props = defineProps<ModalProps>()
const emits = defineEmits(['update:modelValue'])

const closeModal = () => {
    emits('update:modelValue', false)
}

const handleOverlayClick = () => {
    if (props.overlayClick !== false) {
        closeModal()
    }
}

const show = computed(() => props.modelValue)
</script>

<template>
    <div v-if="show" class="modal">
        <div class="modal__overlay" @click="handleOverlayClick"></div>
        <div class="modal__content" :class="customClass" @click.stop>
            <slot name="header">
                <div class="modal__header">
                    <h3 class="modal__header-title">{{ header }}</h3>
                    <span
                        v-if="showCloseButton"
                        class="modal__close-button"
                        @click="closeModal"
                    >
                        <buttonClose class="modal__close-button-icon" />
                    </span>
                </div>
            </slot>
            <div class="modal__body">
                <slot name="body"></slot>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.modal {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    width: 100vw;
    height: 100vh;
    padding: 0 15px;
    z-index: 9999;

    &__overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
    }
    &__content {
        background: var(--main-background-color);
        z-index: 9999;
        padding: 30px;
        display: flex;
        flex-direction: column;
        border-radius: 20px;
        width: 40vw;
        animation: fadeIn 0.3s ease;

        @media (min-width: 1920px) {
            width: 40%;
            max-width: 40vw;
        }
        @media (min-width: 1180px) and (max-width: 1919px) {
            width: 50%;
            max-width: 50vw;
        }
        @media (max-width: 1179px) {
            width: 90%;
            max-width: 90vw;
            border-radius: 10px;
            padding: 15px;
        }
        @media (max-width: 520px) {
            min-width: 100%;
        }
    }
}

.modal__header {
    display: flex;
    justify-content: space-between;
    padding-bottom: 30px;

    &-title {
        font-size: 22px;
        line-height: 145%;
        font-weight: 600;
    }

    .modal__close-button {
        cursor: pointer;
        display: flex;
        align-items: center;
        &-icon {
            fill: var(--default-svg-color);
            transition: 0.3s;
            &:hover {
                fill: var(--default-svg-color-hover);
            }
        }
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}
</style>
