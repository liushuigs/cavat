from cv.models.article import Article


class ArticlePipeline(object):
    def process_item(self, item, spider):
        # print '-'.center(100, '-')
        # print 'storage start'.center(100, '-')
        # print '-'.center(100, '-')
        success = self.insert(item)
        if success:
            print 'store successfully!'
        else:
            print 'store failure!'
        # article = Article()
        # article.get_one(1)
        # print '-'.center(100, '-')
        # print 'storage end'.center(100, '-')
        # print '-'.center(100, '-')
        # pass

    def insert(self, item):
        import pymysql as MySQLdb
        db_host = '127.0.0.1'
        db_user = 'root'
        db_psw = '123456'
        db_name = 'cavat'
        conn = None
        conn = MySQLdb.connect(db_host, db_user, db_psw, db_name, charset='utf8',
                               cursorclass=MySQLdb.cursors.DictCursor)
        try:
            # TODO replace it with a more flexible syntax
            sql = "INSERT INTO `article` (" + ','.join(
                    item.keys()) + ") VALUES (" \
                                   "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                   "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                   "%s)"
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
