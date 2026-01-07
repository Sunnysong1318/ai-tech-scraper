import os
import sys
from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
from groq import Groq
# 注意：這裡改用 sync_api
from playwright.sync_api import sync_playwright

# 加載環境變數
load_dotenv()

app = FastAPI(title="AI News Scraper Service")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def perform_sync_scrape(url: str):
    """
    使用同步模式執行 Playwright 爬蟲，這是 Windows 上最穩定的解決方案
    """
    with sync_playwright() as p:
        # 啟動瀏覽器
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            # 模擬瀏覽器行為，設定較長的超時與等待
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            
            title = page.title()
            # 抓取網頁主要文本
            content = page.evaluate("document.body.innerText")
            return {"title": title, "content": content[:3000]}
        except Exception as e:
            print(f"爬蟲過程發生錯誤: {e}")
            raise e
        finally:
            browser.close()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "example_usage": "/analyze?url=https://news.ycombinator.com/",
        "docs": "/docs"
    }

@app.get("/analyze")
def analyze_news(url: str = Query(..., description="要分析的新聞網址")):
    """
    接收網址，爬取內容，並透過 Groq AI 生成摘要
    """
    try:
        # 1. 執行爬蟲 (同步執行)
        scraped_data = perform_sync_scrape(url)
        
        # 2. 調用 Groq AI 分析
        prompt = f"""
        你是一個科技新聞分析師，請針對以下網頁內容提供 150 字內的繁體中文精簡分析。
        
        網頁標題：{scraped_data['title']}
        內容截取：{scraped_data['content']}
        """
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "你是一位精通繁體中文的專業 AI 工程師。"},
                {"role": "user", "content": prompt}
            ]
        )
        
        # 3. 回傳最終結果
        return {
            "status": "success",
            "metadata": {
                "title": scraped_data['title'],
                "url": url
            },
            "ai_analysis": completion.choices[0].message.content
        }
        
    except Exception as e:
        print(f"後端報錯: {str(e)}")
        raise HTTPException(status_code=500, detail=f"伺服器內部錯誤: {str(e)}")

# 這是為了讓你可以直接 python main.py 執行 (可選)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)