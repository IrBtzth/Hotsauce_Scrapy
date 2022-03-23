
from os import rmdir
from pathlib import Path, PurePath

from pyrsistent import field
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
        
        countParseWrite = kwargs['countParseWrite']
        
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

        nameFile =filePath + '.csv'
        
        try:
            pandafile = pd.DataFrame(file,columns=['name', 'priceNormal', 'priceWithoutax', 'branch', 'link']) 

            if countParseWrite == 0:
                pandafile.to_csv(nameFile,mode='a',header=True, index=False)
                countParseWrite = 1
            else:
                pandafile.to_csv(nameFile,mode='a',header=False,index=False)
        except ValueError as ve:
            print('\n\n')
            print('The error is' + str(ve))
        
        next_page_button_link = response.xpath('//div[@class="pagination"]/ul[@class="pagination-list"]/li[@class="pagination-item pagination-item--next"]/a[@class="pagination-link"]/@href').extract_first()

        if next_page_button_link is not None:
        
            yield response.follow(next_page_button_link, callback = self.parseWrite_AllViews, cb_kwargs={'filePath': filePath, 'countParseWrite':countParseWrite})
            

    def parseAllViews(self, response, **kwargs):
        folderPath = kwargs[ 'AllViewPath']
        folderName = kwargs['folderName']
        folderLink = kwargs['folderLink']
        allViews_links =  response.xpath('//div[@class="sidebarBlock"]//li[@class="navList-item"]/a/@href').getall()
        allViews_names =  response.xpath('//div[@class="sidebarBlock"]//li[@class="navList-item"]/a/text()').getall()
        

        error = response.xpath('//ul/li[2]/a/span[@itemprop="name"]/text()').get()
        countParseWrite = 0
        count = 0
        
        if (error == 'VIEW ALL CATEGORIES')and  (allViews_links==[] or len(allViews_links)==1):
            rmdir(folderPath)
        elif allViews_links == []:
            folderLink = str(folderLink)
            folderPath = str(folderPath) + '/'+ str(folderName)
            yield response.follow(folderLink, dont_filter = True, callback = self.parseWrite_AllViews, cb_kwargs={'filePath':  folderPath, 'countParseWrite':countParseWrite})
        else:
            for link in allViews_links:
                allViews_names[count] = allViews_names[count].replace("/", "-")
                filePath = str(folderPath) +'/' + allViews_names[count]
               
                yield response.follow(link, callback = self.parseWrite_AllViews, cb_kwargs={'filePath':  filePath, 'countParseWrite':countParseWrite})
                count+=1
            


    def parse(self, response):
        links_mainMenu = response.xpath('//ul[@class="MainMenu"]/li/a/@href').getall()
        mainMenu_nameList = response.xpath('//ul[@class="MainMenu"]/li/a[@href]//text()').getall()
        
        count = 0

        Path('Main Menu').mkdir(exist_ok=True)
        path = PurePath.joinpath(Path.cwd(), 'Main Menu')

        for link in links_mainMenu: 
            if count < len(mainMenu_nameList):
                PurePath.joinpath(path , mainMenu_nameList[count]).mkdir(parents = True)
                AllViewPath = PurePath.joinpath(path, mainMenu_nameList[count])            
            yield response.follow(link, callback = self.parseAllViews, cb_kwargs={'AllViewPath': AllViewPath, 'folderName': mainMenu_nameList[count], 'folderLink': link})
            count+=1