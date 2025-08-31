import { ChatRequest, ChatResponse, BusinessConfig, Language, Intent } from './types';

const API_BASE_URL = 'http://localhost:8000'; // Change this to your backend URL

export const sendMessage = async (request: ChatRequest): Promise<ChatResponse> => {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return {
    ...data,
    timestamp: new Date(data.timestamp)
  };
};

export const getSupportedLanguages = async (): Promise<Language[]> => {
  const response = await fetch(`${API_BASE_URL}/languages`);
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data.languages;
};

export const getSupportedIntents = async (): Promise<Intent[]> => {
  const response = await fetch(`${API_BASE_URL}/intents`);
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data.intents;
};

export const configureBusiness = async (config: BusinessConfig): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/configure`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(config),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
};

export const checkHealth = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
};