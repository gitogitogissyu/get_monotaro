import os

from slackclient import SlackClient 
import time

def channel_list(client):
    channels = client.api_call("channels.list")
    if channels['ok']:
        return channels['channels']
    else:
        return None



def send_message(client, channel_id, message):
    client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message)

def init():
    slack_token = r"xoxb-613121361426-669239468036-LgjGQsPP4q5dOb03F0OqQ0cE"
    client = SlackClient(slack_token)
    channel_list(client)


#https://qiita.com/Washio3146/items/1fc60e7781cbd3d283a5
def readslack_(client):
    #疎通確認
    client.rtm_connect()
    #ループで追あ回すため変数を初期化
    rtm_read_jsondata = None
    rtm_read_jsondata = client.rtm_read()
    #1秒待つAPI
    time.sleep(1)
    print(rtm_read_jsondata)



def whileLoop(client):
    while(True):
        print(client.rtm_read())
        time.sleep(1)




