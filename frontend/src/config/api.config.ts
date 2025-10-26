export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  ENDPOINTS: {
    CHAT: '/api/v1/chat',
    NEW_SESSION: '/api/v1/sessions/new',
    DELETE_SESSION: (sessionId: string) => `/api/v1/sessions/${sessionId}`,
    SESSION_HISTORY: (sessionId: string) => `/api/v1/sessions/${sessionId}/history`,
  },
  TIMEOUT: 30000,
} as const;
