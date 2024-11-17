<script setup lang="ts">
import { defineEmits, ref, computed, onMounted } from 'vue'
import eyeIcon from '#/eye.svg'
import eyeSlashIcon from '#/eye-slash.svg'

//ts-ignore
const props = defineProps({
    type: {
        type: String,
        required: false,
        default: 'text',
    },
    name: {
        type: String,
        required: true,
    },
    id: {
        type: String,
        required: false,
        default: null,
    },
    icon: {
        type: [Boolean, String],
        required: false,
        default: false,
    },
    label: {
        type: [Boolean, String],
        required: false,
    },
    labelWrapper: {
        type: String,
        required: false,
        default: 'label_wrapper',
    },
    placeholder: {
        type: String,
        required: false,
    },
    labelClass: {
        type: [String, Object, Array],
        required: false,
        default: 'label__control',
    },
    inputClass: {
        type: [String, Object, Array],
        required: false,
        default: 'input__control',
    },
    prop: {
        type: String,
        required: false,
    },
    disabled: {
        type: Boolean,
        required: false,
        default: false,
    },
    checked: {
        type: Boolean,
        required: false,
        default: false,
    },
    autocomplete: {
        type: String,
        required: false,
        default: 'off',
    },
    mask: {
        type: [Boolean, Object],
        required: false,
        default: false,
    },
    static: {
        type: Boolean,
        required: false,
        default: false,
    },
    value: {
        type: [String, Number, Boolean],
        required: false,
    },
    modelValue: {
        type: [String, Number, Boolean],
        required: false,
    },
    maxLength: {
        type: Number,
        required: false,
    },
    maxValue: {
        type: Number,
        required: false,
    },
    minValue: {
        type: Number,
        required: false,
    },
    toFixed: {
        type: Number,
        required: false,
        default: 2,
    },
    maskIp: {
        type: String,
        required: false,
    },
    required: {
        type: Boolean,
        required: false,
        default: false,
    },
    error: {
        type: [Boolean, String],
        required: false,
        default: false,
    },
    errors: {
        type: Array,
        required: false,
        default: [],
    },
})

const label = computed(() => {
    return props.label === false
        ? false
        : props.label || 'Название'
})

const emit = defineEmits([
    'update:modelValue',
    'loaded',
    'after-update',
    'blur',
    'focus',
    'password-visible',
])

const input = ref<HTMLInputElement | null>(null)
const iconVisible = ref(false)

const model = computed({
    get(): any {
        return props.static ? props.value : props.modelValue
    },
    set(value: string | number) {
        if (
            props.type === 'number'
        ) {
            let oldValue = input.value?.value ?? ''
            setTimeout(() => {
                if (
                    props.type === 'number'
                ) {
                    if (
                        props.minValue !== undefined &&
                        parseFloat(oldValue) < props.minValue
                    ) {
                        oldValue = props.minValue.toString()
                    }

                    if (
                        props.maxValue !== undefined &&
                        parseFloat(oldValue) > props.maxValue
                    ) {
                        oldValue = props.maxValue.toString()
                    }

                    emit('update:modelValue', oldValue)
                }

                if (props.maxLength) {
                    oldValue = oldValue.substr(0, props.maxLength)
                    emit('update:modelValue', oldValue)
                }
            }, 1)
        }

        if (props.mask) {
            let oldValue = input.value?.value ?? ''
            let newValue = oldValue

            const firstSymbol = newValue.charAt(0)
            let maskedValue = ''

            if (!isNaN(parseInt(firstSymbol))) {
                if (
                    firstSymbol === '7' ||
                    firstSymbol === '8' ||
                    firstSymbol === '9'
                ) {
                    maskedValue = '+7'
                    newValue = maskedValue + newValue.slice(1)
                } else if (firstSymbol === '3') {
                    maskedValue = '+375 '
                    newValue = maskedValue + newValue.slice(1)
                } else {
                    maskedValue = ''
                    newValue = oldValue
                }
            }
            setTimeout(() => {
                emit('update:modelValue', newValue)
            }, 1)
        }

        emit('update:modelValue', value)
        emit('after-update')
    },
})

const filterCharacters = (inputValue: string): string => {
    if (props.maskIp) {
        return inputValue.replace(/[^0-9.]/g, '')
    }
    return inputValue
}

const inputStyle = computed(() => {
    return {
        paddingBlock: '0px',
        paddingInline: '0px',
        paddingLeft: props.icon === 'search' ? '40px' : '15px',
    }
})

const handleInput = (event: Event): void => {
    const target = event.target as HTMLInputElement
    let inputValue = target.value

    inputValue = inputValue.replace(/\D/g, '')

    const filteredValue = filterCharacters(inputValue)

    if (inputValue !== filteredValue) {
        target.value = filteredValue
        emit('update:modelValue', filteredValue)
    }
}

interface ErrorObject {
    $property: string;
    $message: string;
}

function findError() {
    if (!Array.isArray(props.errors)) {
        return null;
    }

    const prop = props.errors.find((error: any): error is ErrorObject => {
        return (error as ErrorObject).$property === props.prop;
    });

    if (prop) return prop.$message;
    return null;
}


const handleIconClick = () => {
    iconVisible.value = !iconVisible.value
    emit('password-visible')
    console.log('ok')
}

onMounted(() => {
    if (input.value) {
        emit('loaded', input.value.value)
    }
})
</script>

<template>
    <div>
        <template v-if="$slots.label" :class="labelWrapper">
            <label :class="labelClass" :for="id ? id : name">
                <slot name="label"></slot>
            </label>
            <span v-if="required" class="asterisk">*</span>
        </template>
        <template v-else-if="label">
            <label
                :class="labelClass"
                :for="id ? id : name"
                v-html="label"
            ></label>
            <span v-if="required" class="asterisk">*</span>
        </template>
        <div class="input_container">
            <div class="input_container_content">
                <input
                    :style="inputStyle"
                    ref="input"
                    :type="type"
                    :name="name"
                    :id="id ? id : name"
                    :class="[inputClass, { error_field: error }]"
                    :placeholder="placeholder"
                    :disabled="disabled"
                    :checked="checked"
                    :autocomplete="autocomplete"
                    :value="value || modelValue"
                    v-mask="mask"
                    v-model="model"
                    @blur="$emit('blur', $event)"
                    @focus="$emit('focus')"
                    @input="handleInput"
                    :maskIp="maskIp"
                    :maxLength="maxLength"
                    :max="maxValue"
                    :min="minValue"
                />

                <eyeIcon
                    v-if="iconVisible && props.icon === 'password'"
                    class="password_icon"
                    @click="handleIconClick"
                />
                <eyeSlashIcon
                    v-if="!iconVisible && props.icon === 'password'"
                    class="password_icon"
                    @click="handleIconClick"
                />
            </div>
            <Transition name="fade">
                <div class="error" v-if="error">
                    <span class="error__message">
                        <slot name="error-text">{{ findError() }}</slot>
                    </span>
                </div>
            </Transition>
            <div class="faggot__pass" v-if="$slots.faggotPass">
                <slot name="faggotPass"></slot>
            </div>
        </div>
        <Tooltip v-if="$slots.beforeTip">
            <slot name="beforeTip"></slot>
        </Tooltip>
        <slot name="icon"></slot>
        <Transition name="fade"> </Transition>
        <slot name="notes"></slot>
    </div>
</template>

<style lang="scss">
.label_wrapper {
    display: flex;
    align-items: center;
}
.label__control {
    display: inline-block;
    font-weight: 500;
    cursor: pointer;
    &.label-main {
        color: var(--text-color-headers);
    }
}
.input__control_wrapper {
    position: relative;
    width: 100%;
    margin-bottom: 1rem;
    &:not(.inline) {
        .label_wrapper {
            margin-bottom: 5px;
        }
    }
    &.inline {
        display: flex;
        flex-direction: row-reverse;
        align-items: center;
        justify-content: flex-end;
        .wrapper {
            display: inline-block;
            &:first-child {
                margin-right: 40px;
            }
        }
        .default_checkbox {
            margin-right: 8px;
        }
        .label__control {
            line-height: 15px;
        }
        a {
            color: var(--main-color);
        }
    }
}
.input__control_wrapper.agreement {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    .label_wrapper {
        width: 90%;
    }
    .default_checkbox {
        min-width: 20px;
        margin-right: 8px;
        order: -1;
    }
}
.input__control {
    display: block;
    background-color: var(--main-background-color);
    height: 40px;
    width: 100%;
    border: 1px solid var(--btn-gray-color);
    border-radius: 8px;
    padding: 0px 16px 0px 12px;
    font-weight: 500;
    font-size: 13px;
    line-height: 154%;
    color: var(--text-color-headers);
    &::placeholder {
        color: var(--text-light-color);
        font-weight: 400;
        padding: 12px 16px 12px 0px;
    }
    &:focus {
        border: none;
        box-shadow: 0 0 2px var(--main-color);
        outline: none !important;
        &::placeholder {
            color: transparent;
        }
    }
    &:focus-visible {
        border: none;
        &::placeholder {
            color: var(--main-background-color);
        }
    }
    &.success {
        border: 1px solid $green-color;
    }
    &[disabled] {
        cursor: text;
    }
}

.input_container {
    padding: 2px 0 20px 0;
    &_content {
        position: relative;
        display: flex;
        align-items: center;
    }
}

.input_icon {
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
}

.default_checkbox {
    -webkit-appearance: none;
    -moz-appearance: none;
    display: inline-block;
    width: 20px;
    height: 20px;
    line-height: 20px;
    background-color: var(--main-background-color);
    border: 2px solid var(--btn-gray-color);
    border-radius: 3px;
    transition: all 0.2s;
    outline: none;
    cursor: pointer;
    &:checked {
        background-color: var(--main-color);
        background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg width='14' height='14' viewBox='0 0 14 14' fill='none' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='M11.6666 3.5L5.24998 9.91667L2.33331 7' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3e%3c/svg%3e");
        background-position: center center;
        background-repeat: no-repeat;
        border-color: var(--main-color);
        filter: brightness(0.9);
    }
    &:disabled {
        background-color: var(--btn-gray2-color-hover);
    }
    &:disabled:checked {
        background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg width='14' height='14' viewBox='0 0 14 14' fill='none' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='M11.6666 3.5L5.24998 9.91667L2.33331 7' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3e%3c/svg%3e");
        background-position: center center;
        background-repeat: no-repeat;
        border: none;
    }
}

.search_dropdown {
    margin: 0rem 1rem;
    width: auto;
}
.password_icon {
    position: absolute;
    right: 15px;
    cursor: pointer;
}

.asterisk {
    color: $red-color;
    display: inline-block;
    margin-left: 3px;
}
.faggot__pass {
    padding-top: 5px;
    display: flex;
    justify-content: flex-end;
}
</style>
