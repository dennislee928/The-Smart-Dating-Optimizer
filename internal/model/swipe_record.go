package model

import (
	"time"
)

// SwipeRecord 滑卡記錄模型
type SwipeRecord struct {
	ID              int64     `gorm:"primaryKey;autoIncrement"`
	DatingAccountID int64     `gorm:"not null;index:idx_swipe_records_account"`
	ProfileID       *int64    `gorm:"index:idx_swipe_records_profile"`
	ABTestID        *int64    `gorm:"index:idx_swipe_records_test"`
	TargetName      string    `gorm:"type:varchar(100)"`
	TargetAge       int       `gorm:"type:integer"`
	TargetBio       string    `gorm:"type:text"`
	TargetPhotos    JSONB     `gorm:"type:jsonb"`
	TargetDistance  int       `gorm:"type:integer"` // in km
	SwipeDirection  string    `gorm:"type:varchar(10);not null;index:idx_swipe_records_direction"` // 'left', 'right', 'super'
	IsMatch         bool      `gorm:"default:false"`
	AIScore         *float64  `gorm:"type:decimal(5,2)"`
	DecisionReason  string    `gorm:"type:text"`
	SwipedAt        time.Time `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP;index:idx_swipe_records_swiped_at"`
	CreatedAt       time.Time `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`

	// Relations
	DatingAccount DatingAccount `gorm:"foreignKey:DatingAccountID"`
	Profile       *Profile      `gorm:"foreignKey:ProfileID"`
	ABTest        *ABTest       `gorm:"foreignKey:ABTestID"`
	Match         *Match        `gorm:"foreignKey:SwipeRecordID"`
}

// TableName 指定表名
func (SwipeRecord) TableName() string {
	return "swipe_records"
}

