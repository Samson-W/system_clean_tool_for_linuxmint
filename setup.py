#!/usr/bin/env python

# You should have received a copy of the GNU General Public License
# along with Gufw; if not, see http://www.gnu.org/licenses for more
# information.

from DistUtilsExtra.auto import setup

# Create data files
data = [ ('share/systemtool/daemon',              ['./systemtool/daemon/GUI_systemtool.py']),
	 ('share/systemtool/daemon',              ['./systemtool/daemon/live_initctllist']),
	 ('share/systemtool/daemon',              ['./systemtool/daemon/apt_cleaner.py']),
	 ('share/systemtool/daemon',              ['./systemtool/daemon/cache_cleaner.py']),
	 ('share/systemtool/daemon',              ['./systemtool/daemon/Common.py']),
	 ('share/systemtool/daemon',              ['./systemtool/daemon/log_cleaner.py']),
	 ('share/systemtool/daemon',              ['./systemtool/daemon/system_cleaner.py']),
	 ('share/systemtool/daemon',              ['./systemtool/daemon/web_cleaner.py']),
	 ('share/systemtool/daemon',              ['./systemtool/daemon/system_optimization.png']),
	 ('share/systemtool/daemon',              ['./systemtool/daemon/system_optimization.png']),
	 ('share/systemtool/daemon',              ['./systemtool/daemon/get_cur_exec_user_to_file.py'])
       ]

# Setup stage
setup(
    name         = "system-tool",
    version      = "1.0",
    description  = "An easy, System service open / close, garbage clean-up system.!",
    author       = "",
    author_email = "",
    url          = "",
    license      = "GPL2",
    data_files   = data,
    )
