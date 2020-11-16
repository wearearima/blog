---
layout: post
title:  "Squeezing the most out of your Data Lake (Part I, Hudi)"
date:   2020-10-20 9:00:00
author: juan
lang: en
categories: big data, data lake, apache hudi
tags: big data, data lake, apache hudi, docker, data warehouse, parquet, avro, orc, delta lake, iceberg
header-image: 2020-10-20-exprimiendo-tu-data-lake-parte-I-hudi/post-header.jpg
---

Since the first databases emerged in the 70s, a way to fully utilize this information has always been sought by trying to extract indicators that help in decision-making. This is how the tools known as Data Warehouse were born, which were aimed at storing and getting the most out of this information. Many of these tools are made up of [columnar databases](https://en.wikipedia.org/wiki/Column-oriented_DBMS){:target="_blank"} that allow analytical queries to be made in a much more efficient way than the row-oriented databases commonly used in operational databases.

Over time, the needs and volumes of information with which companies work have grown exponentially. In the last 15 years, we have seen companies such as Google, Microsoft, Amazon, Facebook, Uber, Netflix or Twitter handling huge volumes of data and traffic. Traditional Data Warehouses were not capable of handling these volumes in a reasonable period of time and in many cases they needed several days to be able to execute the queries.

This situation forced these companies to lead a change by launching papers and new tools that would allow them to analyze vast amounts of information more efficiently. The starting gun was fired by Google publishing the papers [Google File System](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf){:target="_blank"} (2003) and [Map Reduce](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf){:target="_blank"} (2004). A few years later (2006), Yahoo published the open source project Hadoop, which was based on the  previously mentioned Google papers. Hadoop changed the data analytics industry as we had known it until then and started the movement called “Big Data”.

The Hadoop stack basically allowed us to store ([HDFS](https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html){:target="_blank"}) and process ([Map Reduce](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf){:target="_blank"}) the information in a distributed way. This increased the processing capacity as it could be scaled horizontally by adding more machines to the system.

Having a distributed file system like HDFS made it possible for many organizations to start storing data that they previously had to discard. This trend became even more prominent with the birth of products such as Amazon S3, which allowed the storage of any type of information cheaply in the cloud. This new reality led James Dixon (founder of Pentaho) to conceive the idea of Data Lake in 2010. Data Lakes were presented as data stores in which you could find raw information as it had been received and without any type of processing. In this way, you could start storing information with the expectation that one day it might be of use.

This approach, which was attractive to many organizations, also involved an obvious danger. Storing the information without any criteria could cause our Data Lake to become a mess, where finding and organizing the information could be quite complicated and therefore, you would never get any benefit from it.

<p align="center">
    <img src="/assets/images/2020-10-20-exprimiendo-tu-data-lake-parte-I-hudi/messy-room.png">
</p>

Another disadvantage of Hadoop is that it was necessary to have programming knowledge to be able to perform analytical operations on the data stored in the distributed file system. This made it impossible for some managers or analysts to carry out the tasks on their own without the help of a programmer. For this reason, a multitude of projects began to emerge, such as Apache Hive, which added SQL layers on top of this type of distributed file system. These SQL layers were accompanied by new storage formats that were more efficient and resembled those used in traditional databases since some were row oriented (Avro) and others column oriented (Parquet, ORC).

<p align="center">
    <img src="/assets/images/2020-10-20-exprimiendo-tu-data-lake-parte-I-hudi/parquet-orc-avro.png">
</p>

Having Data Lakes capable of storing information in an efficient and accessible way through SQL, might lead us to think that these could completely replace the more traditional Data Warehouses. Although the line that separates them is getting thinner, there are certain characteristics that Data Lakes do not have and that over time have been seen to be necessary:

* Being able to perform updates efficiently. Formats such as Parquet, by default, are not prepared to be updated and require manual processes which are lengthy and not very efficient.
* ACID transactions with which to ensure the atomicity, consistency, isolation and durability of operations.
* <i>Lineage</i> or tracking, to know what modifications have been made to data over time.
* Evolution of the scheme or structure.

In recent years, some solutions have appeared that seek to meet these needs, such as:

* Apache hudi
* Delta Lake
* Apache Iceberg

In this article we are going to talk about Apache Hudi, but we will probably talk about Delta Lake and Iceberg in future posts.

<p align="center">
    <img src="/assets/images/2020-10-20-exprimiendo-tu-data-lake-parte-I-hudi/apache-hudi.png">
</p>

<i>Apache Hudi</i> is an open source project aimed at creating efficient data lakes and storing large data sets on HDFS file systems or cloud file systems such as S3. The very name of the project is a statement of intent for the features it provides: Hudi (<b>H</b>adoop <b>U</b>psert <b>D</b>elete and <b>I</b>ncremental).

<i>Hudi</i> therefore, allows you to apply updates efficiently on Parquet files stored in distributed file systems, taking care of aspects such as compaction and granting ACID capabilities. In addition, it allows you to make incremental queries so that you can obtain all the modifications that have been carried out from a given moment. This opens the door to being able to perform streaming analytics without having to introduce complex infrastructures such as those proposed in the [lambda architecture](http://lambda-architecture.net){:target="_blank"}.

Hudi has two operating modes, each of which is more suitable depending on the frequency with which data is read or written:

* Copy on Write (CoW) 
* Merge on Read (MoR)

The differences between these two modes can be found in the [official documentation](https://hudi.apache.org/docs/concepts.html#table-types--queries){:target="_blank"}.

In the [following](https://github.com/wearearima/hudi-exercise){:target="_blank"} Github repository we have implemented an example in which you can see how Hudi is used, as well as some of its capabilities. In this example, Wikipedia entries are processed with Apache Spark, identifying those that correspond to celebrities. The result is stored in HDFS with Parquet format using the Hudi tool. Once this operation has been completed, new processes are carried out that trigger updates to the data. In these, we will see how HUDI automatically manages the creation and compaction of the new Parquet files, saving <i>commits</i> in each of the operations with which the <i>lineage</i> of the data can be checked .

We will use the `hudi-spark` module that offers a <i>Datasource API</i> with which a Spark Dataframe can be written (and read) in a Hudi table, as follows:

```python
df.write.format("hudi") \
.options(**hudi_options).mode("overwrite").save(basePath)
```
However, it has another module called <i>DeltaStreamer</i> which you can use to work with streaming sources, such as Apache Kafka. More information [here](https://hudi.apache.org/docs/writing_data.html){:target="_blank"}.


## Conclusions

In this article we have seen the motivation that led to the birth of the data stores known as Data Lake. We have also mentioned some of the shortcomings and drawbacks they have and how tools have appeared that seek to alleviate them. Does this mean that Data Lakes are going to evolve enough to become our only source of data? Perhaps it is too early to make such a statement, but what does seem certain is that we are in a time of change in the big data ecosystem and that the next few years will be exciting in this sector.