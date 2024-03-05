#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from sites import db, app
from sites.user.model import User

with app.app_context():
    if not User.query.filter().first():
        record = User()
        record.user_name = 'admin'
        record.pass_word = '123456'
        record.user_type = 1
        record.create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.add(record)
        db.session.commit()
