from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import requests

def checkword(w):
    url = 'https://www.moedict.tw/uni/' + w
    r = requests.get(url)
    datas = r.json()
    msg = '國字：' + datas['title'] + '\n'
    msg += '部首：' + datas['radical'] + '\n'
    msg += '筆劃：' + str(datas['stroke_count']) + '\n\n'
    for i in range(len(datas['heteronyms'])):
        msg += '注音：' + datas['heteronyms'][i]['bopomofo'] + '\n'
        msg += '拼音：' + datas['heteronyms'][i]['pinyin'] + '\n'    
        for j in range(len(datas['heteronyms'][i]['definitions'])):
            if 'type' in datas['heteronyms'][i]['definitions'][j]:
                msg += '[{}] {}\n'.format(
                    datas['heteronyms'][i]['definitions'][j]['type'],
                    datas['heteronyms'][i]['definitions'][j]['def'])
        msg += '\n'
    return msg

app = Flask(__name__)

line_bot_api = LineBotApi('PFjJexLUqZyO4NjB2vNeMMK7tZhoIJurM0jlD/8BzVCFYQoLOcM0RQ8cbRxYXBwp0347a9EqL5EyDXn/zCdC6dA1cAitwOFtRu5ROOz/C8VwR1bwSuxPckGxDz6ijKhgc5F2X7sCvqNNYhMnt+lzFQdB04t89/1O/w1cDnyilFU=')
handler1 = WebhookHandler('07e8fe603cc6a45936caf5ca294ffd1e')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=checkword(event.message.text)))


if __name__ == "__main__":
    app.run()
