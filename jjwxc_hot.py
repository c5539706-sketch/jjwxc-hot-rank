import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def fetch_jjwxc_hot():
    # 晋江总收藏榜URL
    url = "https://www.jjwxc.net/bookbase.php?fw0=0&fbsj0=0&yc0=0&xx0=0&mainview0=0&sd0=0&lx0=0&library0=0&thumbs0=0&sortType=2&page=1"
    
    # ⚠️ 重要：必须替换成你自己的Cookie！现在先填个占位符
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Cookie': 'your_cookie_here'   # ← 先这样填，别留空字符串
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'lxml')
        
        books = []
        # 简单示例：取前10个有title属性的a标签（你需要根据实际页面结构调整）
        for item in soup.select('tr')[1:11]:
            title_tag = item.select_one('a[title]')
            if title_tag:
                books.append({
                    'title': title_tag.get('title', ''),
                    'url': 'https://www.jjwxc.net' + title_tag.get('href', ''),
                    'platform': '晋江',
                    'rank_source': '总收藏榜'
                })
        
        output = {
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'platform': 'jjwxc',
            'books': books[:10]
        }
        
        # 保存为JSON文件
        with open('jjwxc_hot.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print("✅ 热榜更新成功，共抓取", len(books), "本书")
        
    except Exception as e:
        print(f"❌ 失败：{e}")

if __name__ == '__main__':
    fetch_jjwxc_hot()
