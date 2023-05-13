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

app = Flask(__name__)

line_bot_api = LineBotApi('xhaFrelNRXRIFeQWVo4KdS0I9rDYkAQJb5j54Gw1z8vcUH+BLJa7RO0kCcKPO2WB244JWi+I4zSpN8Rhw3+eBAlTiwpCv3aOQp+rhWfJjpvuVbhH11tkteIthqOE1NLl5a3OBif0l+mXN9SGdwcqkAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c40b2a1ffbfb8115c9a7dbb5d1b38972')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()