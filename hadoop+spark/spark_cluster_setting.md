Spark cluster setting
======================

>Hadoop setting:http://www.powerxing.com/install-hadoop-cluster/  
\#2: http://my.oschina.net/leejun2005/blog/394928

0.account
-----------------
Create a account names "hadoop" on all cluster-terminal.  
then login hadoop to do below things.

1.depend
-----------------
* java
  * $JAVA_HOME << java.dir
  * $PATH << $JAVA_HOME/bin
* scala
  * $SCALA_HOME << scala.dir
  * $PATH << $SCALA_HOME/bin
* Hadoop
  * install and setup hadoop cluster
    * hosts
    * ssh
    * setting files
      * core-site.xml
      * hdfs-site.xml
      * mapred-site.xml
      * yarn-site.xml
      * slaves
    * hdfs namenode -format
    * Run in Full-Distributed Mode at least once.
* python

2.Spark setting
-----------------
    conf ($SPARK_HOME/conf)
* spark-env.sh
  * export SCALA_HOME=/usr/lib/scala-2.10.3
  * export JAVA_HOME=/usr/java/jdk1.6.0_31
  * export SPARK_MASTER_IP=10.32.21.165
  * export SPARK_WORKER_INSTANCES=3 //set '1' if you have one worker only
  * export SPARK_MASTER_PORT=8070
  * export SPARK_MASTER_WEBUI_PORT=5772
  * export SPARK_WORKER_PORT=8092
  * export SPARK_WORKER_MEMORY=5000m
* slaves

　

    $PATH (~/.bashrc)
* $HADOOP_HOME = hadoop.dir
* $SPARK_HOME << spark.dir
* $HADOOP_CONF_DIR = hadoop.dir/etc/hadoop
* $YARN_CONF_DIR = hadoop.dir/etc/hadoop
* $SPARK_LIBARY_PATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$HADOOP_HOME/lib/native
* $PATH << $SPARK_HOME/bin : $SPARK_HOME/sbin
* $PYTHONPATH << $SPARK_HOME/python/ : $SPARK_HOME/python/lib/py4j-xxx-src.zip
* $SPARK_MASTER = localhost
* $SPARK_LOCAL_IP = localhost

3.Test
-----------------
    $SPARK_HOME/sbin
* start-all.sh
  * start-master.sh
  * start-slaves.sh

//question : need hadoop & yarn running?
mode:yarn-cluster


* hdfs: http://master:50070/
* yarn: http://master:8088/
* spark-webui: http://master:5772/
