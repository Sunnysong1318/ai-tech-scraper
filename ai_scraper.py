import csv
import os
from dotenv import load_dotenv
from groq import Groq
from playwright.sync_api import sync_playwright

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("找不到 API Key，請檢查 .env 檔案設定！")

client = Groq(api_key=api_key)

def analyze_all_news(news_list):
    try:
        # 1. 內容清洗：移除可能導致 JSON 解析失敗的特殊符號
        # 只取前 100 條
        titles = [n[0].replace('"', '').replace("'", "") for n in news_list[:100]]
        formatted_news = "\n".join([f"- {t}" for t in titles])
        
        # 2. 極簡化呼叫：移除所有非必要參數
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {
                    "role": "user",
                    "content": f"這是技術新聞標題，請用繁體中文總結成 3 個重點：\n\n{formatted_news}"
                }
            ],
            temperature=0.5, # 增加穩定性
            max_tokens=500   # 限制輸出長度，避免超時
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI 報錯詳情: {str(e)}"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("🚀 正在抓取多頁數據...")
        all_news = []
        page.goto("https://news.ycombinator.com/")
        
        # 抓取前 3 頁，累積數據
        for _ in range(3):
            page.wait_for_selector(".titleline")
            items = page.locator(".titleline > a").all()
            for item in items:
                all_news.append([item.inner_text(), item.get_attribute("href")])
            
            # 翻頁
            more_btn = page.locator(".morelink")
            if more_btn.is_visible():
                more_btn.click()
                page.wait_for_load_state("networkidle")

        print(f"📊 抓取完成，共 {len(all_news)} 條。正在啟動 AI 批量分析...")
        
        final_report = analyze_all_news(all_news)
        
        print("\n=== AI 深度分析報告 ===")
        print(final_report)
        
        # 儲存報告
        with open('final_tech_report.txt', 'w', encoding='utf-8') as f:
            f.write(final_report)
            
        browser.close()
        print("\n✅ 任務成功！報告已儲存。")

if __name__ == "__main__":
    run()