import { ref } from 'vue'

export function usePasswordVisibility() {
    const visibility = ref<{ [key: string]: boolean }>({})

    const toggleVisibility = (field: string) => {
        visibility.value[field] = !visibility.value[field]
    }

    const inputType = (field: string) => {
        return visibility.value[field] ? 'text' : 'password'
    }

    return { toggleVisibility, inputType }
}
