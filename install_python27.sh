sudo yum install epel-release -y
sudo yum install python-pip -y
sudo yum install centos-release-scl -y
sudo yum install python27 -y
sudo yum install -y gcc python-devel
export PATH=/opt/rh/python27/root/usr/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/opt/rh/python27/root/usr/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export MANPATH=/opt/rh/python27/root/usr/share/man:${MANPATH}
# For systemtap
export XDG_DATA_DIRS=/opt/rh/python27/root/usr/share:${XDG_DATA_DIRS:-/usr/local/share:/usr/share}
# For pkg-config
export PKG_CONFIG_PATH=/opt/rh/python27/root/usr/lib64/pkgconfig${PKG_CONFIG_PATH:+:${PKG_CONFIG_PATH}}
pip install --upgrade pip
pip install requests  --no-cache-dir
pip install datetime  --no-cache-dir
pip install ConfigParser --no-cache-dir
pip install pandas --no-cache-dir
pip install numpy  --no-cache-dir
pip install psutil  --no-cache-dir
pip install jsonpickle  --no-cache-dir