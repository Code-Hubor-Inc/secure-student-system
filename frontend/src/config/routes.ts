// 

import { ROUTES } from './constants';

export const publicRoutes = [
    ROUTES.LOGIN,
    ROUTES.REGISTER,
    ROUTES.FORGOT_PASSWORD,
];

export const protectedRoutes = [
    ROUTES.DASHBOARD,
    ROUTES.FILE_PROTECTION,
    ROUTES.ID_PROTECTION,
    ROUTES.SECURE_PORTALS,
    ROUTES.SETTINGS,
];

export const adminRoutes = [
    ROUTES.ADMIN.USERS,
    ROUTES.ADMIN.INSTITUTIONS,
    ROUTES.ADMIN.AUDIT,
    ROUTES.ADMIN.SETTINGS,
];