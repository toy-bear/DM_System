#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sites import db, app

class Banner(db.Model):
    __tablename__ = 'banner'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    img_path = db.Column(db.String(255), nullable=False)
    # 1 教师 2 学生
    banner_type = db.Column(db.Integer, nullable=False)
    # 100启动 -100禁用
    status=db.Column(db.Integer, nullable=False)
    create_time=db.Column(db.String(255), nullable=False)
    update_time=db.Column(db.String(255), nullable=False)


with app.app_context():
    db.create_all()

