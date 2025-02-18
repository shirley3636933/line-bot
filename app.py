from flask import Flask, request, abort
from linebot.v3.messaging import MessagingApi, ReplyMessageRequest
from linebot.v3.webhook import WebhookHandler, MessageEvent
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import TextMessage

app = Flask(__name__)

# ✅ 設定你的 LINE API 金鑰（請替換為你的值）
LINE_ACCESS_TOKEN = "DfGtWtvUmKbxbUUY84CHoyrztgc9/ezGvmo7INsNQbTrDAVoDURki2qaUuONj7KsZ+VeHXDODb2ODXYSZBHUhyHKcRrx3L8nJHAY32RYzyOXxc+kn7d4ZuniYdvNg4FkeoRwIPi+/0hqCBV13ADdRQdB04t89/1O/w1cDnyilFU="
LINE_SECRET = "c9faefc9e6aa82f4b43e8a79f5a92929"

# ✅ 初始化 LINE API
line_bot_api = MessagingApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_SECRET)

@app.route("/", methods=["GET"])
def home():
    return "LINE Bot 伺服器運行中！"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]  # 取得 LINE 傳來的簽名
    body = request.get_data(as_text=True)  # 取得使用者的訊息內容

    try:
        handler.handle(body, signature)  # 驗證簽名，然後交給 handler 處理
    except InvalidSignatureError:
        abort(400)

    return "OK"

# ✅ 修正這一行，確保格式正確
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if hasattr(event, "message") and hasattr(event.message, "text"):
        user_message = event.message.text  # 取得使用者傳來的訊息
        reply_text = f"你說了：{user_message}"  # 設定回應內容

        # 讓機器人回應使用者
        line_bot_api.reply_message(
            event.reply_token,
            ReplyMessageRequest(messages=[TextMessage(text=reply_text)])
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
