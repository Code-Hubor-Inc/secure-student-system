// 

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { appConfig, apiConfig } from '../../config/app-config';
import { ApiError, RequestConfig } from '../../types/api';
import { STORAGE_KEYS } from '../../config/constants';

class ApiClient {
    private client: AxiosInstance;

    constructor() {
        this.client = axios.create({
            baseURL: appConfig.apiBaseUrl,
            timeout: apiConfig.timeout,
            headers: {
                'Content-Type': 'application/json',
            },
        });

        this.setupInterceptors();
    }

    private setupInterceptors(): void {
        // Request interceptor
        this.client.interceptors.request.use(
            (config) => {
                const token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                }
                return config;
            },
            (error) => Promise.reject(error)
        );

        // Response interceptor
        this.client.interceptors.response.use(
            (response) => response,
            (error) => {
                if (error.response?.status === 401) {
                    this.handleUnauthorized();
                }
                return Promise.reject(this.normalizeError(error));
            }
        );
    }

    private handleUnauthorized(): void {
        localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
        localStorage.removeItem(STORAGE_KEYS.USER_DATA);
        window.location.href = '/login';
    }

    private normalizeError(error: any): ApiError {
        if (error.response?.data) {
            return {
                message: error.response.data.detail || 'An error occurred',
                code: error.response.data.code || 'UNKNOWN_ERROR',
                details: error.response.data.details,
            };
        }

        return {
            message: error.message || 'Network error',
            code: 'NETWORK_ERROR',
        };
    }

    async get<T>(url: string, config?: RequestConfig): Promise<T> {
        const response: AxiosResponse<T> = await this.client.get(url, config);
        return response.data;
    }

    async post<T>(url: string, data?: any, config?: RequestConfig): Promise<T> {
        const response: AxiosResponse<T> = await this.client.post(url, data, config);
        return response.data;
    }

    async delete<T>(url: string, config?: RequestConfig): Promise<T> {
        const response: AxiosResponse<T> = await this.client.delete(url, config);
        return response.data;
    }
}

export const apiClient = new ApiClient();