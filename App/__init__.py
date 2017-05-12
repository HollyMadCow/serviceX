#!/usr/bin/python
# coding: utf-8

import os
from flask import Flask
# from flask.ext.pymongo import MongoClient
from flask.ext.httpauth import HTTPBasicAuth
# import MySQLdb
# from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Index,Boolean,Float
from App import config
from datetime import datetime
# from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import SQLAlchemyUserDatastore, Security

#path = os.getcwd()
# datepath = datetime.now().strftime('%Y%m%d')
# # temppath = os.path.join(os.getcwd(), datepath)
# temppath = os.path.join(os.getcwd(), 'uploads')
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app = Flask(__name__)
app.config.from_object(config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__))
# db = SQLAlchemy(app)
# client = MongoClient()
# db = MySQLdb.connect(host="localhost", user="yhwjjkwh", passwd="zlw255151", db="jkwh", charset="utf8")
# engine = create_engine("mysql://yhwjjkwh:zlw255151@localhost:3306/jkwh?charset=utf8",encoding="utf-8", echo=True)
auth = HTTPBasicAuth()
# from App.models import User#, Role, roles_users

from App.models import User
from App.routes import api

# metadata = MetaData()
# user = Table('user', metadata,
#         Column('id', Integer, primary_key=True),
#         Column('username', String(30)),
#         Column('password', String(64)),
# 		Column('isadmin',Boolean)
#     )
#
# jklist = Table('jklist',metadata,
# 			   Column('id',Integer,primary_key=True),
# 			   Column
#
# )

# # Flask-Security
# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security().init_app(app, user_datastore, register_blueprint=False)
#
# # init database data
# try:
#     # db.create_all()
#     # db.session.add(User("test1", "test1"))
#     # db.session.add(User("test2", "test2"))
#     # db.session.add(Role("admin", "管理员"))
#     # db.session.commit()
#     # db.engine.execute(roles_users.insert(), user_id=1, role_id=1)
#     # db.session.commit()
# except:
#     pass