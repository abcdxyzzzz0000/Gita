import api from './api';
import { Shloka } from '../types/models';

export interface ProblemCategory {
  id: string;
  title: string;
  description: string;
  icon: string;
}

export interface Recommendation {
  shloka: Shloka;
  explanation: string;
  relevance_score: number;
}

export const lifeGuidanceService = {
  async getProblems(): Promise<ProblemCategory[]> {
    const response = await api.get<ProblemCategory[]>('/life-guidance/problems');
    return response.data;
  },

  async getRecommendations(problem: string, topK: number = 5): Promise<Recommendation[]> {
    const response = await api.get<Recommendation[]>('/life-guidance/recommendations', {
      params: { problem, top_k: topK },
    });
    return response.data;
  },
};
