#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161229 15:09:15
##################################
#6-44.用copyreg实现可靠的pickle操作
##################################

#内置的pickle模块能够将Python对象序列化为字节流，也能把这些字节反序列化为Python对象。经过pickle处理的字节流，不应该在未受信任的程序之间传播。pickle的设计目标是提供一种二进制渠道，使开发者能够在自己所控制的各个程序之间传递Python对象。

#例如我们要用Python对象表示玩家的游戏进度。下面这个GameState类，包含了玩家当前的级别，以及剩余的生命数。

class GameState(object):
    def __init__(self):
        self.level = 0
        self.lives = 4

#程序会在游戏过程中修改GameState对象

state = GameState()
state.level += 1
state.lives -= 1

#玩家退出游戏时，程序可以把游戏状态保存到文件里，以便稍后恢复。使用pickle模块来实现这个功能，是非常简单的。下面这段代码，会把GameState对象直接写到一份文件里:

import pickle

state_path = 'game_state.bin'
with open(state_path, 'wb') as f:
    pickle.dump(state, f)

#之后，可以用load函数来加载这个文件，并把GameState对象还原回来。还原好的GameState对象，与没有经过序列化操作的普通对象一样，看不出太大区别。

with open(state_path, 'rb') as f:
    state_after = pickle.load(f)
print(state_after.__dict__)

#当我们给对象添加计分功能时，上面那种写法在恢复字节流到Python对象时便会暴露一些问题。下面，给GameState类添加point字段。

class GameState(object):
    def __init__(self):
        self.level = 0
        self.lives = 4
        self.points = 0

#针对新版的GameState类来使用pickle模块，其效果与早前相同。

state = GameState()
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)

#但是，如果有一份游戏存档，是用旧版的GameState格式保存的，而现在玩家又要用这份存档来继续游戏，会出现问题。

with open(state_path, 'rb') as f:
    state_after = pickle.load(f)
print(state_after.__dict__)

#还原出来的对象，竟然没有points属性！

#要想解决这些问题，也非常简单，只需要借助内置的copyreg模块即可。开发者可以用copyreg模块注册一些函数，Python对象的序列化，将由这些函数负责。这使得我们可以控制pickle操作的行为，令其变得更加可靠。


"""1.为缺失的属性提供默认值"""
#使用带默认值的构造器
import copyreg

class GameState(object):
    def __init__(self, level=0, lives=5, points=0):
        self.level = level
        self.lives = lives
        self.points = points

#为了用这个构造器进行pickle操作，笔者定义了下面这个辅助函数，它接受GameState对象，并将其转换为一个包含参数的元组，以便提供给copyreg模块。返回的这个元组，含有unpickle操作所使用的函数，以及要传给那个unpickle函数的参数。
def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs,)
def unpickle_game_state(kwargs):
    return GameState(**kwargs)

#下面通过内置的copyreg模块来注册pickle_game_state函数

copyreg.pickle(GameState, pickle_game_state)

#下面正常进行序列化和反序列化

state = GameState()
state.points += 1000
serialized = pickle.dumps(state)
print(serialized[:25])
state_after = pickle.loads(serialized)
print(state_after.__dict__)

#修改GameState定义，给玩家一定数量的魔法卷轴

class GameState(object):
    def __init__(self, level=0, lives=5, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points
        self.magic = magic


#再次使用刚刚序列化过的数据进行反序列化
state_after = pickle.loads(serialized)
print (state_after.__dict__)

"""2.用版本号管理类"""

#有的时候，我们要从现有的Python类中移除某些字段，而这种操作，会导致新类无法与旧类兼容，例如我们现在移除lives字段

class GameState(object):
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic

#修改了构造器之后，程序就无法对旧版游戏数据进行反序列化操作了。因为旧版游戏数据中所有字段，都会通过unpickle_game_state函数，传给GameState构造器，这样就会出错。

## pickle.loads(serialized)


#修改方法是在copyreg那个函数中注册的pickle_game_state)中添加版本号

def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    kwargs['version'] = 2
    return unpickle_game_state, (kwargs,)
def unpickle_game_state(kwargs):
    version = kwargs.pop('version', 1)
    if version == 1:
        kwargs.pop('lives')
    return GameState(**kwargs)

copyreg.pickle(GameState, pickle_game_state)

state_after = pickle.loads(serialized)
print(state_after.__dict__)



    
#内置的pickle模块，只适合用来在彼此信任的程序之间，对相关对象执行序列化和反序列化操作。

#我们可以把内置的copyreg模块同pickle结合起来使用，以便为旧数据添加缺失的属性值、进行类的版本管理，并给序列化之后的数据提供固定的引入路径。































