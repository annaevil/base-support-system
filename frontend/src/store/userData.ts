import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const allowedColors = [
    '#FF5733',
    '#33FF57',
    '#3357FF',
    '#F39C12',
    '#8E44AD',
    '#2ECC71',
    '#E74C3C',
    '#1ABC9C',
    '#3498DB',
    '#008000',
    '#2F4F4F',
    '#FF7F50',
    '#6A5ACD',
    '#F4A460',
]

function stringToColor(str: string) {
    let hash = 0
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash)
        hash = hash & hash
    }
    const index = Math.abs(hash) % allowedColors.length
    return allowedColors[index]
}

export const useUserStore = defineStore(
    'user',
    () => {
        const name = ref('')
        const surname = ref('')
        const email = ref('')
        const avatarColor = ref('')
        const initial = ref('')

        const fullName = computed(() => `${name.value} ${surname.value}`)

        const setUserData = (
            nameValue: string,
            surnameValue: string,
            emailValue: string
        ) => {
            name.value = nameValue
            surname.value = surnameValue
            email.value = emailValue
            avatarColor.value = stringToColor(`${nameValue} ${surnameValue}`)
            initial.value = nameValue.charAt(0).toUpperCase()
        }

        return {
            name,
            surname,
            email,
            avatarColor,
            initial,
            fullName,
            setUserData
        }
    },
    {
        persist: true,
    }
)
