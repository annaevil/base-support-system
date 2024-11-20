import { createRouter, createWebHistory } from 'vue-router'
import Auth from '@/views/Auth.vue'
import HomePage from '@/views/HomePage.vue'
import NotFound from '@/views/NotFound.vue'
import Profile from '@/views/Profile.vue'
import Manager from '@/views/Manager.vue'
import Specialist from '@/views/Specialist.vue'

const routes = [
    {
        path: '/',
        name: 'HomePage',
        component: HomePage,
        redirect: '/profile',
    },
    {
        path: '/auth',
        name: 'Auth',
        component: Auth,
        meta: {title: 'Authorization'}
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile,
        meta: {title: 'Profile'}
    },
    {
        path: '/manager',
        name: 'Manager',
        component: Manager,
        meta: {title: 'Manager'}
    },
    {
        path: '/specialist',
        name: 'Specialist',
        component: Specialist,
        meta: {title: 'Specialist'}
    },
    {
        path: '/:catchAll(.*)',
        name: 'NotFound',
        component: NotFound,
        meta: {title: 'Not found'}
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router