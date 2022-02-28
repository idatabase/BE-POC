import logging
import requests
import json
import azure.functions as func

LINE_MESSAGING_API  = 'https://api.line.me/v2/bot/message/push'

LINE_HEADER = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': 'Bearer YOUR-ACCESS-TOKEN'
}

def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')

    try:
        payload = req.get_json()
        userId = payload['userId']
        message = payload['message']

        if(userId != ""):
            PushMessage(userId, message)

    except Exception as e: 
        logging.error(e)
        pass
    
    return func.HttpResponse(f"This HTTP triggered function executed successfully.")


def PushMessage(userId, message):
    
    data = {
        "to": userId,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }

    data = json.dumps(data)

    result = requests.post(LINE_MESSAGING_API , headers = LINE_HEADER, data = data)

    logging.info(result.text)
