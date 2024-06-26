# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 20/mar./2024  at 15:24 $'

import requests

from static.extensions import url_endpoint_doit


def getInfoForSalesContact(**kwargs):
    name = None
    email = None
    phone = None
    flags = {
        "is_end": True
    }
    txt = "Info for sale contact\n"
    for k, v in kwargs.items():
        match k:
            case "name":
                name = v
            case "email":
                email = v
            case "phone":
                phone = v
            case _:
                pass
    data = {
        "name": name,
        "email": email,
        "phone": phone
    }
    response = requests.post(url_endpoint_doit, json=data)
    # print(f"Name: {name}, Email: {email}, Phone: {phone}")
    txt += f"Name: {name}, Email: {email}, Phone: {phone}"
    # print(response.text)
    txt += response.text
    from templates.Functions_Aux import write_log_file
    write_log_file(txt)
    return ["data recievend a seller will contact the client"], flags
