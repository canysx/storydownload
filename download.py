import requests
import time
from lxml import etree
def fenleiUrl():
    page = 1
    page_num = 1
    while page < 11:
        while True:
              #"http://www.dashubao.net/fenlei/sort1/0/1.htm"
            url = "http://www.dashubao.net/fenlei/sort"+str(page)+"/0/" +str(page_num)+ ".htm"
            print("="*30)
            headers = {"User-agent":"User-Agent:Opera/9.80WindowsNT6.1;U;en)Presto/2.8.131Version/11.11"}
            data = requests.get(url,headers = headers)
            data.encoding = 'gbk'
            #print(data.text)
            page_last = etree.HTML(data.text)
            page_last = page_last.xpath('//div/a[@class="last"]/text()')
            #print(page_last)
            textUrl(data)
            page_num +=1
            if page_num > int(page_last):
                break
        page += 1
def textUrl(data):
    html = etree.HTML(data.text)
    # 找到每本小说的地址
    html = html.xpath("//div/h3/a/@href")
    #print(html)
    for item in html:
        zhangjieUrl(item)
def zhangjieUrl(item):
    headers = {"User-agent":"User-Agent:Opera/9.80WindowsNT6.1;U;en)Presto/2.8.131Version/11.11"}
    # 访问每本小说
    itemUrl = item[0:-10]
    #print(itemUrl)
    zhangjie_url = requests.get(itemUrl,headers = headers)
    zhangjie_url.encoding = 'gbk'
    #print(zhangjie_url.text)
    html = etree.HTML(zhangjie_url.text)
    # 获取小说名字
    textName = html.xpath("//h1/text()")
    print("小说名字为:" + textName[0])
    # 获取每本小说的章节
    data = html.xpath("//dd/a/@href")
    time.sleep(1)
    print("正在获取小说章节...")
    time.sleep(1)
    print("正在下载,请稍等...")
    for i in data:
        textInfo(i,itemUrl,textName)
    print("下载完成")
    print("="*30)
def textInfo(i,itemUrl,textName):
    fileName = textName[0] + ".txt"
    #print(fileName)
    url = itemUrl+i
    headers = {"User-agent":"User-Agent:Opera/9.80WindowsNT6.1;U;en)Presto/2.8.131Version/11.11"}
    info = requests.get(url,headers)
    info.encoding = 'GBK'
    #print(info.text)
    infoText = etree.HTML(info.text)
    #获取章节名字
    infoNum = infoText.xpath("//div/h2//text()")
    with open(fileName,"a",encoding='utf-8') as f:
            f.write(str(infoNum))
    # 获取章节内容
    text = infoText.xpath('//div[@class="yd_text2"]//text()')
    for i in text:
            with open(fileName,"a",encoding='utf-8') as f:
                f.write(i)
    #print(infoNum)
if __name__ == "__main__":
    fenleiUrl()
