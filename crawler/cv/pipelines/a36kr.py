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
            # TODO replace it with a more flexible syntax
            sql = "INSERT INTO `article` (" + ','.join(
                    item.keys()) + ") VALUES (" \
                                   "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                   "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                   "%s)"
            self.cursor.execute(sql, item.values())
            if self.cursor.rowcount:
                return True
            return self.cursor.rowcount
        except:
            return False
        finally:
            pass
