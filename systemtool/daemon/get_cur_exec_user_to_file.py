# -*- coding: utf-8 -*-
#!/usr/bin/python
import os

cur_user_name_file="/tmp/.systemtoolcurusername"

f=open(cur_user_name_file,'w')
username=os.path.expanduser('~')
f.write(username)
f.close()

