// 

import { apiClient } from './base-api';
import { ApiResponse } from '../../types/common';
import { User, LoginCredentials, RegisterData, AuthResponse } from '../../types/auth';

export const authApi = {
    async login(credentials: LoginCredentials): Promise<ApiResponse<AuthResponse>> {
        const formData = new FormData();
        formData.append('username', credentials.email);
        formData.append('password', credentials.password);

        return apiClient.post('/auth/login', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });
    },

    async register(userData: RegisterData): Promise<ApiResponse<User>> {
        return apiClient.post('/auth/register', userData);
    },

    async getCurrentUser(): Promise<ApiResponse<User>> {
        return apiClient.get('/auth/me');
    },

    async logout(): Promise<ApiResponse> {
        return apiClient.post('/auth/logout');
    }
}