import logging
import requests
import json
import azure.functions as func

LINE_MESSAGING_API  = 'https://api.line.me/v2/bot/message/reply'

LINE_HEADER = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': 'Bearer YOUR-ACCESS-TOKEN'
}

def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')

    try:
        payload = req.get_json()
        replyToken = payload['events'][0]['replyToken']
        message = payload['events'][0]['message']['text']

        switcher = {
            'ดี': "ดีมาก",
            'สวัสดี': "สวัสดีครับ/ค่ะ",
            'ลาก่อน': "แล้วพบกันใหม่",
        }

        replyMessage = switcher.get(message, "")

        if(replyMessage != ""):
            ReplyMessage(replyToken, replyMessage)

    except:
        pass
    
    return func.HttpResponse(f"This HTTP triggered function executed successfully.")


def ReplyMessage(replyToken, replyMessage):
    
    data = {
        "replyToken": replyToken,
        "messages": [{
            "type": "text",
            "text": replyMessage
        }]
    }

    data = json.dumps(data)

    requests.post(LINE_MESSAGING_API , headers = LINE_HEADER, data = data)
