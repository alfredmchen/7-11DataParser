import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/json;q=0.9,image/webp,*/*;q=0.8'
                }
dic = {'01':'台北市','02':'基隆市','03':'新北市','04':'桃園市','05':'新竹市','06':'新竹縣','07':'苗栗縣','08':'台中市','10':'彰化縣'
       ,'11':'南投縣','12':'雲林縣','13':'嘉義市','14':'嘉義縣','15':'台南市','17':'高雄市','19':'屏東縣','20':'宜蘭縣'
       ,'21':'花蓮縣','22':'台東縣','23':'澎湖縣','24':'連江縣','25':'金門縣'}


def getStoreInfo(cityid,city):
    global headers
    url = "https://emap.pcsc.com.tw/EMapSDK.aspx"
    xml = {"commandid": "GetTown", "cityid": cityid}
    resp = requests.post(url, data=xml, headers=headers).text
    soup1 = BeautifulSoup(resp, "xml")
    townTags = soup1.find_all("TownName")
    townList = []
    finaltable = pd.DataFrame(columns=('poiname', 'x', 'y', 'telno', 'faxno', 'address', "storeimagetitle"))
    for i in townTags:
        townList.append(i.get_text())
    for town in townList:
        xml2 = {"commandid": "SearchStore", "city": city, "town":town}
        resp1 = requests.post(url, data = xml2, headers = headers).text
        soup = BeautifulSoup(resp1,"xml")
        GeoTags = soup.find_all("GeoPosition")
        temp ={}
        for geo in GeoTags:
            string = str(geo)
            soup2 = BeautifulSoup(string,"xml")
            temp['poiname'] = soup2.find('POIName').get_text()
            temp['x'] = soup2.find('X').get_text()
            temp['y'] = soup2.find('Y').get_text()
            temp['telno'] = soup2.find('Telno').get_text()
            temp['faxno'] = soup2.find('FaxNo').get_text()
            temp['address'] = soup2.find('Address').get_text()
            temp['storeimagetitle'] = soup2.find('StoreImageTitle').get_text()
            finaltable = finaltable.append(temp,ignore_index=True)

    return finaltable

if __name__ == '__main__':
    sevenElevenInfo = pd.DataFrame(columns=('poiname', 'x', 'y', 'telno', 'faxno', 'address', "storeimagetitle"))
    for keys, values in dic.items():
        temp = getStoreInfo(keys,values)
        sevenElevenInfo = sevenElevenInfo.append(temp,ignore_index=True)
    sevenElevenInfo.to_excel("seveneleveninfo.xlsx",sheet_name='seveneleveninfo')









