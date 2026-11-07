import os
import json
import requests

TOKEN = os.environ["BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}/"

FILE = "usernames.json"


def load_users():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []


def save_users(users):
    with open(FILE, "w") as f:
        json.dump(users, f)


def send(chat_id, message):
    requests.post(API + "sendMessage", data={
        "chat_id": chat_id,
        "text": message
    })


def main():
    users = load_users()
    offset = 0

    while True:
        data = requests.get(API + "getUpdates", params={
            "offset": offset,
            "timeout": 30
        }).json()

        for update in data.get("result", []):
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            chat = msg.get("chat", {})
            chat_id = chat.get("id")
            text = msg.get("text", "")

            if not chat_id:
                continue

            if text == "/start":
                send(chat_id,
                     "مرحباً بك في Insta Monitor 🔍\n"
                     "أرسل /add username لإضافة يوزر للمراقبة.\n"
                     "أرسل /list لعرض القائمة.")

            elif text.startswith("/add "):
                username = text.split(maxsplit=1)[1].strip().lstrip("@")

                if username not in users:
                    users.append(username)
                    save_users(users)

                send(chat_id, f"تمت إضافة @{username} للقائمة.")

            elif text == "/list":
                send(chat_id, "\n".join("@" + u for u in users)
                     if users else "القائمة فارغة.")

            elif text.startswith("/remove "):
                username = text.split(maxsplit=1)[1].strip().lstrip("@")
                if username in users:
                    users.remove(username)
                    save_users(users)
                send(chat_id, "تم تحديث القائمة.")


if __name__ == "__main__":
    main()
