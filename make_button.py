from flask import Flask, request
import requests
import json
import utilits
 
app = Flask(__name__)

#Кнопка в телеге, которая отвечает за какую то операцию

def button(chat_id, text):

    method = "sendMessage"
    code = utilits.token
    url = f"https://api.telegram.org/bot{code}/{method}"
    data = {"chat_id": chat_id, "text": text, "reply": json.dumps({"inline_keyboard": [[{
        "text": "Какое то действие"
    }]]})}

    requests.post(url, data=data)

#Функкция которая делает запрос в телегу

def report_messages(chat_id, text):
    method = "sendMessage"
    code = utilits.token
    url = f"https://api.telegram.org/bot{code}/{method}"

#данные которые мы отправляем в этом запросе
    data_address = {"chat_id": chat_id, "text": text}
    requests.post(url, data_address=data_address)

@app.route("/", methods=["POST"])
def dialog():
    chat_id = request.json["message"]["chat"]["id"]
    button(chat_id=chat_id, text='Сообщение получено')
    return {"ok": True}
 
 
if __name__ == "__main__":
    app.run()