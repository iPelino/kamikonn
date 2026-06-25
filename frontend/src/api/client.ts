import axios from 'axios';
import { useAuthStore } from '../stores/authStore';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

apiClient.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().accessToken;
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && originalRequest.url !== '/auth/token/refresh/' && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const response = await axios.post(
          `${apiClient.defaults.baseURL}/auth/token/refresh/`,
          {},
          { withCredentials: true }
        );

        const { access } = response.data;
        const authStore = useAuthStore.getState();
        if (authStore.user) {
          authStore.setAuth(authStore.user, access);
        } else {
          useAuthStore.setState({ accessToken: access });
        }

        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access}`;
        }
        return apiClient(originalRequest);
      } catch (refreshError) {
        useAuthStore.getState().clearAuth();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
