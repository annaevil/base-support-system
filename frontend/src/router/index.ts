import { createRouter, createWebHistory } from 'vue-router'
import Auth from '@/views/Auth.vue'
import HomePage from '@/views/HomePage.vue'
import NotFound from '@/views/NotFound.vue'

const routes = [
    {
        path: '/',
        name: 'HomePage',
        component: HomePage,
        meta: {title: 'Base support'}
    },
    {
        path: '/auth',
        name: 'Auth',
        component: Auth,
        meta: {title: 'Authorization'}
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