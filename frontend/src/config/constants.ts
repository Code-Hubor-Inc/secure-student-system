// 

export const STORAGE_KEYS = {
    AUTH_TOKEN: 'secure_student_token',
    USER_DATA: 'secure_student_user',
    THEME: 'secure_student_theme',
};

export const ROUTES = {
    HOME: '/',
    LOGIN: '/login',
    REGISTER: '/register',
    FORGOT_PASSWORD: '/forgot-password',
    DASHBOARD: '/dashboard',
    FILE_PROTECTION: '/files',
    ID_PROTECTION: '/id-protection',
    SECURE_PORTALS: '/portals',
    SETTINGS: '/settings',
    ADMIN: {
        USERS: '/admin/users',
        INSTITUTIONS: '/admin/institutions',
        AUDIT: '/admin/audit',
        SETTINGS: '/admin/settings',
    },
};

export const FILE_CONFIG = {
    MAX_FILE_SIZE: 100 * 1024 * 1024, //100MB
    ALLOWED_FILE_TYPES: [
        'image/jpeg',
        'image/png',
        'image/gif',
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ],
};

export const SECURITY_LEVELS = {
    STANDARD: 'standard',
    ENHANCED: 'enhanced',
    STRICT: 'strict',
} as const;