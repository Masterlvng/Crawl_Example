import re
import requests as rq

def typeCode(FundCode):
    url = 'http://webfund6.financialexpress.net/clients/zil/pricetable.aspx?\
            User=PUBLIC&Region=ME&Range=VISTA&Currency=Local&FundCode=%s' % FundCode

    p = re.compile('<td class="FundLeft"><a href="#" id="(.*?)"')
    r = rq.get(url)
    return p.findall(r.text)[0][9:]

def GetPrice(date,tcode):
    url = 'http://webfund6.financialexpress.net/clients/ZIL/WebServices/Charting.asmx'
    accept='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    type='text/xml; charset=utf-8'
    data='<?xml version="1.0" encoding="utf-16"?><soap:Envelope \
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
            xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
            xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\
            <soap:Body><LoadPriceHistories \
            xmlns="http://webfund6.financialexpress.net/clientsV21/zil/webservices/">\
            <typeCode>%s</typeCode><date>%s</date>\
            </LoadPriceHistories></soap:Body></soap:Envelope>'
    r = rq.post(url,data %(tcode,date),headers={'Accept':accept,'Content-Type':type})
    p = re.compile('<LoadPriceHistoriesResult>(.*)</LoadPriceHistoriesResult>')
    print p.findall(r.text)[0]

if __name__ =='__main__':
    t=typeCode('EQEUR')
    GetPrice('04/02/2013',t)


