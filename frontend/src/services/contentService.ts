import api from './api';
import { Chapter, Shloka } from '../types/models';

export interface ShlokaDetail extends Shloka {
  explanation?: string;
}

export interface SemanticSearchResult {
  shloka: Shloka;
  relevance_score: number;
}

export const contentService = {
  async getChapters(): Promise<Chapter[]> {
    const response = await api.get<Chapter[]>('/chapters');
    return response.data;
  },

  async getShlokas(chapterId: number): Promise<Shloka[]> {
    const response = await api.get<Shloka[]>(`/chapters/${chapterId}/shlokas`);
    return response.data;
  },

  async getShlokaDetail(shlokaId: string): Promise<ShlokaDetail> {
    const response = await api.get<ShlokaDetail>(`/shlokas/${shlokaId}`);
    return response.data;
  },

  async semanticSearch(query: string, topK: number = 5): Promise<SemanticSearchResult[]> {
    const response = await api.get<SemanticSearchResult[]>('/search/semantic', {
      params: { q: query, top_k: topK },
    });
    return response.data;
  },
};
