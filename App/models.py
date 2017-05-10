# coding: utf-8
from flask import Flask, abort, request, jsonify, g, url_for, config
# from App import client
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from App import auth
from App import app
import MySQLdb
import geohash
from time import time
from datetime import datetime
import json
import functools


class User:
    username = ''
    password = ''
    usertoken = ''
    userrole = ''
    userlo = ''
    userla = ''
    usergeohash = ''
    existuser = ''

    def __init__(self, username, password):
        db = MySQLdb.connect(host="localhost", user="yhwjjkwh", passwd="zlw255151", db="jkwh", charset="utf8")
        cursor = db.cursor()
        self.username = username
        self.password = password
        sql = "SELECT * FROM user WHERE username=%s AND password = %s"
        try:
            cursor.execute(sql, (self.username, self.password))
            results = cursor.fetchone()
            if results is not None:
                self.existuser = True
                self.userrole = results[3]
                # self.usertoken = results[4]
            else:
                self.existuser = False
            cursor.close()
            db.close()
        except MySQLdb.Error:
            cursor.close()
            db.close()



    def read_usersaved(self):
        pass

    def savepoint(self, lo, la, pointid, pointname, kindof, batch, buildby, area, imgfilename):
        db = MySQLdb.connect(host="localhost", user="yhwjjkwh", passwd="zlw255151", db="jkwh", charset="utf8")
        cursor = db.cursor()
        pointhash = geohash.encode(la, lo, 9)
        sql = "INSERT INTO jklist (pointid, pointname, la, lo, geohash, kindof, batch, buildby, area) VALUES (%s," \
              "%s,%s,%s,%s,%s,%s,%s,%s)"
        sql2 = "INSERT INTO pointphotolist (pointid, photoname, addeddate) VALUES (%s,%s,%s)"
        d1 = datetime.now()
        d2 = d1.strftime('%Y-%m-%d %H:%M:%S')
        try:
            cursor.execute(sql, (pointid, pointname, la, lo, pointhash, kindof, batch, buildby, area))
            db.commit()
            for i in imgfilename:
                cursor.execute(sql2, (pointid, imgfilename[i], d2))
                db.commit()
            return {"msg": "ok"}
        except MySQLdb.Error:
            db.rollback()
            cursor.close()
            db.close()
            return {"msg": "写入数据失败"}

    def savetemppoint(self, lo, la, pointid, pointname, kindof, batch, buildby, area, imgfilename, username):
        db = MySQLdb.connect(host="localhost", user="yhwjjkwh", passwd="zlw255151", db="jkwh", charset="utf8")
        cursor = db.cursor()
        pointhash = geohash.encode(la, lo, 9)
        sql = "INSERT INTO temppointlist (pointid, pointname, la, lo, geohash, kindof, batch, buildby, area, " \
              "saveddate, pointowner) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql2 = "INSERT INTO tempphotolist (pointid, photoname, addeddate) VALUES (%s,%s,%s)"
        d1 = datetime.now()
        d2 = d1.strftime('%Y-%m-%d %H:%M:%S')
        try:
            cursor.execute(sql, (pointid, pointname, la, lo, pointhash, kindof, batch, buildby, area, d2, username))
            db.commit()
            for i in imgfilename:
                cursor.execute(sql2, (pointid, imgfilename[i], d2))
                db.commit()
            return {"msg": "ok"}
        except MySQLdb.Error:
            db.rollback()
            cursor.close()
            db.close()
            return {"msg": "写入数据失败"}

    def showusertemppointlist(self):
        db = MySQLdb.connect(host="localhost", user="yhwjjkwh", passwd="zlw255151", db="jkwh", charset="utf8")
        cursor = db.cursor()
        sql = "SELECT isadmin,realname FROM user WHERE username=%s"
        pass

    def returnaroundpoint(self, lo, la):
        pointhash = geohash.encode(la, lo, 9)
        pointhash += '%'
        db = MySQLdb.connect(host="localhost", user="yhwjjkwh", passwd="zlw255151", db="jkwh", charset="utf8")
        cursor = db.cursor()
        sql = "SELECT pointid,pointname,lo,la,kindof,batch,buildby,area FROM jklist WHERE geohash LIKE %s"
        try:
            cursor.execute(sql, (pointhash,))
            results = cursor.fetchall()
            # if results is not None:
            if bool(results) is True:
                l = list()
                i = 0
                for record in results:
                    sqldata = results[i]
                    r = {"pointid": sqldata[0], "pointname": sqldata[1], "lo": sqldata[2], "la": sqldata[3],
                         "kindof": sqldata[4], "batch": sqldata[5], "buildby": sqldata[6], "area": sqldata[7]}
                    l.append(r)
                    i += 1
            else:
                return {"result": "None"}
            cursor.close()
            db.close()
            return l
        except MySQLdb.Error:
            try:
                cursor.close()
                db.close()
            except IndexError:
                cursor.close()
                db.close()


def showuserinfo(username):
    db = MySQLdb.connect(host="localhost", user="yhwjjkwh", passwd="zlw255151", db="jkwh", charset="utf8")
    cursor = db.cursor()
    sql = "SELECT isadmin,realname FROM user WHERE username=%s"
    p = {}
    try:
        cursor.execute(sql, (username,))
        results = cursor.fetchone()
        if results is not None:
            if bool(results[0]) is True:
                p["管理员"] = 1
            else:
                p["管理员"] = 0
            p["姓名:"] = results[1]
            cursor.close()
            db.close()
            return p
        else:
            cursor.close()
            db.close()
            return {"msg": "用户不存在"}
    except MySQLdb.Error:
        cursor.close()
        db.close()
        return {"msg": "写入数据失败"}


class Point:
    geohash = ''
    pointlo = ''
    pointla = ''
    pointname = ''
    pointid = ''
    kindof = ''
    batch = ''
    buildby = ''
    area = ''
    existpoint = ''

    def __init__(self, pointid):
        self.pointid = pointid
        db = MySQLdb.connect(host="localhost", user="yhwjjkwh", passwd="zlw255151", db="jkwh", charset="utf8")
        cursor = db.cursor()
        sql = "SELECT pointname,lo,la,geohash,kindof,batch,buildby,area FROM jklist WHERE pointid=%s"
        try:
            # cursor.execute(sql)
            cursor.execute(sql, (pointid,))
            results = cursor.fetchone()
            if results is not None:
                self.existpoint = True
                self.pointname = results[0]
                self.pointlo = results[1]
                self.pointla = results[2]
                self.geohash = results[3]
                self.kindof = results[4]
                self.batch = results[5]
                self.buildby = results[6]
                self.area = results[7]
                # self.usertoken = results[4]
            else:
                self.existuser = False
            cursor.close()
            db.close()
        except MySQLdb.Error:
            cursor.close()
            db.close()

