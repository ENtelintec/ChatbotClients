# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 14/may./2024  at 16:13 $'

from flask_restx import fields
from static.extensions import api


request_quizz_file_model = api.model('Employee delete all', {
    "type_q":  fields.String(required=True, description="Tipo de quizz"),
    "file": fields.F(required=True, description="Archivo de quizz")
})
