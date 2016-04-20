#########################################################################
# File Name: jdbc.sh
# Author: xiongfusong
# mail: xiongfusong@gmail.com
# Created Time: 三  4/20 00:47:19 2016
#########################################################################
#!/bin/bash
zipfile=elasticsearch-jdbc-2.3.1.0-dist.zip
river=jdbc
if [ ! -f $zipfile ];then
    wget http://xbib.org/repository/org/xbib/elasticsearch/importer/elasticsearch-jdbc/2.3.1.0/$zipfile
fi
if [ ! -d $river ];then
    unzip elasticsearch-jdbc-2.3.1.0-dist.zip
    mv elasticsearch-jdbc-2.3.1.0 $river
fi
bin=$river/bin
lib=$river/lib
echo '{
    "type" : "jdbc",
    "jdbc" : {
        "url" : "jdbc:mysql://localhost:3306/cavat",
        "user" : "common",
        "password" : "common",
        "sql" : "select *, id as _id from article where id = 3",
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
