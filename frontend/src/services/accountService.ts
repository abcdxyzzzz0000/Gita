import api from './api';

export const accountService = {
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    await api.put('/account/password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  },

  async deleteAccount(): Promise<void> {
    await api.delete('/account');
  },
};
