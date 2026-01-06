# 🤖 AI-Powered Tech Insights Scraper

這是一個針對技術社群（如 Hacker News）開發的自動化情報採集系統。結合了現代化爬蟲技術與大語言模型（LLM），實現從數據抓取到深度分析的完整自動化流程。

## 🚀 技術核心 (Tech Stack)
- **Engine**: Python 3.12+
- **Browser Automation**: [Playwright](https://playwright.dev/) (負責處理動態加載與反爬機制)
- **AI Brain**: [Groq Cloud API](https://groq.com/) - Llama 3.1 8B (負責語義分析與摘要)
- **Environment**: Python-dotenv (確保 API 金鑰安全)
- **Version Control**: Git (採用模組化提交規範)

## ✨ 核心功能
- **動態網頁處理**：不同於傳統 `requests`，本專案使用 Playwright 模擬真人行為，能有效應對現代前端渲染的網頁。
- **LLM 批量處理 (Batching)**：為解決 API 頻率限制（429 Error），開發了數據預處理邏輯，將多條新聞合併為單一 Prompt，大幅提升效能並節省 Token。
- **安全性設計**：遵循資安最佳實踐，API Key 透過環境變數管理，防止敏感資訊外洩。

## 🛠️ 安裝與執行
1. **複製專案**:
   ```bash
   git clone [https://github.com/Sunnysong1318/ai-tech-scraper.git](https://github.com/Sunnysong1318/ai-tech-scraper.git)
   cd ai-tech-scraper