
import Common
import os
import sys
from os.path import join,getsize


apt_cache_dir = "/var/cache/apt/archives/"

class AptCls(Common.Common):
    """apt cleaner"""
    
    def __init__(self):
        Common.Common.__init__(self)
        self.apt_dir_list = []
        self.cur_userhome = Common.Common.get_cur_username(self)
        self.apt_cache_lock_file = os.path.join(apt_cache_dir, 'lock')
    
    def set_apt_dir_to_list(self):
        if os.path.exists(apt_cache_dir):
            self.apt_dir_list.append(apt_cache_dir)
            self.file_isexist = True
        print "set_apt_dir_to_list",self.apt_dir_list 
    
    def get_cleaner_list(self, dir):
        """ Get all cleaner file list"""
        if len(dir) <= 0:
            print "get cleaner list dir error "
            return -1
        for root, dirs, files in os.walk(dir):
            for name in files:
                fullpathname = join(root, name)
                fullpathname = unicode(fullpathname, 'utf8')
                print "get_cleaner_list  root and name is ", root, name
                if fullpathname.find(self.apt_cache_lock_file) < 0:
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
        if self.file_countnum > 0:
            self.file_countnum -= 1 
        return self.allsizebyte, self.file_countnum
        
    
#test
#test = AptCls()

#test.get_cleaner_list(apt_cache_dir)
    
#test.get_all_homedir()