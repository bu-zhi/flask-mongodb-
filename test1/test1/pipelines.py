# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from twisted.internet import reactor, defer
import pymongo
class Test1Pipeline:
    '''
        def __init__(self):
        # 建立MongoDB数据库连接
        client = pymongo.MongoClient('127.0.0.1', 27017)
        # 连接所需数据库,ScrapyChina为数据库名
        db = client['dazuoye']
        # 连接所用集合，也就是我们通常所说的表，image为表名
        self.post = db['image']
    def process_item(self, item, spider):
        postItem = dict(item)  # 把item转化成字典形式
        self.post.insert(postItem)  # 向数据库插入一条记录
        return item  # 会在控制台输出原item数据，可以选择不写

    '''

    def __init__(self, mongo_uri, mongo_db, mongo_col):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_col = mongo_col

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', 'mongodb://127.0.0.1:27017/'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_col=crawler.settings.get('MONGO_COL'),
        )

    def open_spider(self, spider):
        """
        爬虫启动时，启动
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.mongodb = self.client[self.mongo_db]

    def close_spider(self, spider):
        """
        爬虫关闭时执行
        :param spider:
        :return:
        """
        self.client.close()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        out = defer.Deferred()
        reactor.callInThread(self._insert, item, out, spider)
        yield out
        defer.returnValue(item)

    def _insert(self, item, out, spider):
        """
        插入函数
        :param item:
        :param out:
        :return:
        """
        self.mongodb[self.mongo_col].insert(dict(item))
        reactor.callFromThread(out.callback, item)

