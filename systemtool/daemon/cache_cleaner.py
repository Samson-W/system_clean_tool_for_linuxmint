# -*- coding: utf-8 -*-
import Common
from os.path import join, exists
import os

png_cleanall = 1
record_cleanall = 2
png_andrecord_cleanall = 3

cache_fail_dir_name=".cache/thumbnails/fail/"
cache_large_dir_name=".cache/thumbnails/large/"
cache_normal_dir_name=".cache/thumbnails/normal/"

class png_cache_Cls(Common.Common):
    """system cleaner"""
    
    def __init__(self):
        Common.Common.__init__(self)
        self.cur_userhome = Common.Common.get_cur_username(self)
        self.png_cache_dir_list = []
        #缩略图缓存
        self.fail_png_catch = join(self.cur_userhome,cache_fail_dir_name)
        self.large_png_catch = join(self.cur_userhome,cache_large_dir_name)
        self.normal_png_catch = join(self.cur_userhome,cache_normal_dir_name)
    
    def get_clean_allsize(self):
        pass
    
    def set_png_catch_list(self):
        """设置要进行删除的缩略图缓存路径到列表中"""
        if exists(self.fail_png_catch):
            self.png_cache_dir_list.append(self.fail_png_catch)
        if exists(self.large_png_catch):
            self.png_cache_dir_list.append(self.large_png_catch)
        if exists(self.normal_png_catch):
            self.png_cache_dir_list.append(self.normal_png_catch)
        if len(self.png_cache_dir_list) > 0:
            self.file_isexist = True
        print "self.png_cache_cls_list", self.png_cache_dir_list
        return
    
    def remove_cache_dir(self):
        """对要进行删除的缩略图缓存路径进行删除目录下的所有文件"""
        for catch in self.png_catch:
            if exists(catch) == True:
                Common.Common.remove_dir(self, catch)
            else:
                pass
        return

class flash_cache_Cls(Common.Common):
    """system cleaner"""
    
    def __init__(self):
        Common.Common.__init__(self)
        self.cur_userhome = Common.Common.get_cur_username(self)
        #flash cookies
        self.flash_cookies = join(self.cur_userhome, ".macromedia/Flash_Player/macromedia.com/support/flashplayer/sys/")
        #flash catch
        self.flash_catch = join(self.cur_userhome, ".adobe/Flash_Player/AssetCache/")
        self.flash_cache_cls_list = []
    
    def set_trash_file_to_list(self):
        if exists(self.flash_cookies):
            self.flash_cache_cls_list.append(self.flash_cookies)
            self.file_isexist = True
        print self.flash_cache_cls_list
      
    def remove_cookies_dir(self):
        """对要flash cookies目录下的所有文件及文件夹进行删除"""
        if exists(self.flash_cookies) == True:
            Common.Common.remove_dir(self, self.flash_cookies)
        else:
            pass
        return
    
#test = png_cache_Cls()
#test.set_png_catch_list()
