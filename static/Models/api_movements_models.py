# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 03/may./2024  at 15:33 $'

from flask_restx import fields
from static.extensions import api

movement_model = api.model('MovementAMC', {
    "id": fields.Integer(required=True, description="The movement id"),
    "id_product": fields.Integer(required=True, description="The product id"),
    "type_m": fields.String(required=True, description="The movement type"),
    "quantity": fields.Float(required=True, description="The movement quantity"),
    "movement_date": fields.String(required=True, description="The movement date", example="2024-04-03"),
    "sm_id": fields.Integer(required=True, description="The movement id"),
    "previous_q":  fields.Float(required=True, description="The previous quantity")
})

movements_output_model = api.model('MovementsOutAMC', {
    "data": fields.List(fields.Nested(movement_model)),
    "msg": fields.String(required=True, description="The message")
})

movement_insert_model = api.model('MovementInputAMC', {
    "info":  fields.Nested(movement_model),
    "id": fields.Integer(required=True, description="The movement id to modify")
})

movement_delete_model = api.model('MovementDeleteAMC', {
    "id":  fields.Integer(required=True, description="The movement id to delete")
})
