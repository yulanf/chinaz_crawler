# 更新yum
yum update -y

# 安装chrome
echo '[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl.google.com/linux/linux_signing_key.pub' > /etc/yum.repos.d/google-chrome.repo
yum install google-chrome-stable -y


# 安装Xvfb
# yum install Xvfb -y
# yum install xorg-x11-fonts* -y

# 安装vim
yum install vim -y

# 安装git
yum install git -y

# 安装chromedriver
yum install unzip -y
wget http://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver


# 安装python依赖
yum install gcc patch libffi-devel python-devel  zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel -y

# 安装pyenv
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
source ~/.bash_profile

# 安装python3.7.4
pyenv install 3.7.4
pyenv global 3.7.4

# 安装截图相关包
pip3 install -U pip
pip3 install selenium 
pip3 install pillow
pip3 install redis
# pip3 install pyvirtualdisplay