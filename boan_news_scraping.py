import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


data = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

# 제목에 오늘 날짜 추가용
now = datetime.now()
formatted_date = now.strftime("%Y_%m_%d")

for i in range(1, 10 + 1): # 1 ~ 10 페이지까지
    # 보안뉴스 취약점 경고 및 보안 업데이트 페이지
    url = f"https://www.boannews.com/media/s_list.asp?Page={i}&search=&mkind=&kind=&skind=5&find="
    res = requests.get(url, headers=headers, verify=False) # SSL 인증서 무시
    html = res.text
    soup = BeautifulSoup(html, "lxml")

    for i in range(20): # 한 페이지당 20개의 기사 존재
        title = soup.select('#news_area > div > a > span')[i].text.strip() # 제목
        desc = soup.select('#news_area > div > a:nth-child(3)')[i].text.strip() # 간략한 본문
        link = "https://www.boannews.com" + soup.select('#news_area > div > a:nth-child(3)')[i]['href'] # 링크

        print("제목:", title)
        print("본문:", desc)
        print("링크:", link)
        print('-----')

        data.append([title, desc, link]) # 리스트 형식으로 제목, 본문, 링크 추가


table_headers = ["제목", "본문", "링크"] # 헤더 부분
df = pd.DataFrame(data, columns=table_headers) # 데이터 프레임 생성
df.index = df.index + 1 # 인덱스 번호 1부터
df.to_excel(f"boan_news_{formatted_date}.xlsx", index_label='No') # xlsx 형식으로 저장

print("[+] 작업이 완료되었습니다.")