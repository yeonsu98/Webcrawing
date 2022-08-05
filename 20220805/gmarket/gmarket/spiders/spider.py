import scrapy
from gmarket.items import GmarketItem

class GMSpider(scrapy.Spider):
    name = "GMB"
    allow_domain = ["gmarket.co.kr"] # 설정한 도메인에서만 수집
    start_urls = ["http://corners.gmarket.co.kr/Bestsellers"] # 최초 requests, response하는 url
    
    def parse(self, response):# parse 이름 바꾸면 안됨
        links = response.xpath('//*[@id="gBestWrap"]/div/div[3]/div/ul/li/a/@href').extract()
        for link in links[:20]:
            yield scrapy.Request(link, callback=self.parse_content)
    
    def parse_content(self, response):
        item = GmarketItem()
        item["title"] = response.xpath('//*[@id="itemcase_basic"]/div[1]/h1/text()')[0].extract()
        item["price"] = response.xpath('//*[@id="itemcase_basic"]/div[1]/p/span/strong/text()')[0].extract()
        item["link"] = response.url
        yield item
