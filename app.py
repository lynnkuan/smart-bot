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

line_bot_api.push_message('U8e9d4f515c2539e3dd57be4d5aa8e106', TextSendMessage(text='HiHi寶貝帆，我愛你！'))

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
