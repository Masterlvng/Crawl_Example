import re
import gevent
from gevent import monkey;monkey.patch_socket(dns=False)
import requests as rq
from pyExcelerator import *
import time,datetime
BASE_URL = 'http://finance,yahoo.com/q/hp?s=^DJI'

def format_d(d_str):
    conv_month = {'Jan':'1',
                  'Feb':'2',
                  'Mar':'3',
                  'Apr':'4',
                  'May':'5',
                  'Jun':'6',
                  'Jul':'7',
                  'Aug':'8',
                  'Sep':'9',
                  'Oct':'10',
                  'Nov':'11',
                  'Dec':'12'}
    l_date=re.split('\W+',d_str)
    if l_date[0] in conv_month:
        l_date[0] = conv_month[l_date[0]]
    return reduce(lambda x,y:x + '-' +y,l_date)

def last_position(url):
    p = re.compile('y=(.*)">Last')
    html = rq.get(url,headers={'Host':'finance.yahoo.com'}).text
    rst = p.findall(html)
    return rst[0] if len(rst) else None

def create_task(url):
    end_pos = last_position(url)
    if end_pos:
        page = map(str,range(0,int(end_pos)+66,66))
        return [url + '&z=66&y=' + offset for offset in page[1:] ]
    else:
        return [url]

def worker(url,fp,offset):
    tbre = re.compile('</th></tr><tr>(.*)\ *',re.M)
    ctre = re.compile('">(.*?)<')
    html = rq.get(url,headers={'Host':'finance.yahoo.com'}).text
    table = tbre.findall(html)
    cell = ctre.findall(table[0])
    row = offset - 1
    for x in range(len(cell)):
        col = x % 7
        if not col:
            row += 1
            fp.write(row,col,format_d(cell[x]))
        else:
            fp.write(row,col,cell[x])

def dispatch_task(task,fp):
    jobs = [ gevent.spawn(worker,t,fp,i*66)   for i,t in enumerate(task)]
    gevent.joinall(jobs,timeout=10)





if __name__ == '__main__':

    w = Workbook()
    ws = w.add_sheet('1')
    start = time.time()
    task = create_task('http://67.195.146.230/q/hp?s=^DJI')
    dispatch_task(task,ws)
    w.save('demo.xls')
    end = time.time()
    print 'finished!'
    print 'It costs',str(datetime.timedelta(seconds=(end-start)))
