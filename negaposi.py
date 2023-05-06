from janome.tokenizer import Tokenizer
import pandas as pd
import collections
import plotly.graph_objects as go

# カラム名と値の位置ずれを制御
pd.set_option('display.unicode.east_asian_width', True)

# csvファイルを読み込み
df_dic = pd.read_csv('wago.121808.pn', sep='\t', names=("判定", "用言"), encoding='utf-8')

# ネガ、ポジの表現に変更する
print(df_dic)
print(df_dic["判定"].value_counts())
df_dic["判定"] = df_dic["判定"].str.replace(r"\（.*\）", "", regex=True)

# 用言のスペースを無くしておく
df_dic["用言"] = df_dic["用言"].str.replace(" ", "")
keys = df_dic["用言"].tolist()
values = df_dic["判定"].tolist()
dic = dict(zip(keys, values))

# 歌詞の用言を読み込む
# csvファイルを読み込み
df_file = pd.read_csv('mrchildren-lyrics.csv', encoding='utf-8')

# 歌詞をデータフレームからリストに変換
song_lyrics = df_file['歌詞'].tolist()
t = Tokenizer()
word_list = []
for s in song_lyrics:
    result = [token.base_form for token in t.tokenize(s) if token.part_of_speech.split(',')[0] in ['動詞']] 
    word_list.extend(result)

# 削除するワードをリスト化（動詞）
stopwords = ['合う', 'あう','する', 'てる', 'いる', 'れる', 'なる', 'ある', 'いく', 'くれる', 'くる', 'く', 'られる', 'みる', 'しまう', 'ゆく', 'せる', 'やる']
for stopword in stopwords: 
    word_list = [i for i in word_list if i != stopword]

# 全用言数をカウント
word_list_num = len(word_list)

# 各用言が辞書にあるか確認し、あれば感情とともに配列に格納
results = []
for sentence in word_list: 
    word_score = [] 
    score = dic.get(sentence) 
    word_score = (sentence, score) 
    results.append(word_score)
p_lists = []
n_lists = []
None_lists = []
for result in results: 
    if result[1] == 'ポジ': 
        p_lists.append(result[0]) 
    elif result[1] == 'ネガ': 
        n_lists.append(result[0]) 
    else: None_lists.append(result[0])

# 円グラフ用にリストを作っておく
pie_list = []

# グラフ用にデータを抽出
x = p_lists
c = collections.Counter(x)
graph_list = dict(c.most_common())

# graph_list = {k:v for k, v in graph_list.items() if v > 50}
# plotlyでグラフ化
graphtitle = "全動詞数 = " + str(word_list_num) + "　ポジティブに分類された数 = " + str(len(x))
fig = go.Figure([go.Bar(x=list(graph_list.keys()), y=list(graph_list.values()))])
fig.update_layout(title={'text': graphtitle})
fig.show()

# グラフをhtml形式で保存。
filename = "verb-posi"
with open(filename + '.html', 'w') as f: 
    f.write(fig.to_html(include_plotlyjs='cdn'))

# 円グラフ用のリストに追加
pie_list.append(len(x))

# グラフ用にデータを抽出
x = n_lists
c = collections.Counter(x)
graph_list = dict(c.most_common())

# graph_list = {k:v for k, v in graph_list.items() if v > 50}
# plotlyでグラフ化
graphtitle = "全動詞数 = " + str(word_list_num) + "　ネガティブに分類された数 = " + str(len(x))
fig = go.Figure([go.Bar(x=list(graph_list.keys()), y=list(graph_list.values()))])
fig.update_layout(title={'text': graphtitle})
fig.show()

# グラフをhtml形式で保存。
filename = "verb-nega"
with open(filename + '.html', 'w') as f: 
    f.write(fig.to_html(include_plotlyjs='cdn'))

# 円グラフ用のリストに追加
pie_list.append(len(x))

# グラフ用にデータを抽出
x = None_lists
c = collections.Counter(x)
graph_list = dict(c.most_common())

# graph_list = {k:v for k, v in graph_list.items() if v > 10}
# plotlyでグラフ化
graphtitle = "全動詞数 = " + str(word_list_num) + "　分類されなかった数 = " + str(len(x))
fig = go.Figure([go.Bar(x=list(graph_list.keys()), y=list(graph_list.values()))])
fig.update_layout(title={'text': graphtitle})
fig.show()

# グラフをhtml形式で保存。
filename = "verb-none"
with open(filename + '.html', 'w') as f: 
    f.write(fig.to_html(include_plotlyjs='cdn'))

# 円グラフ用のリストに追加
pie_list.append(len(x))

# 円グラフを作成
labels = ['positive','negative', 'None']
fig = go.Figure(data=[go.Pie(labels=labels, values=pie_list, pull=[0.2, 0.2, 0])])
fig.update_traces(direction='clockwise')
fig.show()

# グラフをhtml形式で保存。
filename = "verb-pie"
with open(filename + '.html', 'w') as f: 
    f.write(fig.to_html(include_plotlyjs='cdn'))