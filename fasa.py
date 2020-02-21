#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
from pathlib import Path
import requests
import subprocess
import re

VERSION="0.1"
HOME=str(Path.home())
CONFIG_PATH=HOME + "/.config/fasa"

def create_config_dir():
    try:
        err = subprocess.run(['mkdir', CONFIG_PATH], stdout=subpress.PIPE)
    except:
        print("Could not create {} directory".format(CONFIG_PATH))
        print("{}".format(err.stdout.decode('utf-8')))

def get_asa_list():
	try:
	    page = requests.get("https://lists.archlinux.org/pipermail/arch-security/2018-January/thread.html")
	except:
	    print("Something went wrong receiving the arch-security list")
	    return None
	reg = re.compile('\s[\w-]*:\s')
	data = page.text
	pkg = reg.findall(data)
	pkg_list = [ x.strip()[:-1] for x in pkg]
	return pkg_list


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


def print_version():
    print("Fasa version: {}".format(VERSION))


def main():
    print_version()
    print("Home:{}".format(HOME))
    print("Config path {}".format(CONFIG_PATH))
    get_asa_list()

if __name__ == "__main__":
    main()
