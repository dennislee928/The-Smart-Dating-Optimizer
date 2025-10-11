package vo

import "time"

// SwipeRecordVO 滑卡記錄回應
type SwipeRecordVO struct {
	ID              int64     `json:"id"`
	DatingAccountID int64     `json:"dating_account_id"`
	ProfileID       *int64    `json:"profile_id,omitempty"`
	ABTestID        *int64    `json:"ab_test_id,omitempty"`
	TargetName      string    `json:"target_name"`
	TargetAge       int       `json:"target_age"`
	TargetBio       string    `json:"target_bio"`
	TargetPhotos    []string  `json:"target_photos"`
	TargetDistance  int       `json:"target_distance"`
	SwipeDirection  string    `json:"swipe_direction"`
	IsMatch         bool      `json:"is_match"`
	AIScore         *float64  `json:"ai_score,omitempty"`
	DecisionReason  string    `json:"decision_reason,omitempty"`
	SwipedAt        time.Time `json:"swiped_at"`
}

// SwipeHistoryResponse 滑卡歷史回應
type SwipeHistoryResponse struct {
	Swipes   []SwipeRecordVO `json:"swipes"`
	Total    int64           `json:"total"`
	Page     int             `json:"page"`
	PageSize int             `json:"page_size"`
}

// SwipeStatsVO 滑卡統計回應
type SwipeStatsVO struct {
	TotalSwipes    int     `json:"total_swipes"`
	RightSwipes    int     `json:"right_swipes"`
	LeftSwipes     int     `json:"left_swipes"`
	SuperSwipes    int     `json:"super_swipes"`
	MatchesCount   int     `json:"matches_count"`
	MatchRate      float64 `json:"match_rate"`
	AvgAIScore     float64 `json:"avg_ai_score"`
	AvgTargetAge   float64 `json:"avg_target_age"`
}

