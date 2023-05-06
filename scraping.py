import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from datetime import datetime
#スクレイピングしたデータを入れる表を作成
list_df = pd.DataFrame(columns=['曲名','発売日', '表示回数', '歌詞'])
for page in range(1,3): # ミスチルの歌詞ページは2ページなので、範囲は1-2。 
    base_url = 'https://www.uta-net.com' 
    #歌詞一覧ページ 
    url = 'https://www.uta-net.com/artist/684/0/' + str(page) + '/' 
    response = requests.get(url) 
    soup = BeautifulSoup(response.text, 'lxml') 
    # links = soup.find_all('td', class_='side td1') 
    links = soup.find_all('td', class_='side td1') 
    for link in links: 
        a = base_url + (link.a.get('href')) 
        #歌詞詳細ページ 
        response = requests.get(a) 
        soup = BeautifulSoup(response.text, 'lxml') 
        # 曲名を取得 
        song_name = soup.find('h2').text 
        # 発売日、表示回数などを取得 
        detail = soup.find('p', class_="detail").text 
        # 発売日を取得 
        match = re.search(r'\d{4}/\d{2}/\d{2}', detail) 
        release_date = datetime.strptime(match.group(), '%Y/%m/%d').date() 
        # 表示回数を取得 
        p = r'この曲の表示回数：(.*)回' 
        impressions = re.search(p, detail).group(1) 
        # 歌詞を取得 
        song_lyrics = soup.find('div', itemprop='lyrics') 
        song_lyric = song_lyrics.text 
        song_lyric = song_lyric.replace('\n','') 
        song_lyric = song_lyric.replace('この歌詞をマイ歌ネットに登録 >このアーティストをマイ歌ネットに登録 >','') 
        #サーバーに負荷を与えないため1秒待機 
        time.sleep(1) 
        #取得した歌詞を表に追加 
        tmp_se = pd.DataFrame([[song_name], [release_date], [impressions], [song_lyric]], index=list_df.columns).T 
        list_df = list_df.append(tmp_se)
#csv保存
list_df.to_csv('list.csv', mode = 'w', encoding='utf-8')