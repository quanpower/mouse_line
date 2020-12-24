# mouse_line
mouse_line


1.
Server deployment:
$ pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

Install Python Library

$ python manage.py makemigrations

Run Django database migrate file.

$ python manage.py migrate

Confirm migrate database. Django Primordial support sqlite3 database. If you wanna change database to others. Please editor singosgu/settings.py.

Run Server:
Local Server

$ daphne -p 8008 django_wms.asgi:application

Local Server Port Customize

$ daphne -b 172.16.6.250 -p 8008 django_wms.asgi:application

If you customize the Port. The user in local area network can use 'server IP:Port' to browse the software

2.

asn.AsnListModel: (fields.E180) SQLite does not support JSONFields.

先去sqlite官网下载对应的DLL软件包https://www.sqlite.org/download.html，然后替换掉当前使用的sqlite3.dll文件。例如我的windows为64位版本，所以下载了sqlite-dll-win64-x64-3320300.zip这个软件包，本地python的安装路径为C:\python36，直接将C:\python36\DLLs\sqlite3.dll用下载的软件包里的sqlite3.dll文件替换，然后再次运行migrate顺利创建了数据库表

3.quasar

node.js
npm install yarn -g

yarn全局安装命令需要配置环境变量，将 yarn global bin 的地址配置到用户变量内

yarn global add @quasar/cli

git rm wms/db.sqlite3 --cached
