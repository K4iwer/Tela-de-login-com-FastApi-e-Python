export interface LoginRequest {
  username: string;  
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
}

export interface RegisterResponse {
  id: string;
  username: string;
  email: string;
}

export interface ApiError {
  detail: string | { error: string };
}