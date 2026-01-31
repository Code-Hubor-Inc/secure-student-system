// 

import { authApi } from './api/auth-api';
import { User, LoginCredentials, RegisterData } from '../types/auth';
import { STORAGE_KEYS } from '../config/constants';

class AuthService {
    private token: string | null = null;
    private user: User | null = null;

    constructor() {
        this.loadFromStorage();
    }

    private loadFromStorage(): void {
        this.token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
        const userData = localStorage.getItem(STORAGE_KEYS.USER_DATA);
        if (userData) {
            try {
                this.user = JSON.parse(userData);
            } catch {
                this.clearStorage();
            }
        }
    }

    private saveToStorage(token: string, user: User): void {
        localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, token);
        localStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(user));
        this.token = token;
        this.user = null;
    }

    private clearStorage(): void {
        localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
        localStorage.removeItem(STORAGE_KEYS.USER_DATA);
        this.token = null;
        this.user = null;
    }

    async login(credentials: LoginCredentials): Promise<User> {
        const response = await authApi.login(credentials);

        if (!response.success || !response.data) {
            throw new Error(response.message || 'Login failed');
        }

        const { access_token, token_type } = response.data;
        const token = `${token_type} ${access_token}`;

        // Get user data
        const userResponse = await authApi.getCurrentUser();
        if (!userResponse.success || !userResponse.data) {
            throw new Error('Failed to fetch user data');
        }

        this.saveToStorage(token, userResponse.data);
        return userResponse.data;
    }

    async register(userData: RegisterData): Promise<User> {
        const response = await authApi.register(userData);

        if (!response.success || !response.data) {
            throw new Error(response.message || 'Registration failed');
        }

        return response.data;
    }

    async logout(): Promise<void> {
        try {
            await authApi.logout();
        } catch (error) {
            console.warn('Logout API call failed', error);
        } finally {
            this.clearStorage();
        }
    }

    getCurrentUser(): User | null {
        return this.user;
    }

    getToken(): string | null {
        return this.token;
    }

    isAuthenticated(): boolean {
        return !!this.token && !!this.user;
    }

    isAdmin(): boolean {
        return this.user?.is_superuser || false;
    }
}

export const authService = new AuthService();