from pathlib import Path, PurePath
import scrapy
import csv

#nextbuttom = response.xpath('//div[@class="pagination"]/ul[@class="pagination-list"]/li[@class="pagination-item pagination-item--next"]/a[@class="pagination-link"]/@href').get()
class SpiderHotSauce(scrapy.Spider):

    name = 'hotsauce'

    start_urls = [
        'https://www.hotsauce.com/'
    ]

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'ROBOTSTXT_OBEY': False
    }

    def parseWrite_AllViews(self, response, **kwargs):
        page = kwargs['page']
        csvFile = kwargs['csvFile']

        name= response.xpath('//div[@class="card-body"]/h4/a/text()').getall()
        price = response.xpath('//div[@class="price-section price-section--withoutTax "]/span/text()').getall()
        link = response.xpath('//div[@class="card-body"]/h4/a/@href').getall()
        branch = response.xpath('//div[@class="brand-rating"]//p[@class="card-text" and @data-test-info-type="brandName"]/text()').getall()
        priceWithoutax = list(filter(lambda x: (price.index(x)%2!=0),price))
        priceNormal = list(filter(lambda x: (price.index(x)%2==0),price))

        row= [[name[i], priceNormal[i], priceWithoutax[i],branch[i],link[i]] for i in range(0,len(name)-1) ]
        
        writer = csv.writer(csvFile)
        writer.writerows(row)
        page+=1
        pagestr = "?sort=alphaasc&page=" + str(page)
        next_page_button_link= response.urljoin(pagestr)

        if (next_page_button_link.find("?sort=alphaasc&page=")!= -1) and page >= 3:
            lastpage = "page=" + str(page-1)
            thispage = "page=" + str(page)
            pagestr =  next_page_button_link.replace(lastpage, thispage)
            next_page_button_link= response.urljoin(pagestr)
     

        if row != []:
            yield response.follow(next_page_button_link, callback = self.parseWrite_AllViews, cb_kwargs={'csvFile': csvFile, 'page':page})
                 
        


    def parseAllViews(self, response, **kwargs):
        ruta = kwargs[ 'rutaAllView']
        allViews_links =  response.xpath('//div[@class="sidebarBlock"]//li[@class="navList-item"]/a/@href').getall()
        allViews_names =  response.xpath('//div[@class="sidebarBlock"]//li[@class="navList-item"]/a/text()').getall()

        
        count = 0
        page = 1
        if allViews_links == []:
            csvFile= open(f'{ruta}/{"sjnsdkjcsd"}.csv', 'w')
        else:
            for link in allViews_links:
                csvFile =  open(f'{ruta}/{allViews_names[count]}.csv', 'w') 
                header = ['Name', 'Price', 'Price witout Tax', 'Brand', 'Link']
                writer = csv.writer(csvFile)
                writer.writerow(header)
                yield response.follow(link, callback = self.parseWrite_AllViews, cb_kwargs={'csvFile': csvFile, 'page':page, 'links': link})
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

    

        

       

    