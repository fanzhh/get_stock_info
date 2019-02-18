# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class StockDataItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stock_id = Field()  # 股票代码
    ddate = Field()     # 日期
    openning = Field()  # 开盘价
    high = Field()      # 最高
    ending = Field()    # 收盘价
    low = Field()       # 最低
    trading = Field()   # 交易量
    amount = Field()    # 交易金额
