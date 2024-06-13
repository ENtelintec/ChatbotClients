# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 10/may./2024  at 16:31 $'

from flask_restx import fields
from static.extensions import api


client_emp_sm_response_model = api.model('EmployeeSMResponse', {
    'data': fields.List(fields.List(fields.String)),
    'comment': fields.String(description='comment'),
    })

product_model_SM_selection = api.model('Product Data', {
    'id': fields.String(required=True, description='The product id'),
    'name': fields.String(required=True, description='The product name'),
    'udm': fields.String(required=True, description='The product unit of measure'),
    'stock':  fields.Integer(required=True, description='The product stock')
})

items_model_sm = api.model('ItemsModel', {
    'id': fields.String(required=True, description='The product id'),
    'name': fields.String(required=True, description='The product name'),
    'stock':  fields.Integer(required=True, description='The product stock'),
    'comment': fields.String(required=True, description='The product comment'),
    'quantity': fields.Float(required=True, description='The product quantity')
})
history_model_sm = api.model('HistoryModel', {
    'date': fields.String(required=True, description='The product id'),
    'user': fields.Integer(required=True, description='The product name'),
    'event': fields.String(required=True, description='The product unit of measure')
})

products_answer_model = api.model('AnswerProducts', {
    'data': fields.List(fields.Nested(product_model_SM_selection)),
    'page': fields.Integer(required=True, description='The page number send'),
    'pages': fields.Integer(required=True, description='The total number of'
                                                       ' pages with the selected limit')
})

products_request_model = api.model('ProductSearch', {
    'limit':  fields.Integer(required=True, description='The results limit', example=10),
    'page': fields.Integer(required=True, description='The output page default: 1', example=0)
})

sm_model = api.model('Material_request', {
    'id': fields.Integer(required=True, description='The id <ignored on add event>'),
    'sm_code': fields.String(required=True, description='The sm code'),
    'folio': fields.String(required=True, description='The folio'),
    'contract': fields.String(required=True, description='The contract'),
    'facility': fields.String(required=True, description='The facility'),
    'location': fields.String(required=True, description='The location'),
    'client_id': fields.Integer(required=True, description='The client id', example=1),
    'order_quotation': fields.String(required=True, description='The order or quotation'),
    'emp_id': fields.String(required=True, description='The employee id', example=1),
    'date': fields.String(required=True, description='The date'),
    'limit_date': fields.String(required=True, description='The limit date'),
    'status': fields.Integer(required=True, description='The status of the sm'),
    'history':  fields.List(fields.Nested(history_model_sm)),
    'comment': fields.String(required=True, description='The comment'),
    'items':  fields.List(fields.Nested(items_model_sm))
})

table_sm_model = api.model('TableMaterialRequest', {
    'data': fields.List(fields.Nested(sm_model)),
    'page': fields.Integer(required=True, description='The page number send'),
    'pages': fields.Integer(required=True, description='The total number of'
                                                       ' pages with the selected limit')
})

table_request_model = api.model('TableRequest', {
    'limit':  fields.Integer(required=True, description='The results limit', example=10),
    'page': fields.Integer(required=True, description='The output page default: 1', example=0)
})

sm_product_request_model = api.model('material_requestProductRequest', {
    'id': fields.Integer(required=True, description='The product id', example=1),
    'quantity': fields.Integer(required=True, description='The quantity'),
    'comment': fields.String(required=True, description='The comment')
})

sm_post_model = api.model('material_requestPost', {
    "info":  fields.Nested(sm_model),
    "items": fields.List(fields.Nested(sm_product_request_model))
})

sm_put_model = api.model('material_requestPut', {
    "info":  fields.Nested(sm_model),
    "items": fields.List(fields.Nested(sm_product_request_model)),
    "id": fields.Integer(required=True, description='The id')
})


delete_request_sm_model = api.model('DeleteRequestmaterial_request', {
    'id': fields.Integer(required=True, description='The id'),
    'sm_code': fields.String(required=True, description='The sm code')
})

new_cliente_model = api.model('NewClienteSM', {
    'name': fields.String(required=True, description='The name'),
    'address': fields.String(required=True, description='The address'),
    'phone': fields.String(required=True, description='The phone'),
    'email': fields.String(required=True, description='The email'),
    'rfc': fields.String(required=True, description='The rfc')
})

new_product_model = api.model('NewProductSM', {
    'name': fields.String(required=True, description='The name'),
    'udm': fields.String(required=True, description='The udm'),
    'supplier': fields.Float(required=True, description='The supplier'),
    'stock': fields.Integer(required=True, description='The stock'),
    'sku': fields.String(required=True, description='The sku'),
    'category':  fields.Integer(required=True, description='The category')
})

data_sm_plots = api.model('DataSMBoard', {
    'data': fields.Raw(required=False, description='The data'),
    'val_x': fields.List(fields.String, required=False, description='The x values'),
    'val_y': fields.List(fields.List(fields.Float, required=False, description='The y values')),
    'title': fields.String(required=True, description='The title'),
    'ylabel': fields.String(required=True, description='The y label'),
    'legend': fields.List(fields.String, required=True, description='The legend')
})

request_sm_plot_data_model = api.model('RequestSMPlotData', {
    'data': fields.List(fields.Nested(data_sm_plots)),
    'type': fields.String(required=True, description='The type of plot')
})


