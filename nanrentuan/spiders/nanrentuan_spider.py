import scrapy
from nanrentuan.items import NanrentuanItem
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader,Identity

class NanrentuanSpider(scrapy.spiders.Spider):
    name = "nanrentuan"
    allowed_domains = ['nh87.cn']
    start_urls = [
        'http://www.nh87.cn/find.html'
    ]
    url = 'www.nh87.cn'
    def parse(self,response):
        selector = Selector(response)
        articles = selector.xpath('//div[@class="vote item box"]')[:10]
        for article in articles:
            item = NanrentuanItem()
            item['name'] = ''.join(article.xpath('lable/text()').extract()) # 获取name格式为字符串而不是列表
            item['url'] = article.xpath('a/@href').extract()
            url = article.xpath('a/@href').extract()
            posturl = 'http://www.nh87.cn' + url[0]
            request = Request(posturl,callback=self.parse_detail)
            request.meta['item'] = item
            yield request

    def parse_detail(self,response):
        l = ItemLoader(response.meta['item'],response)
        # l.add_xpath('fanhao','//span[@class="list_text"]/em/b/a/text()')
        l.add_xpath('image_name','//span[@class="list_text"]/em/b/a/text()')
        photo = response.xpath('//span[@class="list_img"]/a/img/@data-original').extract()
        # item = response.meta['item']
        # item['fanhao'] = selector.xpath('//span[@class="list_text"]/em/b/a/text()').extract()
        # photo = selector.xpath('//span[@class="list_img"]/a/img/@data-original').extract()
        img = []
        for p in photo:
            img.append('http://www.nh87.cn'+p)
        l.add_value('image_urls',img)
        # 返回item
        return l.load_item()