import api from './api';
import { Shloka } from '../types/models';

export interface DailyWisdomData {
  id: string;
  date: string;
  chapter: number;
  shloka_number: number;
  explanation: string;
  shloka: Shloka;
}

export interface WisdomHistoryEntry {
  id: string;
  date: string;
  chapter: number;
  shloka_number: number;
  explanation: string;
  shloka_meaning: string;
}

export const dailyWisdomService = {
  async getDailyWisdom(date?: string): Promise<DailyWisdomData> {
    const params = date ? { date } : {};
    const response = await api.get<DailyWisdomData>('/daily-wisdom', { params });
    return response.data;
  },

  async getHistory(limit: number = 7): Promise<WisdomHistoryEntry[]> {
    const response = await api.get<WisdomHistoryEntry[]>('/daily-wisdom/history', {
      params: { limit },
    });
    return response.data;
  },
};
