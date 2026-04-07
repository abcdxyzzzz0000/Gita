import { create } from 'zustand';
import { Chapter, Shloka } from '../types/models';

interface ContentState {
  chapters: Chapter[];
  shlokas: Record<number, Shloka[]>;
  isLoading: boolean;
  error: string | null;

  setChapters: (chapters: Chapter[]) => void;
  setShlokas: (chapterId: number, shlokas: Shloka[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useContentStore = create<ContentState>((set) => ({
  chapters: [],
  shlokas: {},
  isLoading: false,
  error: null,

  setChapters: (chapters) => set({ chapters, isLoading: false }),
  setShlokas: (chapterId, shlokas) =>
    set((state) => ({
      shlokas: { ...state.shlokas, [chapterId]: shlokas },
      isLoading: false,
    })),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error, isLoading: false }),
}));
