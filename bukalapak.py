import scrapy
import time
import socks
import socket
import requests
from random import randint


'''
Untuk mendapatkan data selector seperti di bawah ini, lakukan interogasi data secara manual dengan scrapy shell terlebih dahulu,
$> scrapy shell 'url'

response.css('article.product-display::attr(data-name)').extract() #judul barang
response.css('span.product__condition::text').extract() #kondisi barang bekas/baru
response.css('h5.user__name a::text').extract() # penjual
response.css('div.user-city a.user-city__txt::text').extract() #kota penjual
response.css('div.product-price::attr(data-reduced-price)').extract() # harga barang
response.css('article.product-display::attr(data-url)').extract() #url iklan
response.css('div.product__rating span.rating::attr(title)').extract()[x], #rating barang
response.css('a.review__aggregate span::text').extract()[x], #total review 
'''

baseurl = "https://www.bukalapak.com"

def ToRify():
    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
    socket.socket = socks.socksocket
    currentip = requests.get("http://icanhazip.com").text
    print "=================="
    print "ToRify Using IP Address: " + currentip
    print "=================="

class LapakSpider(scrapy.Spider):
    name = "bukalapak"
    start_urls = ["https://www.bukalapak.com/products?utf8=&source=navbar&from=omnisearch&page=&search_source=omnisearch_organic"]
    currentpage = 1
    def parse(self,response):
        x = 0
        ToRify()
        for barang in response.css('li.product--sem'):
            yield {
            'Barang': response.css('article.product-display::attr(data-name)').extract()[x], # judul barang
            'Kondisi': response.css('span.product__condition::text').extract()[x], #kondisi barang bekas/baru
            'Penjual': response.css('h5.user__name a::text').extract()[x], # penjual
            'Kota': response.css('div.user-city a.user-city__txt::text').extract()[x], #kota penjual
            'Harga': response.css('div.product-price::attr(data-reduced-price)').extract()[x], # harga barang
            'URL': response.css('article.product-display::attr(data-url)').extract()[x], #url iklan   
            #'Rating': response.css('div.product__rating span.rating::attr(title)').extract()[x], #rating barang
            #'Jumlah review': response.css('a.review__aggregate span::text').extract()[x], #total review         
            }
            x=x+1
        
        time.sleep(randint(3,15))
        
        page = self.currentpage + 1
        next_page= "https://www.bukalapak.com/products?utf8=&source=navbar&from=omnisearch&page=%s&search_source=omnisearch_organic" % page
        if response.css('li.product--sem') is not None:
            next_page = response.urljoin(next_page)
            self.currentpage = page
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
        else:
            print "Finished."
