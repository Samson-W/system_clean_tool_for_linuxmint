# -*- coding: utf-8 -*-
import Common
from os.path import join
import os

#firefox相关的
#cookies
foxcookies_file=".mozilla/firefox/*/cookies.sqlite"
#Dom store
foxdom_store=".mozilla/firefox/*/webappsstore.sqlite"
#URL历史
foxurl_history=".mozilla/firefox/*/places.sqlite"
#会话恢复:sessionstore.bak sessionstore.js
foxseeionstore=".mozilla/firefox/*/sessionstore.*"
#密码：
foxpwd=".mozilla/firefox/*/signons.sqlite"
#站点首选项：
foxcontent=".mozilla/firefox/*/content-prefs.sqlite"
#表单历史：
foxformhistory=".mozilla/firefox/*/formhistory.sqlite"
#foxcache
foxcache="~/.cache/mozilla/firefox/cojs83dh.default/Cache/"

#firefox配置文件
firefox_profile = ".mozilla/firefox/profiles.ini"
fox_cache_head=".cache/mozilla/firefox/"
fox_sql_head=".mozilla/firefox/"

class webbrows_Cls(Common.Common):
    """system cleaner"""
    
    def __init__(self):
        Common.Common.__init__(self)
        self.cur_userhome = Common.Common.get_cur_username(self)
        self.cur_foxmidname = ""
        self.foxcookies_file = ""
        self.foxurl_history = ""
        self.foxpwd = ""
        self.foxcontent = ""
        self.foxformhistory = ""
        self.foxcache = ""
        self.fox_cache_dir_list = []
        self.cookies_firefox_file_len = 0L
        self.cookies_firefox_file_count = 0L
        self.urlhis_firefox_file_len = 0L
        self.urlhis_firefox_file_count = 0L
        
        firefox_profile_path = join(self.cur_userhome, firefox_profile)
        if os.path.exists(firefox_profile_path) == False:
            print "not firefox profile , please check it",firefox_profile_path
            return
        
        self.cur_foxmidname = Common.Common.ini_parser(self, firefox_profile_path, "Profile0", "Path")
        print "username is ", self.cur_userhome , self.cur_foxmidname
        self.foxcookies_file = join(join(join(self.cur_userhome, fox_sql_head), self.cur_foxmidname),"cookies.sqlite")
        print "self.foxcookies_file", self.foxcookies_file
        self.foxurl_history = join(join(join(self.cur_userhome, fox_sql_head), self.cur_foxmidname),"places.sqlite")
        self.foxpwd = join(join(join(self.cur_userhome, fox_sql_head), self.cur_foxmidname),"signons.sqlite")
        self.foxcontent = join(join(join(self.cur_userhome, fox_sql_head), self.cur_foxmidname),"content-prefs.sqlite")
        self.foxformhistory = join(join(join(self.cur_userhome, fox_sql_head), self.cur_foxmidname),"formhistory.sqlite")
        self.foxcache = join(join(join(self.cur_userhome, fox_cache_head), self.cur_foxmidname),"Cache/")
    
    def set_fox_cache_dir_to_list(self):
        if os.path.exists(self.foxcache):
            self.fox_cache_dir_list.append(self.foxcache)
            self.file_isexist = True
        print self.fox_cache_dir_list
    
    
#test = webbrows_Cls()
#cur_userhome = test.get_cur_username()
#test.ini_parser(join(cur_userhome, firefox_profile), "Profile0", "Path")


        