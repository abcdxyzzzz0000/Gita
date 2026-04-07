import api from './api';
import { Shloka } from '../types/models';

export interface SearchResult {
  shloka: Shloka;
  matched_text: string;
  matched_field: string;
}

export const searchService = {
  async keywordSearch(query: string, limit: number = 20): Promise<SearchResult[]> {
    const response = await api.get<SearchResult[]>('/search', {
      params: { q: query, limit },
    });
    return response.data;
  },
};
