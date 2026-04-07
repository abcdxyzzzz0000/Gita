export interface User {
  id: string;
  email: string;
  oauth_provider?: string | null;
  created_at: string;
  last_login: string;
  notification_enabled: boolean;
  notification_time: string;
}

export interface Chapter {
  id: number;
  title: string;
  sanskrit_name: string;
  description: string;
  shloka_count: number;
}

export interface Shloka {
  id: string;
  chapter: number;
  shloka_number: number;
  sanskrit_text: string;
  transliteration: string;
  meaning: string;
  audio_file_path?: string;
  themes?: string[];
  is_bookmarked?: boolean;
}

export interface AuthResponse {
  user: User;
  access_token: string;
}

export interface ApiError {
  detail: string;
}

export type RootStackParamList = {
  Login: undefined;
  Register: undefined;
  MainTabs: undefined;
  ShlokaList: { chapterId: number; chapterTitle: string };
  ShlokaDetail: { shlokaId: string };
  Bookmarks: undefined;
  Settings: undefined;
  LifeGuidance: undefined;
  ReadingProgress: undefined;
  WisdomHistory: undefined;
};

export type TabParamList = {
  Home: undefined;
  Chapters: undefined;
  Search: undefined;
  Profile: undefined;
};
