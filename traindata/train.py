import requests
from bs4 import BeautifulSoup
url = "https://tip.railway.gov.tw/tra-tip-web/tip"
Data = requests.get(url)
Data.encoding = "utf-8"

sp = BeautifulSoup(Data.text, "html.parser")
result=sp.select(".map-panel a")
info = ""
for item in result:
  info += item.text + ""
print(info)