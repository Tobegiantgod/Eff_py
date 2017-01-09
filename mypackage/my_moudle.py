#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170109 13:49:49
##################################
#7-51 为自编的模块定义根异常，以便将调用者与API相隔离
##################################

def determine_weight(volume, density):
    if density <= 0:
        raise InvalidDensityError('Density must be positive')

class Error(Exception):
    """Base-class for all exceptions raised by this module."""

class InvalidDensityError(Error):
    """There was a problem with a provided density value."""

class NegativeDensityError(InvalidDensityError):
    """A provided density value was negative."""


