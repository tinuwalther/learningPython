import requests, json

# Initialize variables
webhook_url         = 'your webhook address'
author_name         = 'Python Hook'
author_avatar       = 'http://img1.wikia.nocookie.net/__cb20111027212138/pichipichipitchadventures/es/images/thumb/f/fd/Captain-Hook-Wallpaper-disney-villains-976702_1024_768.png/456px-Captain-Hook-Wallpaper-disney-villains-976702_1024_768.png'

section_title       = '[INFO] Send with Python'
section_description = 'Invoke-RestMethod to the WebHookUrl'
section_color       = 16760576 #FFBF00

fact_title          = "You are boarded"
fact_message        = "Python Hook boarded your messenger!"

# New section as embed object
embeds = {
    'title'       : section_title,
    "description" : section_description,
    "color"       : section_color,
    'fields'      : [
        {"name" : fact_title, "value" : fact_message, "inline": "false"},
    ],
}

# Full message
data = {
    'username'  : author_name,
    'avatar_url': author_avatar,
    "embeds"    : [embeds],
}

# Content-Type
headers = {
    "Content-Type": "application/json"
}

result = requests.post(webhook_url, json=data, headers=headers)
if 200 <= result.status_code < 300:
    print(f"[INFO] Webhook sent {result.status_code}")
else:
    print(f"[WARN] Not sent with {result.status_code}, response:\n{result.json()}")