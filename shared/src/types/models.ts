export interface User {
  id: string;
  email: string;
  oauthProvider?: 'google' | null;
  createdAt: string;
  lastLogin: string;
  notificationEnabled: boolean;
  notificationTime: string;
}

export interface Chapter {
  id: number;
  title: string;
  sanskritName: string;
  description: string;
  shlokaCount: number;
}

export interface Shloka {
  id: string;
  chapter: number;
  shlokaNumber: number;
  sanskritText: string;
  transliteration: string;
  meaning: string;
  audioFilePath?: string;
  themes: string[];
  isBookmarked?: boolean;
}

export interface ShlokaDetail extends Shloka {
  explanation?: string;
}

export interface Bookmark {
  id: string;
  userId: string;
  chapter: number;
  shlokaNumber: number;
  createdAt: string;
  shloka?: Shloka;
}

export interface ReadingProgress {
  id: string;
  userId: string;
  chapter: number;
  shlokaNumber: number;
  lastReadAt: string;
}

export interface DailyWisdom {
  id: string;
  date: string;
  chapter: number;
  shlokaNumber: number;
  explanation: string;
  shloka?: Shloka;
}

export interface AuthResponse {
  user: User;
  accessToken: string;
}

export interface ApiError {
  detail: string;
}

export interface ProfileStats {
  bookmarkCount: number;
  shlokasRead: number;
  chaptersCompleted: number;
  daysActive: number;
}

export interface UserProfile {
  user: User;
  stats: ProfileStats;
}
