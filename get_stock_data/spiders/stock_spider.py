import scrapy
import re
import numpy as np
import csv
from datetime import datetime

from get_stock_data.items import StockDataItem

class StockSpider(scrapy.Spider):
    name = "stocks"

    def __init__(self, stock_file='', year=0, season=0, *args, **kwargs):
        super(StockSpider, self).__init__(*args, **kwargs)
        self.stock_file = stock_file
        if year == 0:
            self.year = list(range(1997,2018))
        else:
            self.year = list(range(int(year),2018))
        if season == 0:
            self.season = [1,2,3,4]
        else:
            self.season = [int(season)]

    def generate_urls(self,file_name,year,season):
        stock_codes = list(csv.reader(open(file_name,'rt'),delimiter=','))
        urls = []
        url_template = 'http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%d&jidu=%d'
        for stock_code in stock_codes:
            for y in self.year:
                for s in self.season:
                    urls.append(url_template % (stock_code[0],y,s))
        print(urls)
        return urls
    
    def start_requests(self):
        urls = self.generate_urls(self.stock_file,self.year,self.season)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.status != 404:
            data = response.xpath('//td/div[not(a)]/text()').extract()
            stock_date = [re.sub('\s+', '', n) for n in response.xpath('//td/div[not(strong)]/a/text()').extract()]
            if len(data) > 0:
                data_list = []
                if len(stock_date) > 0:
                    i = 0
                    for ddate in stock_date:
                        tmp = []
                        tmp.append(ddate)
                        for dd in data[i:i+6]:
                            tmp.append(dd)
                        data_list.append(tmp)
                        i = i + 6
                else:
                    data = [re.sub('\s+','',n) for n in data]
                    step = 7
                    for i in range(0,len(data),step):
                        data_list.append(data[i:i+7])
                match = re.search('stockid/(.+?).phtml',response.url)
                if match:
                    stock_id = match.group(1)
                else:
                    stock_id = '00000'
                #with open("data/%s.csv" % stock_id,'a') as f:
                #    wr = csv.writer(f)
                #    wr.writerows(data_list)
                item = StockDataItem()
                for d in data_list:
                    item['stock_id'] = stock_id
                    item['ddate'] = d[0]
                    item['openning'] = d[1]
                    item['high'] = d[2]
                    item['ending'] = d[3]
                    item['low'] = d[4]
                    item['trading'] = d[5]
                    item['amount'] = d[6]
                    yield item

