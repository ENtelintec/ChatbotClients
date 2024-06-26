# -*- coding: utf-8 -*-
__author__ = "Edisson Naula"
__date__ = "$ 02/nov./2023  at 17:32 $"

from dotenv import dotenv_values
from flask_restx import Api

model_openai = "gpt-4-0613"
# local_father_path_dpb = "C:/Users/Edisson/Telintec Dropbox/SOFTWARE TELINTEC"
secrets = dotenv_values(".env")
api = Api(doc='/IA/doc')
# url_api = "http://127.0.0.1:5000/AuthAPI/api/v1/auth/loginUP"
# url_api = "https://ec2-3-144-117-149.us-east-2.compute.amazonaws.com/AuthAPI/api/v1/auth/loginUP"
# IMG_PATH_COLLAPSING = Path("./img")
client_name = "doitconsulting"
AV_avaliable_tools_files = {
    "doitconsulting": "files/tools_AV_Doit.json",
}
delta_bitacora_edit = 14
status_dic = {0: "Pendiente", 1: "En Proceso", 2: "Completado", 3: "Finalizado", -1: "Cancelado"}
format_timestamps = "%Y-%m-%d %H:%M:%S"
format_date = "%Y-%m-%d"
dict_deps = {"Dirección": 1, "Operaciones": 2, "Administración": 3, "RRHH": 4, "REPSE": 5, "IA": 6, "Otros": 7}
format_timestamps_filename = '%Y-%m-%d'
client_id = 1
client_tag = "doitconsulting"
log_path = "./"
flag_logs = True
url_endpoint_doit = 'https://gptapi.mgnit.net/api/asistente'
