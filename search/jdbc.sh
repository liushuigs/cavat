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
    if [ ! -d ${zipfile%-*} ];then
        unzip elasticsearch-jdbc-2.3.1.0-dist.zip
    fi
    mv ${zipfile%-*} $river
fi
