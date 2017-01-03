#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170103 09:32:50
##################################
#6-45.应该用datetime模块来处理本地时间，而不是用time模块
##################################

#协调世界时(Coordinated Universal Time, UTC)是一种标准的时间表述方式，它与时区无关。有些计算机，用某一时刻与UNIX时间原点之间相差的秒数，来表示那个时刻所对应的时间，对于这些计算机来说，UTC是一种非常好的计时方式。

#1.time模块

#在内置的time模块中，有个名叫localtime的函数，它可以把UNIX时间戳(UNIX timestamp,也就是某个UTC时刻距离UNIX计时原点的秒数)转换为与宿主计算机的时区相符的当地时间(笔者所用电脑的时区是太平洋夏时令时，Pacific Daylight Time，PDT)。

from time import localtime,strftime

now = 1407694710
local_tuple = localtime(now)
time_format = '%Y-%m-%d %H:%M:%S'
time_str = strftime(time_format, local_tuple)
print(time_str)

#程序通常还需要做反向处理，也就是说，要把用户输入的本地时间，转换为UTC时间。我们可以用strptime函数来解析包含时间信息的字符串，然后调用mktime函数，将本地时间转换为UNIX时间戳。

from time import mktime, strptime

time_tuple = strptime(time_str, time_format)
utc_now = mktime(time_tuple)
print(utc_now)

#许多操作系统都提供了时区配置文件，如果时区信息发生变化，它们就会自动更新。我们可以在Python程序中借助time模块来使用这些时区信息。例如，下面这段代码会以太平洋夏时令(PDT)为标准，把航班从旧金山的起飞时间解析出来。

parse_format = '%Y-%m-%d %H:%M:%S %Z'
depart_sfo = '2015-05-01 15:45:16 CST'
time_tuple = strptime(depart_sfo, parse_format)
time_str = strftime(time_format, time_tuple)
print(time_str)

#我们看到, 因为我们在中国，striptime函数不能解析太平洋夏时令时，只能解析中国本地时间。如果要使用time模块，那就只应该用它在UTC与宿主计算机的当地时区之间进行转换。对于其他类型的转换来说，还是使用datetime模块比较好。

#在内置的datetime模块中，有个名叫datetime的类，它也能像刚才所讲的time模块那样，用来在Python程序中描述时间。与time模块类似，datetime可以把UTC格式的当前时间，转换为本地时间。

from datetime import datetime, timezone

now = datetime(2014, 8, 10, 18, 18, 30)
now_utc = now.replace(tzinfo=timezone.utc)
now_local = now_utc.astimezone()
print(now_local)

#datetime模块还可以把本地时间轻松地转换成UTC格式的UNIX时间戳。

time_str = '2014-08-10 11:18:30'
now = datetime.strptime(time_str, time_format)
time_tuple = now.timetuple()
utc_now = mktime(time_tuple)
print(utc_now)

#datetime中并没有提供UTC之外的时区定义。

#所幸Python开发者社区提供了pytz模块，填补了这一空缺。

#为了有效地使用pytz模块，我们总是应该先把当地时间转换为UTC，然后针对UTC值进行datetime操作(例如，执行与时区偏移有关的操作),最后再把UTC转回当地时间。


#下面这段代码把航班到达纽约的时间，转换为UTC格式的datetime对象。
import pytz
arrival_nyc = '2014-05-01 23:33:24'
nyc_dt_naive = datetime.strptime(arrival_nyc, time_format)
eastern = pytz.timezone('US/Eastern')
nyc_dt = eastern.localize(nyc_dt_naive)
utc_dt = pytz.utc.normalize(nyc_dt.astimezone(pytz.utc))
print(utc_dt)

#得到UTC格式的datetime之后，再把它转换成旧金山当地时间。

pacific = pytz.timezone('US/Pacific')
sf_dt = pacific.normalize(utc_dt.astimezone(pacific))
print(sf_dt)

#我们还可以把这个时间，轻松地转换成尼泊尔(Nepal)当地时间。
nepal = pytz.timezone('Asia/Katmandu')
nepal_dt = nepal.normalize(utc_dt.astimezone(nepal))
print(nepal_dt)

#转化为中国上海时间
shanghai = pytz.timezone('Asia/Shanghai')
shanghai_dt = shanghai.normalize(nepal_dt.astimezone(shanghai))
print(shanghai_dt)

#不要用time模块在不同时区之间进行转换，请使用datetime模块与开发者社区提供的pytz模块搭配起来使用，开发者总是应该先把时间表示成UTC格式，然后对其执行各种转换操作，然后再把它转回本地时间。


