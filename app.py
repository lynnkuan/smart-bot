#載入LineBot所需要的模組

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

app = Flask(__name__)
 
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('7p/pmQaxQEI2j94+foeP+SQ44KUiLIEL3ww8Q2cjxSysMO1HF1phVg/9WoQfiyaLAMCKF5eAJJ+uCwpHf7JfLbIV/4K5IMLUjkF6v2vd0KU2Xzo1oHLFyUiRuknfj4rsB4Paa1g7FTItIibLANScRQdB04t89/1O/w1cDnyilFU=')
 
# 必須放上自己的Channel Secret
handler = WebhookHandler('7f480d9cf76e60d1bb04c372b589eae1')

line_bot_api.push_message('U8e9d4f515c2539e3dd57be4d5aa8e106', TextSendMessage(text='HiHi該更新囉！'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
 
    return 'OK'

# 訊息傳遞區塊
import re
import requests
from bs4 import BeautifulSoup
import json
import requests
import datetime

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    def greeding(event):
        flex_message = TextSendMessage(text='您好，今日想要閱讀哪一類型的新聞',
                                quick_reply = QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label='finance',text='金融')),
                                    QuickReplyButton(action=MessageAction(label='technology',text='科技')),
                                    QuickReplyButton(action=MessageAction(label='sustainability',text='永續')),
                                    QuickReplyButton(action=MessageAction(label='international',text='國際')),
                                    QuickReplyButton(action=MessageAction(label='law',text='法遵')),
                                ]))
        url = 'https://money.udn.com/money/index'
        response = request.get(url)
        if response.status_code == 200:
         soup =  BeautifulSoup(response.text, 'html.parser')
         headlines = soup.find_all('li', class_='money-search__item')
        line_bot_api.reply_message(event.reply_token, flex_message)
def tixcraft(event):
        try:
            response2 = requests.get("https://money.udn.com/money/cate/12017?from=edn_navibar")
            root = BeautifulSoup(response2.text,"html.parser")

            concerts = root.find_all("div",class_="story_content")                 
            message2 = ""
            for concert in concerts:                                                   
                message2 += concerts.text.strip() + "\n"                
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message2))
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='tixcraft資料庫更新時段，請稍後再嘗試'))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
