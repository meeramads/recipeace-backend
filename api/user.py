import models
import os
import sys
import secrets
from PIL import Image
from flask import Blueprint, request, jsonify, url_for, send_file
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('user', 'user', url_prefix='/user')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)

    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    file_path_for_avatar = os.path.join(os.getcwd(), 'static/profile_pics' + picture_name)

    output_size = (125, 175)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(file_path_for_avatar)

    return picture_name


@user.route('/register', methods=["POST"])
def register():
    print(request)
    print(type(request))
    pay_file = request.files
    payload = request.form.to_dict()
    dict_file = pay_file.to_dict()

    print(payload)
    print(dict_file)

    payload['email'].lower()

    try:
        
        models.User.get(models.User.email == payload['email'])

        return jsonify(data={}, status={"code": 401, "message": "This email is already in use"})

    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])

        file_picture_path = save_picture(dict_file['file'])
        
        payload['image'] = file_picture_path

        user = models.User.create(**payload)

        print(user, '<----- this is the new users')

        login_user(user)

        current_user.image = file_picture_path
        
        user_dict = model_to_dict(user)
        print(user_dict, 'THIS IS THE USER DICT')
        print(type(user_dict))

        del user_dict['password']

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print(payload, '< --- this is playload')
    try:
        user = models.User.get(models.User.email== payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            print(user, ' this is user')
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})

@user.route('/<id>', methods=["GET"])
def get_one_user(id):
    user_by_id = models.User.get_by_id(id)

    return jsonify(data=model_to_dict(user_by_id), status={"code": 200, "message": "Success"})

@user.route('/<id>', methods=["PUT"])
def update_user(id):
    payload = request.get_json()

    query = models.User.update(**payload).where(models.User.id == id) 
    query.execute()

    updated_user = models.User.get_by_id(id)

    return jsonify(data=model_to_dict(updated_user), status={"code": 200, "message": "Success"})

@user.route('/<id>', methods=["DELETE"])
def delete_user(id):
    query = models.User.delete().where(models.User.id == id)
    query.execute()

    return jsonify(data='resources successfully deleted', status={"code": 200, "message": "Success"})
