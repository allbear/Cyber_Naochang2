# twitter-stream1.py
import tweepy
from datetime import timedelta
from dotenv import load_dotenv
import os
import csv
import random
from os.path import join, dirname
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
CK = os.environ.get("CK")
CS = os.environ.get("CS")
AT = os.environ.get("AT")
AS = os.environ.get("AS")


class Listener(tweepy.StreamListener):
   def on_status(self, status):
      status.created_at += timedelta(hours=9)
      print('------------------------------')
      user = status.author.name
      text = status.text.replace("#imas_cg一挙配信DAY1", "")
      icon = status.author.profile_image_url.replace("normal", "400x400")

      if "retweeted_status" in status._json.keys() or "#" in text or "RT" in text:
         return True
      # if random.randint(1, 2) != 1:#対象が多いときの対策
      #     return True
      with open("../text/global_stream.csv", "a") as f:
         print(text)
         writer = csv.writer(f)
         writer.writerow([user, text, icon])
      return True

   def on_error(self, status_code):
      print('エラー発生: ' + str(status_code))
      return True

   def on_timeout(self):
      print('Timeout...')
      return True


# Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

# Listenerクラスのインスタンス
listener = Listener()
# 受信開始
stream = tweepy.Stream(auth, listener)
stream.filter(track=["imas_cg一挙配信DAY1"])  # 指定の検索ワードでフィルタ
