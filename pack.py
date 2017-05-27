#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import subprocess
import os
import time
from os import path as osp

EXPORT_OPTIONS_PLIST = 'exportOptions.plist'

options = None

def clearFile(filePath):
    clearCmd = 'rm -r %s' % filePath
    process = subprocess.Popen(clearCmd, shell=True)
    process.wait()
    print '文件已清除:', filePath, '\n'

def makeDirectory(path):
    if os.path.exists(path) == False:
        os.mkdir(path)

def getExportArchivePath(scheme):
    date = time.strftime('%m月%d日%H时%M分%S秒', time.localtime())
    path = os.path.join(getExportArchiveDirectory(scheme), date)
    makeDirectory(path)
    return path

def getExportArchiveDirectory(scheme):
    path = os.path.abspath(scheme + '_ipa')
    makeDirectory(path)
    return path

def getSaveArchivePath(scheme):
    return os.path.join(getSaveArchiveDirectory(scheme), '%s.xcarchive' % scheme)

def getSaveArchiveDirectory(scheme):
    path = os.path.abspath(scheme + '_archive')
    makeDirectory(path)
    return path

def setGitIgnore(scheme):
    ipaDir = osp.basename(getExportArchiveDirectory(scheme)) + '/*'
    archiveDir = osp.basename(getSaveArchiveDirectory(scheme)) + '/*'
    ignoreFilePath = osp.join(osp.abspath(''), '.gitignore')
    with open(ignoreFilePath, 'r') as ignoreFile:
        fileData = ignoreFile.read()
        lineData = fileData.split('\n')
        ignoreIpaDir = False
        ignoreArchiveDir = False
        for line in ignoreFile.readlines():
            if ipaDir in line:
                ignoreIpaDir = True
            if archiveDir in line:
                ignoreArchiveDir = True
        if ignoreIpaDir != True:
            lineData.insert(1, ipaDir)
        if ignoreArchiveDir != True:
            lineData.insert(1, archiveDir)
    with open(ignoreFilePath, 'w') as ignoreFile:
        for line in lineData:
            ignoreFile.write(line + '\n')

def shouldSetGitIgnore():
    ignoreFilePath = osp.join(osp.abspath(''), '.gitignore')
    if osp.exists(ignoreFilePath):
        setGitIgnore(options.scheme)

def exportArchive(scheme, configuration, savePath):
    exportPath = getExportArchivePath(scheme)

    exportCmd = 'xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s' % (savePath, exportPath, EXPORT_OPTIONS_PLIST)

    print '\033[32mExport cmd:', exportCmd, '\033[0m'

    process = subprocess.Popen(exportCmd, shell=True)
    process.wait()

    exportArchiveReturnCode = process.returncode

    if exportArchiveReturnCode != 0:
        print '\n** Export 操作失败 **\n'
        clearFile(saveArchivePath)
        clearFile(exportPath)
    else:
        shouldSetGitIgnore()

def archiveWorkspace(workspace, scheme, destination, configuration):
    saveArchivePath = getSaveArchivePath(scheme)

    archiveCmd = 'xcodebuild -workspace %s -scheme %s ' % (workspace, scheme)
    if destination == 'simulator':
        archiveCmd += '-destination \'platform=iOS Simulator, OS=latest\' '
    else:
        archiveCmd += '-destination \'generic/platform=iOS\' '
    archiveCmd += '-configuration %s ' % ('Release' if configuration == 'Release' else 'Debug')
    archiveCmd += 'archive -archivePath %s ' % saveArchivePath
    archiveCmd+= '-quiet '

    print '\033[32mArchive cmd:', archiveCmd, '\033[0m'

    process = subprocess.Popen(archiveCmd, shell=True)
    process.wait()

    buildReturnCode = process.returncode

    if buildReturnCode != 0:
        print '\n** Archive 操作失败 **\n'
        clearFile(saveArchivePath)
    else:
        exportArchive(scheme, configuration, saveArchivePath)
        clearFile(saveArchivePath)

def xcodebuild():
    workspace = options.workspace
    scheme = options.scheme
    destination = options.destination
    configuration = options.configuration

    if workspace is None:
        print '\n** 必须设置workspace **\n'
    elif scheme is None:
        print '\n** 必须设置scheme **\n'
    else:
        archiveWorkspace(workspace, scheme, destination, configuration)

def redirect():
    os.chdir(options.path)

def getOptions():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='包含.xcworkspace文件的路径', metavar = '[path]')
    parser.add_argument('-w', '--workspace', help='.xcworkspace文件名（带后缀）', metavar='[name.xcworkspace]')
    parser.add_argument('-s', '--scheme', help='scheme名', metavar='[schemename]')
    parser.add_argument('-d', '--destination', help='需要安装的设备类型', metavar='[device/simulator]')
    parser.add_argument('-c', '--configuration', help='版本类型', metavar='[Debug/Release]')

    global options
    options = parser.parse_args()
    options.destination = options.destination if (options.destination is not None) else 'device'
    options.configuration = options.configuration if (options.configuration is not None) else 'Debug'

if __name__ == '__main__':
    getOptions()
    redirect()
    xcodebuild()