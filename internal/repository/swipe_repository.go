package repository

import (
	"time"

	"github.com/pclee/smart-dating-optimizer/internal/model"
	"gorm.io/gorm"
)

// SwipeRepository 滑卡記錄資料庫操作介面
type SwipeRepository interface {
	Create(swipe *model.SwipeRecord) error
	BatchCreate(swipes []model.SwipeRecord) error
	FindByID(id int64) (*model.SwipeRecord, error)
	FindByDatingAccount(accountID int64, page, pageSize int) ([]model.SwipeRecord, int64, error)
	FindByProfileID(profileID int64, page, pageSize int) ([]model.SwipeRecord, int64, error)
	FindByABTestID(abTestID int64) ([]model.SwipeRecord, error)
	FindByDateRange(accountID int64, startDate, endDate time.Time) ([]model.SwipeRecord, error)
	GetStats(accountID int64, profileID *int64) (*SwipeStats, error)
}

// SwipeStats 滑卡統計結構
type SwipeStats struct {
	TotalSwipes  int
	RightSwipes  int
	LeftSwipes   int
	SuperSwipes  int
	MatchesCount int
	AvgAIScore   float64
}

type swipeRepository struct {
	db *gorm.DB
}

// NewSwipeRepository 建立滑卡記錄 repository
func NewSwipeRepository(db *gorm.DB) SwipeRepository {
	return &swipeRepository{db: db}
}

func (r *swipeRepository) Create(swipe *model.SwipeRecord) error {
	return r.db.Create(swipe).Error
}

func (r *swipeRepository) BatchCreate(swipes []model.SwipeRecord) error {
	return r.db.CreateInBatches(swipes, 100).Error
}

func (r *swipeRepository) FindByID(id int64) (*model.SwipeRecord, error) {
	var swipe model.SwipeRecord
	err := r.db.First(&swipe, id).Error
	if err != nil {
		return nil, err
	}
	return &swipe, nil
}

func (r *swipeRepository) FindByDatingAccount(accountID int64, page, pageSize int) ([]model.SwipeRecord, int64, error) {
	var swipes []model.SwipeRecord
	var total int64

	offset := (page - 1) * pageSize

	if err := r.db.Model(&model.SwipeRecord{}).
		Where("dating_account_id = ?", accountID).
		Count(&total).Error; err != nil {
		return nil, 0, err
	}

	err := r.db.Where("dating_account_id = ?", accountID).
		Order("swiped_at DESC").
		Limit(pageSize).
		Offset(offset).
		Find(&swipes).Error

	return swipes, total, err
}

func (r *swipeRepository) FindByProfileID(profileID int64, page, pageSize int) ([]model.SwipeRecord, int64, error) {
	var swipes []model.SwipeRecord
	var total int64

	offset := (page - 1) * pageSize

	if err := r.db.Model(&model.SwipeRecord{}).
		Where("profile_id = ?", profileID).
		Count(&total).Error; err != nil {
		return nil, 0, err
	}

	err := r.db.Where("profile_id = ?", profileID).
		Order("swiped_at DESC").
		Limit(pageSize).
		Offset(offset).
		Find(&swipes).Error

	return swipes, total, err
}

func (r *swipeRepository) FindByABTestID(abTestID int64) ([]model.SwipeRecord, error) {
	var swipes []model.SwipeRecord
	err := r.db.Where("ab_test_id = ?", abTestID).
		Order("swiped_at ASC").
		Find(&swipes).Error
	return swipes, err
}

func (r *swipeRepository) FindByDateRange(accountID int64, startDate, endDate time.Time) ([]model.SwipeRecord, error) {
	var swipes []model.SwipeRecord
	err := r.db.Where("dating_account_id = ? AND swiped_at BETWEEN ? AND ?",
		accountID, startDate, endDate).
		Order("swiped_at ASC").
		Find(&swipes).Error
	return swipes, err
}

func (r *swipeRepository) GetStats(accountID int64, profileID *int64) (*SwipeStats, error) {
	stats := &SwipeStats{}
	query := r.db.Model(&model.SwipeRecord{}).Where("dating_account_id = ?", accountID)

	if profileID != nil {
		query = query.Where("profile_id = ?", *profileID)
	}

	// 總滑卡數
	query.Count(&stats.TotalSwipes)

	// 按方向統計
	query.Where("swipe_direction = ?", "right").Count(&stats.RightSwipes)
	query.Where("swipe_direction = ?", "left").Count(&stats.LeftSwipes)
	query.Where("swipe_direction = ?", "super").Count(&stats.SuperSwipes)

	// 配對數
	query.Where("is_match = ?", true).Count(&stats.MatchesCount)

	// 平均 AI 分數
	var avgScore *float64
	query.Select("AVG(ai_score)").Scan(&avgScore)
	if avgScore != nil {
		stats.AvgAIScore = *avgScore
	}

	return stats, nil
}

