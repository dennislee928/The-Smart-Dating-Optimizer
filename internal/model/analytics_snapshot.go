package model

import (
	"time"
)

// AnalyticsSnapshot 分析快照模型
type AnalyticsSnapshot struct {
	ID                  int64     `gorm:"primaryKey;autoIncrement"`
	DatingAccountID     int64     `gorm:"not null;index:idx_analytics_account"`
	ProfileID           *int64    `gorm:"index"`
	ABTestID            *int64    `gorm:"index"`
	SnapshotDate        time.Time `gorm:"type:date;not null;index:idx_analytics_date"`
	TotalSwipes         int       `gorm:"default:0"`
	RightSwipes         int       `gorm:"default:0"`
	LeftSwipes          int       `gorm:"default:0"`
	MatchesCount        int       `gorm:"default:0"`
	MatchRate           *float64  `gorm:"type:decimal(5,2)"` // percentage
	MessageResponseRate *float64  `gorm:"type:decimal(5,2)"` // percentage
	AvgAIScore          *float64  `gorm:"type:decimal(5,2)"`
	Metadata            JSONB     `gorm:"type:jsonb"`
	CreatedAt           time.Time `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`

	// Relations
	DatingAccount DatingAccount `gorm:"foreignKey:DatingAccountID"`
	Profile       *Profile      `gorm:"foreignKey:ProfileID"`
	ABTest        *ABTest       `gorm:"foreignKey:ABTestID"`
}

// TableName 指定表名
func (AnalyticsSnapshot) TableName() string {
	return "analytics_snapshots"
}
