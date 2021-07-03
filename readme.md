# ipcheck



### 一、介绍
本项目主要分为两部分：

1. 管理节点部分：  
   使用tgbot对节点进行增删，以及当节点发生变动时进行推送。
2. 监测节点部分：  
   利用国内外机器对ip或域名进行监测。  


### 二、管理节点部分  
这部分主要由 tgbot + 数据库 + 定时检测三部分组成。  

1.1 下载 sql模板，建立MySQL数据库  
1.2 git clone https://github.com/cloudfly23/ipcheck  
1.3 pip3 install -r requirements.txt  
1.4 在 bot.py 和 time.py 填好变量  
1.5 python3 bot.py  
1.6 定时任务中加入 python3 time.py

### 三、检测节点搭建
检测节点提供多种搭建方式，推荐 serverless 方法，稳定且多节点。   

提供4家 serverless 的模板，在 serverless 文件夹下可以找到。  

自建节点提供 php 版本和 python 版本，在child 文件夹下可以找到。  
php 需要开启exec函数，此操作存在风险，请视情况使用。   

   
## To do：
编写好文档