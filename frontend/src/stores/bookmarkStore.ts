import { create } from 'zustand';
import { BookmarkData, bookmarkService } from '../services/bookmarkService';

interface BookmarkState {
  bookmarks: BookmarkData[];
  isLoading: boolean;

  fetchBookmarks: () => Promise<void>;
  addBookmark: (chapter: number, shlokaNumber: number) => Promise<void>;
  removeBookmark: (bookmarkId: string) => Promise<void>;
  removeBookmarkByShloka: (chapter: number, shlokaNumber: number) => Promise<void>;
  isBookmarked: (chapter: number, shlokaNumber: number) => boolean;
  getBookmarkId: (chapter: number, shlokaNumber: number) => string | null;
}

export const useBookmarkStore = create<BookmarkState>((set, get) => ({
  bookmarks: [],
  isLoading: false,

  fetchBookmarks: async () => {
    set({ isLoading: true });
    try {
      const bookmarks = await bookmarkService.getBookmarks();
      set({ bookmarks, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },

  addBookmark: async (chapter, shlokaNumber) => {
    // Optimistic update
    const tempBookmark: BookmarkData = {
      id: `temp-${Date.now()}`,
      user_id: '',
      chapter,
      shloka_number: shlokaNumber,
      created_at: new Date().toISOString(),
    };
    set((state) => ({ bookmarks: [tempBookmark, ...state.bookmarks] }));

    try {
      const bookmark = await bookmarkService.createBookmark(chapter, shlokaNumber);
      set((state) => ({
        bookmarks: state.bookmarks.map((b) =>
          b.id === tempBookmark.id ? bookmark : b
        ),
      }));
    } catch {
      // Rollback
      set((state) => ({
        bookmarks: state.bookmarks.filter((b) => b.id !== tempBookmark.id),
      }));
    }
  },

  removeBookmark: async (bookmarkId) => {
    const prev = get().bookmarks;
    // Optimistic
    set((state) => ({
      bookmarks: state.bookmarks.filter((b) => b.id !== bookmarkId),
    }));

    try {
      await bookmarkService.deleteBookmark(bookmarkId);
    } catch {
      set({ bookmarks: prev });
    }
  },

  removeBookmarkByShloka: async (chapter, shlokaNumber) => {
    const prev = get().bookmarks;
    set((state) => ({
      bookmarks: state.bookmarks.filter(
        (b) => !(b.chapter === chapter && b.shloka_number === shlokaNumber)
      ),
    }));

    try {
      await bookmarkService.deleteBookmarkByShloka(chapter, shlokaNumber);
    } catch {
      set({ bookmarks: prev });
    }
  },

  isBookmarked: (chapter, shlokaNumber) => {
    return get().bookmarks.some(
      (b) => b.chapter === chapter && b.shloka_number === shlokaNumber
    );
  },

  getBookmarkId: (chapter, shlokaNumber) => {
    const bm = get().bookmarks.find(
      (b) => b.chapter === chapter && b.shloka_number === shlokaNumber
    );
    return bm?.id ?? null;
  },
}));
