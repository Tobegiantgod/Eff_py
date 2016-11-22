#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161122 15:22:53
##################################
#4-30 考虑用@property来代替属性重构
##################################

#@property还有一种高级的用法，就是可以把简单的数值属性迁移为实时计算(on-the-fly calculation)的属性

#利用纯Python对象实现带有配额的露桶

from datetime import datetime, timedelta


class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return 'Bucket(quota=%d)' % self.quota


#漏桶算法若要正常运行，就必须保证：无论向桶中加多少水，都必须在下一个周期将其清空。

def fill(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount
    print('add %d quote' % amount)
    print('Filled',bucket)

#每次在执行消耗配额的操作之前，都必须先确认桶里有足够的配额可供使用。

def deduct(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True

def do_deduct(bucket, amount):
    if deduct(bucket, amount):
        print ('Had %d quota' % amount)
    else:
        print('Not enough for %d quota' % amount)
    print('deduct',bucket)


#使用这个类的对象之前，先往桶里加水


bucket = Bucket(60)
fill(bucket, 100)









#然后消耗自己所需的配额

do_deduct(bucket, 99)

#继续消耗会导致待消耗的配额比剩余配额还多。

do_deduct(bucket, 3)


#上面这种实现方式的缺点时：以后无法得知漏桶的初始配额。配额会在每个周期内持续流失，如果降到0,那么deduct就总是返回False,为了解决这一问题，我们在类中使用max_quota来记录本周期的初始配额，并用quota_consumed来记录本周期内所消耗的配额。

class Bucket_imp(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time =datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        quota=self.max_quota - self.quota_consumed
       
        if amount == 0:
            self.max_quota = 0
            self.quota_consumed =0
        elif amount > quota :
            self.max_quota += amount-quota
        elif amount < quota:
            self.quota_consumed+= quota-amount
        
            

    def __repr__(self):
        return ("Bucket(max_quota=%d, quota_consumed=%d)" % (self.max_quota, self.quota_consumed))


bucket = Bucket_imp(60)
fill(bucket, 100)
do_deduct(bucket, 99)
fill(bucket, 200)
do_deduct(bucket, 1)















