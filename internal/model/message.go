package model

import (
	"time"
)

// Message 訊息模型
type Message struct {
	ID             int64     `gorm:"primaryKey;autoIncrement"`
	MatchID        int64     `gorm:"not null;index:idx_messages_match"`
	Sender         string    `gorm:"type:varchar(20);not null"` // 'user', 'match'
	Content        string    `gorm:"type:text;not null"`
	SentimentScore *float64  `gorm:"type:decimal(5,2)"`
	SentAt         time.Time `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP;index:idx_messages_sent_at"`
	CreatedAt      time.Time `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`

	// Relations
	Match Match `gorm:"foreignKey:MatchID"`
}

// TableName 指定表名
func (Message) TableName() string {
	return "messages"
}

