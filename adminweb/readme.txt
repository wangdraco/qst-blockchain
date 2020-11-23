1，关于自动生成代码的使用
mod_temp目录是自动生成框架文件的程序
在temp_config.json中配置完对应的参数后，就可以运行 run_template.py
成功后， 生成forms， controllers和 models文件，并在在templates目录下生成html文件
还要做最后的修改工作：
(1) 在models.py中 ，把db的引用改为 from app import db
(2) 在__init__.py中 把forms文件加进去
(3) 打开leftsidebar.html，新增加一个菜单

2,关于生成requirements.txt 文件：
(1) 在命令行执行  pip freeze > requirements.txt
(2) 在其他机器上 引入： pip install -r requirements.txt
（3）或者使用 pip install --upgrade -r requirements.txt ，
    安装最新版本的依赖包，前提是 把requirements.txt里pyzmq==18.0.2 换成pyzmq>=18.0.2
注意，安装mod-wsgi的时候， 需要先设置apache的环境变量  MOD_WSGI_APACHE_ROOTDIR="d:/apache24"

3，碰到pip安装出现error: Microsoft Visual C++ 14.0 is required. 的情况，
   可以从https://www.lfd.uci.edu/~gohlke/pythonlibs下载whl文件直接安装
   pip install  greenlet-0.4.15-cp37-cp37m-win_amd64.whl

4, 在pycharm上建立virtualenv环境
5, 在命令行进入这个虚拟环境，用activate命令激活
   从git上fetch最新版本的数据
   D:\odoo-dev\venv>git clone -b 12.0 --depth 1 --single-branch https://github.com/odoo/odoo.git
6, 下载完成后，修改requirements.txt文件（如果需要的话）,然后pip安装
  pip install -r requirements.txt -i https://pypi.douban.com/simple/ #豆瓣源安装 或https://mirrors.aliyun.com/pypi/simple/

python -m ensurepip --upgrade 把  setuptools更新到最新
