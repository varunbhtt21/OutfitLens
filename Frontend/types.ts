export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user?: User; // Optional because login doesn't return it
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface RegisterResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export enum ImageType {
  USER_PHOTO = 'user_photo',
  CLOTHING_PHOTO = 'clothing_photo',
  GENERATED_RESULT = 'generated_result'
}

export interface ImageModel {
  id: string;
  url: string;
  image_type: ImageType;
  file_size: number;
  width: number;
  height: number;
  created_at: string;
}

export enum GenerationStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export interface Generation {
  id: string;
  user_id: string;
  user_photo: ImageModel;
  clothing_photo: ImageModel;
  result_image?: ImageModel;
  status: GenerationStatus;
  error_message?: string;
  processing_time_ms?: number;
  created_at: string;
  updated_at: string;
  completed_at?: string;
}

export interface ImageListResponse {
  images: ImageModel[];
  total: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}
