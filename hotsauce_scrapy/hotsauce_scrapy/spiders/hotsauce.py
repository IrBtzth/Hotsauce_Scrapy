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
        csvFile = kwargs['csvFile']
        name= response.xpath('//div[@class="card-body"]/h4/a/text()').getall()
        price = response.xpath('//div[@class="price-section price-section--withoutTax "]/span/text()').getall()
        link = response.xpath('//div[@class="card-body"]/h4/a/@href').getall()
        branch = response.xpath('//div[@class="brand-rating"]//p[@class="card-text" and @data-test-info-type="brandName"]/text()').getall()
        priceWithoutax = list(filter(lambda x: (price.index(x)%2==0),price))
        priceNormal = list(filter(lambda x: (price.index(x)%2!=0),price))

        header = ['Name', 'Price', 'Price witout Tax', 'Brand', 'Link']
        
        row= [[name[i], priceNormal[i], priceWithoutax[i],branch[i],link[i]] for i in range(0,len(name)-1) ]
        
        writer = csv.writer(csvFile)
        writer.writerow(header)
        writer.writerows(row)
    
        


    def parseAllViews(self, response, **kwargs):
        ruta = kwargs[ 'rutaAllView']
        allViews_links =  response.xpath('//div[@class="sidebarBlock"]//li[@class="navList-item"]/a/@href').getall()
        allViews_names =  response.xpath('//div[@class="sidebarBlock"]//li[@class="navList-item"]/a/text()').getall()
        count = 0

        if allViews_links == []:
            csvFile= open(f'{ruta}/{"sjnsdkjcsd"}.csv', 'w')
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

    

        

       

    