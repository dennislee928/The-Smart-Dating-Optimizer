package vo

import "time"

// ABTestVO A/B 測試回應
type ABTestVO struct {
	ID               int64      `json:"id"`
	DatingAccountID  int64      `json:"dating_account_id"`
	TestName         string     `json:"test_name"`
	ProfileAID       int64      `json:"profile_a_id"`
	ProfileBID       int64      `json:"profile_b_id"`
	StartDate        time.Time  `json:"start_date"`
	EndDate          *time.Time `json:"end_date,omitempty"`
	Status           string     `json:"status"`
	SwipesPerProfile int        `json:"swipes_per_profile"`
	CreatedAt        time.Time  `json:"created_at"`
	UpdatedAt        time.Time  `json:"updated_at"`
}

// ABTestResultVO A/B 測試結果回應
type ABTestResultVO struct {
	ABTestID         int64              `json:"ab_test_id"`
	TestName         string             `json:"test_name"`
	Status           string             `json:"status"`
	StartDate        time.Time          `json:"start_date"`
	EndDate          *time.Time         `json:"end_date,omitempty"`
	ProfileAStats    ProfileStatsVO     `json:"profile_a_stats"`
	ProfileBStats    ProfileStatsVO     `json:"profile_b_stats"`
	Winner           string             `json:"winner"` // 'profile_a', 'profile_b', 'tie', 'inconclusive'
	Recommendation   string             `json:"recommendation"`
}

// ABTestListResponse A/B 測試列表回應
type ABTestListResponse struct {
	ABTests []ABTestVO `json:"ab_tests"`
	Total   int64      `json:"total"`
}

