from pathlib import Path, PurePath
import scrapy
import csv

#nextbuttom = response.xpath('//div[@class="pagination"]/ul[@class="pagination-list"]/li[@class="pagination-item pagination-item--next"]/a[@class="pagination-link"]/@href').extract_first()
class SpiderHotSauce(scrapy.Spider):

    name = 'hotsauce'

    start_urls = [
        'https://www.hotsauce.com/'
    ]

    

    def parseWrite_AllViews(self, response, **kwargs):
        csvFile = kwargs['csvFile']
        
        name= response.xpath('//div[@class="card-body"]/h4/a/text()').getall()
        price = response.xpath('//div[@class="price-section price-section--withoutTax "]/span/text()').getall()
        link = response.xpath('//div[@class="card-body"]/h4/a/@href').getall()
        branch = response.xpath('//div[@class="brand-rating"]//p[@class="card-text" and @data-test-info-type="brandName"]/text()').getall()
        priceWithoutax = list(filter(lambda x: (price.index(x)%2!=0),price))
        priceNormal = list(filter(lambda x: (price.index(x)%2==0),price))


        try:
            row= [[name[i], priceNormal[i], priceWithoutax[i],branch[i],link[i]] for i in range(0,len(name)-1) ]
            writer = csv.writer(csvFile)
            writer.writerows(row)
        except:
            print("SE ESCONETO")
            

        if response.xpath('//div[@class="price-section price-section--withoutTax "]/span[@data-product-rrp-without-tax]/text()').getall() == []:
            price = response.xpath('//div[@class="price-section price-section--withoutTax "]/span[@data-product-rrp-without-tax]/text()')
            row= [[name[i], price[i],branch[i],link[i]] for i in range(0,len(name)-1) ]
        
       
        
        next_page_button_link = response.xpath('//div[@class="pagination"]/ul[@class="pagination-list"]/li[@class="pagination-item pagination-item--next"]/a[@class="pagination-link"]/@href').extract_first()

        if next_page_button_link is not None:
        
            yield response.follow(next_page_button_link, callback = self.parseWrite_AllViews, cb_kwargs={'csvFile': csvFile})
                 
        


    def parseAllViews(self, response, **kwargs):
        ruta = kwargs[ 'rutaAllView']
        allViews_links =  response.xpath('//div[@class="sidebarBlock"]//li[@class="navList-item"]/a/@href').getall()
        allViews_names =  response.xpath('//div[@class="sidebarBlock"]//li[@class="navList-item"]/a/text()').getall()

        
        count = 0
        
        if allViews_links == []:
            csvFile= open(f'{ruta}/{"sjnsdkjcsd"}.csv', 'w')
        else:
            for link in allViews_links:
                allViews_names[count] =allViews_names[count].replace("/", "-")
                csvFile =  open(f'{ruta}/{allViews_names[count]}.csv', 'w') 
                header = ['Name', 'Price', 'Price witout Tax', 'Brand', 'Link']
                writer = csv.writer(csvFile)
                writer.writerow(header)
                yield response.follow(link, callback = self.parseWrite_AllViews, cb_kwargs={'csvFile': csvFile})
                count+=1


    def parse(self, response):
        links_mainMenu = response.xpath('//ul[@class="MainMenu"]/li/a/@href').getall()
        mainMenu_nameList = response.xpath('//ul[@class="MainMenu"]/li/a[@href]/text()').getall()
        count = 0


        Path('Main Menu').mkdir(exist_ok=True)
        ruta = PurePath.joinpath(Path.cwd(), 'Main Menu')

        for link in links_mainMenu: 
            if count < len(mainMenu_nameList):
                PurePath.joinpath(ruta , mainMenu_nameList[count]).mkdir(parents = True)
                rutaCarpetas = PurePath.joinpath(ruta, mainMenu_nameList[count])
            
            yield response.follow(link, callback = self.parseAllViews, cb_kwargs={'rutaAllView': rutaCarpetas})
            count+=1

    

        

       

    