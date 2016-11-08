#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161108 09:41:25
##################################
#3-24 以@classmethod的形式的多态去通用地构建对象
##################################

#在Python中不仅对象支持多态，类也支持多态。多态，使继承体系中的多个类都满足相同的接口或继承自相同的抽象类，但却有着各自不同的功能：

#例如，为了实现一套MapReduce流程，我们定义公共基础类来表示输入的数据，它的read方法必须由子类来实现：

class InputData(object):
    def read(self):
        raise NotImplementedError


#现在编写InputData的具体子类，以便从磁盘文件里读取数据：

class PathInputData(InputData):
    def __init__(self,path):
        #super().__init__(self)
        self.path = path

    def read(self):
        return open(self.path).read()

#我们可能需要很多像PathInputData这样的类来充当InputData的子类，每个子类都需要实现标准接口中的read方法，并以字节的形式返回待处理的数据。其他InputData的子类可能会通过网络读取并压缩数据。



#此外，我们还需要为MapReduce工作线程定义一套类似的抽象接口，以便用标准的方式来处理输入的数据：

class Worker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError


#下面定义具体的Worker子类，以实现我们想要的MapReduce功能。本例所实现的功能，是一个简单的换行符计数器：

class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


#上面把需要的类都定义好了，我们还需要创建对象把它们联系起来。下面这段代码可以列出某个目录的内容，并为该目录下的每个文件创建一个PathInputData实例：

import os 

def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))

#用generate_inputs方法所返回的InputData实例来创建LineCountWorkers实例

def create_workers(input_list):
    workers= [] 
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers

#现在执行这些Worker实例，以便将MapReduce流程中的map步骤派发到多个线程之中。接下来，反复调用reduce方法，将map步骤的结果合并成一个最终值。

from threading import Thread

def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, rest = workers[0], workers[0:1]
    for worker in rest:
        first.reduce(worker)
    return first.result


#最后，把上面这些代码片段都拼装到函数里面，以便执行MapReduce流程的每个步骤。

def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)

#用一系列输入文件来测试mapreduce函数，可以得到正常的结果。
tmpdir='/home/daydup/Dev/eff_py/test'
result = mapreduce(tmpdir)

print('There are', result, 'lines')



#但是这种写法有个大问题，就是MapReduce函数不够通用。如果要编写其他的InputData或Worker子类，那就得重写generate_inputs、creat_workers和mapreduce函数，以便与之匹配。


#解决这个问题的最佳方案，是使用@classmethod形式的多态

#首先修改InputData类，为它添加通用的generate_inputs类方法，该方法会根据通用的接口来创建新的InputData实例

class GenericInputData(object):
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


class PathInputData_c(GenericInputData):
    def __init__(self, path):
        self.path = path

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class GenericWorker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


class LineCountWorker_c(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


#最后重写mapreduce函数，令其变得完全通用。

def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)


config = {'data_dir': tmpdir}
print mapreduce(LineCountWorker_c, PathInputData_c, config)


