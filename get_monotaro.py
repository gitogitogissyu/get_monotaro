#モノタロウのURLを突っ込むだけで自動的に発注フォーマットになおしてくれるプログラム．
#一応べた書きしているけど，少しなおしてあげて関数化してあげれば使いやすくなるかなーと思ったり思わなかったり

#今はモノタロウだけだけど，結局欲しいデータの部分だけjsonかなにかに書いてあとはそこから必要なデータを引っ張ってくればそれで終わりでいいのでは？？？



# ーーーーー旧コメント．見なくてもいいよーーーーーーーー

#参考https://qiita.com/Azunyan1111/items/b161b998790b1db2ff7a こっちはpython2系の話だった．
#参考https://qiita.com/Senple/items/724e36fc1f66f5b14231
# こっちがpython3系だった．
#IEEE系だと，表示させるのにJavascriptがあって，いきなりURLを読み込んでもその部分を表示してくれない問題があった．
#そのため，JSレンダリングも含めてスクレイピングするようにするため，ブラウザ（PhantomJS）をpython内で起動して，
#その結果からスクレイピングを行うことにする．
# 参考：https://www.yoheim.net/blog.php?q=20170302



import urllib3
from bs4 import BeautifulSoup
import certifi

from selenium import webdriver
from pprint import pprint
import time
from urllib import parse

import urllib.request
import sys
from collections import defaultdict

#正規表現操作に使うライブラリ
import re

chromedriver_path = r'C:\Users\Razer\Desktop\chromedriver_win32\chromedriver.exe'


# ファイルにURLを羅列的に記入してそれを読み込む関数．
# https://qiita.com/chanmaru/items/1b64aa91dcd45ad91540
import fileimport_test


def urlfile_to_format():
    filename = fileimport_test.fileimportDialog()
    f = open(filename)
    line = f.readline()
    while line:
        makeFormat(line,5)
        line = f.readline()
    f.close()



    

def makeFormat(url_, order_q = 1):

    #アクセスするURL
    url = url_#これはモノタロウのやつ

    #URLチェック．
    parse_result = parse.urlparse(url)
    if not((r"/p/" in parse_result.path) and (r"www.monotaro.com" in parse_result.hostname)):
        print("your input URL is wrong. please check agein.")
        return None

    #ブラウザ立ち上げ(ドライバの.exeファイルを起動しないとつかない)
    driver = webdriver.Chrome(executable_path=chromedriver_path)


    #ブラウザにURLを突っ込んで動かす
    driver.get(url)

    #1秒待つ．（ページ読み込み，処理部分を待つ）
    time.sleep(2)

    #ブラウザのHTML情報をよみだす
    html = driver.page_source

    #Soupに突っ込んで分解準備
    soup = BeautifulSoup(html, 'html.parser')


    #抽出部，指定の仕方はここを参照　https://qiita.com/rusarusa/items/d7f014ba80d6fe7a3e07
    result = soup.find_all("a",class_="icon-pdf")
    result_title = soup.find_all("h2",class_="")

    item_name = soup.find("span",class_="item")
    item_brand = soup.find("span",class_="itd_brand")
    item_info = soup.find("dl",class_="itd_info_dl").find_all(['dt', 'dd'])

    item_price_str = item_info[-1].get_text().replace('\n','')

    #この書き方未だに理解できていない...　https://qiita.com/ikanamazu/items/ba2a32a1a5924f3bd8e9
    all_price = int(re.sub(r"\D","",item_price_str)) * order_q


    # https://shotanuki.com/beautifulsoup%E3%81%A7%E8%A4%87%E6%95%B0%E3%82%BF%E3%82%B0%E3%82%92%E5%90%8C%E6%99%82%E3%81%AB%E6%8C%87%E5%AE%9A%E3%81%99%E3%82%8B/

    #表示部．
    print("・メーカー名："+item_brand.get_text().replace('\n',''))
    print("・製品名："+item_name.get_text())
    print("・製品コード："+item_info[1].get_text())
    print("・単価："+item_price_str)
    print("・個数："+str(order_q))
    print("・合計価格：￥"+"{:,}".format(all_price))
    print("・販売店：モノタロウ")
    print("・参考URL："+url)

    driver.close()
    
if __name__ is '__main__':
    urlfile_to_format()
    


"""
#一旦ダウンロード数に制限かける
for a in result[:3]:
    #URLを合体させるときには，urllibの中に入ってるparce.urljoinを使えば，一発でURLの基礎部分とそうじゃない部分を合体してくれる．
    #参考：https://torina.top/detail/305/
    print(parse.urljoin(url,a.get("href")))



for a in result_title:
    print(a.get_text().strip())

"""

"""
# 複数変数を回すための関数
#https://python.civic-apps.com/zip-enumerate/
for (a,b) in zip(result,result_title):
    fullurl = parse.urljoin(url,a.get("href"))
    filename = b.get_text().strip()+".pdf"

    print(fullurl)
    print(filename)

    download(fullurl,filename)

"""

# driver.get_screenshot_as_png()
"""
#https://shotanuki.com/beautifulsoup%E3%81%A7%E8%A4%87%E6%95%B0%E3%82%BF%E3%82%B0%E3%82%92%E5%90%8C%E6%99%82%E3%81%AB%E6%8C%87%E5%AE%9A%E3%81%99%E3%82%8B/
def dl_to_array_dict(product_div):
    data = defaultdict(list)
    for product in product_div.find_all(['dt', 'dd']):
        if product.name == 'dt':
            key = product.text
        if key and product.name == 'dd':
            data[key].append(product.text)
    return data
"""

