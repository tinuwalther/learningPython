import requests, json

webhook_url     = 'your Webhook address'
author_name     = 'Python Hook'
author_avatar   = 'http://panks.me/images/posts/python-logo.png'
section_title   = '[INFO] Hello python coders'
fact_title      = "Embeded message"
fact_message    = "I send this message over a jupyter notebook from my iMac!"

embeds = {
    'title': section_title, "color": 32767,
    'fields': [
        {"name" : fact_title, "value" : fact_message, "inline": "false"},
    ],
}

data = {
    'username': author_name, 'avatar_url': author_avatar, "embeds": [embeds],
}

headers = {
    "Content-Type": "application/json"
}

result = requests.post(webhook_url, json=data, headers=headers)
if 200 <= result.status_code < 300:
    print(f"[INFO] Webhook sent {result.status_code}")
else:
    print(f"[WARN] Not sent with {result.status_code}, response:\n{result.json()}")