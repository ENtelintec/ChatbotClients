# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 02/nov./2023  at 17:32 $'

from flask_restx import fields
from static.extensions import api

permission_model = api.model('Permission', {
    'name': fields.String(required=True, description='The name'),
    'description': fields.String(required=True, description='The description')
    })

token_model = api.model('Token', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password or pass_key')
    })


resume_model = api.model('Resume', {
    "id": fields.Integer(required=True, description="The id"),
    "name": fields.String(required=True, description="The name"),
    "contract": fields.String(required=True, description="The contract"),
    "absences": fields.Integer(required=True, description="The absences"),
    "late": fields.Integer(required=True, description="The late"),
    "extra": fields.Integer(required=True, description="The extra"),
    "total_h_extra": fields.Integer(required=True, description="The total"),
    "primes": fields.Integer(required=True, description="The primes"),
    "absences_details": fields.String(required=True, description="The absences details"),
    "late_details": fields.String(required=True, description="The late details"),
    "extra_details": fields.String(required=True, description="The extra details"),
    "primes_details": fields.String(required=True, description="The primes details")
    })


employees_resume_model = api.model('EmployeesResume', {
    "data": fields.List(fields.Nested(resume_model)),
    })

token_info_model = api.model('TokenInfo', {
    "access_token": fields.String(required=True, description="The access token"),
    "expires_in": fields.Integer(required=True, description="The number of seconds until the token expires"),
    "timestamp": fields.String(required=True, description="The time the token was created"),
    "remaining_time": fields.String(required=True, description="The number of seconds until the token expires")
})

token_permissions_model = api.model('TokenPermissions', {
    "token": fields.String(required=True, description="The access token")
})

permissions_answer = api.model('PermissionsAnswer', {
    "permissions": fields.String(required=True, description="The permissions"),
    "username": fields.String(required=True, description="The username"),
    "error": fields.String(required=False, description="The error")
})
expected_headers_per = api.parser()
expected_headers_per.add_argument('Authorization', location='headers', required=True)

expected_headers_bot = api.parser()
expected_headers_bot.add_argument('Authorization', location='headers', required=True)


fichaje_request_model = api.model('FichajeRequest', {
    'date': fields.String(required=True, description='The date', example="2024-03-01"),
})

fichaje_add_update_request_model = api.model('Fichaje Add Request', {
    'id': fields.Integer(required=True, description='The id <ignored when adding event>'),
    'date': fields.String(required=True, description='The date', example="2024-03-01"),
    'event':  fields.String(required=True, description='The event', example="falta"),
    'value':  fields.Float(required=True, description='The value', example=1.0),
    'comment':  fields.String(required=True, description='The comment', example="This is a comment"),
    'id_emp':  fields.Integer(required=True, description='The id of the editor employee ', example=1),
    'contract':  fields.String(required=True, description='The contract of the empployee', example="INFRA")
})

fichaje_delete_request_model = api.model('Fichaje Delete Request', {
    'id': fields.Integer(required=True, description='The id'),
    'date': fields.String(required=True, description='The date', example="2024-03-01"),
    'event':  fields.String(required=True, description='The event', example="falta"),
    'id_emp':  fields.Integer(required=True, description='The id of the editor employee ', example=1),
    'contract':  fields.String(required=True, description='The contract of the empployee', example="INFRA")
})




notification_model = api.model('Notification', {
    'id':  fields.Integer(required=False, description='The id on the DB (only for answer)'),
    'title': fields.String(required=True, description='The title'),
    'msg': fields.String(required=True, description='The message of the notification'),
    'status': fields.Integer(required=True, description='The status'),
    'sender_id': fields.Integer(required=True, description='The sender id'),
    'timestamp': fields.String(required=True, description='The timestamp', example="2024-04-30 17:48:26"),
    'receiver_id': fields.Integer(required=True, description='The receiver id'),
    'app': fields.List(fields.String(required=True, description='The app'), example=["app1", "app2"])
})

notification_request_model = api.model('NotificationRequest', {
    'data':   fields.List(fields.Nested(notification_model)),
    'msg': fields.String(required=True, description='The message from the server'),
})

notification_insert_model = api.model('NotificationInputAMC', {
    "info":  fields.Nested(notification_model, description="The notification info to insert"),
    "id": fields.Integer(required=True, description="The notification id to modify, only required in update")
})

notification_delete_model = api.model('NotificationDeleteAMC', {
    "id":  fields.Integer(required=True, description="The notification id to delete")
})


response_av_model = api.model('ResponseAV', {
    'answer': fields.String(required=True, description='The message from the server'),
    'files': fields.List(fields.String(required=True, description='The files')),
    'id': fields.Integer(required=True, description='The id of the av chat'),
})

request_av_response_model = api.model('RequestAVResponse', {
    'msg': fields.String(required=True, description='The message to the server'),
    'department': fields.String(required=True, description='The department'),
    'filename': fields.String(required=True, description='The name of the file to use with the av'),
    'files': fields.List(fields.String(required=True, description='The files the av use including <filename>')),
    'id': fields.Integer(required=False, description='The id of the av chat'),
})

files_av_model = api.model('ResponseFilesAV', {
    'path': fields.String(required=True, description='The path of the file'),
    'name': fields.String(required=False, description='The name of the file'),
    'file_openai': fields.String(required=False, description='The file id of the openai'),
    'file_id': fields.String(required=False, description='The file id of the assistat'),
    'department':  fields.String(required=True, description='The department'),
    'status': fields.String(required=True, description='The status of the file')
})
response_files_av_model = api.model('ResponseFilesAV', {
    'files': fields.List(fields.Nested(files_av_model)),
})