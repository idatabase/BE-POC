import logging
import requests
import json
from hashlib import sha256
import azure.functions as func

LINE_LOGIN_API  = 'https://api.line.me/v2/profile'

def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')

    try:
        payload = req.get_json()
        
        citizenId = payload['citizenId']
        mobileNo = payload['mobileNo']
        userId = payload['userId']
        accessToken = payload['accessToken']

        logging.info('citizenId = {}, mobileNo = {}, userId = {}, accessToken = {}'.format(citizenId, mobileNo, userId, accessToken))

        if(userId != "" and accessToken != "") :
            result = GetUserProfile(accessToken)

            jsonData = json.loads(str(result))
            
            if(jsonData["userId"]==userId):
                return func.HttpResponse (
                    json.dumps({
                    'customerRefNo': '{}'.format(sha256(userId.encode('utf-8')).hexdigest()),
                    }) 
                )

    except Exception as e: 
        logging.error(e)
        pass
    
    return func.HttpResponse(f"This HTTP triggered function executed successfully.")


def GetUserProfile(accssToken):

    header = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer {}'.format(accssToken)
    }

    result = requests.get(LINE_LOGIN_API , headers = header)

    logging.info(result.text)

    return result.text
