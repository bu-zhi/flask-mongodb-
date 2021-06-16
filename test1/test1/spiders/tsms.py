import scrapy
import json
import bson.binary
from ..items import Test1Item
import requests
count=1
class TsmsSpider(scrapy.Spider):
    name = 'tsms'

    def start_requests(self):
        leibie = ['originalbydesign', 'wallpapers', 'nature', 'people']
        for i in leibie:
            for j in range(1, 5):
                url = 'https://unsplash.com/napi/topics/' + i + '/photos?page=' + str(j) + '&per_page=10'
                yield scrapy.Request(url=url, callback=self.parse)
                #start_urls.append('https://unsplash.com/napi/topics/' + i + '/photos?page=' + str(j) + '&per_page=10')
    #allowed_domains = ['unsplash.com']
    #start_urls = []
    #start_urls = ['https://unsplash.com/napi/topics/{}/photos?page=1{}&per_page=10']
    #leibie = ['originalbydesign','wallpapers','nature','people','architecture','current-events','business-work','experimental','fashion',
              #'film','health','interiors','street-photography','technology','travel','textures-patterns','animals','food-drink','athletics',
              #'spirituality','arts-culture','history']



    def parse(self, response):
        res = json.loads(response.text)
        #print(res)
        global count
        for re in res:
            item = Test1Item()
            item['content'] =bson.binary.Binary(requests.get(url=re['urls']['full']).content)
            item['author'] =re['user']['name']
            item['title'] =re['alt_description']
            item['number'] =count
            count+=1
            #item['class'] =
            item['download'] = re['links']['download']+'?force=true'
            yield item