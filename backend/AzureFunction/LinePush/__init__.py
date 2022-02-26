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
        uuid = payload['uuid']
        message = payload['message']

        if(uuid != ""):
            PushMessage(uuid, message)

    except Exception as e: 
        logging.error(e)
        pass
    
    return func.HttpResponse(f"This HTTP triggered function executed successfully.")


def PushMessage(uuid, message):
    
    data = {
        "to": uuid,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }

    data = json.dumps(data)

    result = requests.post(LINE_MESSAGING_API , headers = LINE_HEADER, data = data)

    logging.info(result.text)
