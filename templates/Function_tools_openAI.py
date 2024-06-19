# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 20/mar./2024  at 15:24 $'


def getInfoForSalesContact(**kwargs):
    name = None
    email = None
    phone = None
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
    print(f"Name: {name}, Email: {email}, Phone: {phone}")
    return ["data recievend a seller will contact the client"]
