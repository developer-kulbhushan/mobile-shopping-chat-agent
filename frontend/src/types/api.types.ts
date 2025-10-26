export interface ChatRequest {
  message: string;
  session_id?: string;
}

export interface ChatResponse {
  session_id: string;
  intent?: string;
  response: string;
  context_data?: PhoneDetails | ComparisonData | PhoneDetails[];
  timestamp: string;
}

export interface NewSessionResponse {
  session_id: string;
  message: string;
}

export interface ErrorResponse {
  detail: string;
  error_code?: string;
}

export interface PhoneDetails {
  id: number;
  name: string;
  brand: string;
  price: number;
  os: string;
  display_size_inch: number;
  display_type: string;
  refresh_rate: number;
  processor: string;
  ram_gb: number;
  storage_gb: number;
  battery_mah: number;
  charging_speed_w: number;
  rear_camera_mp: number;
  front_camera_mp: number;
  camera_features: string;
  network: string;
  weight_g: number;
  rating: number;
  popularity_score: number;
  features: string[];
  use_cases: string[];
  pros: string[];
  cons: string[];
  released_year: number;
  created_at?: string;
  updated_at?: string;
}

export interface ComparisonData {
  phone_1: PhoneDetails;
  phone_2: PhoneDetails;
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  intent?: string;
  context_data?: PhoneDetails | ComparisonData | PhoneDetails[];
  timestamp: string;
}

export type IntentType =
  | 'search_recommendation'
  | 'compare'
  | 'details'
  | 'query'
  | 'chitchat'
  | 'irrelevant'
  | 'adversarial';
