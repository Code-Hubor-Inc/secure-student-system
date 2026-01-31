// 

export interface ApiError {
    message: string;
    code: string;
    details?: any;
}

export interface RequestConfig {
    requiresAuth?: boolean;
    retrycount?: number;
    timeout?: number;
    headers?: Record<string, string>;
}