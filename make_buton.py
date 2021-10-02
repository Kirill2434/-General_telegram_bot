from flask import Flask, request
import requests
import json
import utilits
 
app = Flask(__name__)

def report_messages(chat_id, text):
    method = "sendMessage"
    code = utilits.token
    url = f"https://api.telegram.org/bot{code}/{method}"
    data_address = {"chat_id": chat_id, "text": text}
    requests.post(url, data_address=data_address)

def s_messege (chat_id, text = 'Результат получен'):
    method = "sendMessage"
    code = utilits.token
    url = f"https://api.telegram.org/bot{code}/{method}"
    answer = {'chat_id': chat_id, 'text': text}
    r = request.post(url, json=answer)
    return r.json()




@app.route("/", methods=["POST"])
def dialog():
    return {"ok": True}
 
 
if __name__ == "__main__":
    app.run()