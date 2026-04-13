import api from './api';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  passages?: { text: string; relevance_score: number }[];
  timestamp: Date;
}

export interface ChatResponse {
  response: string;
  passages: { text: string; relevance_score: number }[];
}

export const chatService = {
  async sendMessage(message: string): Promise<ChatResponse> {
    const response = await api.post<ChatResponse>('/chat/message', { message });
    return response.data;
  },
};
