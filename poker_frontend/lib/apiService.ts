
import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
    timeout: 2000,
    headers: { 'Content-Type': 'application/json' },
});


export const apiService = {
    async get(path: string) {
        return axiosInstance.get(path);
    },
    async post<T>(path: string, data: T) {
        return axiosInstance.post(path, data);
    },
    async put<T>(path: string, data: T) {
        return axiosInstance.put(path, data);
    },
    async delete(path: string) {
        return axiosInstance.delete(path);
    },
};

