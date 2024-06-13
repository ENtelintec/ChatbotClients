# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 20/mar./2024  at 15:24 $'

import json

from static.extensions import tools_AV_avaliable


def getToolsForDepartment(**kwargs):
    name = None
    for k, v in kwargs.items():
        match k:
            case "name":
                name = v
            case _:
                pass
    name = name if name is not None else "default"
    if name in tools_AV_avaliable.keys():
        return tools_AV_avaliable[name]
    else:
        return []


def getProductCategories(**kwargs):
    for k, v in kwargs.items():
        match k:
            case _:
                pass
    flag, error, result, columns = get_product_categories()
    if flag:
        result.insert(0, columns)
        return result
    else:
        print(error)
        return []


def getProductsAlmacen(**kwargs):
    id_p = None
    name = None
    category = None
    for k, v in kwargs.items():
        match k:
            case "id":
                id_p = v
            case "name":
                name = v
            case "category":
                category = v
            case _:
                pass
    # fill with "" if an argument is None
    id_p = id_p if id_p is not None else "%"
    name = name if name is not None else "%"
    category = category if category is not None else "%"
    flag, error, result, columns = get_products_almacen(id_p, name, category)
    if flag:
        result.insert(0, columns)
        return result
    else:
        print(error)
        return [], columns


def getHighStockProducts(**kwargs):
    category = None
    quantity = None
    for k, v in kwargs.items():
        match k:
            case "category":
                category = v
            case "quantity":
                quantity = v
            case _:
                pass
    category = category if category is not None else "%"
    quantity = quantity if quantity is not None else 10
    flag, error, result, columns = get_high_stock_products(category=category, quantity=quantity)
    if flag:
        result.insert(0, columns)
        return result
    else:
        print(error)
        return []


def getLowStockProducts(**kwargs):
    category = None
    quantity = None
    for k, v in kwargs.items():
        match k:
            case "category":
                category = v
            case "quantity":
                quantity = v
            case _:
                pass
    category = category if category is not None else "%"
    quantity = quantity if quantity is not None else 10
    flag, error, result, columns = get_low_stock_products(category=category, quantity=quantity)
    if flag:
        result.insert(0, columns)
        return result
    else:
        print(error)
        return []


def getNoStockProducts(**kwargs):
    category = None
    for k, v in kwargs.items():
        match k:
            case "category":
                category = v
            case _:
                pass
    category = category if category is not None else "%"
    flag, error, result, columns = get_no_stock_products(category=category)
    if flag:
        result.insert(0, columns)
        return result
    else:
        print(error)
        return []


def getCostumer(**kwargs):
    name = None
    id_c = None
    for k, v in kwargs.items():
        match k:
            case "name":
                name = v
            case "id":
                id_c = v
            case _:
                pass
    name = name if name is not None else "%"
    id_c = id_c if id_c is not None else "%"
    flag, error, result, columns = get_costumers_amc(name, id_c)
    if flag:
        result.insert(0, columns)
        return result
    else:
        print(error)
        return []


def getSupplier(**kwargs):
    name = None
    id_s = None
    for k, v in kwargs.items():
        match k:
            case "name":
                name = v
            case "id":
                id_s = v
            case _:
                pass
    name = name if name is not None else "%"
    id_s = id_s if id_s is not None else "%"
    flag, error, result, columns = get_supplier_amc(name, id_s)
    if flag:
        result.insert(0, columns)
        return result
    else:
        print(error)
        return []


def getOrder(**kwargs):
    id_o = None
    name_c = None
    status = None
    id_c = None
    date = None
    for k, v in kwargs.items():
        match k:
            case "id":
                id_o = v
            case "customer":
                name_c = v
            case "status":
                status = v
            case "id_custumer":
                id_c = v
            case "date":
                date = v
            case _:
                pass
    pass
    id_o = id_o if id_o is not None else "%"
    id_c = id_c if id_c is not None and name_c is not None else None
    name_c = name_c if name_c is not None else "%"
    status = status if status is not None else "%"
    flag, error, result, columns = get_orders_amc(id_o, name_c, status, id_c, date)
    if flag:
        result.insert(0, columns)
        return result
    else:
        print(error)
        return []


def getProductMovement(**kwargs):
    type_movement = None
    id_p = None
    id_m = None
    date = None
    for k, v in kwargs.items():
        match k:
            case "type":
                type_movement = v
            case "id":
                id_m = v
            case "id_p":
                id_p = v
            case "date":
                date = v
            case _:
                pass
    type_movement = type_movement if type_movement is not None else "%"
    id_m = id_m if id_m is not None else "%"
    id_p = id_p if id_p is not None else "%"
    flag, error, result, columns = get_product_movement_amc(type_movement, id_m, id_p, date)
    if flag:
        result.insert(0, columns)
        return result
    else:
        print(error)
        return []


def getSupplyInventory(**kwargs):
    name = None
    id_s = None
    for k, v in kwargs.items():
        match k:
            case "name":
                name = v
            case "id":
                id_s = v
            case _:
                pass
    name = name if name is not None else "%"
    id_s = id_s if id_s is not None else "%"
    flag, error, result, columns = get_supply_inv_amc(name, id_s)
    if flag:
        result.insert(0, columns)
        return result
    else:
        print(error)
        return []


def getTotalFichajeEmployee(**kwargs):
    name = None
    id_e = None
    date = None
    for k, v in kwargs.items():
        match k:
            case "name":
                name = v
            case "id":
                id_e = v
            case "date":
                date = v
            case _:
                pass
    name = name if name is not None else "%"
    id_e = id_e if id_e is not None else None
    flag, error, result, columns = get_fichaje_emp_AV(name, id_e)
    if flag:
        if len(result) > 0:
            emp_id, absences_dict, lates_dict, extras_dict, primes_dict = result
            faltas, faltas_value = get_cumulative_data_fichajes_dict(json.loads(absences_dict), date=date)
            atrasos, atrasos_value = get_cumulative_data_fichajes_dict(json.loads(lates_dict), date=date)
            extras, extras_value = get_cumulative_data_fichajes_dict(json.loads(extras_dict), date=date)
            primas, primas_value = get_cumulative_data_fichajes_dict(json.loads(primes_dict), date=date)
            data = [emp_id, faltas, atrasos, atrasos_value, extras, extras_value, primas]
            data.insert(0, columns)
            return data
        else:
            return []
    else:
        print(error)
        return []


def getActiveEmployees(**kwargs):
    status = None
    quantity = None
    date = None
    for k, v in kwargs.items():
        match k:
            case "status":
                status = v
            case "quantity":
                quantity = v
            case "date":
                date = v
            case _:
                pass
    status = status if status is not None else "%"
    quantity = quantity if quantity is not None else 10
    flag, error, result, columns = get_employees_w_status(status, quantity, date)
    if flag:
        result.insert(0, columns)
        return result
    else:
        print(error)
        return []


def getEmployeeInfo(**kwargs):
    id_e = None
    for k, v in kwargs.items():
        match k:
            case "id":
                id_e = v
            case _:
                pass
    id_e = id_e if id_e is not None else None
    flag, error, result, columns = get_employee_info(id_e)
    if flag:
        result = [result]
        result.insert(0, columns)
        return result
    else:
        print(error)
        return []
