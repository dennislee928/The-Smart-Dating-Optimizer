// API Response Types
export interface APIResponse<T = any> {
  success: boolean;
  message?: string;
  data?: T;
  error?: ErrorInfo;
}

export interface ErrorInfo {
  code: string;
  message: string;
  details?: string;
}

// User Types
export interface User {
  id: number;
  email: string;
  username: string;
  created_at: string;
  updated_at: string;
}

export interface LoginResponse {
  token: string;
  expires_at: string;
  user: User;
}

// Dating Account Types
export interface DatingAccount {
  id: number;
  user_id: number;
  platform: string;
  account_id?: string;
  is_active: boolean;
  last_sync_at?: string;
  created_at: string;
  updated_at: string;
}

// Profile Types
export interface Profile {
  id: number;
  dating_account_id: number;
  profile_name: string;
  bio: string;
  photos: string[];
  age: number;
  gender: string;
  interests: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProfileStats {
  profile_id: number;
  profile_name: string;
  total_swipes: number;
  right_swipes: number;
  left_swipes: number;
  matches_count: number;
  match_rate: number;
  message_response_rate: number;
  avg_ai_score: number;
}

// A/B Test Types
export interface ABTest {
  id: number;
  dating_account_id: number;
  test_name: string;
  profile_a_id: number;
  profile_b_id: number;
  start_date: string;
  end_date?: string;
  status: string;
  swipes_per_profile: number;
  created_at: string;
  updated_at: string;
}

export interface ABTestResult {
  ab_test_id: number;
  test_name: string;
  status: string;
  start_date: string;
  end_date?: string;
  profile_a_stats: ProfileStats;
  profile_b_stats: ProfileStats;
  winner: string;
  recommendation: string;
}

// Swipe Types
export interface SwipeRecord {
  id: number;
  dating_account_id: number;
  profile_id?: number;
  ab_test_id?: number;
  target_name: string;
  target_age: number;
  target_bio: string;
  target_photos: string[];
  target_distance: number;
  swipe_direction: string;
  is_match: boolean;
  ai_score?: number;
  decision_reason?: string;
  swiped_at: string;
}

export interface SwipeStats {
  total_swipes: number;
  right_swipes: number;
  left_swipes: number;
  super_swipes: number;
  matches_count: number;
  match_rate: number;
  avg_ai_score: number;
  avg_target_age: number;
}

// Analytics Types
export interface DashboardStats {
  total_swipes: number;
  total_matches: number;
  match_rate: number;
  message_response_rate: number;
  active_profiles: number;
  active_ab_tests: number;
  recent_swipes: SwipeRecord[];
  top_performing_profile: ProfileStats;
  weekly_trend: AnalyticsSnapshot[];
}

export interface AnalyticsSnapshot {
  id: number;
  dating_account_id: number;
  profile_id?: number;
  ab_test_id?: number;
  snapshot_date: string;
  total_swipes: number;
  right_swipes: number;
  left_swipes: number;
  matches_count: number;
  match_rate?: number;
  message_response_rate?: number;
  avg_ai_score?: number;
  metadata?: Record<string, any>;
}

// Pagination Types
export interface PaginationMeta {
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: PaginationMeta;
}

