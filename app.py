import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["joke", "oil","type","jokedraw","oildraw","retype"],
    transitions=[
        {
            "trigger": "advance",
            "source": "type",
            "dest": "joke",
            "conditions": "is_going_to_joke",
        },
        {
            "trigger": "advance",
            "source": "type",
            "dest": "oil",
            "conditions": "is_going_to_oil",
        },
        {
             'trigger': 'advance',
            'source': 'joke',
            'dest': 'jokedraw',
            'conditions': 'is_going_to_jokedraw'
        },
        {
             'trigger': 'advance',
            'source': 'oil',
            'dest': 'oildraw',
            'conditions': 'is_going_to_oildraw'
        },
        { 
            "trigger": "go_back", 
            "source": 'jokedraw', 
            "dest": "joke"
            },
            
             { 
            "trigger": "go_back", 
            "source": 'oildraw', 
            "dest": "oil"
            },
             { 
            "trigger": "advance", 
            "source":['oildraw','jokedraw','type',"joke", "oil"] , 
            "dest": "retype"
            },
            { 
            "trigger": "go_back", 
            "source": 'retype', 
            "dest": "type"
            },

            
    ],
    initial="type",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    keyword = ["笑話","撩妹","抽卡","重新"]
    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            line_bot_api.reply_message(event.reply_token, canmessage)
            continue
        
        for key in keyword:

            if(key == event.message.text): 
                response = machine.advance(event)
                if response == False:
                    send_text_message(event.reply_token, "ERROR")
                # else:
                #     send_text_message(event.reply_token, "ENTERING STATE")
                print(f"\nFSM STATE: {machine.state}")
                return "OK"
        

    print(f"\nFSM STATE: {machine.state}")
    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
