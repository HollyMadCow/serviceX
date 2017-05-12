# -*- coding:utf-8 -*-
from flask import request, jsonify, abort, url_for
from flask.ext.restful import Resource, reqparse
from passlib.apps import custom_app_context as pwd_context
# from App import client
from flask.ext.security import auth_token_required, roles_required, login_user
from .models import User, Point, showuserinfo
import MySQLdb
import json
from App import auth
from App import app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
ALLOWED_EXTENSIONS = set(['png', 'JPG', 'jpg', 'jpeg', 'gif'])


def verify_user(username, password):
	db = MySQLdb.connect(host="localhost", user="yhwjjkwh", passwd="zlw255151", db="jkwh", charset="utf8")
	cursor = db.cursor()
	sql = "SELECT * FROM user WHERE username=%s AND password = %s"
	cursor.execute(sql, (username, password))
	results = cursor.fetchone()
	if results is not None:

		db.close()
		return True
	else:
		db.close()
		return False


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class Login(Resource):
	def post(self):
		username = request.authorization.get('username')
		password = request.authorization.get('password')
		# username = request.form.get('username')
		# password = request.form.get('password')
		user = User(username, password)
		if user.existuser is True:
			return jsonify({"userrole": user.userrole, "usertoken": user.usertoken})
		else:
			return jsonify({"msg": "登录失败"})
			# return {'Login Info': "Failed Login"}


class GetAroundPoint(Resource):
	def get(self):
		if request.authorization is None:
			return {"msg": "Worng User Infomation!"}
		else:
			username = request.authorization.get('username')
			password = request.authorization.get('password')
			if verify_user(username, password) is True:
				user = User(username, password)
				lo = float(request.args.get('lo'))
				la = float(request.args.get('la'))
				return user.returnaroundpoint(lo, la)
			else:
				return {"msg": "用户名密码错误!"}


class AddPoint(Resource):
	def post(self):
		if request.authorization is None:
			return {"msg": "用户名密码错误!"}
		else:
			username = request.authorization.get('username')
			password = request.authorization.get('password')
			if verify_user(username, password) is True:
				user = User(username, password)
				if bool(user.userrole) is True:
					lo = float(request.form.get('lo', '0.000000'))
					la = float(request.form.get('la', '0.000000'))
					pointname = request.form.get('pointname')
					pointid = int(request.form.get('pointid'))
					kindof = request.form.get('kindof')
					batch = request.form.get('batch', '未知')
					buildby = request.form.get('buildby', '未知')
					area = request.form.get('area')
					imagefilename = eval(request.form.get('imgfilename'))
					if pointname is not None and pointid is not None and kindof is not None and area is not None:
						return user.savepoint(lo, la, pointid, pointname, kindof, batch, buildby, area, imagefilename)
				else:
					return {"msg": "无此权限"}
			else:
				return {"msg": "用户名密码错误!"}


class UploadImgFile(Resource):
	def post(self):
		photolist = {}
		for key in request.files:
			file = request.files[key]
			if file and allowed_file(file.filename):
				try:
					if os.path.exists(app.config['UPLOAD_FOLDER']) is False:
						os.makedirs(app.config['UPLOAD_FOLDER'])
					tempfilename = file.filename
					tempfilename = "." + tempfilename.split(".")[-1]
					filename = datetime.now().strftime("%Y%m%d%H%M%S%f") + tempfilename
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					photolist[key] = filename
				except IOError as err:
					return {"msg": "图片保存失败!"}
			else:
				return {"msg": "请上传图片文件!"}
		return photolist
		# file = request.files['imgfile1']
		# if file and allowed_file(file.filename):
		# 	try:
		# 		tempfilename = file.filename
		# 		tempfilename = "." + tempfilename.split(".")[-1]
		# 		filename = datetime.now().strftime("%Y%m%d%H%M%S%f") + tempfilename
		# 		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		# 		return {"msg": "ok"}
		# 	except IOError as err:
		# 			return {"msg": "图片保存失败!"}
		# else:
		# 	return {"msg": "请上传图片文件!"}


class GetPointInfo(Resource):
	def get(self, pointid):
		if request.authorization is None:
			return {"msg": "用户名密码错误!"}
		else:
			username = request.authorization.get('username')
			password = request.authorization.get('password')
			if verify_user(username, password) is True:
				point = Point(pointid)
				if point.existpoint is True:
					return {"poingid": point.pointid, "lo": point.pointlo, "la": point.pointla, "pointname": point.pointname,
												"kindof": point.kindof, "batch": point.batch, "buildby": point.buildby,
												"area": point.area}
				else:
					return {"msg": "无效点位编号"}
			else:
				return {"msg": "用户名密码错误!"}


class GetPointList(Resource):
	def get(self):
		pass


class GetUserInfo(Resource):
	def get(self, username):
		if request.authorization is None:
			return {"msg": "用户名密码错误!"}
		else:
			username1 = request.authorization.get('username')
			password1 = request.authorization.get('password')
			if verify_user(username1, password1) is True:
				user = User(username1, password1)
				if bool(user.userrole) is True:
					return showuserinfo(username)
				elif username == username1:
					return showuserinfo(username)
				else:
					return {"msg": "无此权限"}
			else:
				return {"msg": "用户名密码错误!"}


class SumbitPointInfo(Resource):
	def post(self):
		pass


class ModifyPointInfo(Resource):
	def put(self):
		pass


class ApplyPointToMaster(Resource):
	def put(self):
		pass


class GetPersonalSavedPointInfo(Resource):
	def get(self):
		pass


class GetPersonalSavedPointList(Resource):
	def get(self):
		if request.authorization is None:
			return {"msg": "用户名密码错误!"}
		else:
			username = request.authorization.get('username')
			password = request.authorization.get('password')
			if verify_user(username, password) is True:
				user = User(username, password)
				return user.showusertemppointlist()
			else:
				return {"msg": "用户名密码错误!"}


class DeletePersonalSavedPoint(Resource):
	def delete(self):
		pass


class AddPersonalPoint(Resource):
	def post(self):
		if request.authorization is None:
			return {"msg": "用户名密码错误!"}
		else:
			username = request.authorization.get('username')
			password = request.authorization.get('password')
			if verify_user(username, password) is True:
				user = User(username, password)
				if bool(user.userrole) is True:
					lo = float(request.form.get('lo', '0.000000'))
					la = float(request.form.get('la', '0.000000'))
					pointname = request.form.get('pointname')
					pointid = int(request.form.get('pointid'))
					kindof = request.form.get('kindof')
					batch = request.form.get('batch', '未知')
					buildby = request.form.get('buildby', '未知')
					area = request.form.get('area')
					imagefilename = eval(request.form.get('imgfilename'))
					if pointname is not None and pointid is not None and kindof is not None and area is not None:
						return user.savetemppoint(lo, la, pointid, pointname, kindof, batch, buildby, area, imagefilename, username)
				else:
					return {"msg": "无此权限"}
			else:
				return {"msg": "用户名密码错误!"}




