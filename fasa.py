#!/bin/python

from bs4 import BeautifulSoup as bs
import requests

def get_asa_list():
    page = requests.get("https://lists.archlinux.org/pipermail/arch-security/2018-January/thread.html")
    data = page.text
    asa_data = bs(data)
    body = asa_data.body
    complete_asa = body.findAll('li')
    print(complete_asa)


get_asa_list()
