## 使用`uv`管理项目依赖
### 安装
[详情参考uv文档](https://uv.doczh.com/getting-started/installation/)
```sh
# winget 安装（注意默认安装在C盘）
winget install uv
# or 官方提供的安装脚本
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
### 运行
```sh
cd backend
# 创建虚拟环境
uv venv
# 安装依赖项
uv pip install -e .
# 运行实例
uv run python main.py
```
## MySQL配置
### 安装(假设你使用debian系发行版)
```sh
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install mysql-server
sudo service mysql start
sudo service mysql status
sudo mysql
```
### 创建用户
```sql
-- 注意，下面正在创建一个访问域为 localhost ，拥有所有权限的账户
CREATE USER 'admin'@'localhost' IDENTIFIED BY '你的密码';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EXIT;

-- 如果是部署阶段的话1.修改访问域2.限制外部用户权限
```
### 运行sql文件
直接用navicat吧，用ssh来回传文件挺麻烦的