package model

import (
	"time"
)

// ABTest A/B 測試模型
type ABTest struct {
	ID               int64     `gorm:"primaryKey;autoIncrement"`
	DatingAccountID  int64     `gorm:"not null;index:idx_ab_tests_account"`
	TestName         string    `gorm:"type:varchar(100);not null"`
	ProfileAID       int64     `gorm:"not null"`
	ProfileBID       int64     `gorm:"not null"`
	StartDate        time.Time `gorm:"type:timestamp with time zone;not null"`
	EndDate          *time.Time `gorm:"type:timestamp with time zone"`
	Status           string    `gorm:"type:varchar(20);default:'active';index:idx_ab_tests_status"` // 'active', 'completed', 'paused'
	SwipesPerProfile int       `gorm:"default:100"`
	CreatedAt        time.Time `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`
	UpdatedAt        time.Time `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`

	// Relations
	DatingAccount DatingAccount `gorm:"foreignKey:DatingAccountID"`
	ProfileA      Profile       `gorm:"foreignKey:ProfileAID"`
	ProfileB      Profile       `gorm:"foreignKey:ProfileBID"`
	SwipeRecords  []SwipeRecord `gorm:"foreignKey:ABTestID"`
	AnalyticsSnapshots []AnalyticsSnapshot `gorm:"foreignKey:ABTestID"`
}

// TableName 指定表名
func (ABTest) TableName() string {
	return "ab_tests"
}

