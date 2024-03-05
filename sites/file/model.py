#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sites import db, app


class File(db.Model):
    __tablename__ = 'file'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(255), nullable=False)
    # 私密文件地址
    private_file_path = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    # 1 私密 2 公开
    private = db.Column(db.Integer, nullable=False)
    # 可查看完整文件人
    can_view_operator = db.Column(db.String(255), nullable=False)
    operator = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.String(255), nullable=False)
    update_time = db.Column(db.String(255), nullable=False)


with app.app_context():
    db.create_all()
