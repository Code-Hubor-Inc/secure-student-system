// 

export const appConfig = {
    appName: import.meta.env.VITE_APP_NAME || 'Secure Student System',
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
    version: import.meta.env.VITE_APP_VERSION || '1.0.0',
    debug: import.meta.env.VITE_DEBUG === 'true',
};

export const apiConfig = {
    timeout: 30000,
    maxRetries: 3,
    uploadTimeout: 60000,
};