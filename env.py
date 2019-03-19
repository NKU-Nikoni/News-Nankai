# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 23:14:24 2018

@author: hasee
"""
import os
def getTxt():
        txt = open("env.txt","r").read()#
        return txt
kusTxt=getTxt()
words=kusTxt.split(',')
for word in words:
    os.system("pip3 install "+word)
    print("{} install succeed".format(word))