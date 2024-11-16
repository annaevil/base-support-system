import {
    required,
    minLength,
    maxLength,
    email,
    helpers,
} from '@vuelidate/validators'

export const requiredRule = (message = 'Поле обязательно для заполнения') => {
    return helpers.withMessage(message, required)
}

export const minLengthRule = (
    length: number,
    message = `Минимальная длина ${length} символов`
) => {
    return helpers.withMessage(message, minLength(length))
}

export const maxLengthRule = (
    length: number,
    message = `Максимальная длина ${length} символов`
) => {
    return helpers.withMessage(message, maxLength(length))
}

export const emailRule = (message = 'Неправильный формат email') => {
    return helpers.withMessage(message, email)
}

