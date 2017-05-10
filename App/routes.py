# coding: utf-8
from App import app
from flask.ext.restful import Api
from App.controller import Login, GetAroundPoint, AddPoint, GetPointInfo, GetPointList, GetUserInfo, SumbitPointInfo,\
	ModifyPointInfo, ApplyPointToMaster, GetPersonalSavedPointInfo, DeletePersonalSavedPoint, AddPersonalPoint,\
	UploadImgFile


api = Api(app, default_mediatype="application/json")
api.add_resource(Login, '/v1/login')
api.add_resource(GetAroundPoint, '/v1/getaroundpoint')
api.add_resource(AddPoint, '/v1/addpoint')
api.add_resource(UploadImgFile, '/v1/uploadimgfile')
api.add_resource(GetPointInfo, '/v1/getpointinfo/<int:pointid>')
api.add_resource(GetPointList, '/v1/getpointlist')
api.add_resource(GetUserInfo, '/v1/getuserinfo/<username>')
api.add_resource(SumbitPointInfo, '/v1/sumbitpointinfo')
api.add_resource(ModifyPointInfo, '/v1/modifypointinfo')
api.add_resource(ApplyPointToMaster, '/v1/applypointtomaster')
api.add_resource(GetPersonalSavedPointInfo, '/v1/getpersonalsavedpointinfo')
api.add_resource(DeletePersonalSavedPoint, '/v1/deletepersonalsavedpoint')
api.add_resource(AddPersonalPoint, '/v1/addpersionalpoint')
# api.add_resource(Register, '/v1/reg')
