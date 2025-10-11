package model

import (
	"testing"
)

func TestUserTableName(t *testing.T) {
	user := User{}
	expected := "users"
	
	if user.TableName() != expected {
		t.Errorf("Expected table name %s, got %s", expected, user.TableName())
	}
}

func TestUserModel(t *testing.T) {
	user := User{
		Email:    "test@example.com",
		Username: "testuser",
	}
	
	if user.Email != "test@example.com" {
		t.Errorf("Expected email test@example.com, got %s", user.Email)
	}
	
	if user.Username != "testuser" {
		t.Errorf("Expected username testuser, got %s", user.Username)
	}
}

