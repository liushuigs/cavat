from cv.models.article import Article
from cv.util.config import CvConfig
import pymysql as MySQLdb


class ArticlePipeline(object):
    def __init__(self):
        parser = CvConfig()
        self.conn = None
        self.conn = MySQLdb.connect(
                host=parser.get('db', 'host'),
                user=parser.get('db', 'user'),
                passwd=parser.get('db', 'passwd'),
                db=parser.get('db', 'db'),
                charset='utf8',
                cursorclass=MySQLdb.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if item:
            self.insert(item, spider.logger)

    def insert(self, item, logger):
        try:
            # only update the fields that are not None
            update_item = {}
            for key in item:
                if key is not 'created_ts' and item[key] is not None:
                    update_item[key] = item[key]

            sql = "INSERT INTO `article` (" + ','.join(
                    item.keys()) + ") VALUES (" + ",".join(["%s"] * 21) + \
                  ") ON DUPLICATE KEY UPDATE " + ",".join([key + "=%s" for key in update_item.keys()])
            self.cursor.execute(sql, item.values() + update_item.values())
            self.conn.commit()
            row_count = self.cursor.rowcount
            action = 'update' if row_count == 2 else 'insert'
            logger.info('[%s] [%s]', action, item["url"])
        except Exception, e:
            logger.warning("store error [%s], e: [%s]" % (item["url"], e))
