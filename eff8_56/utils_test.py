#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170112 15:15:21
##################################
## utils_test.py ##
##################################

from unittest import TestCase, main
from utils import to_str



class UtilsTestCase(TestCase):

    def test_to_str_bytes(self):
        self.assertEqual('hello', to_str(b'hello'))

    def test_to_str_str(self):
        self.assertEqual('hello', to_str('hello'))

    def test_to_str_bad(self):
        self.assertRaises(TypeError, to_str, object())

if __name__ == '__main__' :
    main()

#通过setUp和tearDown方法，我们可以配置测试环境，系统在执行每个测试程序之前，都会调用一次setUp方法，在执行完每个测试之后，也都会调用一次tearDown方法，这就使得各项测试之间，可以彼此独立地运行。

class MyTest(TestCase):
    def setUp(self):
#       self.test_dir = TemporaryDirectory()
        pass
    def tearDown(self):
#       self.test_dir.cleanup()
        pass
    #Test methods follow
    #...

#要想确信Python程序能够正常运行，唯一的办法就是编写测试。

#我们可以在TestCase子类中，为每一个需要测试的行为，定义对应的测试方法，其名称必须为test开头。

