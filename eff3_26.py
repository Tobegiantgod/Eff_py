#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161111 15:45:51
##################################
#3-26 只在使用Mix-in组件制作工具类时进行多重继承
##################################

class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)


    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output


    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()

        elif isinstance(value, dict):
            return self._traverse_dict(value)
         
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]

        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)

        else:
            return value

class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

tree = BinaryTree(10, left=BinaryTree(7, right=BinaryTree(9)), right=BinaryTree(13, left=BinaryTree(11)))

from pprint import pprint


pprint(tree.to_dict())


#mix-in的最大优势在于，使用者可以随时安排这些通用的功能，并且能在必要的时候覆写它们，例如下面在这个BinaryTree的子类中，覆写_traverse方法。


class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
        super(BinaryTreeWithParent, self).__init__(value, left=left, right=right)
        self.parent = parent

    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and key == 'parent'):
            return value.value
        else:
            return super(BinaryTreeWithParent, self)._traverse(key, value)



root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent = root)
root.left.right=BinaryTreeWithParent(9, parent=root.left)
pprint(root.to_dict())


#定义了BinaryTreeWithParent._traverse方法之后，如果其他类的某个属性也是BinaryTreeWithParent类型，那么ToDictMixin会自动地处理好这些属性。

class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent

my_tree = NamedSubTree('foobar', root.left.right)

pprint(my_tree.to_dict())


#多个mix-in之间也可以相互组合。例如，可以编写这样一个mix-in,它能够为任意类提供通用的JSON序列化功能。

import json
class JsonMixin(object):
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        print kwargs, '\n'
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())


class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        print switch, '\n'
        self.switch = Switch(**switch)
        self.machines = [Machine(**kwargs) for kwargs in machines]

class Machine(ToDictMixin, JsonMixin):
    
    def __init__(self, **kwargs):
        self.disk = kwargs.pop('disk', None)
        self.cores = kwargs.pop('cores', None)
        self.ram = kwargs.pop('ram', None)
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)

class Switch(ToDictMixin, JsonMixin):
    def __init__(self, **kwargs):
        self.speed = kwargs.pop('speed', None)
        self.ports = kwargs.pop('ports', None)
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)





serialized = """{
    "switch": {"ports": 5, "speed": 1e9},
    "machines":[
        {"cores": 8, "ram": 32e9, "disk": 5e12},
        {"cores": 4, "ram": 16e9, "disk": 1e12}
    ]
}"""

deserialized = DatacenterRack.from_json(serialized)
roundtrip = deserialized.to_json()
pprint (roundtrip)
assert json.loads(serialized) == json.loads(roundtrip)
pprint (json.loads(roundtrip))


#将各个功能实现为可插拔的mix-in组件，然后令相关的类继承自己需要的那些组件，即可定制该类实例所应该具备的行为，能用mix-in组件实现的效果，就不要用多重继承来做，把简单的行为封装到mix-in组件里，然后就可以用多个mix-in组合出复杂的行为了。














