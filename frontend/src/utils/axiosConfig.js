import axios from 'axios'
import { useUserStore } from '@/stores/userStore'

export function setupAxiosInterceptors() {
    axios.interceptors.response.use(
        response => response,
        async error => {
            const originalRequest = error.config

            if (error.response.status === 401 && !originalRequest._retry) {
                originalRequest._retry = true

                const userStore = useUserStore()
                const refreshed = await userStore.refresh()

                if (refreshed) {
                    return axios(originalRequest)
                } else {
                    userStore.logout()
                }
            }

            return Promise.reject(error)
        }
    )
}

export function initializeAuth() {
    const userStore = useUserStore()
    const storedToken = localStorage.getItem('access_token')
    const storedRefreshToken = localStorage.getItem('refresh_token')

    if (storedToken && storedRefreshToken) {
        userStore.user = {
            username: localStorage.getItem('username') || '',
            token: storedToken
        }
        userStore.isLoggedIn = true
    }
}
