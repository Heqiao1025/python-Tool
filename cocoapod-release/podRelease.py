#! /usr/bin/python
# -*- coding: UTF-8 -*-

import os
import subprocess
import re
from datetime import date,datetime

private_pod_repo_name = 'DJSpec'
versionType = 3;
oldVersion = ''
releaseVersion = ''

def runCmd(cmdString):
    return subprocess.call(cmdString, shell=True) == 0

#git method
def gitAdd():
    return runCmd('git add .')
    
def gitCommit(message):
    return runCmd('git commit -m \'' +message + '\'')

def gitPush():
    return runCmd('git push origin master')

def gitPull():
    return runCmd('git pull origin master')    

def gitTag(version):
    return runCmd('git tag ' + version)

def gitPushTag():
    runCmd
    return runCmd('git push origin --tags')

def gitDeleteTag(version):
    return runCmd('git tag -d' + version)

def gitStashSave():
    return runCmd('git status save ForCTemp') 

def gitStashPop():
    return runCmd('git status pop 0')

def gitFastPush():
    gitStashSave()
    if gitPull():
        gitStashPop()
        gitAdd()
        gitCommit('dump version')    
        if gitPush():
            return True
        else:
            return False
    else:
        return False
    


#pod release
def podRemoteVerify():
	return runCmd('pod sepc lint ' + specFile() + '--allow-warnings --use-libraries --verbose')

def podRemotePush():
	global private_pod_repo_name
	return runCmd('pod repo push --allow-warnings --use-libraries --verbose ' + private_pod_repo_name + ' ' + specFile())

def isVaildVersion(version):
	if len(version)==0:
		print 'podspec版本号无版本号'
	versionList = version.split('.')
	if len(versionList) != 3:
		print 'podspec版本号书写不规范'
		exit()

def isPodSpec(file_path):
    ext = os.path.splitext(file_path)[1]
    if ext == '.podspec':
        return True
    return False

def specFile():
    specNum = 0
    specfile = ''
    # 只读取根目录下文件夹
    for root, folders, files in os.walk('.'):
        for filename in files:
            if isPodSpec(os.path.join(root, filename)):
                specNum+=1
                specfile = filename
        if specNum > 1:
            print "索引文件不唯一"
            exit()
        elif specNum == 0:
            print "未查询到索引文件"
            exit()
        return specfile 

def readSpecVersion(fileString):
    for line in fileString.xreadlines():
        if type(line) is str:
            if ('.version' in line) and ('=' in line):
            	if ('{' in line) and ('}' in line) :
                	continue
                else:
                	p = re.compile(r'"(.*?)"', re.S)
                	versions = re.findall(p, line)
                	break
    if len(versions)>1:
    	print "podspec版本号不唯一"
    	exit()
    elif len(versions)==0:
    	print "未查询到podspec版本号"
    	exit()
    else:      
    	return versions[0]

def reloadSpecVersion(fileString):
	global releaseVersion, oldVersion
	file_data = ""
	file_lines = fileString.xreadlines()
	for line in file_lines:
		if ('.version' in line) and ('=' in line):
			if ('{' in line) and ('}' in line):
				file_data += line
			else:
				line = line.replace(oldVersion, releaseVersion)
				file_data += line
		else:
			file_data += line
	return file_data
	

def addSpecVersion(version):
	global versionType, releaseVersion, oldVersion
	oldVersion = version
	versionList = version.split('.')
	if versionType == 1:
		addSiteStr = versionList[0]
		addSiteNum = int(addSiteStr) + 1
		releaseVersion = str(addSiteNum) + '.' + versionList[1] + '.' + versionList[2]
	elif versionType == 2:
		addSiteStr = versionList[1]
		addSiteNum = int(addSiteStr) + 1
		releaseVersion = versionList[0] + '.' + str(addSiteNum) + '.' + versionList[2]
	else:
		addSiteStr = versionList[2]
		addSiteNum = int(addSiteStr) + 1
		releaseVersion = versionList[0] + '.' + versionList[1] + '.' + str(addSiteNum)

def podRelease():
	global releaseVersion
	version = readSpecVersion(open(specFile()))
	isVaildVersion(version)
	addSpecVersion(version)
	new_file_data = reloadSpecVersion(open(specFile()))
	open(specFile(), 'w').write(new_file_data)
	if gitFastPush():
		gitTag(releaseVersion)
		if gitPushTag():
			podRemotePush()
		

        
def InputActive():
    global versionType
    while 1:
        inputStr = raw_input("请输入数字\n1.大版本发布\n2.新特性发布\n3.bug及小功能发布\n\n")
        if inputStr is '1':
            versionType = 1
            podRelease()
            break
        elif inputStr is '2':
            versionType = 2
            podRelease()
            break
        elif inputStr is '3':
            versionType = 3
            podRelease()
            break
        else :
            print '输入不识别,再次输入\n\n'

if __name__ == "__main__":
    InputActive()

