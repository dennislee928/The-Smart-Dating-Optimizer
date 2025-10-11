package vo

import "time"

// ProfileVO 個人檔案回應
type ProfileVO struct {
	ID              int64     `json:"id"`
	DatingAccountID int64     `json:"dating_account_id"`
	ProfileName     string    `json:"profile_name"`
	Bio             string    `json:"bio"`
	Photos          []string  `json:"photos"`
	Age             int       `json:"age"`
	Gender          string    `json:"gender"`
	Interests       []string  `json:"interests"`
	IsActive        bool      `json:"is_active"`
	CreatedAt       time.Time `json:"created_at"`
	UpdatedAt       time.Time `json:"updated_at"`
}

// ProfileListResponse 個人檔案列表回應
type ProfileListResponse struct {
	Profiles []ProfileVO `json:"profiles"`
	Total    int64       `json:"total"`
}

// ProfileStatsVO 個人檔案統計回應
type ProfileStatsVO struct {
	ProfileID           int64   `json:"profile_id"`
	ProfileName         string  `json:"profile_name"`
	TotalSwipes         int     `json:"total_swipes"`
	RightSwipes         int     `json:"right_swipes"`
	LeftSwipes          int     `json:"left_swipes"`
	MatchesCount        int     `json:"matches_count"`
	MatchRate           float64 `json:"match_rate"`
	MessageResponseRate float64 `json:"message_response_rate"`
	AvgAIScore          float64 `json:"avg_ai_score"`
}

