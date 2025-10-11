package vo

import "time"

// AnalyticsSnapshotVO 分析快照回應
type AnalyticsSnapshotVO struct {
	ID                  int64      `json:"id"`
	DatingAccountID     int64      `json:"dating_account_id"`
	ProfileID           *int64     `json:"profile_id,omitempty"`
	ABTestID            *int64     `json:"ab_test_id,omitempty"`
	SnapshotDate        time.Time  `json:"snapshot_date"`
	TotalSwipes         int        `json:"total_swipes"`
	RightSwipes         int        `json:"right_swipes"`
	LeftSwipes          int        `json:"left_swipes"`
	MatchesCount        int        `json:"matches_count"`
	MatchRate           *float64   `json:"match_rate,omitempty"`
	MessageResponseRate *float64   `json:"message_response_rate,omitempty"`
	AvgAIScore          *float64   `json:"avg_ai_score,omitempty"`
	Metadata            map[string]interface{} `json:"metadata,omitempty"`
}

// DashboardStatsVO 儀表板統計回應
type DashboardStatsVO struct {
	TotalSwipes         int                `json:"total_swipes"`
	TotalMatches        int                `json:"total_matches"`
	MatchRate           float64            `json:"match_rate"`
	MessageResponseRate float64            `json:"message_response_rate"`
	ActiveProfiles      int                `json:"active_profiles"`
	ActiveABTests       int                `json:"active_ab_tests"`
	RecentSwipes        []SwipeRecordVO    `json:"recent_swipes"`
	TopPerformingProfile ProfileStatsVO    `json:"top_performing_profile"`
	WeeklyTrend         []AnalyticsSnapshotVO `json:"weekly_trend"`
}

// PerformanceTrendResponse 表現趨勢回應
type PerformanceTrendResponse struct {
	Snapshots []AnalyticsSnapshotVO `json:"snapshots"`
	StartDate time.Time             `json:"start_date"`
	EndDate   time.Time             `json:"end_date"`
}

