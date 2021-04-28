import os
from slack import WebClient
from .models import Menu
from datetime import date

def my_cron_job():
    today = date.today()
    menu = Menu.objects.get(today)

    if not menu:
        message = "Sorry team there is no menu for today :("
    else:
        uuid = str(menu.uuid)
        message = "Hi team, here is the menu for today: \n" + "http://localhost:8000/menu/" + uuid

    client = WebClient(token = "xoxb-2014251975012-1993396992055-x4VgFLcosZF0GV7dii2neb3u")
    client.chat_postMessage(
        channel = 'C020E7DVD2Q',
        text = message)