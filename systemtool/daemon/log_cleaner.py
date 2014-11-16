# -*- coding: utf-8 -*-
import Common
import glob
import os
from os.path import getsize

log_old="/var/log/*.log.*"
log_old1="/var/log/*/*.gz"
log_old2="/var/log/*.gz"

class syslog_Cls(Common.Common):
    """system cleaner"""
    
    def __init__(self):
        Common.Common.__init__(self)
    
    def set_old_log_to_list_fun(self, pathname):
        """得到所有日志的历史压缩文件"""
        for logfile in glob.glob(pathname):
            self.clearner_list.append(logfile)
    
    def set_old_log_file_to_list(self):
        self.set_old_log_to_list_fun(log_old)
        self.set_old_log_to_list_fun(log_old1)
        self.set_old_log_to_list_fun(log_old2)
        if len(self.clearner_list) > 0:
            self.file_isexist = True
        print "set_trash_file_to_list clearner_list is", self.clearner_list
        
    
    
#test = syslog_Cls()
#test.get_old_log_list(log_old)  
#test.get_old_log_list(log_old1)
#test.get_log_clean_count()
#test.get_all_log_size_byte()
#print "log clean count is ", test.file_countnum
#print "log clean size count is ", test.dirsizebyte
    