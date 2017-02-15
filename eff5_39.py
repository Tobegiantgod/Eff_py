#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161223 15:46:43
##################################
#5-39 用Queue来协调各线程之间的工作
##################################

#如果Python程序要同时执行许多事务，那么开发者要经常需要协调这些事务。各种协调方式中，较为高效的一种，则是采用管线函数。

#首先要做的, 是设计一种任务传递方式，以便在管线的不同阶段之间传递工作任务。这种方式，可以用线程安全的生产者--消费者队列来建模。

from threading import Thread, Lock
from collections import deque
from time import sleep
class MyQueue(object):
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()


#我们用Python线程来表示管线的各个阶段，这种Worker线程，会从MyQueue这样的队列中取出待处理的任务，并针对该任务运行相关函数，然后把运行结果放到另一个MyQueue队列里。此外，Worker线程还会记录查询新任务的次数，以及处理完的任务数量。

class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                sleep(0.01) #No work to do
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1

def download(item):
    return item

def resize(item):
    return item

def upload(item):
    return item

#现在，创建相关的队列，然后根据队列与工作线程之间的对应关系，把整条管线的三个阶段拼接好。

download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()
threads = [Worker(download,download_queue,resize_queue), Worker(resize, resize_queue, upload_queue), Worker(upload, upload_queue, done_queue),]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())




#最后，等待管线将所有条目都处理完毕。完全处理好的任务，会出现在done_queue队列里面。

while len(done_queue.items) < 1000:
    pass   
    #print ("Daydup is the smartest people in the world")
        
processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print('Processed', processed, 'items after polling', polled, 'times')

#在管线中，每个阶段的工作函数，其执行速度可能会有所差别，这就使得前一阶段可能会拖慢后一阶段的进度，从而令整条管线迟滞。其次，Worker线程的run方法，会一直执行其循环。即便到了该退出的时候，我们也没办法通知Worker线程停止这一循环。

#用Queue类来弥补自编队列的缺陷

#内置的queue模块中， 有个名叫Queue的类，该类能够彻底解决上面提出的那些问题。Queue类使得工作线程无需再频繁地查询输入队列的状态，因为它的get方法会持续阻塞，直到有新的数据加入。例如，我们启动一条线程，并令该线程等待Queue队列中的输入数据：

from queue import Queue
queue = Queue()

def consumer():
    print('Consumer waiting')
    queue.get()
    print('Consumer done')

thread = Thread(target=consumer)
thread.start()

print('Producer putting')
queue.put(object())
thread.join()
print('Producer done')

#定义缓冲区的容量，如果队列已满，那么后续的put方法就会阻塞。例如，定义一条线程，令该线程先等待片刻，然后再去消费queue队列中的任务:

queue = Queue(1)

def consumer_a():
    sleep(0.1)
    queue.get()
    print('Consumer got 1')
    queue.get()
    print('Consumer got 2')

thread = Thread(target=consumer_a)
thread.start()

#之所以要令消费线程等待片刻，是想给生产线程留出一定的时间，使其可以在consumer()方法调用get之前，率先通过put方法，把两个对象放到队列里面。

queue.put(object())
print('Producer put 1')
queue.put(object())
print('Producer put 2')
thread.join()
print('Producer done')

#我们还可以通过Queue类的task_done方法来追踪工作进度。有了这个方法，我们就不用像原来那样，在管线末端的done_queue处进行轮询，而是可以直接判断:管线中的某个阶段，是否已将输入队列中的任务，全部处理完毕。

in_queue = Queue()

def consumer():
    print('Consumer waiting')
    work = in_queue.get()
    print('Consumer working')
    #Doing work
    #...
    print('Consumer done')
    in_queue.task_done()

Thread(target = consumer).start()

#现在，生产者线程的代码，既不需要在消费者线程上面调用join方法，也不需要轮询消费者线程。生产者只需要在Queue实例上面调用join，并等待in_queue结束即可。即便调用in_queue.join()时队列为空，join也不会立刻返回。必须等待消费者队列中每个条目都调用task_done()之后,生产者线程才可以从join处继续向下执行。

in_queue.put(object())
print('Producer waiting')
in_queue.join()
print('Producer done')

#我们把这些行为都封装到Queue的子类里面，并且令工作线程可以通过这个ClosableQueue类，判断出自己何时应该停止处理。这个子类定义了close方法，此方法会给队列中添加一个特殊的对象，用以表明该对象之后再也没有其他任务需要处理了：

class ClosableQueue(Queue):
    SENTINEL = object()
    def close(self):
        self.put(self.SENTINEL)

#然后，为该类定义迭代器，此迭代器在发现特殊对象时，会停止迭代。__iter__方法也会在适当的时机调用task_done，使得开发者可以追踪队列的工作进度。

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()

#现在根据ClosableQueue类的行为，来重新定义工作线程。这一次，只要for循环耗尽，线程就会退出。

class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

#接下来，用新的工作线程类，来重新创建线程列表。

download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()

threads = [StoppableWorker(download, download_queue, resize_queue),StoppableWorker(resize, resize_queue, upload_queue), StoppableWorker(upload, upload_queue, done_queue)]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())
download_queue.close()

download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), 'items finished')

