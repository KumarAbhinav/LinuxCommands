#!linuxapp/bin/python
from flask import render_template, request, json
from app import app
import crypt
import os, sys, pwd

SUDO_PASSWORD = "RANDOM"

def getRoot():
    # If we aren't running as root, relaunch the command using sudo.

    if os.geteuid() != 0:
        print("This script requires root (super-user) permissions to run. You may be asked to enter your password.")
        os.execvp("sudo", ["sudo"] + sys.argv)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/createUser', methods=['POST'])
def createUser():
    """
    Linux user will be created
    """
    _name = request.form['inputName']

    if find_user(_name):
        return json.dumps({'message':'User already exists !'})

    if not check_valid(_name):
        return json.dumps({'message':'User can be created entered length should be less than 32 !'})

    _password = request.form['inputPassword']

    # Check if user to be created with sudo rights
    '''if _sudo:
        os.system("echo RANDOM | sudo -S adduser "+_name+" sudo ")
        return json.dumps({'message':'User created successfully !'})'''

    enc_pass = crypt.crypt(_password,"22")

    if os.getegid()!=0:
        os.system("echo "+SUDO_PASSWORD+" | sudo -S useradd -p "+enc_pass+" "+_name)

    else:
        os.system("useradd -p "+enc_pass+" "+_name)

    return json.dumps({'message':'User created successfully !'})


@app.route('/deleteUser', methods=['POST'])
def deleteUser():
    """delete the user"""

    _name = request.form['inputName']

    if not find_user(_name):
        return json.dumps({'message':'''User doesn't exists !'''})

    if os.getegid()!=0:
        os.system("echo "+SUDO_PASSWORD+" | sudo -S userdel "+_name)
    else:
        os.system("echo RANDOM | sudo -S userdel "+_name)
    return json.dumps({'message':'User deleted successfully !'})


@app.route('/modifyUser')
def modifyUser():
    """Modify User"""
    pass

def check_valid(name):
    """basic validity check for length"""
    if len(name) < 32:
        return True
    return False

def find_user(name):
    """Check if user already exists"""
    try:
        if pwd.getpwnam(name):
            return True
    except KeyError:
        return False