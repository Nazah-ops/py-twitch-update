import requests
import json
class TitleGeneration:

    def __init__(self) -> None:
        pass


    @staticmethod
    def generateTitle(keyword):
        print(keyword)
        """Generates a title given a string of keywords to take as input.
        Makes a call to an third party service and gets the data as a response 
        Returns a string, wich is the AI generated title"""

        url = "https://7flz19.aitianhu1.top/api/please-donot-reverse-engineering-me-thank-you"

        payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "OPENAI_API_KEY": "sk-AItianhuFreeForEveryone",
            "options": {
                "parentMessageId": "chatcmpl-9BP8kl1RTvUPM2Uhb0fU2pqLMeDL6"
            },
            "prompt": f'''can you make a title with these keywords with maximum 6 words:{keyword} ''',
            "systemMessage": "You are an AI assistant, a large language model trained. Follow the user's instructions carefully. Respond using markdown.",
            "temperature": 0.8,
            "top_p": 1
        })
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': 'https://7flz19.aitianhu1.top',
            'Connection': 'keep-alive',
            'Referer': 'https://7flz19.aitianhu1.top/',
            'Cookie': 'sl-session=XdljNyYTFGZKXAbFoCG9bg==; SERVERID=srv99n2^|ZhLBv; sl_jwt_session=sJgSIr7PEmb2TYifeA0waA==; cdn=aitianhu; SERVERID=srv99n2|ZhLCH',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        lines = (response.text.split("\n"))
        last_item = json.loads(lines.pop())

        return last_item["text"].replace("*", "")
