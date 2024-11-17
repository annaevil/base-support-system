<script setup lang="ts">
import { defineProps } from 'vue'

// @ts-ignore
const props: object = defineProps({
    processing: {
        type: Boolean,
        required: false,
        default: false,
    },
    labelSend: {
        type: String,
        required: false,
    },
    labelCancel: {
        type: String,
        required: false,
    },
    disabled: {
        type: Boolean,
        required: false,
        default: false,
    },
    ring: {
        type: Boolean,
        required: false,
        default: true,
    },
    cancel: {
        type: Boolean,
        required: false,
        default: false,
    },
    isSubmit: {
        type: Boolean,
        required: false,
        default: true,
    },
    wrapperClass: {
        type: [String, Object, Array] as unknown as () =>
            | string
            | object
            | string[],
        required: false,
        default: 'submit_control_wrapper',
    },
    marginClass: {
        type: String,
        required: false,
        default: '',
    },
    buttonFullWidth: {
        type: Boolean,
        required: false,
        default: false,
    },
})

</script>

<template>
    <div :class="[wrapperClass, marginClass]">
        <slot name="between"></slot>
        <button
            v-if="isSubmit"
            type="submit"
            :class="{
                button: true,
                ring: ring,
                processing: processing,
                full_width: buttonFullWidth,
            }"
            :disabled="disabled || processing"
        >
            <slot name="default">{{ labelSend }}</slot>
            <span v-if="processing && ring" class="dual_ring"></span>
        </button>
        <button
            v-if="!isSubmit"
            type="button"
            :class="{
                button: true,
                ring: ring,
                processing: processing,
                btn_full_width: buttonFullWidth,
            }"
            :disabled="disabled || processing"
            @click.prevent="$emit('accept')"
        >
            <slot name="default">{{ labelSend }}</slot>
            <span v-if="processing && ring" class="dual_ring"></span>
        </button>
        <button
            type="button"
            class="btn_gray"
            v-if="cancel"
            @click.prevent="$emit('cancel')"
        >
            <slot name="cancel">{{ labelCancel }}</slot>
        </button>
        <slot name="after"></slot>
    </div>
</template>

<style lang="scss">
.submit_control_wrapper {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
    width: 100%;
    margin-bottom: 1rem;
    margin-top: 20px;
}

.button {
    position: relative;
    display: inline-block;
    padding: 12px 13px;
    line-height: 18px;
    font-weight: 600;
    background-color: $main-color;
    color: $main-background-color;
    border: none;
    border-radius: 8px;
    font-family: 'SfProDisplay', sans-serif;
    font-weight: 500;
    cursor: pointer;
    min-width: 85px;
    font-size: 16px;
    text-align: center;
    transition: background-color 0.3s ease;
    &:not([disabled]):hover {
        color: $main-background-color;
        background-color: $hover-btn-color;
    }
    &:not([disabled]):active {
        color: $main-background-color;
        background-color: $hover-btn-color;
    }
    &:disabled {
       background-color: var(--btn-blue-disabled);
    }
    &.ring.processing {
        padding-left: 34px;
    }
}

.dual_ring {
    display: inline-block;
    width: 18px;
    height: 18px;
    position: absolute;
    left: 8px;
    top: calc(50% - 9px);
    &::after {
        content: ' ';
        display: block;
        width: 12px;
        height: 12px;
        background-color: transparent;
        border-radius: 50%;
        border: 2px solid;
        border-color: $main-background-color transparent $main-background-color
            transparent;
        animation: dual-ring 1.2s linear infinite;
    }
}

@keyframes dual_ring {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}

$prefix-cls: vel;
.#{$prefix-cls}_loading {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    @keyframes ring {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
    .ring {
        display: inline-block;
        width: 64px;
        height: 64px;

        &::after {
            content: ' ';
            display: block;
            width: 46px;
            height: 46px;
            margin: 1px;
            border-radius: 50%;
            border: 5px solid $btn-gray-color;
            border-color: $btn-gray-color transparent $btn-gray-color
                transparent;
            animation: ring 1.2s linear infinite;
        }
    }
}

.ms_4 {
    margin-left: 1.5rem;
}

.btn_gray {
    display: inline-block;
    padding: 12px 16px;
    line-height: 18px;
    font-family: 'SfProDisplay', sans-serif;
    font-weight: 500;
    font-size: 13px;
    background-color: var(--btn-gray2-color);
    color: var(--white-text-color);
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    &:hover {
        background-color: var(--btn-gray2-color-hover);
    }
    &:disabled {
        background-color: var(--btn-gray2-color-hover);
        color: var(--text-light-color);
    }
}

.reverse {
    display: flex;
    justify-content: end;
}

.full_width {
    width: 100%;
}
</style>
