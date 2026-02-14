// lib/chat-api.ts
import { apiClient } from './api';

export interface ChatRequest {
  conversation_id?: number;
  message: string;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: Array<{
    [key: string]: any;
  }>;
}

// Chat API functions
export const chatApi = {
  // Send a message to the chatbot
  sendMessage: async (
    userId: string, 
    message: string, 
    conversationId?: number
  ): Promise<{ data?: ChatResponse; error?: string }> => {
    const requestData: ChatRequest = {
      message,
      ...(conversationId && { conversation_id: conversationId })
    };
    
    return apiClient.post<ChatResponse>(`/api/${userId}/chat`, requestData);
  },
};