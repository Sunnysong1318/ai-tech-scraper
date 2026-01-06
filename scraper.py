import csv
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        data_list = []
        page.goto("https://news.ycombinator.com/")

        # 抓取前 5 頁
        for page_num in range(1, 5):
            print(f"正在抓取第 {page_num} 頁...")
            
            # 等待標題出現
            page.wait_for_selector(".titleline")
            items = page.locator(".titleline > a").all()
            
            for item in items:
                title = item.inner_text()
                link = item.get_attribute("href")
                data_list.append([title, link])
            
            # "More"
            if page_num < 2:
                # 找到 "More" 
                more_button = page.locator(".morelink")
                if more_button.is_visible():
                    more_button.click()
                    # 給一點緩衝時間讓頁面加載
                    page.wait_for_load_state("networkidle")
                else:
                    break

        # 儲存結果
        with open('multi_page_news.csv', 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['標題', '連結'])
            writer.writerows(data_list)
            
        browser.close()
        print(f"成功！共抓取 {len(data_list)} 筆資料，已存入 multi_page_news.csv")

if __name__ == "__main__":
    run()