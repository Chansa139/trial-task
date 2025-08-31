export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  detectedLanguage?: string;
  intent?: string;
  confidence?: number;
}

export interface ChatRequest {
  message: string;
  session_id: string;
  business_config?: BusinessConfig | null;
}

export interface ChatResponse {
  message: string;
  session_id: string;
  detected_language?: string;
  intent?: string;
  confidence?: number;
  timestamp: Date;
}

export interface BusinessConfig {
  business_name: string;
  primary_language: string;
  supported_languages: string[];
  knowledge_base_url?: string;
  api_key?: string;
}

export interface Language {
  code: string;
  name: string;
  native_name: string;
}

export interface Intent {
  code: string;
  name: string;
  description: string;
}

export interface Analytics {
  totalMessages: number;
  languagesDetected: Record<string, number>;
  intentsClassified: Record<string, number>;
  averageResponseTime: number;
}