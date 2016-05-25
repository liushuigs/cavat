#########################################################################
# File Name: mysql2es.sh
# Author: xiongfusong
# mail: xiongfusong@gmail.com
# Created Time: 四  4/21 23:40:38 2016
#########################################################################
#!/bin/bash
river=jdbc

bin=$river/bin
lib=$river/lib
echo '{
    "type" : "jdbc",
    "jdbc" : {
        "url" : "jdbc:mysql://localhost:3306/cavat",
        "user" : "root",
        "password" : "123456",
        "sql" : "select *, id as _id from article limit 100",
        "index" : "cavat",
        "type" : "article"
    }
}' | java \
       -cp "${lib}/*" \
       -Dlog4j.configurationFile=${bin}/log4j2.xml \
       org.xbib.tools.Runner \
       org.xbib.tools.JDBCImporter

# GET result
# method 1: curl -XGET http://localhost:9200/cavat/article/3
# method 2: use chrome plugin -- sense, Query command: GET /cavat/article/3

# NOTE: Make sure elasticsearch is running!

