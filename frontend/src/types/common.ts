// 

export interface ApiResponse<T = any> {
    success: boolean;
    message: string;
    data: T;
}

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    size: number;
    pages: number;
}

export interface BaseEntry {
    id: number;
    created_at: string;
    updated_at: string;
}