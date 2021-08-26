import os
from fake_useragent import UserAgent
import requests
import chromedriver_binary
from selenium import webdriver
from bs4 import BeautifulSoup
from decimal import Decimal, Context
import time
import datetime
import config  # config.pyから.envの内容をimport

# 静大ID
SHIZUDAI_ID = config.MY_SHIZUDAI_ID
# パスワード
PASS_WORD = config.MY_PASS_WORD
# 学務情報システムのURL
BASE_URL = config.BASE_URL
# 自分で取得したLINE Notifyのトークン
LINE_TOKEN = config.LINE_NOTIFY_TOKEN
# LINE NotifyのAPIのURL
LINE_API = config.LINE_NOTIFY_API

# ChromeDriverをbroserとして変数化
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.getcwd() + "/headless-chromium"    
browser = webdriver.Chrome(os.getcwd() + "/chromedriver",chrome_options=chrome_options)

def gakujo_login(url, user_id, password):  # 学務情報システムにログインするメソッド
    browser.implicitly_wait(3)
    browser.get(url)
    print("ログインページにアクセス")
    print(browser.current_url)
    time.sleep(1)

    # ログイン画面へ遷移
    name = "btn_login"
    to_login = browser.find_element_by_class_name(name)
    to_login.click()
    time.sleep(1)

    # 　静大IDを入力
    id = "username"
    element = browser.find_element_by_id(id)
    element.clear()
    element.send_keys(user_id)
    time.sleep(1)

    # パスワードを入力
    id = "password"
    element = browser.find_element_by_id(id)
    element.clear()
    element.send_keys(password)
    time.sleep(1)

    # POST!!!!ログインボタンを押す
    name = "_eventId_proceed"
    login_form = browser.find_element_by_name(name)
    login_form.click()
    print("学務情報システムにログインしたぞ〜")
    time.sleep(1)


def access_kyoumu_system():  # 教務システムにアクセスするメソッド
    # 教務システムにアクセス
    selector = "ul.list-arrow.ml15 > li.icon-arrow-gray > a"
    kyoumu_link = browser.find_element_by_css_selector(selector)
    kyoumu_link.click()
    print("教務システムにアクセスしました")

    # ウィンドウハンドルを取得
    allHandles = browser.window_handles

    # 操作を新規ウィンドウに移す
    browser.switch_to_window(allHandles[1])


def access_seiseki():  # 成績情報ページにアクセスするメソッド
    # 成績情報の参照
    selector = "body > table:nth-child(4) > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td:nth-child(2) > a"
    element = browser.find_element_by_css_selector(selector)
    element.click()
    print("成績一覧ページきた")

    # 報告日順にする
    selector = "body > table:nth-child(10) > tbody > tr > td > table > tbody > tr:nth-child(1) > td:nth-child(10) > a"
    element = browser.find_element_by_css_selector(selector)
    element.click()
    selector = "body > table:nth-child(10) > tbody > tr > td > table > tbody > tr:nth-child(1) > td:nth-child(10) > a"
    element = browser.find_element_by_css_selector(selector)
    element.click()
    print(browser.current_url)
    time.sleep(1)


def decimal_normalize(f):
    """数値fの小数点以下を正規化し、文字列で返す"""
    def _remove_exponent(d):
        return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()
    a = Decimal.normalize(Decimal(str(f)))
    b = _remove_exponent(a)
    return str(b)


def notify_new_grade(token, api):
    # 成績情報の参照ページのHTMLを取得
    html = browser.page_source

    # ファイルハンドルを引数に生成
    soup = BeautifulSoup(html, 'html.parser')

    # テーブルを指定
    table = soup.find_all('table')
    result = table[14]
    tds = result.find_all('td')
    array = []

    # テーブルの内容をlistに追加
    for td in tds:
        array.append(td.text)

    # listをフォーマット
    array = [t.replace('\n', '') for t in array]
    array = [t.replace('\t', '') for t in array]
    array = [t.replace('\u3000', '') for t in array]
    array = [t.strip() for t in array]
    # ['科目名', '担当教員名', '科目区分', '必修選択区分', '単位', '評価', '得点', '科目GP', '取得年度', '報告日']
    new_array = array[0:11]
    print(new_array)

    # 成績だけの配列を生成
    grade_array = array[11:]
    print(len(grade_array))
    class_num = len(grade_array)/11
    print(class_num)

    # 講義の数をint型にする
    class_num = decimal_normalize(class_num)
    class_num = int(class_num)

    # 空の配列に成績を1講義ずつ入れる。
    all_grades = []
    for n in range(class_num):
        all_grades.append(grade_array[11*(n-1):11*n])
    print(all_grades)

    # 今日の日付 yyyy-mm-dd 形式
    now = datetime.date.today()

    # 文字列に変換
    now = now.strftime('%Y-%m-%d')
    print(now)

    # class_nameで配列を検索し、該当するものを返す
    line_array = [d for d in all_grades if now in d]
    print(line_array)

    # listの長さを取得
    line_num = len(line_array)
    print(line_num)

    # listの長さで条件分岐し、LINEのメッセージを決める
    # 今日の成績が出ていればその成績をNotify
    if line_num > 1:
        n = 0
        while n < line_num:
            message = '\n' + line_array[n][0]+' '+line_array[n][5] + \
                ' '+line_array[n][6]+'点 ' + ' GP '+line_array[n][7]
            n = n+1
            payload = {'message': message}
            headers = {'Authorization': 'Bearer ' + token}
            requests.post(api, data=payload, headers=headers)
    # ここを消せば出ていない時の通知をオフにします
    else:
        message = '\n更新された成績はありません'
        payload = {'message': message}
        headers = {'Authorization': 'Bearer ' + token}
        requests.post(api, data=payload, headers=headers)


def line_notify():
    gakujo_login(BASE_URL, SHIZUDAI_ID, PASS_WORD)
    access_kyoumu_system()
    access_seiseki()
    notify_new_grade(LINE_TOKEN, LINE_API)
    browser.quit()
