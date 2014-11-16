# -*- coding: utf-8 -*-

from __future__ import division
import os
import os.path
from os.path import getsize, join, exists
from __builtin__ import len
import ConfigParser
import string
import sys

firefox_ini = "/home/ufo/.mozilla/firefox/profiles.ini"
#cur_user_name_file seam to source file:get_cur_exec_user_to_file
cur_user_name_file="/tmp/.systemtoolcurusername"
#os release file
OS_RELEASE_COFGFILE="/etc/os-release"

class Common:
    """code thar is commonly shared throughout clearner"""
    
    def __init__(self):
        self.allsizebyte = 0L
        self.file_countnum = 0L
        self.allsizeMB = 0L
        self.allsizeKB = 0L
        self.dirsizeMB = 0L
        self.dirsizeKB = 0L
        self.cleaner_dict = {}
        #存放将要进行删除的项（全路径名）
        self.clearner_list = []
        #保存当前系统的home下有多个用户的家目录名
        self.user_all_list = []
        #保存当前用户的根目录名称
        self.cur_username = ""
        #save firefox_path of ~/.mozilla/firefox/profiles.ini
        self.firefox_path = None
        #check clean file is exist
        self.file_isexist = False
        
    def ini_parser(self, ini_file_path, section, option):
        """Read .mozilla/firefox/profiles.ini get firefox cache file and sqlite file """
        cf = ConfigParser.ConfigParser()
        cf.read(ini_file_path)
        #self.firefox_path  = cf.get("Profile0", "Path")
        self.firefox_path  = cf.get(section, option)
        print "ini_parser firefox_path is ", self.firefox_path
        return self.firefox_path
    
    def Generation_clearndict(self):
        firefox_clslist = []
        #firefox_clslist.append("")
    
    def get_cleaner_list(self, dir):
        """ Get all cleaner file list 得到将要进行清理的项到列表中"""
        if len(dir) <= 0:
            print "get cleaner list dir error "
            return -1
        for root, dirs, files in os.walk(dir):
            for name in files:
                fullpathname = join(root, name)
                fullpathname = unicode(fullpathname, 'utf8')
                print "get_cleaner_list  root and name is ", root, name
                self.clearner_list.append(fullpathname)
            
        print "self cleaner list is ", self.clearner_list
        return self.clearner_list
    
    def get_dirsize_Byte(self, dir):
        """Get a directory of the total number of bytes."""
        if len(dir) <= 0:
            print "get a directory of the total number of bytes params error"
            return 0
        for root, dirs, files in os.walk(dir):
            print "dir is ", dirs, files
            try:
                self.allsizebyte += sum(getsize(join(root,name)) for name in files)
                self.file_countnum += len(files)
            except:
                print sys.exc_info()[0],sys.exc_info()[1]
                pass
            print "dirsize is %d filenum is %d", self.allsizebyte, self.file_countnum
            return self.allsizebyte, self.file_countnum 
    
    def get_file_size_Byte(self, filename):
        file_size = 0
        try:
            file_size = getsize(filename)
        except (OSError):
            print sys.exc_info()[0],sys.exc_info()[1]
            pass
        
        return file_size
    
    def get_all_file_size_bycleanfilelist(self):
        if len(self.clearner_list):
            for cleanfile in self.clearner_list:
                self.allsizebyte += self.get_file_size_Byte(cleanfile)
                self.file_countnum += 1
        print "get_all_file_size_bycleanfilelist allsize count", self.allsizebyte, self.file_countnum
    
    def get_size_MB(self):
        """get size of MB by self.allsizebyte"""
        if self.allsizebyte <= 0:
            return 0
        self.allsizeMB = self.allsizebyte / 1024 / 1024
        return self.allsizeMB
    
    def get_size_KB(self):
        """get size of KB by self.allsizebyte"""
        if self.allsizebyte <= 0:
            return 0
        self.allsizeKB = self.allsizebyte / 1024
        return self.allsizeKB

    def get_dirsize_mb(self, dir):
        """Get a directory of the total number of MB."""
        if len(dir) <= 0:
            print "get a directory of the total number of bytes params error"
            return 0
        dirsizeall = self.get_dirsize_Byte(dir)
        if dirsizeall < 0:
            print "get dir size byte is less than 0"
            return 0
        self.dirsizeMB = self.allsizebyte / 1024 / 1024
        print "dir size mb is ", self.dirsizeMB
        return self.dirsizeMB
    
    def get_dirsize_Kb(self, dir):
        """Get a directory of the total number of KB."""
        if len(dir) <= 0:
            print "get a directory of the total number of bytes params error"
            return 0
        dirsizeall = self.get_dirsize_Byte(dir)
        if dirsizeall < 0:
            print "get dir size byte is less than 0"
            return 0
        self.dirsizeKB = self.allsizebyte / 1024
        return self.dirsizeKB

    def remove_dir(self, dir):
        """recursive delete files"""
        if len(dir) <= 0:
            return -1
        for root, dirs, files in os.walk(dir, topdown=False):
            for name in files:
                try:
                    #os.remove(join(root, name))
                    fullpathname = join(root, name)
                    fullpathname = unicode(fullpathname, 'utf8')
                    os.unlink(fullpathname)
                except (OSError):
                    print sys.exc_info()[0],sys.exc_info()[1]
                    pass
            for name in dirs:
                try:
                    fullpathname = join(root, name)
                    fullpathname = unicode(fullpathname, 'utf8')
                    os.rmdir(fullpathname)
                except (OSError):
                    print sys.exc_info()[0],sys.exc_info()[1]
                    pass
        return 0
    
    def get_all_user_name(self):
        self.user_all_list = os.listdir("/home")
        return self.user_all_list
    
    def get_cur_username(self):
        f=open(cur_user_name_file,'r')
        strstr=f.readlines()
        self.cur_username += str(strstr[0])
        return self.cur_username
        print "get_cur_username is ", self.cur_username
    
    def get_cur_username_exec_after(self):
        self.cur_username += os.path.expanduser('~')
        return self.cur_username
    
    def remove_clean_list(self):
        for entry in self.clearner_list:
            exist = os.path.exists(entry)
            if exist == True:
                try:
                    os.remove(entry)
                except:
                    print sys.exc_info()[0],sys.exc_info()[1]
                    pass
            else:
                pass
    
    def empty_content_of_file(self, filename):
        if os.path.exists(filename):
            fileobj = open(filename, "w")
            fileobj.close()
    
    def get_os_release(self):
        """check cur os is oem or live-cd. return True is OEM, otherwish is live-cd"""
        is_oem = False
        if os.path.exists(OS_RELEASE_COFGFILE):
            is_oem = "OEM" in open(OS_RELEASE_COFGFILE,'rt').read()
        return is_oem
          
#test common
#test = Common()
#test.get_dirsize_mb("/var/cache/apt/archives")
#test.get_cleaner_list("/var/cache/apt/archives")
#test.get_dirsize_mb("/home/ufo/.mozilla/firefox/*.default/")
#test.ini_parser(firefox_ini)

#print "this is cleaner call"