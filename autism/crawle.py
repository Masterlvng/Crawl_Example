# -*- coding:utf-8 -*-
import re
import gevent
from gevent import monkey;monkey.patch_socket(dns=False)
import requests as rq
import StringIO
import time,datetime
CHROM = []
SYM = {}
TYPE = 'CNV'
LIST_URL = 'http://129.237.137.150/cgi/features.cgi?chrom=%s&feat_list=%s'
FILE_URL = 'http://129.237.137.150/cgi/feature_file.cgi?%s'

def init_crawle():
    chrom = range(1,23)
    chrom.append('x')
    chrom.append('y')


def obtain_list(n_chrom):
    url = LIST_URL %(n_chrom,TYPE)
    p = re.compile('<a href="./feature_file.cgi\?(.+)"',re.M)
    r = rq.get(url)
    content = r.text
    SYM[n_chrom] = p.findall(content)

def obtain_file(n_chrom):
    def write_file(filename,content):
        with open('database/'+str(filename),'w') as f:
            f.write(content)
    p = re.compile('<td>([\w\s\.\-]*)</td>',re.M)
    '''
    file = {}
    buf = StringIO.StringIO()
    for i, a in enumerate(SYM[n_chrom]):
        url = FILE_URL % a
        file[i] = p.findall(rq.get(url).text)
        print >> buf,','.join(file[i])
        print file[i]

    write_file(n_chrom,buf.getvalue())
    buf.close()
    '''
    def task(url):
        print url
        return p.findall(rq.get(url).text)

    jobs = [ gevent.spawn(task,FILE_URL %a) \
            for a in SYM[n_chrom]]
    gevent.joinall(jobs,timeout=10)
    buf = StringIO.StringIO()


    for form in jobs:
        #print >> buf,','.join(form)
        print form.value







if __name__ == '__main__':

    start = time.time()
    init_crawle()
    obtain_list(1)
    obtain_file(1)
    end = time.time()
    print str(datetime.timedelta(seconds=(end-start)))



