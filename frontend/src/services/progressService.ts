import api from './api';

export interface ChapterProgress {
  chapter: number;
  read: number;
  total: number;
  percentage: number;
}

export interface ProgressData {
  recent: { chapter: number; shloka_number: number; last_read_at: string }[];
  chapter_progress: ChapterProgress[];
  total_read: number;
  streak: number;
  last_read: { chapter: number; shloka_number: number; last_read_at: string } | null;
}

export const progressService = {
  async recordProgress(chapter: number, shlokaNumber: number): Promise<void> {
    await api.post('/progress', { chapter, shloka_number: shlokaNumber });
  },

  async getProgress(): Promise<ProgressData> {
    const response = await api.get<ProgressData>('/progress');
    return response.data;
  },
};
