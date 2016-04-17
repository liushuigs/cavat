# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class CvPipeline(object):
    def process_item(self, item, spider):
        return item
    def insert(self, item):
        import pymysql as MySQLdb
        db_host = '127.0.0.1'
        db_user = 'root'
        db_psw = '123456'
        db_name = 'cavat'
        conn = None
        conn = MySQLdb.connect(db_host, db_user, db_psw, db_name, charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
        try:
            sql = "INSERT INTO `article` ("+','.join(item.keys())+") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            with conn.cursor() as cursor:
                cursor.execute(sql, item.values())
            conn.commit()
            if cursor.rowcount:
                return True
            return cursor.rowcount
        except:
            return False
        finally:
            if conn:
                conn.close()

class ArticlePipeline(CvPipeline):
    def process_item(self, item, spider):
        print '-'.center(100, '-')
        print 'storage start'.center(100, '-')
        print '-'.center(100, '-')
        bool = self.insert(item)
        if bool:
            print 'Successfully!'
        else:
            print 'Failure!'
        print '-'.center(100, '-')
        print 'storage end'.center(100, '-')
        print '-'.center(100, '-')
        pass
