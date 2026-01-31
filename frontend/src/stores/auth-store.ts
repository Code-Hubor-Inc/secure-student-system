// 

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, AuthState } from '../types/auth';
import { authService } from '../services/auth-service';

interface AuthStore extends AuthState {
    login: (email: string, password: string) => Promise<void>;
    register: (email: string, fullName: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    checkAuth: () => Promise<void>;
    setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthStore>()(
    persist(
        (set, get) => ({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,

            setLoading: (loading: boolean) => set({ isLoading: loading }),

            login: async (email: string, password: string) => {
                set({ isLoading: true });
                try {
                    const user = await authService.login({ email, password });
                    set({
                        user,
                        token: authService.getToken(),
                        isAuthenticated: true,
                        isLoading: false,
                    });
                } catch (error) {
                    set({ isLoading: false })
                    throw error;
                }
            },

            register: async (email: string, fullName: string, password: string) => {
                set({ isLoading:  true });
                try {
                    await authService.register({ email, fullName, password});
                    set({ isLoading: false });
                } catch (error) {
                    set({ isLoading: false });
                    throw error;
                }
            },

            logout: async () => {
                set({ isLoading: true });
                try {
                    await authService.logout();
                    set({
                        user: null,
                        token: null,
                        isAuthenticated: false,
                        isLoading: false,
                    });
                } catch (error) {
                    set({ isLoading: false });
                    throw error;
                }
            },

            checkAuth: async () => {
                const token = authService.getToken();
                const user = authService.getCurrentUser();

                if (token && user) {
                    set({
                        user,
                        token,
                        isAuthenticated: true,
                    });
                } else {
                    set({
                        user: null,
                        token: null,
                        isAuthenticated: false,
                    });
                }
            },
        }),
        {
            name: 'auth-storage',
            partialize: (state: AuthStore) => ({
                user: state.user,
                token: state.token,
                isAuthenticated: state.isAuthenticated,
            }),
        }
    )
);