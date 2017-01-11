#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170110 20:20:27
##################################
#7-53 用虚拟环境隔离项目，并重建其依赖关系
##################################

#本demo不可作为python程序运行执行，需要在unix终端中运行以下命令。

#python可以使用pyvenv命令的来创建自己开发的虚拟环境。每一套虚拟环境，都必须位于各自独立的目录之中。下面产生相应的目录树与文件,并激活虚拟环境。

$pyvenv /tmp/myproject
$cd /tmp/myproject
$source bin/activate
(project)$ 

#进入虚拟环境之后，使用which python3 可以查看当前python解释器的指向。

(myproject)$ which python3
/tmp/myproject/bin/python3

#使用pip3 list 查看当前软件包

(myproject)$pip3 list

#使用deactivate命令返回系统环境。

(myproject)$deactivate
$which python3
/usr/bin/python3


#在虚拟你环境中，可以使用pip3 freeze 命令把开发环境所对应的软件包依赖关系，明确地保存到文件中。按惯例，这个文件应该叫做requirements.txt

(myproject)$ pip3 freeze > requirements.txt
(myproject)$ cat requirements.txt

#在另一个虚拟环境中，我们可以通过该文件来复制与之前相同的环境。

(otherproject)$ pip3 install -r /tmp/myproject/requirements.txt


#借助虚拟环境，我们可以在同一台电脑上面同时安装某软件包的多个版本，而且能保证它们不会冲突。




