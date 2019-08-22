import models
import os
import sys
import secrets
from PIL import Image
from flask import Blueprint, request, jsonify, url_for, send_file
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user', url_prefix='/user')

@user.route('/register', methods=["POST"])
def register():
    pay_file = request.files
    payload = request.form.to_dict()
    dict_file = pay_file.to_dict()

return 'hi from register'