# -*- coding: utf-8 -*-
import Common
import os
from os.path import getsize
from os.path import join
from os.path import exists
import shutil

#系统相关的:
#与用户相关的：
#user_homedir/bash_history
bash_history_name=".bash_history"
#vim
vim_history_name=".viminfo"
#回收站(root用户所没有的)
trash_filedir_name=".local/share/Trash/files/"
trash_infodir_name=".local/share/Trash/info/"
#最近使用文档记录
use_record_name = ".local/share/recently-used.xbel"


class traceCls(Common.Common):
    """system cleaner"""
    
    def __init__(self):
        Common.Common.__init__(self)
        self.isscaned = 0
        self.trace_dir_list = []
        self.cur_userhome = Common.Common.get_cur_username(self)
        self.bash_history_file_path = join(self.cur_username, bash_history_name)
        self.vim_history_file_path = join(self.cur_username, vim_history_name)
        self.use_record_file_path = join(self.cur_username, use_record_name)
        self.bash_history_file_len = 0L
        self.bash_history_file_count = 0L
        self.vim_history_file_len = 0L
        self.vim_history_file_count = 0L
        self.use_record_file_len = 0L
        self.use_record_file_count = 0L
    
    def set_trash_file_to_list(self):
        """删除当前用户目录下的系统操作记录相关的项"""
        filepathname = join(self.cur_username, trash_filedir_name)
        infopathname = join(self.cur_username, trash_infodir_name)
        if os.path.exists(filepathname) and os.path.exists(infopathname):
            self.file_isexist = True
            self.trace_dir_list.append(filepathname)
            self.trace_dir_list.append(infopathname)
        print "set_trash_file_to_list trace_dir_list is ", self.trace_dir_list
        
    def remove_trash_dir_file(self):
        for trashdir in self.trace_dir_list:
            shutil.rmtree(trashdir)
    
    
    
#test
#test = traceCls()

#test.set_trash_file_to_list()
#for filename in test.trace_dir_list:
#    test.get_cleaner_list(filename)
#print "clearner_list clearner_list ", test.clearner_list
#test.remove_clean_list()