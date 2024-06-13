# -*- coding: utf-8 -*-
__author__ = "Edisson Naula"
__date__ = "$ 02/nov./2023  at 17:32 $"

import json

from dotenv import dotenv_values
from flask_restx import Api
from pathlib import Path

paths_dpb_folders = json.load(open("files/paths_general.json"))
local_father_path_dpb = "C:/Users/Edisson/Telintec Dropbox/SOFTWARE TELINTEC"
secrets = dotenv_values(".env")
api = Api()
# url_api = "http://127.0.0.1:5000/AuthAPI/api/v1/auth/loginUP"
url_api = "https://ec2-3-144-117-149.us-east-2.compute.amazonaws.com/AuthAPI/api/v1/auth/loginUP"
IMG_PATH_COLLAPSING = Path("./img")
ventanasApp_path = "static/ventanasAppGUI.json"
cache_file_EM_path = "files/EM_cache.pkl"
cache_file_Fichajes_path = "files/Fichajes_cache.pkl"
cache_file_Tickets_path = "files/Tickets_cache.pkl"
cache_file_Chats_path = "files/Chats_cache.pkl"
cache_file_Notificaciones_path = "files/Notificaciones_cache.pkl"
cache_file_resume_fichaje_path = "files/fichajes_resume_cache.pkl"
cache_file_emp_fichaje = "files/emp_name_ids_fichajes_cache.pkl"
files_fichaje_path = "files/files_fichaje/"
cache_oct_file_temp_path = "files/OCT_cache.csv"
cache_oct_fichaje_path = "files/contracts_cache.pkl"
filepath_settings = "files/settings.json"
filepath_recomendations = "files/recomendations.json"
quizzes_dir_path = "static/quizzes_dir.json"
quizzes_RRHH = {
    "0": {
        "name": "Encuesta de Salida", 
        "path": "files/quizz_salida.json", 
        "type": 0
    },
    "1": {
        "name": "Encuesta de Norma_035_50",
        "path": "files/quizz_norma035_50_v1.json",
        "type": 1,
    },
    "2": {
        "name": "Encuesta de Norma_035_+50",
        "path": "files/quizz_norma035_+50_v2.json",
        "type": 2,
    },
    "3": {
        "name": "Encuesta de clima laboral",
        "path": "files/quizz_clima_laboral.json",
        "type": 3,
    },
    "4": {
        "name": "Encuesta eva 360",
        "path": "files/quizz_eva_360.json",
        "type": 4,
    },
}
conversion_quizzes_path = "files/conversions_quizzes.json"
filepath_recommendations = "files/recommendations.json"
quizz_out_path = "files/quizz_out/"
log_file_bitacora_path = "files/logs/bitacora"
log_file_sm_path = "files/logs/sm"
patterns_files_fichaje = ["Fichaje", "Ternium"]
department_tools_openAI = {
    "director": "files/tools_AV_default.json",
    "rrhh": "files/tools_AV_rrhh.json",
    "administrator": "files/tools_AV_default.json",
    "almacen": "files/tools_AV_almacen.json",
    "default": "files/tools_AV_default.json",
}
tools_AV_avaliable = {
    "default": [{"type": "code_interpreter"}, {"type": "retrieval"}],
    "rrhh": [
        {"type": "code_interpreter"},
        {"type": "retrieval"},
        {
            "type": "function",
            "name": "getTotalFichajeEmployee",
            "args": ["id", "name", "date"],
        },
        {
            "type": "function",
            "name": "getActiveEmployees",
            "args": ["status", "quantity", "date"],
        },
        {"type": "function", "name": "getEmployeeInfo", "args": ["id"]},
    ],
    "almacen": [
        {"type": "code_interpreter"},
        {"type": "retrieval"},
        {"type": "function", "name": "getProductCategories", "args": ["name"]},
        {
            "type": "function",
            "name": "getProductsAlmacen",
            "args": ["name", "id", "category"],
        },
        {
            "type": "function",
            "name": "getHighStockProducts",
            "args": ["category", "quantity"],
        },
        {
            "type": "function",
            "name": "getLowStockProducts",
            "args": ["category", "quantity"],
        },
        {"type": "function", "name": "getCostumer", "args": ["name", "id"]},
        {"type": "function", "name": "getSupplier", "args": ["name", "id"]},
        {
            "type": "function",
            "name": "getOrder",
            "args": ["id", "customer", "status", "id_customer", "date"],
        },
        {
            "type": "function",
            "name": "getProductMovement",
            "args": ["type", "id", "id_p", "date"],
        },
        {"type": "function", "name": "getSupplyInventory", "args": ["name", "id"]},
        {"type": "function", "name": "getNoStockProducts", "args": ["category"]},
    ],
}
windows_names_db_frame = [
    "Empleados",
    "Clientes",
    "Departamentos",
    "Encargados",
    "Proveedores",
    "Productos",
    "Ordenes",
    "Tickets",
    "Chats",
    "O. Virtuales",
]
delta_bitacora_edit = 14
status_dic = {0: "Pendiente", 1: "En Proceso", 2: "Completado", 3: "Finalizado", -1: "Cancelado"}
format_timestamps = "%Y-%m-%d %H:%M:%S"
format_date = "%Y-%m-%d"
dict_deps = {"Dirección": 1, "Operaciones": 2, "Administración": 3, "RRHH": 4, "REPSE": 5, "IA": 6, "Otros": 7}
format_timestamps_filename = '%Y-%m-%d'
