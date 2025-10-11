package database

import (
	"fmt"
	"log"

	"github.com/pclee/smart-dating-optimizer/internal/config"
	"github.com/pclee/smart-dating-optimizer/internal/model"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

var DB *gorm.DB

// InitDatabase 初始化資料庫連線
func InitDatabase(cfg *config.Config) error {
	dsn := fmt.Sprintf(
		"host=%s port=%s user=%s password=%s dbname=%s sslmode=%s",
		cfg.Database.Host,
		cfg.Database.Port,
		cfg.Database.User,
		cfg.Database.Password,
		cfg.Database.DBName,
		cfg.Database.SSLMode,
	)

	var err error
	DB, err = gorm.Open(postgres.Open(dsn), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Info),
	})

	if err != nil {
		return fmt.Errorf("無法連接資料庫: %w", err)
	}

	log.Println("資料庫連接成功")
	return nil
}

// AutoMigrate 執行自動遷移（僅開發環境使用）
func AutoMigrate() error {
	err := DB.AutoMigrate(
		&model.User{},
		&model.DatingAccount{},
		&model.Profile{},
		&model.ABTest{},
		&model.SwipeRecord{},
		&model.Match{},
		&model.Message{},
		&model.AnalyticsSnapshot{},
		&model.AIModel{},
		&model.AutomationLog{},
	)

	if err != nil {
		return fmt.Errorf("自動遷移失敗: %w", err)
	}

	log.Println("資料庫自動遷移完成")
	return nil
}

// GetDB 取得資料庫實例
func GetDB() *gorm.DB {
	return DB
}
