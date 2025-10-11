package config

import (
	"log"
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

// Config 應用程式設定結構
type Config struct {
	Server   ServerConfig
	Database DatabaseConfig
	JWT      JWTConfig
	CORS     CORSConfig
}

// ServerConfig 伺服器設定
type ServerConfig struct {
	Port    string
	GinMode string
}

// DatabaseConfig 資料庫設定
type DatabaseConfig struct {
	Host     string
	Port     string
	User     string
	Password string
	DBName   string
	SSLMode  string
}

// JWTConfig JWT 設定
type JWTConfig struct {
	Secret          string
	ExpirationHours int
}

// CORSConfig CORS 設定
type CORSConfig struct {
	AllowedOrigins []string
}

// LoadConfig 載入設定
func LoadConfig() *Config {
	// 載入 .env 檔案
	if err := godotenv.Load(); err != nil {
		log.Println("警告: 找不到 .env 檔案，使用環境變數")
	}

	jwtExpHours, _ := strconv.Atoi(getEnv("JWT_EXPIRATION_HOURS", "168"))

	return &Config{
		Server: ServerConfig{
			Port:    getEnv("SERVER_PORT", "8080"),
			GinMode: getEnv("GIN_MODE", "debug"),
		},
		Database: DatabaseConfig{
			Host:     getEnv("DB_HOST", "localhost"),
			Port:     getEnv("DB_PORT", "5432"),
			User:     getEnv("DB_USER", "postgres"),
			Password: getEnv("DB_PASSWORD", ""),
			DBName:   getEnv("DB_NAME", "smart_dating_optimizer"),
			SSLMode:  getEnv("DB_SSLMODE", "disable"),
		},
		JWT: JWTConfig{
			Secret:          getEnv("JWT_SECRET", "default_secret_change_me"),
			ExpirationHours: jwtExpHours,
		},
		CORS: CORSConfig{
			AllowedOrigins: []string{
				getEnv("CORS_ALLOWED_ORIGINS", "http://localhost:3000"),
			},
		},
	}
}

// getEnv 取得環境變數，若不存在則返回預設值
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
