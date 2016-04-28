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
        success = self.insert(item)
        if success:
            print 'store successfully!'
        else:
            print 'store failure!'

    def insert(self, item):
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
            if self.cursor.rowcount:
                return True
            return self.cursor.rowcount
        except:
            return False
        finally:
            pass
