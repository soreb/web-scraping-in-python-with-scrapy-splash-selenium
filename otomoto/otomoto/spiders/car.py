# -*- coding: utf-8 -*-
import scrapy


class CarSpider(scrapy.Spider):
    name = 'car'
    allowed_domains = ['www.otomoto.pl']
    start_urls = ['https://www.otomoto.pl/osobowe']

    def start_requests(self):
        yield scrapy.Request(url='https://www.otomoto.pl/osobowe',callback=self.parse, headers= {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'  
        })
        
    def parse(self, response):
        for car in response.xpath("//div[@class='offer-item__content ds-details-container']"):
            yield{
                'title' : car.xpath(".//div/h2/a/@title").get(),
                'url' : car.xpath(".//div/h2/a/@href").get(),
                'year' : car.xpath(".//ul/li[@data-code='year']/span/text()").get(),
                'mileage' : car.xpath(".//ul/li[@data-code='mileage']/span/text()").get(),
                'engine_capacity' : car.xpath(".//ul/li[@data-code='engine_capacity']/span/text()").get(),
                'fuel_type' : car.xpath(".//ul/li[@data-code='fuel_type']/span/text()").get(),
                'price' : car.xpath(".//span[@class='offer-price__number ds-price-number']/span[1]/text()").get(),
                'currency' : car.xpath(".//span[@class='offer-price__currency ds-price-currency']/text()").get(),
                'city' : car.xpath(".//h4/span[2]/text()").get(),
                'region' : car.xpath(".//h4/span[3]/text()").get(), 
                'User-Agent' : response.request.headers['User-Agent']
            }
        
        next_page = response.xpath("//li[@class='next abs']/a/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse,headers= {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'  
        })