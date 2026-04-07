import api from './api';
import { User } from '../types/models';

export interface ProfileStats {
  bookmark_count: number;
  shlokas_read: number;
  chapters_completed: number;
  days_active: number;
}

export interface ProfileData {
  user: User;
  stats: ProfileStats;
}

export const profileService = {
  async getProfile(): Promise<ProfileData> {
    const response = await api.get<ProfileData>('/profile');
    return response.data;
  },
};
