import { API_CONFIG } from '../config/api.config';
import type {
  ChatRequest,
  ChatResponse,
  NewSessionResponse,
  ErrorResponse,
} from '../types/api.types';

class APIService {
  private baseUrl: string;
  private timeout: number;

  constructor() {
    this.baseUrl = API_CONFIG.BASE_URL;
    this.timeout = API_CONFIG.TIMEOUT;
  }

  private async fetchWithTimeout(
    url: string,
    options: RequestInit
  ): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const error: ErrorResponse = await response.json();
      throw new Error(error.detail || 'An error occurred');
    }
    return response.json();
  }

  async createSession(): Promise<NewSessionResponse> {
    const url = `${this.baseUrl}${API_CONFIG.ENDPOINTS.NEW_SESSION}`;
    const response = await this.fetchWithTimeout(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return this.handleResponse<NewSessionResponse>(response);
  }

  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const url = `${this.baseUrl}${API_CONFIG.ENDPOINTS.CHAT}`;
    const response = await this.fetchWithTimeout(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    return this.handleResponse<ChatResponse>(response);
  }

  async deleteSession(sessionId: string): Promise<void> {
    const url = `${this.baseUrl}${API_CONFIG.ENDPOINTS.DELETE_SESSION(sessionId)}`;
    await this.fetchWithTimeout(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async getSessionHistory(sessionId: string): Promise<any> {
    const url = `${this.baseUrl}${API_CONFIG.ENDPOINTS.SESSION_HISTORY(sessionId)}`;
    const response = await this.fetchWithTimeout(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return this.handleResponse(response);
  }
}

export const apiService = new APIService();
