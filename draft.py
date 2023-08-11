import requests
from videoThreads import videoThread
import time

print('Starting...')

url = 'https://live-akc-sa-east-1.media.starott.com/gru1/qb01/starplus/event/2023/08/10/Janela_Completa_Olimpia_P_20230810_1691703952031/cmaf-cenc-ctr-1200K/1200_slide.m3u8'

thread = videoThread(url, 'https://www.starplus.com')
thread.start()

time.sleep(300)

thread.subprocess.wait()