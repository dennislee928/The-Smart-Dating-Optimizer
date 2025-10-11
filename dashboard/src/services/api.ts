import axios, { AxiosInstance } from 'axios';
import type { APIResponse, LoginResponse, DashboardStats } from '@/types/api';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080/api/v1',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for adding auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor for handling errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token expired, redirect to login
          this.clearToken();
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token');
    }
    return null;
  }

  private setToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  }

  private clearToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  // Auth API
  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await this.client.post<APIResponse<LoginResponse>>(
      '/auth/login',
      { email, password }
    );
    if (response.data.success && response.data.data) {
      this.setToken(response.data.data.token);
      return response.data.data;
    }
    throw new Error(response.data.error?.message || 'Login failed');
  }

  async register(email: string, password: string, username: string): Promise<void> {
    const response = await this.client.post('/auth/register', {
      email,
      password,
      username,
    });
    if (!response.data.success) {
      throw new Error(response.data.error?.message || 'Registration failed');
    }
  }

  logout(): void {
    this.clearToken();
  }

  // Dashboard API
  async getDashboardStats(accountId: number): Promise<DashboardStats> {
    const response = await this.client.get<APIResponse<DashboardStats>>(
      `/analytics/dashboard`,
      { params: { dating_account_id: accountId } }
    );
    if (response.data.success && response.data.data) {
      return response.data.data;
    }
    throw new Error(response.data.error?.message || 'Failed to fetch dashboard stats');
  }

  // Add more API methods here...
}

export const apiClient = new APIClient();

