import requests as rq
import re
from pyExcelerator import *

POST_DATA = """<?xml version="1.0" encoding="utf-16"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><GetSLFunds xmlns="http://localhost/Clients/StandardLifeHK/WebServices/SLHKWebService.asmx">\
        <filter>UnitName like '%%%s%%' or UnitNameTranslate like '%%%s%%' or ReferenceCode like '%%%s%%'</filter><sort>UnitName ASC</sort><pageNo>0</pageNo>\
        </GetSLFunds></soap:Body></soap:Envelope>"""


URL = 'http://webfund6.financialexpress.net/clients/StandardLifeHK/webservices/SLHKWebService.asmx'

class element():

    def __init__(self,HstartDate,DateRange,SLFundName,CitiCode,FundCode,\
                 TabName='PriceTab',Version='ZH-CN'):
        self.SLFundName,self.TabName = SLFundName,TabName
        self.CitiCode,self.FundCode = CitiCode,FundCode
        self.Version = Version
        self.HstartDate,self.DateRange=HstartDate,DateRange
        self.cpyear = self.HstartDate.split('/')[2]
        self.cpmonth = self.HstartDate.split('/')[1]
        self.hdMinHis='24/07/2005'
    @property
    def Data(self):
        return 'HistorystartDate='+self.HstartDate+'&cpMonth='+self.cpmonth+\
                '&cpYear='+self.cpyear+'&DateRange='+self.DateRange+'&hdMinHistoryDate='\
                +self.hdMinHis+'&hdDateRangeValue=&hdHistorystartDate='\
                '&SLFundName='+self.SLFundName+'&TabName='+self.TabName+'&CitiCode='+\
                self.CitiCode + '&Version='+self.Version+ '&FundFilterValues=%s\
                0,0,0,0,0,0,0;UnitName,ASC;First' % self.FundCode

def SLFandCiti(FundCode):
    data = POST_DATA % (FundCode,FundCode,FundCode)
    r = rq.post(URL,data,headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
                                  'Content-Type':'text/xml;charset=utf-8',\
                                  'Accept-Language':'en-US,en;q=0.5'})

    p = re.compile('UnitNameTranslate="(.*?)" CitiCode="(.*?)"')
    return p.findall(r.text)[0]

def prepare_post(Startd,Range,FundCode):
    SLFundName,CitiCode = SLFandCiti(FundCode)
    return element(Startd,Range,unicode(SLFundName).encode('utf-8'),unicode(CitiCode).encode('utf-8')\
                   ,FundCode)

def excute(elem,fp):
    url = 'http://webfund6.financialexpress.net/Clients/StandardLifeHK/FundDetails.aspx?citicode='+elem.CitiCode+'&version=CN'
    print elem.Data
    r = rq.post(url,elem.Data,headers={'Content-Type':'application/x-www-form-urlencoded'})
    content = parse_price(r.text)
    write(fp,content)

def parse_price(html):
    p = re.compile('<td class="alignCenter">(.*?)</td>')
    return p.findall(html)

def write(fp,content):
    row = -1
    for x in range(len(content)):
        col = x % 4
        if not col:
            row += 1
        fp.write(row,col,content[x])


if __name__ == '__main__':
    e = prepare_post('07/02/2012','3','02ME')
    w = Workbook()
    ws=w.add_sheet('1')
    excute(e,ws)
    w.save('demo.xls')
