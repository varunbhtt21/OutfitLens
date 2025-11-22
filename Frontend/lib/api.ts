import axios from 'axios';
import { useAuthStore } from '../store/authStore';
import type { LoginResponse, RegisterResponse, User, ImageModel, ImageListResponse, Generation, PaginatedResponse } from '../types';

// Base API configuration
export const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for 401 handling and token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Handle 401 Unauthorized
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Try to refresh the token
        const refreshToken = useAuthStore.getState().refreshToken;
        if (refreshToken) {
          const response = await api.post('/api/v1/auth/refresh-token', {
            refresh_token: refreshToken,
          });

          const { access_token } = response.data;
          useAuthStore.getState().updateAccessToken(access_token);

          // Retry the original request with new token
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        useAuthStore.getState().logout();
        window.location.href = '/#/login';
      }
    }

    return Promise.reject(error);
  }
);

// --- Authentication API ---
export const authApi = {
  login: async (email: string, password: string): Promise<{ tokens: LoginResponse; user: User }> => {
    // Step 1: Login to get tokens
    const loginRes = await api.post<LoginResponse>('/api/v1/auth/login', { email, password });
    const tokens = loginRes.data;

    // Step 2: Get user data with the access token
    const userRes = await api.get<User>('/api/v1/users/me', {
      headers: { Authorization: `Bearer ${tokens.access_token}` }
    });

    return {
      tokens,
      user: userRes.data
    };
  },

  register: async (data: { email: string; password: string; full_name: string }): Promise<RegisterResponse> => {
    const res = await api.post<RegisterResponse>('/api/v1/auth/register', data);
    return res.data;
  },

  refreshToken: async (refreshToken: string): Promise<{ access_token: string; token_type: string }> => {
    const res = await api.post('/api/v1/auth/refresh-token', { refresh_token: refreshToken });
    return res.data;
  }
};

// --- User API ---
export const userApi = {
  getMe: async (): Promise<User> => {
    const res = await api.get<User>('/api/v1/users/me');
    return res.data;
  },

  updateProfile: async (data: { full_name: string }): Promise<User> => {
    const res = await api.put<User>('/api/v1/users/me', data);
    return res.data;
  },

  changePassword: async (data: { old_password: string; new_password: string }): Promise<{ message: string }> => {
    const res = await api.patch<{ message: string }>('/api/v1/users/me/password', data);
    return res.data;
  },

  deleteAccount: async (): Promise<{ message: string }> => {
    const res = await api.delete<{ message: string }>('/api/v1/users/me');
    return res.data;
  }
};

// --- Image API ---
export const imageApi = {
  upload: async (file: File, type: 'user_photo' | 'clothing_photo'): Promise<ImageModel> => {
    const formData = new FormData();
    formData.append('file', file);

    const endpoint = type === 'user_photo'
      ? '/api/v1/images/upload/user-photo'
      : '/api/v1/images/upload/clothing-photo';

    const res = await api.post<ImageModel>(endpoint, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  getAll: async (type?: string): Promise<{ items: ImageModel[]; total: number }> => {
    const res = await api.get<ImageListResponse>('/api/v1/images', {
      params: type ? { image_type: type } : undefined
    });
    // Backend returns { images, total }, we need to transform to { items, total }
    return {
      items: res.data.images,
      total: res.data.total
    };
  },

  getById: async (id: string): Promise<Blob> => {
    const res = await api.get(`/api/v1/images/${id}`, {
      responseType: 'blob'
    });
    return res.data;
  },

  delete: async (id: string): Promise<{ message: string }> => {
    const res = await api.delete<{ message: string }>(`/api/v1/images/${id}`);
    return res.data;
  }
};

// --- Generation API ---
export const generationApi = {
  create: async (userPhotoId: string, clothingPhotoId: string): Promise<Generation> => {
    const res = await api.post<Generation>('/api/v1/generations', {
      user_photo_id: userPhotoId,
      clothing_photo_id: clothingPhotoId
    });
    return res.data;
  },

  getStatus: async (id: string): Promise<{ id: string; status: string; error_message?: string; result_image?: ImageModel }> => {
    const res = await api.get(`/api/v1/generations/${id}/status`);
    const statusData = res.data;

    // If completed, fetch the full generation to get result_image
    if (statusData.status === 'completed') {
      const fullGen = await generationApi.getById(id);
      return {
        id: fullGen.id,
        status: fullGen.status,
        error_message: fullGen.error_message,
        result_image: fullGen.result_image
      };
    }

    return statusData;
  },

  getById: async (id: string): Promise<Generation> => {
    const res = await api.get<Generation>(`/api/v1/generations/${id}`);
    return res.data;
  },

  getHistory: async (page = 1, pageSize = 20): Promise<PaginatedResponse<Generation>> => {
    const res = await api.get<PaginatedResponse<Generation>>('/api/v1/generations', {
      params: { page, page_size: pageSize }
    });
    return res.data;
  },

  delete: async (id: string): Promise<{ message: string }> => {
    const res = await api.delete<{ message: string }>(`/api/v1/generations/${id}`);
    return res.data;
  }
};
