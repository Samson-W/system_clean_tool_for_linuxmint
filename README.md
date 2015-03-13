system_clean_tool_for_linuxmint
===============================
This project is the use of Python language.
This project is set service to down/up, and clean system trash. but only support linuxmint now. 

Notes:
You need used "initctl list | awk '{print $1}' > live_initctllist" to modify system service table when you first use this tool.

Clean trash items:
1、Trash dir:
~/.local/share/Trash/files/*
~/.local/share/Trash/info/*

2、thumbnails dir:
~/.cache/thumbnails/firefoxmidpath/*.png

3、apt-get install cache:
/var/cache/apt/archives/*

4、firefox cache:
~/.cache/mozilla/firefox/firefoxmidpath/*

5、vim history  file:
~/.viminfo

6、bash history  file:
~/.bash_history

7、firefox cookies file:
~/.mozilla/firefox/firefoxmidpath/cookies.sqlite

8、flash cookies file:
~/.macromedia/Flash_Player/*

9、recently used file:
~/.local/share/recently-used.xbel

10、firefox history:
~/.mozilla/firefox/firefoxmidpath/places.sqlite

11、old log:
/var/log/*.log.*
var/log/*/*.gz
/var/log/*.gz


