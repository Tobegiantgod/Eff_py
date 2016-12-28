#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161228 16:04:37
##################################
#6-43 考虑以contextlib和with语句来改写可复用的try/finally代码
##################################

#有些代码，需要在特殊的情景之下，开发者可以用Python语言的with语句来表示这些代码的运行时机。例如，如果把互斥锁(参见本书第38条)放在with语句之中，那就表示：只有当程序持有该锁的时候，with语句块里的那些代码，才会得到运行。

from threading import Lock
import logging

lock = Lock()
with lock:
    print('Lock is held')

#由于Lock类对with语句提供了适当的支持，所以上面那种写法，可以达到与try/finally结构相仿的效果。

lock.acquire()
try:
    print('Lock is held')
finally:
    lock.release()

#在上面两种写法中，使用with语句的那个版本更好一些，因为它免去了编写try/finally结构所需的重复代码。开发者可以用内置的contextlib模块来处理自己所编写的对象和函数，使他们能够支持with语句。该模块提供了名为contextmanager的修饰器。

#一个简单的函数，只需要经过contextmanager修饰，即可用在with语句之中。这样做，要比标准的写法更加便捷。

#例如，当程序运行到某一部分时，我们希望针对这部分代码，打印更为详细的调试信息。下面定义的这个函数，可以打印两种严重程度(severity level)不同的信息：
def my_function():
    logging.debug('Some debug data')
    logging.error('Error log here')
    logging.warning('Warning log here')
    logging.debug('More debug data')

#系统默认信息级别是WARNING(警告),那么运行该函数时，就只会打印出ERROR(错误)级别的信息。

my_function()

#我们可以定义一种情景管理器，来临时提升该函数的信息级别(log level,日志级别）。下面这个辅助函数，会在运行with块内的代码之前，临时提升信息级别，待with块执行完毕，再恢复原有级别。

from contextlib import contextmanager

@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel() #获得当前的信息级别
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)

#yield表达式所在的地方，就是with块中的语句所要展开执行的地方。with块所抛出任何异常，都会由yield表达式重新抛出，这使得开发者可以在辅助函数里面捕获它。

with debug_logging(logging.DEBUG):
    print('Inside:')
    my_function()
print('After:')
my_function()


#传给with语句的那个情景管理器，本身也可以返回一个对象。而开发者可以通过with复活语句中的as关键字，来指定一个局部变量，Python会把那个对象赋给这个局部变量。这使得with块中的代码，可以直接与外部情境相交互。

#例如，把open传给with语句，并通过as关键字来指定一个目标变量，用以接收open所返回的文件句柄，等到with语句块退出时，该句柄会自动关闭。

with open('my_numbers.txt','w') as handle:
    handle.write('This is some data')

#与每次手工开启并关闭文件句柄的写法相比，上面这个写法更好一些。它使得开发者确信：只要程序离开with语句块，文件就一定会关闭。

#我们只需要在情境管理器里，通过yield语句返回一个值，即可令自己的函数把该值提供给由as关键字所指定的目标变量。

@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)

#由于with语句块可以把严重级别调低，所以在as目标变量上面调用debug等方法时，可以打印出DEBUG级别的调试信息。与之相反，若直接在logging模块上面调用debug，则不会打印出任何DEBUG级别的消息，因为Python自带的那个logger,默认会处在WARNING级别。

with log_level(logging.DEBUG, 'my-log') as logger:
    print('Inside:')
    logger.debug('This is my message!')
    logging.debug('This will not print')
print('outside')
logger = logging.getLogger('my-log')
logger.debug('Debug will not print')
logger.error('Error will print')












