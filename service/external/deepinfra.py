import requests
from service.config import DeepinfraConfig

token = DeepinfraConfig.KEY
endpoint = DeepinfraConfig.ENDPOINT
def createRequest(message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }

    body = {
        "model": "google/gemma-2-9b-it",
        "messages": [
            {
                "role": "user",
                "content": "{}".format(message)
            }
        ]
    }

    request = requests.post(endpoint, json=body, headers=headers)
    if request.status_code == 200:
        data = request.json()
        answer = data['choices']
        for obj in answer:
            mess = obj['message']
            ans = mess['content']
            print(ans)
    else:
        return "Что-то пошло не так. Попробуй, плиз, позже"
    return ans
