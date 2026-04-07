import api from './api';

export interface UserSettings {
  notification_enabled: boolean;
  notification_time: string;
}

export const settingsService = {
  async getSettings(): Promise<UserSettings> {
    const response = await api.get<UserSettings>('/settings');
    return response.data;
  },

  async updateSettings(settings: Partial<UserSettings>): Promise<UserSettings> {
    const response = await api.put<UserSettings>('/settings', settings);
    return response.data;
  },
};
