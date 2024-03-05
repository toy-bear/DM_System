#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 数据库配置 链接地址 最大链接数等
SQLALCHEMY_ECHO = False

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/file_system'
SQLALCHEMY_POOL_RECYCLE = 5
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_SIZE = 100
# 使用session必须配置SECRET_KEY
SECRET_KEY = "TPmi4aLWRbyVq8zu9v82dWYW1"
