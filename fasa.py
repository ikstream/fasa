#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
import requests
import subprocess

def get_asa_list():
    page = requests.get("https://lists.archlinux.org/pipermail/arch-security/2018-January/thread.html")
    data = page.text
    asa_data = bs(data)
    body = asa_data.body
    complete_asa = body.findAll('li')


def get_installed_packages():
    pkgs = subprocess.run(['pacman', '-Qqs'], stdout=subprocess.PIPE)
    pkg_list = pkgs.stdout.decode('utf-8').strip().split('\n')
    return pkg_list


def get_pkg_version(pkg):
    version, number = 3, 5
    pkg_data = subprocess.run(['pacman', '-Qi', pkg], stdout=subprocess.PIPE)
    pkg_info = pkg_data.stdout.decode('utf-8').split()
    if pkg_info[version] in "Version":
        return pkg_info[number]

    i = 0
    for entry in pkg_info:
        if entry in "Version":
            return pkg_info[i + 2]
        i += 1


def compose_pkg_dict():
    pkg_dict = dict()
    pkg_list = get_installed_packages()
    for pkg in pkg_list:
        pkg_dict[pkg] = get_pkg_version(pkg)


def update_installed_pkgs():
    compose_pkg_dict()


def main():
    print("Starting Fasa")

get_asa_list()

if __name__ == "__main__":
    main()
