from bs4 import BeautifulSoup
import requests

def get_html(url):
  resp = requests.get(url)
  return resp.text

def get_urls(html, starting_string):
  soup = BeautifulSoup(html)
  all_urls = []
  for a in soup.find_all('a', href=True):
    url = a['href']
    if url.startswith(starting_string):
      all_urls.append(url)
  return all_urls

get_new_currency_resp = requests.get("https://coinmarketcap.com/new/")

get_new_currency_html = get_new_currency_resp.text
all_coin_urls = get_urls(get_new_currency_html, "/currencies")
telegram_groups = []

for coin_url in all_coin_urls:
  coin_url = "https://coinmarketcap.com" + coin_url
  coin_html = get_html(coin_url)
  all_telegram_urls = get_urls( coin_html, "https://t.me")
  telegram_groups = telegram_groups +  all_telegram_urls

  clean_telegram_list = []
  for telegram_group in telegram_groups:
    if not "CoinMarketCap" in telegram_group:
      clean_telegram_list.append(telegram_group)
print(clean_telegram_list)






from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

api_id = xxx
api_hash = 'xxx'
phone = 'xxxx'
client = TelegramClient('test', api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins

#target_groups = ['https://t.me/fimimarket']
target_groups = clean_telegram_list

telegram_group_names = []
for item in target_groups:
    telegram_group_names.append(item.replace("https://t.me/",""))
print(telegram_group_names)

for target_group in telegram_group_names:
    try:

        client(JoinChannelRequest(target_group))
        all_participants = client.get_participants(target_group, aggressive=True, filter=ChannelParticipantsAdmins)

        for user in all_participants:
            receiver = user.username
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            name = (first_name + ' ' + last_name).strip()

            client.send_message(receiver, "Hey {}, Are you looking for any good marketing team for your project?".format(name, target_group))
            print("message sent to {}".format(receiver))
    except Exception as e:
        print("Error: {}".format(e))


