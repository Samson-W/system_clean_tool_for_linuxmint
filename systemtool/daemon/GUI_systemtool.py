# -*- coding: utf-8 -*-
#!/usr/bin/python
from __future__ import division
from gi.repository import Gtk
import Common
import os
import commands
import time
import system_cleaner
import sys
import log_cleaner
import cache_cleaner
import apt_cleaner
import web_cleaner

#SERVER = " server"
SERVER = " 服务"
TITLE_NAME = "系统优化工具"
AUTO_SERVER_ITEM = "开机启动项"
CLEAN_SYSTEM_BTN = "垃圾清理"
CLEAN_SYS_CLEAR_BTN = "系统清理"
PROCESS_MONITOR = "进程监控"
APPLY_AUTO_SERVER_SET = "应用设置"
SYSTEM_AUTO_SERVER_INFO = "系统自启动服务："
SERVER_ON = 1
SERVER_OFF = 0
cur_system_serverlist = "/tmp/.cur_syste_initctllist"
cur_system_serverlisttmp = "/tmp/.cur_syste_initctllisttmp"
status_temfile="/tmp/.status"
server_list_tmpfile = "/tmp/.serverlist"
base_livebootserverlist = "/usr/share/systemtool/daemon/live_initctllist"
systemtool_icon_path="/usr/share/systemtool/daemon/system_optimization.png"
cur_user_name_file="/tmp/.systemtoolcurusername"

SYS_CLEANER_BTN="系统清理"
CACHE_CLEANER_BTN="缓存清理"
COOKIES_CLEANER_BTN="Cookies清理"
FOX_CLEANER_BTN="浏览器缓存清理"
TRACE_CLEANER_BTN="痕迹清理"
LOG_CLEANER_BTN="日志清理"
PNG_CATCH_CLEANER_BTN="缩略图缓存清理"
CLEAN_CLS_SCANING_BTN="扫  描"
CLEAN_CLS_CLEAR_BTN="清  理"

#系统清理
BASH_trash_BTN_LABLE="回收站"
LOG_CHECK_BTN_LABLE="老旧日志"
PNG_CACHE_CLEANER_BTN="缩略图"
#缓存
APT_CACHE_CHECK_BTN_LABLE="安装包缓存"
FOX_CACHE_CHECK_BTN_LABLE="Firefox缓存"
#cookies 
FOX_COOKIES_CHECK_BTN_LABLE="Firefox cookies"
FLASH_COOKIES_CHECK_BTN_LABLE="Flash cookies"
#痕迹清理
BASH_CHECK_BTN_LABLE="bash历史记录"
BASH_VIM_BTN_LABLE="vim历史记录"
USE_RECORD_DOC_CHECK_BTN_LABLE="最近使用文档记录"
FOX_URL_HIS_CHECK_BTN_LABLE="Firefox历史记录"


SYS_CLEANER_INFO_TEXT="系统清理主要是对命令行模式下的bash命令历史记录、vim中使用过的命令历史记录、回收站的垃圾文件进行清理"


class MyWindow(object):
	def __init__(self,title,width,height):
		self.window = Gtk.Window()
		self.window.set_title(title)
		self.window.set_default_size(width,height)
		self.window.set_icon_from_file(systemtool_icon_path)
		#创建垃圾清理的各种实例
		self.traceCls = system_cleaner.traceCls()
		self.oldlogcls = log_cleaner.syslog_Cls()
		self.pngcachecls = cache_cleaner.png_cache_Cls()
		self.aptcachecls = apt_cleaner.AptCls()
		self.fox_webbrwcls = web_cleaner.webbrows_Cls()
		self.flash_cachecls = cache_cleaner.flash_cache_Cls()
		#get cur os release
		common_test = Common.Common()
		self.isoem = common_test.get_os_release()
		#存放各个清理模块的总长度及个数的字串，方便清理后的提示信息显示
		self.system_cls_info_str = ""
		self.cache_cls_info_str = ""
		self.Cookies_cls_info_str = ""
		self.trace_cls_info_str = ""
		#check is already scaned
		self.sys_cls_scan_yes = False
		self.cache_cls_scan_yes = False
		self.cookies_cls_scan_yes = False
		self.trace_cls_scan_yes = False
		#存放垃圾清理标签页中的多个标签页面中的控制和页号的对应关系的字典
		self.page_dict = {}
		#self.window.connect("destroy",lambda q:Gtk.main_quit())
		self.window.connect("destroy", self.window_destory)
		
		self.notebooks = Gtk.Notebook()
		self.window.add(self.notebooks)
		self.vbox = Gtk.VBox()
		#开机启动项标签页
		upstartlabel = Gtk.Label(AUTO_SERVER_ITEM) 
		self.notebooks.append_page(self.vbox, upstartlabel)
		self.autoisdraw = 0
		
		self.run_init()
		self.apply_but = Gtk.Button()
		#self.apply_but.set_label("apply")
		self.apply_but.set_label(APPLY_AUTO_SERVER_SET)
		apphbox = Gtk.HBox()
		apphbox.pack_end(self.apply_but, False, False, 5)
		self.vbox.pack_start(apphbox, False, False, 30)
		self.apply_but.connect("clicked", self.auto_set_apply)
		
		#垃圾清理标签页
		self.cleanvbox = Gtk.VBox()
		clean_label = Gtk.Label(CLEAN_SYSTEM_BTN)
		self.notebooks.append_page(self.cleanvbox, clean_label)
		self.notebooks.page_num(self.cleanvbox)
		clean_btn_box = self.create_button_cleanbox()
		self.cleanvbox.pack_start(clean_btn_box, False, False, 5)
		#create cleaner notebook
		self.cleaner_notebook = self.create_clean_notebook()
		self.cleaner_notebook.set_show_tabs(False)
		self.cleanvbox.pack_start(self.cleaner_notebook, False, False, 5)
		
		self.window.show_all()
		#self.switch.hide()
		return

	def window_destory(self, __widget):
		self.del_tmp_file()
		Gtk.main_quit()
		return
	
	def create_button_cleanbox(self):
		"""Create the buttonbox for cleaner"""
		
		buttonbox = Gtk.HButtonBox()
		buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
		#create system clean button
		sys_clean_button = Gtk.Button()
		sys_clean_button.set_label(CLEAN_SYS_CLEAR_BTN)
		buttonbox.add(sys_clean_button)
		#create cache clean button
		cacheclean_button = Gtk.Button()
		cacheclean_button.set_label(CACHE_CLEANER_BTN)
		buttonbox.add(cacheclean_button)
		#create cookies clean button
		cookiesclean_button = Gtk.Button()
		cookiesclean_button.set_label(COOKIES_CLEANER_BTN)
		buttonbox.add(cookiesclean_button)
		#create Trace clean button
		traceclean_button = Gtk.Button()
		traceclean_button.set_label(TRACE_CLEANER_BTN)
		buttonbox.add(traceclean_button)
		
		#connect event for button
		sys_clean_button.connect("clicked", self.run_sysclean)
		cacheclean_button.connect("clicked", self.run_cacheclean)
		cookiesclean_button.connect("clicked", self.run_cookiesclean)
		traceclean_button.connect("clicked", self.run_traceclean)
		
		return buttonbox
	
	def run_sysclean(self, __widget):
		#self.bash_chkbtn.set_active(False)
		#self.vim_chkbtn.set_active(False)
		#self.trash_chkbtn.set_active(False)
		self.change_cleaner_notebook_page(CLEAN_SYS_CLEAR_BTN)
		
	def run_cacheclean(self, __widget):
		self.change_cleaner_notebook_page(CACHE_CLEANER_BTN)
	
	def run_cookiesclean(self, __widget):
		self.change_cleaner_notebook_page(COOKIES_CLEANER_BTN)
	
	def run_traceclean(self, __widget):
		self.change_cleaner_notebook_page(TRACE_CLEANER_BTN)
	
	def system_cls_scan_fuc(self, __widget):
		self.system_cls_scandel_fuc(False)
	
	def system_cls_remove_fuc(self, __widget):
		self.system_cls_scandel_fuc(True)
		
	def cache_cls_scan_fuc(self, __widget):
		self.cache_cls_scandel_fuc(False)
	
	def cache_cls_remove_fuc(self, __widget):
		self.cache_cls_scandel_fuc(True)
	
	def cookies_cls_scan_fuc(self, __widget):
		self.cookies_cls_scandel_fuc(False)
	
	def cookies_cls_remove_fuc(self, __widget):
		self.cookies_cls_scandel_fuc(True)
	
	def trace_cls_scan_fuc(self, __widget):
		self.trace_cls_scandel_fuc(False)
	
	def trace_cls_remove_fuc(self, __widget):
		self.trace_cls_scandel_fuc(True)
	
	def system_cls_scandel_fuc(self, really_clean):
		"""really_clean:
        True: exec remove            False: only scaning all entry num and size"""
		
		if really_clean == False:
			self.traceCls.allsizebyte = 0L
			self.traceCls.file_countnum = 0L
			self.traceCls.allsizeMB = 0L
			self.traceCls.allsizeKB = 0L
			self.traceCls.clearner_list = []
			self.traceCls.trace_dir_list = []
			
			self.oldlogcls.clearner_list = []
			self.oldlogcls.allsizebyte = 0L
			self.oldlogcls.file_countnum = 0L
			self.oldlogcls.allsizeMB = 0L
			self.oldlogcls.allsizeKB = 0L
			
			self.pngcachecls.clearner_list = []
			self.pngcachecls.png_cache_dir_list = []
			self.pngcachecls.allsizebyte = 0L
			self.pngcachecls.file_countnum = 0L
			self.pngcachecls.allsizeMB = 0L
			self.pngcachecls.allsizeKB = 0L
			
			if self.trash_chkbtn.get_active():
				self.traceCls.set_trash_file_to_list()
				if self.traceCls.file_isexist:
					for tracename in self.traceCls.trace_dir_list:
						self.traceCls.get_cleaner_list(tracename)
					self.traceCls.get_all_file_size_bycleanfilelist()
			if self.old_log_chkbtn.get_active():
				self.oldlogcls.set_old_log_file_to_list()
				if self.oldlogcls.file_isexist:
					for filename in self.oldlogcls.clearner_list:
						self.oldlogcls.allsizebyte += self.oldlogcls.get_file_size_Byte(filename)
						self.oldlogcls.file_countnum += 1
			if self.png_cache_chkbtn.get_active():
				self.pngcachecls.set_png_catch_list()
				if self.pngcachecls.file_isexist:
					for dirname in self.pngcachecls.png_cache_dir_list:
						self.pngcachecls.get_cleaner_list(dirname)
						self.pngcachecls.get_dirsize_Byte(dirname)
			if self.trash_chkbtn.get_active() == False and self.old_log_chkbtn.get_active() == False and self.png_cache_chkbtn.get_active() == False:
				self.create_waring_msgDialog("请选择清理项进行扫描操作！")
				return
			self.sys_cls_scan_yes = True
			sizemb_sum = self.traceCls.get_size_MB() + self.oldlogcls.get_size_MB() + self.pngcachecls.get_size_MB()
			sizekb_sum = self.traceCls.get_size_KB() + self.oldlogcls.get_size_KB() + self.pngcachecls.get_size_KB()
			sizeByte = self.traceCls.allsizebyte + self.oldlogcls.allsizebyte + self.pngcachecls.allsizebyte
			
			sizemb_sum = round(sizemb_sum, 2)
			sizekb_sum = round(sizekb_sum, 2)
			sizeByte = round(sizeByte, 2)
			all_count = self.traceCls.file_countnum + self.oldlogcls.file_countnum + self.pngcachecls.file_countnum
			print "size kb is ", sizekb_sum, sizemb_sum
			if int(sizemb_sum) > 0:
				self.system_cls_info_str = str(all_count) + "个, 清理总空间大小为：" + str(sizemb_sum) + "MB." 
			elif  int(sizekb_sum) > 0:
				self.system_cls_info_str = str(all_count) + "个, 清理总空间大小为：" + str(sizekb_sum) + "KB."
			else:
				self.system_cls_info_str = str(all_count) + "个, 清理总空间大小为：" + str(sizeByte) + "B."
			infostr = "将要清理的文件数：" + self.system_cls_info_str
			self.sys_cls_info_label.set_text(infostr)
		elif really_clean == True:
			sizeByte = self.traceCls.allsizebyte + self.oldlogcls.allsizebyte + self.pngcachecls.allsizebyte
			all_count = self.traceCls.file_countnum + self.oldlogcls.file_countnum + self.pngcachecls.file_countnum
			if sizeByte == 0 and all_count == 0 and self.sys_cls_scan_yes == False:
				self.create_waring_msgDialog("请先进行扫描操作！")
				return
			if len(self.traceCls.clearner_list) > 0:
				if self.traceCls.file_isexist:
					for deldir in self.traceCls.trace_dir_list:
						self.traceCls.remove_dir(deldir)
			if len(self.oldlogcls.clearner_list) > 0:
				self.oldlogcls.remove_clean_list()
			if len(self.pngcachecls.clearner_list) > 0:
				self.pngcachecls.remove_clean_list()
			infostr = "已经清理的文件数：" + self.system_cls_info_str
			self.sys_cls_info_label.set_text(infostr)
	
	def cache_cls_scandel_fuc(self, really_clean):
		"""really_clean:
        True: exec remove            False: only scaning all entry num and size"""
		if really_clean == False:
			self.aptcachecls.allsizebyte = 0L
			self.aptcachecls.file_countnum = 0L
			self.aptcachecls.allsizeMB = 0L
			self.aptcachecls.allsizeKB = 0L
			self.aptcachecls.clearner_list = []
			self.aptcachecls.apt_dir_list = []
			
			self.fox_webbrwcls.clearner_list = []
			self.fox_webbrwcls.fox_cache_dir_list = []
			self.fox_webbrwcls.allsizebyte = 0L
			self.fox_webbrwcls.file_countnum = 0L
			self.fox_webbrwcls.allsizeMB = 0L
			self.fox_webbrwcls.allsizeKB = 0L
			
			if self.apt_chkbtn.get_active():
				self.aptcachecls.set_apt_dir_to_list()
				if self.aptcachecls.file_isexist:
					for dirname in self.aptcachecls.apt_dir_list:
						self.aptcachecls.get_cleaner_list(dirname)
    					self.aptcachecls.get_dirsize_Byte(dirname)
			if self.fox_cache_chkbtn.get_active():
				self.fox_webbrwcls.set_fox_cache_dir_to_list()
				if self.fox_webbrwcls.file_isexist:
					for filename in self.fox_webbrwcls.fox_cache_dir_list:
						self.fox_webbrwcls.get_cleaner_list(filename)
    					self.fox_webbrwcls.get_dirsize_Byte(filename)
    					self.fox_webbrwcls.file_countnum = len(self.fox_webbrwcls.clearner_list)
			if self.apt_chkbtn.get_active() == False and self.fox_cache_chkbtn.get_active() == False:
				self.create_waring_msgDialog("请选择清理项进行扫描操作！")
				return
			self.cache_cls_scan_yes = True
			sizemb_sum = self.aptcachecls.get_size_MB() + self.fox_webbrwcls.get_size_MB() 
			sizekb_sum = self.aptcachecls.get_size_KB() + self.fox_webbrwcls.get_size_KB() 
			sizeByte = self.aptcachecls.allsizebyte + self.fox_webbrwcls.allsizebyte
			
			sizemb_sum = round(sizemb_sum, 2)
			sizekb_sum = round(sizekb_sum, 2)
			sizeByte = round(sizeByte, 2)
			all_count = self.aptcachecls.file_countnum + self.fox_webbrwcls.file_countnum
			print "size kb is ", sizekb_sum, sizemb_sum
			if int(sizemb_sum) > 0:
				self.cache_cls_info_str = str(all_count) + "个, 清理总空间大小为：" + str(sizemb_sum) + "MB."
			elif  int(sizekb_sum) > 0:
				self.cache_cls_info_str = str(all_count) + "个, 清理总空间大小为：" + str(sizekb_sum) + "KB."
			else:
				self.cache_cls_info_str = str(all_count) + "个, 清理总空间大小为：" + str(sizeByte) + "B."
			infostr = "将要清理的文件数：" + self.cache_cls_info_str
			self.cache_info_label.set_text(infostr)
		elif really_clean == True:
			sizeByte = self.aptcachecls.allsizebyte + self.fox_webbrwcls.allsizebyte
			all_count = self.aptcachecls.file_countnum + self.fox_webbrwcls.file_countnum
			if sizeByte == 0 and all_count == 0 and self.cache_cls_scan_yes == False:
				self.create_waring_msgDialog("请先进行扫描操作！")
				return
			if len(self.aptcachecls.clearner_list) > 0:
				self.aptcachecls.remove_clean_list()
			if len(self.fox_webbrwcls.clearner_list) > 0:
				self.fox_webbrwcls.remove_clean_list()
			infostr = "已经清理的文件数：" + self.cache_cls_info_str
			self.cache_info_label.set_text(infostr)
	
	def cookies_cls_scandel_fuc(self, really_clean):
		"""really_clean:True: exec remove            False: only scaning all entry num and size"""
		self.flash_cachecls.clearner_list = []
		self.flash_cachecls.flash_cache_cls_list = []
		self.flash_cachecls.allsizebyte = 0L
		self.flash_cachecls.file_countnum = 0L
		self.flash_cachecls.allsizeMB = 0L
		self.flash_cachecls.allsizeKB = 0L
		
		sizeByte = 0L
		count_file = 0L
		if really_clean == True:
			sizeByte = self.flash_cachecls.allsizebyte + self.fox_webbrwcls.cookies_firefox_file_len
			all_count = self.flash_cachecls.file_countnum + self.fox_webbrwcls.cookies_firefox_file_count
			print "cookies sizebyte  all_count", sizeByte, all_count
			if sizeByte == 0 and all_count == 0 and self.cookies_cls_scan_yes == False:
				self.create_waring_msgDialog("请先进行扫描操作！")
				return 
			if self.fox_webbrwcls.cookies_firefox_file_len > 0:
				self.fox_webbrwcls.empty_content_of_file(self.fox_webbrwcls.foxcookies_file)
			if len(self.flash_cachecls.clearner_list) > 0:
				self.flash_cachecls.remove_clean_list()
			infostr = "已经清理的文件数：" + self.Cookies_cls_info_str
			self.cookies_info_label.set_text(infostr)
		elif really_clean == False:
			if self.foxcook_chkbtn.get_active():
				self.fox_webbrwcls.cookies_firefox_file_len = 0L
				self.fox_webbrwcls.cookies_firefox_file_count = 0L
				if self.fox_webbrwcls.file_isexist:
					sizeByte = self.fox_webbrwcls.get_file_size_Byte(self.fox_webbrwcls.foxcookies_file)
					count_file += 1
				self.fox_webbrwcls.cookies_firefox_file_len = sizeByte
				self.fox_webbrwcls.cookies_firefox_file_count = count_file;
				print "fox cookies file len is ", self.fox_webbrwcls.cookies_firefox_file_len, self.fox_webbrwcls.cookies_firefox_file_count
			if self.flashcook_chkbtn.get_active():
				self.flash_cachecls.set_trash_file_to_list()
				if self.flash_cachecls.file_isexist:
					for dirname in self.flash_cachecls.flash_cache_cls_list:
						self.flash_cachecls.get_cleaner_list(dirname)
						self.flash_cachecls.get_dirsize_Byte(dirname)
        		self.flash_cachecls.file_countnum = len(self.flash_cachecls.clearner_list)
        	if self.foxcook_chkbtn.get_active() == False and self.flashcook_chkbtn.get_active() == False:
        		self.create_waring_msgDialog("请选择清理项进行扫描操作！")
        		return
        	self.cookies_cls_scan_yes = True
        	sizemb_sum = (sizeByte / 1024 / 1024) + self.flash_cachecls.get_size_MB() 
        	sizekb_sum = (sizeByte / 1024) + self.flash_cachecls.get_size_KB() 
        	sizeByte = sizeByte + self.flash_cachecls.allsizebyte
        	sizemb_sum = round(sizemb_sum, 2)
        	sizekb_sum = round(sizekb_sum, 2)
        	sizeByte = round(sizeByte, 2)
        	all_count = count_file + self.flash_cachecls.file_countnum
        	print "size kb is ", sizekb_sum, sizemb_sum
        	if int(sizemb_sum) > 0:
        		self.Cookies_cls_info_str = str(all_count) + "个, 清理总空间大小为：" + str(sizemb_sum) + "MB."
        	elif  int(sizekb_sum) > 0:
        		self.Cookies_cls_info_str = str(all_count) + "个, 清理总空间大小为：" + str(sizekb_sum) + "KB."
        	else:
        		self.Cookies_cls_info_str = str(all_count) + "个, 清理总空间大小为：" + str(sizeByte) + "B."
        	infostr = "将要清理的文件数：" + self.Cookies_cls_info_str
        	self.cookies_info_label.set_text(infostr)
	
	def trace_cls_scandel_fuc(self, really_clean):
		"""really_clean:True: exec remove            False: only scaning all entry num and size"""
		sizeByte = 0L
		count_file = 0L
		if really_clean == True:
			sizeByte = self.traceCls.bash_history_file_len + self.traceCls.vim_history_file_len + self.traceCls.use_record_file_len + self.fox_webbrwcls.urlhis_firefox_file_len
			all_count = self.traceCls.bash_history_file_count + self.traceCls.vim_history_file_count + self.traceCls.use_record_file_count + self.fox_webbrwcls.urlhis_firefox_file_count
			print "cookies sizebyte  all_count", sizeByte, all_count
			if sizeByte == 0 and all_count == 0 and self.trace_cls_scan_yes == False:
				self.create_waring_msgDialog("请先进行扫描操作！")
				return 
			if self.traceCls.bash_history_file_len > 0:
				self.traceCls.empty_content_of_file(self.traceCls.bash_history_file_path)
			if self.traceCls.vim_history_file_len > 0:
				self.traceCls.empty_content_of_file(self.traceCls.vim_history_file_path)
			if self.traceCls.use_record_file_len > 0:
				self.traceCls.empty_content_of_file(self.traceCls.use_record_file_path)
			if self.fox_webbrwcls.urlhis_firefox_file_len > 0:
				self.fox_webbrwcls.empty_content_of_file(self.fox_webbrwcls.foxurl_history)
			infostr = "已经清理的文件数：" + self.trace_cls_info_str
			self.trace_info_label.set_text(infostr)
		elif really_clean == False:
			self.traceCls.bash_history_file_len = 0L
			self.traceCls.bash_history_file_count = 0L
			self.traceCls.vim_history_file_len = 0L
			self.traceCls.vim_history_file_len = 0L
			self.traceCls.vim_history_file_count = 0L
			self.traceCls.use_record_file_len = 0L
			self.traceCls.use_record_file_count = 0L
			self.fox_webbrwcls.urlhis_firefox_file_len = 0L
			self.fox_webbrwcls.urlhis_firefox_file_count = 0L
			if self.bash_his_chkbtn.get_active():
				if os.path.exists(self.traceCls.bash_history_file_path):
					sizeByte += self.traceCls.get_file_size_Byte(self.traceCls.bash_history_file_path)
					count_file += 1
					self.traceCls.bash_history_file_len = self.traceCls.get_file_size_Byte(self.traceCls.bash_history_file_path)
					self.traceCls.bash_history_file_count = 1
				print "bash_history_file_len file len is ", self.traceCls.bash_history_file_len, self.traceCls.bash_history_file_count
			if self.vim_his_chkbtn.get_active():
				if os.path.exists(self.traceCls.vim_history_file_path):
					sizeByte += self.traceCls.get_file_size_Byte(self.traceCls.vim_history_file_path)
					count_file += 1
					self.traceCls.vim_history_file_len = self.traceCls.get_file_size_Byte(self.traceCls.vim_history_file_path)
					self.traceCls.vim_history_file_count = 1
				print "vim_history_file_len file len is ", self.traceCls.vim_history_file_len, self.traceCls.vim_history_file_count
			if self.use_record_chkbtn.get_active():
				if os.path.exists(self.traceCls.use_record_file_path):
					sizeByte += self.traceCls.get_file_size_Byte(self.traceCls.use_record_file_path)
					count_file += 1
					self.traceCls.use_record_file_len = self.traceCls.get_file_size_Byte(self.traceCls.use_record_file_path)
					self.traceCls.use_record_file_count = 1
				print "use_record_file_len file len is ", self.traceCls.use_record_file_len, self.traceCls.use_record_file_count
			if self.fox_urlhis_chkbtn.get_active():
				if os.path.exists(self.fox_webbrwcls.foxurl_history):
					sizeByte += self.fox_webbrwcls.get_file_size_Byte(self.fox_webbrwcls.foxurl_history)
					count_file += 1
					self.fox_webbrwcls.urlhis_firefox_file_len = self.fox_webbrwcls.get_file_size_Byte(self.fox_webbrwcls.foxurl_history)
					self.fox_webbrwcls.urlhis_firefox_file_count = 1
				print "urlhis_firefox_file_len file len is ", self.fox_webbrwcls.urlhis_firefox_file_len, self.fox_webbrwcls.urlhis_firefox_file_count
        	if self.bash_his_chkbtn.get_active() == False and self.vim_his_chkbtn.get_active() == False and self.use_record_chkbtn.get_active() == False and self.fox_urlhis_chkbtn.get_active() == False:
        		self.create_waring_msgDialog("请选择清理项进行扫描操作！")
        		return
        	self.trace_cls_scan_yes = True
        	sizemb_sum = (sizeByte / 1024 / 1024)
        	sizekb_sum = (sizeByte / 1024)
        	sizemb_sum = round(sizemb_sum, 2)
        	sizekb_sum = round(sizekb_sum, 2)
        	sizeByte = round(sizeByte, 2)
        	all_count = count_file
        	print "size kb is ", sizekb_sum, sizemb_sum
        	if int(sizemb_sum) > 0:
        		self.trace_cls_info_str = str(all_count) + "个, 清理总空间大小为：" + str(sizemb_sum) + "MB."
        	elif  int(sizekb_sum) > 0:
        		self.trace_cls_info_str = str(all_count) + "个, 清理总空间大小为：" + str(sizekb_sum) + "KB."
        	else:
        		self.trace_cls_info_str = str(all_count) + "个, 清理总空间大小为：" + str(sizeByte) + "B."
        	infostr = "将要清理的文件数：" + self.trace_cls_info_str
        	self.trace_info_label.set_text(infostr)
	
	def create_clean_notebook(self):
		"""create clean notebooks."""
		notebooks = Gtk.Notebook()
		#create system clean page
		self.systemvbox = Gtk.VBox()
		#self.syslabel = Gtk.Label(SYS_CLEANER_INFO_TEXT)
		notebooks.append_page(self.systemvbox, None)
		self.page_dict[SYS_CLEANER_BTN] = notebooks.page_num(self.systemvbox)
		#self.systemvbox.pack_start(self.syslabel, False, False, 5)
		self.trash_chkbtn = Gtk.CheckButton(BASH_trash_BTN_LABLE, False)
		self.systemvbox.pack_start(self.trash_chkbtn, False, False, 5)
		#old log btn
		self.old_log_chkbtn = Gtk.CheckButton(LOG_CHECK_BTN_LABLE, False)
		self.systemvbox.pack_start(self.old_log_chkbtn, False, False, 5)
		#png catch btn
		self.png_cache_chkbtn = Gtk.CheckButton(PNG_CACHE_CLEANER_BTN, False)
		self.systemvbox.pack_start(self.png_cache_chkbtn, False, False, 5)
		
		#all len and file count number
		self.sys_cls_info_label = Gtk.Label(None)
		self.systemvbox.pack_start(self.sys_cls_info_label, False, False, 5)
		
		self.sys_cls_Hbox = Gtk.HBox()
		self.systemvbox.pack_start(self.sys_cls_Hbox, False, False, 5)
			
		#当判断已经进行了扫描后，才能够清理按钮到Hbox
		self.sys_cls_clear_btn = Gtk.Button()
		self.sys_cls_clear_btn.set_label(CLEAN_CLS_CLEAR_BTN)
		self.sys_cls_Hbox.pack_end(self.sys_cls_clear_btn, False, False, 5)
		self.sys_cls_clear_btn.connect("clicked", self.system_cls_remove_fuc)
		
		self.sys_cls_scan_btn = Gtk.Button()
		self.sys_cls_scan_btn.set_label(CLEAN_CLS_SCANING_BTN)
		self.sys_cls_Hbox.pack_end(self.sys_cls_scan_btn, False, False, 5)
		self.sys_cls_scan_btn.connect("clicked", self.system_cls_scan_fuc)
		#create system clean page end
		
		#create cache clean page
		self.cache_vbox = Gtk.VBox()
		notebooks.append_page(self.cache_vbox, None)
		self.page_dict[CACHE_CLEANER_BTN] = notebooks.page_num(self.cache_vbox)
		
		self.apt_chkbtn = Gtk.CheckButton(APT_CACHE_CHECK_BTN_LABLE, False)
		self.cache_vbox.pack_start(self.apt_chkbtn, False, False, 5)
		#fox cache btn
		self.fox_cache_chkbtn = Gtk.CheckButton(FOX_CACHE_CHECK_BTN_LABLE, False)
		self.cache_vbox.pack_start(self.fox_cache_chkbtn, False, False, 5)
		
		#all len and file count number
		self.cache_info_label = Gtk.Label(None)
		self.cache_vbox.pack_start(self.cache_info_label, False, False, 5)
		
		self.cache_cls_Hbox = Gtk.HBox()
		self.cache_vbox.pack_start(self.cache_cls_Hbox, False, False, 5)
		#当判断已经进行了扫描后，才能够清理按钮到Hbox
		self.cache_cls_clear_btn = Gtk.Button()
		self.cache_cls_clear_btn.set_label(CLEAN_CLS_CLEAR_BTN)
		self.cache_cls_Hbox.pack_end(self.cache_cls_clear_btn, False, False, 5)
		self.cache_cls_clear_btn.connect("clicked", self.cache_cls_remove_fuc)
		
		self.cache_cls_scan_btn = Gtk.Button()
		self.cache_cls_scan_btn.set_label(CLEAN_CLS_SCANING_BTN)
		self.cache_cls_Hbox.pack_end(self.cache_cls_scan_btn, False, False, 5)
		self.cache_cls_scan_btn.connect("clicked", self.cache_cls_scan_fuc)
		#create cache clean page end
		
		#create cookies clean page
		self.cookies_vbox = Gtk.VBox()
		notebooks.append_page(self.cookies_vbox, None)
		self.page_dict[COOKIES_CLEANER_BTN] = notebooks.page_num(self.cookies_vbox)
		
		self.foxcook_chkbtn = Gtk.CheckButton(FOX_COOKIES_CHECK_BTN_LABLE, False)
		self.cookies_vbox.pack_start(self.foxcook_chkbtn, False, False, 5)
		
		self.flashcook_chkbtn = Gtk.CheckButton(FLASH_COOKIES_CHECK_BTN_LABLE, False)
		self.cookies_vbox.pack_start(self.flashcook_chkbtn, False, False, 5)
		
		#all len and file count number
		self.cookies_info_label = Gtk.Label(None)
		self.cookies_vbox.pack_start(self.cookies_info_label, False, False, 5)
		
		self.cookies_cls_Hbox = Gtk.HBox()
		self.cookies_vbox.pack_start(self.cookies_cls_Hbox, False, False, 5)
		#当判断已经进行了扫描后，才能够清理按钮到Hbox
		self.cookies_cls_clear_btn = Gtk.Button()
		self.cookies_cls_clear_btn.set_label(CLEAN_CLS_CLEAR_BTN)
		self.cookies_cls_Hbox.pack_end(self.cookies_cls_clear_btn, False, False, 5)
		self.cookies_cls_clear_btn.connect("clicked", self.cookies_cls_remove_fuc)
		
		self.cookies_cls_scan_btn = Gtk.Button()
		self.cookies_cls_scan_btn.set_label(CLEAN_CLS_SCANING_BTN)
		self.cookies_cls_Hbox.pack_end(self.cookies_cls_scan_btn, False, False, 5)
		self.cookies_cls_scan_btn.connect("clicked", self.cookies_cls_scan_fuc)
		#create cookies clean page end
		
		#create trace clean page
		self.trace_vbox = Gtk.VBox()
		notebooks.append_page(self.trace_vbox, None)
		self.page_dict[TRACE_CLEANER_BTN] = notebooks.page_num(self.trace_vbox)
		
		self.bash_his_chkbtn = Gtk.CheckButton(BASH_CHECK_BTN_LABLE, False)
		self.trace_vbox.pack_start(self.bash_his_chkbtn, False, False, 5)
		
		self.vim_his_chkbtn = Gtk.CheckButton(BASH_VIM_BTN_LABLE, False)
		self.trace_vbox.pack_start(self.vim_his_chkbtn, False, False, 5)
		
		self.use_record_chkbtn = Gtk.CheckButton(USE_RECORD_DOC_CHECK_BTN_LABLE, False)
		self.trace_vbox.pack_start(self.use_record_chkbtn, False, False, 5)
		
		self.fox_urlhis_chkbtn = Gtk.CheckButton(FOX_URL_HIS_CHECK_BTN_LABLE, False)
		self.trace_vbox.pack_start(self.fox_urlhis_chkbtn, False, False, 5)
		
		#all len and file count number
		self.trace_info_label = Gtk.Label(None)
		self.trace_vbox.pack_start(self.trace_info_label, False, False, 5)
		
		self.trace_cls_Hbox = Gtk.HBox()
		self.trace_vbox.pack_start(self.trace_cls_Hbox, False, False, 5)
		#当判断已经进行了扫描后，才能够清理按钮到Hbox
		self.trace_cls_clear_btn = Gtk.Button()
		self.trace_cls_clear_btn.set_label(CLEAN_CLS_CLEAR_BTN)
		self.trace_cls_Hbox.pack_end(self.trace_cls_clear_btn, False, False, 5)
		self.trace_cls_clear_btn.connect("clicked", self.trace_cls_remove_fuc)
		
		self.trace_cls_scan_btn = Gtk.Button()
		self.trace_cls_scan_btn.set_label(CLEAN_CLS_SCANING_BTN)
		self.trace_cls_Hbox.pack_end(self.trace_cls_scan_btn, False, False, 5)
		self.trace_cls_scan_btn.connect("clicked", self.trace_cls_scan_fuc)
		
		return notebooks
	
	def change_cleaner_notebook_page(self, button_name):
		"""change cleaner notebook when Choice cleaner button """
		if len(self.page_dict) == 0:
			return 
		pagenum = self.page_dict[button_name]
		print("change cleaner noetbook page is", pagenum);
		self.cleaner_notebook.set_current_page(pagenum)
		self.window.show_all()	
	
	
	def del_tmp_file(self):
		rmtmpcmd = "umask u=rwx,g=rwx,o=rwx; rm -f " + cur_system_serverlist + " " + status_temfile + " " + server_list_tmpfile + " " + cur_system_serverlisttmp
		print "rmtmpcmd ", rmtmpcmd
		if os.path.exists(cur_user_name_file):
			os.remove(cur_user_name_file)
		ret, output = commands.getstatusoutput(rmtmpcmd)
		if 0 != ret:	
			self.create_err_msgDialog(output)
			print "error 11", output 
		return
	
	def auto_set_apply(self, __widget):
		"""modify /etc/init/server.conf if server status change"""
		
		for i in range(0, self.servercount):
			isactive = self.genser_switchlist[i].get_active()
			servername = "".join(self.servernamelist[i].split())
			serconfpath = "/etc/init/" + servername + ".conf"
			print "apply serconfpath is ", serconfpath
			tempfile = "/tmp/" + servername + ".conf.tmp"
			#if True == isactive and (0 == cmp(self.sercur_statu[i], "0")):
			status = "".join(self.sercur_statu[i].split())
			#if 0 == cmp("1", status):
			if True == isactive and 0 == cmp("0", status):
				apply_cmd = "sed 's/^#start on/start on/g' " + serconfpath + " >" + tempfile + "; mv -f " + tempfile + " " + serconfpath# + ";"
				print "apply_cmd ", apply_cmd
				#ret = os.system(apply_cmd)
				ret, output = commands.getstatusoutput(apply_cmd)
				#if command return err, don't modify state
				if 0 == ret:
					self.sercur_statu[i] = "1"
				else:
					self.create_err_msgDialog(output)
					print "error 11", output 
					break
				#if 0 == ret:
				#	mvfilename = "mv /tmp/conf.tmp " + serconfpath
				#	os.system(mvfilename)
			if False == isactive and 0 == cmp("1", status):
				apply_cmd = "sed 's/^start on/#start on/g' " + serconfpath + " > " + tempfile +  "; mv -f " + tempfile + " " + serconfpath# + ";"
				#ret = os.system(apply_cmd)
				ret, output = commands.getstatusoutput(apply_cmd)
				if 0 == ret:
					self.sercur_statu[i] = "0"
				else:
					self.create_err_msgDialog(output)
					print "error 22", output
					break
				#if 0 == ret:
				#	mvfilename = "mv /tmp/conf.tmp " + serconfpath
				#	os.system(mvfilename)
		print "auto_set_apply status is ", self.sercur_statu
		self.set_switch_button()
		#sed "s/start on/#start on/g" ssh.conf  > ssh.conf.tmp
		return 
    
	def create_err_msgDialog(self, format):
		self.errdialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR,  Gtk.ButtonsType.CLOSE, format)
		self.errdialog.connect("response", self.err_msgbox_response)
		self.errdialog.run()
		return 
	
	def create_waring_msgDialog(self, format):
		self.waringdlg = Gtk.MessageDialog(None, 0, Gtk.MessageType.WARNING,  Gtk.ButtonsType.CLOSE, format)
		self.waringdlg.connect("response", self.waring_msgbox_response)
		self.waringdlg.run()
		return 
		
	def err_msgbox_response(self, __widget, response_id):
		
		if response_id == Gtk.ButtonsType.CLOSE:
			print "dialog closed "
		self.errdialog.destroy()
		return
	
	def waring_msgbox_response(self, __widget, response_id):
		if response_id == Gtk.ButtonsType.CLOSE:
			print "waring dlg closed"
		self.waringdlg.destroy()
		return 
		
	def create_sertable(self):
		"""create server table for """
		
		auto_serinfobox = Gtk.VBox()
		#info_label = Gtk.Label(SYSTEM_AUTO_SERVER_INFO)
		info_label = Gtk.Label("")
		auto_serinfobox.pack_start(info_label, False, False, 0)
		self.vbox.pack_start(auto_serinfobox, False, False, 0)
		if 0 == self.autoisdraw:
			t_hbox = []
			self.genser_switchlist = []
			self.genser_labellist = []
			for i in range(0, self.servercount):
				print "server count is ",self.servercount
				print "i is ", i 
				
				t_hbox.append(Gtk.HBox())
				self.genser_switchlist.append(Gtk.Switch())
				t_sername = "".join(self.servernamelist[i].split()) + SERVER				
				print "t_sername is ", t_sername
				self.genser_labellist.append(Gtk.Label(t_sername))
				t_hbox[i].pack_start(self.genser_switchlist[i], False, False, 2)
				t_hbox[i].pack_start(self.genser_labellist[i], False, False, 2)
				self.vbox.pack_start(t_hbox[i], False, False, 2)
			
			#sertable.attach_defaults(self.switch1, 0, 1, 0, 4)
			#sertable.attach_defaults(self.switch2, 1, 2, 1, 3)
			#sertable.attach_defaults(self.switch3, 1, 1, 2, 2)
			#sertable.attach_defaults(self.switch4, 1, 2, 1, 1)
			self.autoisdraw = 1
			
		return 
	
	def set_switch_button(self):
		"""set switch button on/off by server status """
		
		for i in range(0, self.servercount):
			print "status is " ,self.sercur_statu[i]
			status = "".join(self.sercur_statu[i].split())
			if 0 == cmp("1", status):
				self.genser_switchlist[i].set_active(True)
				print "genser_switchlist[i].set_active(True)"
			else:
				self.genser_switchlist[i].set_active(False)
				print "genser_switchlist[i].set_active(False)"
		return 
		
	def get_user_server_todifffile(self, savefile):
		"""get need config user server by cur system initctl list with base system initctl list """
		
		comd = "umask u=rwx,g=rwx,o=rwx; initctl list | awk '{print $1}'  > " + cur_system_serverlisttmp + "; sort " +  cur_system_serverlisttmp + " -o " + cur_system_serverlist
		if 0:
			diffcomd = "umask u=rwx,g=rwx,o=rwx;diff " + base_oembootserverlist + " " + cur_system_serverlist + "  | grep -v ^[0-9] | awk '{print $2}' > " + savefile
		else:
			diffcomd = "umask u=rwx,g=rwx,o=rwx;diff " + base_livebootserverlist + " " + cur_system_serverlist + "  | grep -v ^[0-9] | awk '{print $2}' > " + savefile
		#ret = os.system(comd)
		ret, output = commands.getstatusoutput(comd)
		if 0 == ret:
			commands.getstatusoutput(diffcomd)
			#os.system(diffcomd)
		else:
			self.create_err_msgDialog(output)
		print 'get_user_server_todifffile ret is %d ' % ret 
		return ret
	
	def get_user_server_list(self, sernamefile):
		"""get user server list from diff file"""
		
		self.servernamelist = []
		f = open(sernamefile)
		for line in f.readlines():
			self.servernamelist.append(line)
		f.close()
		print "servernamelist is ", self.servernamelist
		return
	
	def get_user_server_statu(self, servername):
		"""get user server's statu by servername, if statu is on return 1, otherwish return 0"""
		
		serconfpath = "/etc/init/" + servername + ".conf"
		print "serconfpath is ", serconfpath
		cmd_str = "umask u=rwx,g=rwx,o=rwx; cat " + serconfpath + " | grep 'start on' | grep -v '^#' | wc -l > " + status_temfile
		ret, output = commands.getstatusoutput(cmd_str)
		#ret = os.system(cmd_str)
		if 0 != ret:
			self.create_err_msgDialog(output)
			print "get_user_server_stat system exec err"
		f = open(status_temfile)
		statu = f.readline()
		f.close()
		print "get_user_server_statu:server statu is", statu 
		return statu
	
	
	def run_autoitem(self, __widget):
		"""enable/disable server of boot """
		
		ret = self.get_user_server_todifffile(server_list_tmpfile)
		time.sleep(0.3)
		if 0 == ret:
			self.get_user_server_list(server_list_tmpfile)
		#self.servercount is server count number
		self.servercount = self.servernamelist.__len__()
		self.sercur_statu = []
		for i in range(0, self.servercount):
			print "i is %d servername is %d", i, self.servernamelist[i]
			servername = "".join(self.servernamelist[i].split())
			print "servername is ", servername
			status = self.get_user_server_statu(servername)
			if SERVER_ON == status:
				self.sercur_statu.append("on")
			else:
				self.sercur_statu.append("off")
		print "servercount is ", self.servercount
		print "sercur statu is ", self.sercur_statu
		self.create_sertable()
		#self.vbox.pack_start(self.ser_table, False, False, 5)
		#self.ser_table.show_all
		self.vbox.show_all()
		return

	def run_init(self):
		"""enable/disable server of boot """
		
		ret = self.get_user_server_todifffile(server_list_tmpfile)
		if 0 == ret:
			self.get_user_server_list(server_list_tmpfile)
		#self.servercount is server count number
		self.servercount = self.servernamelist.__len__()
		self.sercur_statu = []
		for i in range(0, self.servercount):
			print "i is %d servername is %d", i, self.servernamelist[i]
			servername = "".join(self.servernamelist[i].split())
			print "servername is ", servername
			status = self.get_user_server_statu(servername)
			print "init status is ", status
			self.sercur_statu.append(status)
		print "servercount is ", self.servercount
		print "sercur statu is ", self.sercur_statu
		self.create_sertable()
		self.set_switch_button()
		#self.vbox.pack_start(self.ser_table, False, False, 5)
		#self.ser_table.show_all
		self.vbox.show_all()
		return


	def main(self):
		Gtk.main()

if __name__ == '__main__':
	gui=MyWindow(TITLE_NAME,600,400)
	gui.main() 
