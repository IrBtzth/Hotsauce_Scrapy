
import pandas as pd
from pathlib import Path, PurePath


first_name = ['puta','juean']
last_name = ['sakdjas', 'coco']
a ={'first_name':first_name,'last_name':last_name}
df = pd.DataFrame(a, columns=['first_name', 'last_name'])

df.to_csv('/home/betza/Python/Hotsauce_Scrapy/hotsauce_scrapy/pepito.csv', mode='a',header=False)