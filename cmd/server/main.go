package main

import (
	"log"

	"github.com/gin-gonic/gin"
	"github.com/pclee/smart-dating-optimizer/internal/config"
	"github.com/pclee/smart-dating-optimizer/internal/database"
	"github.com/pclee/smart-dating-optimizer/internal/handler"
	"github.com/pclee/smart-dating-optimizer/internal/repository"
	"github.com/pclee/smart-dating-optimizer/internal/service"
)

// @title Smart Dating Optimizer API
// @version 1.0
// @description 智慧社交改善器 API 文件
// @host localhost:8080
// @BasePath /api/v1
func main() {
	// 載入設定
	cfg := config.LoadConfig()

	// 初始化資料庫
	if err := database.InitDatabase(cfg); err != nil {
		log.Fatalf("資料庫初始化失敗: %v", err)
	}

	// 執行自動遷移（僅開發環境）
	if cfg.Server.GinMode == "debug" {
		if err := database.AutoMigrate(); err != nil {
			log.Printf("自動遷移警告: %v", err)
		}
	}

	// 設定 Gin 模式
	gin.SetMode(cfg.Server.GinMode)

	// 建立 Gin router
	router := gin.Default()

	// CORS 中介層
	router.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, DELETE, PATCH")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	})

	// 初始化依賴
	db := database.GetDB()

	// Repositories
	userRepo := repository.NewUserRepository(db)
	// swipeRepo := repository.NewSwipeRepository(db) // TODO: 整合滑卡相關 API 時使用

	// Services
	userService := service.NewUserService(userRepo)

	// Handlers
	userHandler := handler.NewUserHandler(userService)

	// 路由設定
	v1 := router.Group("/api/v1")
	{
		// 認證路由
		auth := v1.Group("/auth")
		{
			auth.POST("/register", userHandler.Register)
			auth.POST("/login", userHandler.Login)
		}

		// 使用者路由
		users := v1.Group("/users")
		{
			users.GET("/:id", userHandler.GetUser)
			users.PUT("/:id", userHandler.UpdateUser)
		}

		// TODO: 其他路由群組
		// - /dating-accounts
		// - /profiles
		// - /ab-tests
		// - /swipes
		// - /analytics
	}

	// 健康檢查
	router.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"status":  "ok",
			"message": "Smart Dating Optimizer API is running",
		})
	})

	// 啟動伺服器
	addr := ":" + cfg.Server.Port
	log.Printf("伺服器啟動於 http://localhost%s", addr)
	if err := router.Run(addr); err != nil {
		log.Fatalf("伺服器啟動失敗: %v", err)
	}
}
