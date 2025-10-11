# 智慧社交改善器 (The Smart Dating Optimizer)

一個旨在透過數據分析與智慧自動化來提升社交軟體（Tinder, 心交等）配對與互動表現的工具。本專案整合了個人檔案 A/B 測試、配對對象分析以及可自訂策略的智慧滑卡功能。

## 核心功能 (Core Features)

- **📊 個人檔案 A/B 測試 (Profile A/B Tester):** 自動輪換多組照片與自我介紹，並產出數據報告，分析各版本的配對成功率與訊息率。
- **🧠 AI 戀愛助理 (AI Matchmaker's Assistant):** 分析你右滑的對象以及成功配對者的檔案特徵（關鍵字、照片風格），幫助你理解自己的偏好與市場吸引力。
- **🤖 智慧滑卡機器人 (Smart Swiper):** 根據你自訂的規則或 AI 學習模型，自動化執行滑卡操作，只對高潛力對象按下喜歡，節省你的時間。
- **📈 表現儀表板 (Performance Dashboard):** 視覺化呈現你的配對數據、訊息回覆率等關鍵績效指標 (KPI)。

## 技術棧 (Tech Stack)

- **核心邏輯/自動化 (Core Logic/Automation):** Python (Selenium, Playwright) / Go (Rod, chromedp)
- **後端 API (Optional Backend API):** Python (FastAPI) / Node.js + TypeScript (Express) - 用於儀表板數據服務
- **前端儀表板 (Optional Frontend):** JavaScript + Svelte / React
- **數據分析/AI (Data Analysis/AI):** Python (Pandas, NLTK for text, OpenCV/Pillow for image analysis)
- **資料庫 (Database):** SQLite (用於單機快速啟動) / MongoDB (儲存非結構化的個人檔案數據)
- **CI/CD:** GitHub Actions (用於執行程式碼風格檢查與測試)

## 專案結構 (Project Structure)

/smart-dating-optimizer
├── automations/              # 主要的自動化腳本
│   ├── tinder_bot.py
│   └── hearting_bot.go
├── analysis/                 # 數據分析與洞見生成腳本
│   ├── profile_analyzer.py
│   └── stats_generator.py
├── configs/                  # 設定檔，如 A/B 測試的組合
│   ├── profile_a.json
│   └── profile_b.json
├── database/                 # 資料庫文件或遷移腳本
├── dashboard/                # (可選) 前端儀表板專案
├── main.py                   # 專案主進入點
└── requirements.txt
