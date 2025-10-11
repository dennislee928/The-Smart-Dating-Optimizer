package model

import (
	"time"

	"gorm.io/gorm"
)

// Match 配對模型
type Match struct {
	ID                   int64          `gorm:"primaryKey;autoIncrement"`
	SwipeRecordID        int64          `gorm:"not null;index:idx_matches_swipe_record"`
	DatingAccountID      int64          `gorm:"not null;index:idx_matches_account"`
	ProfileID            *int64         `gorm:"index:idx_matches_profile"`
	MatchName            string         `gorm:"type:varchar(100)"`
	MatchProfileData     JSONB          `gorm:"type:jsonb"`
	MatchedAt            time.Time      `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP;index:idx_matches_matched_at"`
	FirstMessageSent     bool           `gorm:"default:false"`
	FirstMessageReceived bool           `gorm:"default:false"`
	ConversationStarted  bool           `gorm:"default:false"`
	UnmatchedAt          *time.Time     `gorm:"type:timestamp with time zone"`
	CreatedAt            time.Time      `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`
	UpdatedAt            time.Time      `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`

	// Relations
	SwipeRecord   SwipeRecord   `gorm:"foreignKey:SwipeRecordID"`
	DatingAccount DatingAccount `gorm:"foreignKey:DatingAccountID"`
	Profile       *Profile      `gorm:"foreignKey:ProfileID"`
	Messages      []Message     `gorm:"foreignKey:MatchID"`
}

// TableName 指定表名
func (Match) TableName() string {
	return "matches"
}

