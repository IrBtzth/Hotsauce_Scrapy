from pathlib import Path, PurePath
import scrapy
import csv
class SpiderHotSauce(scrapy.Spider):

    name = 'hotsauce'

    start_urls = [
        'https://www.hotsauce.com/'
    ]

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'ROBOTSTXT_OBEY': True
    }

    def parseWrite_AllViews(self, response, **kwargs):
        pass

    def parseAllViews(self, response, **kwargs):
        ruta = kwargs[ 'rutaAllView']
        allViews_links =  response.xpath('//div[@class="sidebarBlock"]//li[@class="navList-item"]/a/@href').getall()
        allViews_names =  response.xpath('//div[@class="sidebarBlock"]//li[@class="navList-item"]/a/text()').getall()
        count = 0

        if allViews_links == []:
            csvFile=open(f'{ruta}/{"sjnsdkjcsd"}.csv', 'w')
        else:
            for link in allViews_links:
                csvFile=open(f'{ruta}/{allViews_names[count]}.csv', 'w')
                yield response.follow(link, callback = self.parseWrite_AllViews, cb_kwargs={'csvFile': csvFile})
                count+=1


    def parse(self, response):
        links_mainMenu = response.xpath('//ul[@class="MainMenu"]/li/a/@href').getall()
        mainMenu_nameList = response.xpath('//ul[@class="MainMenu"]/li/a[@href]/text()').getall()
        count = 0


        Path('Main Menu').mkdir(exist_ok=True)
        ruta = PurePath.joinpath(Path.cwd(), 'Main Menu')

        for link in links_mainMenu: 

            PurePath.joinpath(ruta , mainMenu_nameList[count]).mkdir(parents = True)
            rutaCarpetas = PurePath.joinpath(ruta, mainMenu_nameList[count])
            
            yield response.follow(link, callback = self.parseAllViews, cb_kwargs={'rutaAllView': rutaCarpetas})
            count+=1

    

        

       

    