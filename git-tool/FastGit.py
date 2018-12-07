#! /usr/bin/python
# -*- coding: UTF-8 -*-
# Creat for ForC on 18/7/12
# issue email heqiao.china@gmail.com

import os
import subprocess
from datetime import date,datetime


def runCmd(cmdString):
    return subprocess.call(cmdString, shell=True) == 0

def gitAdd():
    return runCmd('git add .')
    
def gitCommit(message):
    return runCmd('git commit -m \'' + message + '\'')

def gitPush(branch):
    return runCmd('git push origin ' + branch)

def gitPull(branch):
    return runCmd('git pull origin ' + branch)    

def gitTag(version):
    return runCmd('git tag ' + version)

def gitPushTag():
    return runCmd('git push origin --tags')

def gitDeleteTag(version):
    return runCmd('git tag -d' + version)

def gitStatus():
    return runCmd('git status')

def gitStashSave():
    return runCmd('git status save ForCTemp') 

def gitStashPop():
    return runCmd('git status pop 0')


def fastCommit():
    branchString = raw_input("输入分支名称\n")
    commitString = raw_input("输入提交信息\n")
    gitAdd()
    gitStashSave()
    gitPull(branchString)
    gitStashPop()
    gitCommit(commitString)
    if gitPush(branchString):
        print '提交成功'
    else:
        print '提交失败'
    
def fastTag():
    tagString = raw_input("输入tag名称\n")
    if gitTag(tagString):
        if gitPushTag():
            print 'tag finish'
        else:
            print 'tag error'
            gitDeleteTag(tagString)

def InputActive():
    inputnum = raw_input("******************git辅助工具******************\n1.一键提交代码\n2.秒打tag\n")
    if inputnum is '1':
        fastCommit()
    elif inputnum is '2':
        fastTag()
    else : 
        print '错误'

if __name__ == "__main__":
    InputActive()

