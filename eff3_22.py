#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161031 16:24:43
##################################
#3-22尽量用辅助类来维护程序的状态，而不要用字典和元组
##################################


#例如要把许多学生的成绩记录下来，可如下定义辅助类：
class SimpleGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name, grade):
        
        try:
            self._grades[name].append(grade)
        except KeyError:
            self._grades[name] = []
            self._grades[name].append(grade)
    
    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)


#使用示例：
book = SimpleGradebook()
book.add_student('Newton',90)
print book.average_grade('Newton')


#下面扩充SimpleGradebook类，使他能够按照科目来保存成绩：
class BySubjectGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name, subject, grade):
        by_subjects={}
        try:
            by_subjects = self._grades[name]

        except KeyError:
            self._grades[name] = {}
            by_subjects = self._grades[name]

        finally:
            by_subjects[subject] = grade
           

    
    def average_grade(self, name):
        by_subjects = self._grades[name]
        sum_grades=0
        for each_subject in by_subjects:
           sum_grades+=by_subjects[each_subject]
        return sum_grades/len(by_subjects)
        
#下面需求又变了，除了要记录每次考试的成绩，还需要记录此成绩所占权重


class WeightGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name, subject, grade, weight):
        by_subjects={}
        try:
            by_subjects = self._grades[name]

        except KeyError:
            self._grades[name] = {}
            by_subjects = self._grades[name]

        finally:
            by_subjects[subject] = (grade,weight)
           

    
    def average_grade(self, name):
        by_subjects = self._grades[name]
        average_grade = 0

        for each_subject in by_subjects:
            average_grade += by_subjects[each_subject][0]*by_subjects[each_subject][1]

        return average_grade

#以上数据结构多层嵌套的时候，例如字典的字典，这种代码很难看懂，也不利于维护。数据结构一旦复杂就应该把它拆分成类，便于维护：


class Subject(object):
    def __init__(self):
        self._grades = []

    def add_grade(self, score, weight):
        self._grades.append(Grade(score,weight))

    def average_grade(self):
        total,total_weight = 0,0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight

class Student(object):
    def __init__(self):
        self._subjects = {}

    def subject(self, name):
        if name not in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count

#最后编写包含所有学生考试成绩的容器类，该容器以学生的名字为键，并且可以动态的添加学生：

class Gradebook(object):
    def __init__(self):
        self._students = {}

    def student(self, name):
        if name not in self._students:
            self._students[name] = Student()
        return self._students[name]






















