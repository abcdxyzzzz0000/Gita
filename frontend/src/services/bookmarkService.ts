import api from './api';

export interface BookmarkData {
  id: string;
  user_id: string;
  chapter: number;
  shloka_number: number;
  created_at: string;
  shloka?: {
    id: string;
    chapter: number;
    shloka_number: number;
    sanskrit_text: string;
    transliteration: string;
    meaning: string;
  };
}

export const bookmarkService = {
  async getBookmarks(): Promise<BookmarkData[]> {
    const response = await api.get<BookmarkData[]>('/bookmarks');
    return response.data;
  },

  async createBookmark(chapter: number, shlokaNumber: number): Promise<BookmarkData> {
    const response = await api.post<BookmarkData>('/bookmarks', {
      chapter,
      shloka_number: shlokaNumber,
    });
    return response.data;
  },

  async deleteBookmark(bookmarkId: string): Promise<void> {
    await api.delete(`/bookmarks/${bookmarkId}`);
  },

  async deleteBookmarkByShloka(chapter: number, shlokaNumber: number): Promise<void> {
    await api.delete(`/bookmarks/by-shloka/${chapter}/${shlokaNumber}`);
  },
};
