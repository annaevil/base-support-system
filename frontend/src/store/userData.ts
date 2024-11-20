import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

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

export const useUserStore = defineStore('user', () => {
    const name = ref(localStorage.getItem('name') || 'Константин')
    const surname = ref(localStorage.getItem('surname') || 'Чернов')
    const email = ref(localStorage.getItem('email') || 'kost2020@mail.ru')
    const phone = ref(localStorage.getItem('phone') || '+49529888890')
    const avatarColor = ref(stringToColor(`${name.value} ${surname.value}`))
    const initial = ref(name.value.charAt(0).toUpperCase())

    const fullName = computed(() => `${name.value} ${surname.value}`)
        localStorage.setItem('name', name.value)
        localStorage.setItem('surname', surname.value)
        localStorage.setItem('email', email.value)
        localStorage.setItem('phone', phone.value)
        avatarColor.value = stringToColor(`${name.value} ${surname.value}`)
        initial.value = name.value.charAt(0).toUpperCase()

    const setUserData = (nameValue : string, surnameValue : string, emailValue : string, phoneValue : string) => {
        name.value = nameValue
        surname.value = surnameValue
        email.value = emailValue
        phone.value = phoneValue
        avatarColor.value = stringToColor(`${nameValue} ${surnameValue}`)
        initial.value = nameValue.charAt(0).toUpperCase()
    }

    return {
        name,
        surname,
        email,
        phone,
        avatarColor,
        initial,
        fullName,
        setUserData
    }
})
