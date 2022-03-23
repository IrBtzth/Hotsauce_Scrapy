from itertools import count
from pathlib import Path, PurePath
import scrapy
import csv
import pandas as pd


#nextbuttom = response.xpath('//div[@class="pagination"]/ul[@class="pagination-list"]/li[@class="pagination-item pagination-item--next"]/a[@class="pagination-link"]/@href').extract_first()
class SpiderHotSauce(scrapy.Spider):

    name = 'hotsauce'

    start_urls = [
        'https://www.hotsauce.com/'
    ]

    


    def parseWrite_AllViews(self, response, **kwargs):
      
        filePath = kwargs['filePath']
        
        count = kwargs['numero']
        
        name= response.xpath('//div[@class="card-body"]/h4/a/text()').getall()
        priceNormal= response.xpath('//div[@class="price-section price-section--withoutTax "]/span[@data-product-rrp-without-tax]/text()').getall()
        priceWithoutax = response.xpath('//div[@class="price-section price-section--withoutTax "]/span[@data-product-price-without-tax]/text()').getall()
        link = response.xpath('//div[@class="card-body"]/h4/a/@href').getall()
        branch = response.xpath('//div[@class="brand-rating"]//p[@class="card-text" and @data-test-info-type="brandName"]/text()').getall()
        file = {'name':name, 'priceNormal': priceNormal, 'priceWithoutax': priceWithoutax, 'branch':branch, 'link':link}
        for i in range(0, len(name)-1):
            itera = response.xpath(f'//li[{str(i+1)}]//div[@class="brand-rating"]//p[@class="card-text" and @data-test-info-type="brandName"]/text()').getall()
            iteraPrice = response.xpath(f'//li[{str(i+1)}]//div[@class="price-section price-section--withoutTax "]/span[@data-product-rrp-without-tax]/text()').getall()
            if itera == []:
                branch.insert(i, "NONE")
            if priceNormal ==[]:
                file = {'name':name,'priceNormal': 'NONE', 'priceWithoutax': priceWithoutax, 'branch':branch, 'link':link}
            elif iteraPrice == []:
                priceNormal.insert(i, "NONE")

        
        numerito = int(len(filePath)-1)
        nameFile =filePath[:numerito] + '.csv'
         
        try:
            pandafile = pd.DataFrame(file,columns=['name', 'priceNormal', 'priceWithoutax', 'branch', 'link']) 

            if count == 0:
                pandafile.to_csv(nameFile,mode='a',header=True, index=False)
                count = 1
            else:
                pandafile.to_csv(nameFile,mode='a',header=False,index=False)
        except ValueError as ve:
            print('\n\n')
            s =[len(file['name']),len(file['priceNormal']),len(file['priceWithoutax']),len(file['branch']),len(file['link'])]
            errores = open('/home/betza/Python/Hotsauce_Scrapy/hotsauce_scrapy/veamos.txt', 'a')
            errores.write(str(s) +" " + str(ve) + " "+ str(response) +'\n')
           
            print(ve)
     

    
       
        
        next_page_button_link = response.xpath('//div[@class="pagination"]/ul[@class="pagination-list"]/li[@class="pagination-item pagination-item--next"]/a[@class="pagination-link"]/@href').extract_first()

        if next_page_button_link is not None:
        
            yield response.follow(next_page_button_link, callback = self.parseWrite_AllViews, cb_kwargs={'filePath': filePath, 'numero':count})
            
                 
        


    def parseAllViews(self, response, **kwargs):
        ruta = kwargs[ 'rutaAllView']
        folderName = kwargs['folderName']
        allViews_links =  response.xpath('//div[@class="sidebarBlock"]//li[@class="navList-item"]/a/@href').getall()
        allViews_names =  response.xpath('//div[@class="sidebarBlock"]//li[@class="navList-item"]/a/text()').getall()
        numero = 0
         
        count = 0
      
        if allViews_links == [] :
            
            filePath = str(ruta)+ str(folderName) + '/'
            try:
                yield response.follow(response, callback = self.parseWrite_AllViews, cb_kwargs={'filePath':  filePath, 'numero':numero})
            except TypeError as te:
                print('\n\n')
                print(te)
                print(filePath)
                print(response)
        else:
            for link in allViews_links:
                allViews_names[count] = allViews_names[count].replace("/", "-")
                filePath = str(ruta) + allViews_links[count].replace("https://www.hotsauce.com/", '/')
         
         
                yield response.follow(link, callback = self.parseWrite_AllViews, cb_kwargs={'filePath':  filePath, 'numero':numero})
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
                folderName = mainMenu_nameList[count]

            
            yield response.follow(link, callback = self.parseAllViews, cb_kwargs={'rutaAllView': rutaCarpetas, 'folderName':folderName})
            count+=1

    

        

       

    