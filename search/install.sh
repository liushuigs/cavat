#########################################################################
# File Name: install.sh
# Author: xiongfusong
# mail: xiongfusong@gmail.com
# Created Time: 一  4/18 22:50:33 2016
#########################################################################
#!/bin/bash
#download
downfile=elasticsearch-2.3.1.zip
unzipdir=elasticsearch-2.3.1
destdir=es
if [ ! -f $downfile ];then
    wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/zip/elasticsearch/2.3.1/$download
fi
if [ -f $downfile ] && [ ! -d $destdir ];then
    unzip $downfile
    mv $unzipdir $destdir
    cd $destdir
    echo "open brower and view website: http://localhost:9200/"
    ./bin/elasticsearch
else
    if [ -d $destdir ];then
        cd $destdir
        echo "open brower and view website: http://localhost:9200/"
        ./bin/elasticsearch
    else
        echo "The folder "$destdir" is not existed!"
        exit 0
    fi
fi
