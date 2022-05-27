from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
# from flaskext.mysql import MySQL #pip install flask-mysql
# import pymysql
from random import sample
import os
from os import getpid
import json


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.config.from_object(__name__)
CORS(app=app, resources={r'/*': {'origins': '*'}})


# mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'testingdb'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

DIRETORIO = '\output'
# DIRETORIO = '/output'
DEBUG = True
MEMBERS = [{'id': '1', 'firstname': 'cairocoders', 'lastname': 'Ednalan', 'address': 'Olongapo city'}, {'id': '2', 'firstname': 'clydey', 'lastname': 'Ednalan', 'address': 'Angles city'}]


@app.route('/')
def index():
    app.logger.info("xxxx")
    pid = str(getpid())
    return render_template('index.html', pid=pid)


@app.route('/calendar')
def calendar():
    app.logger.info("calendar")
    return render_template('calendar.html')


@app.route('/vuejs')
def vuejs():
    app.logger.info("vuejs")
    return render_template('vuejs.html')


@app.route('/ping', methods=['GET'])
def ping_pong():
    app.logger.info("ping")
    return jsonify('pong!')


@app.route('/health', methods=['GET'])
def get():
    app.logger.info("health")
    return json.dumps({'success': True, 'message': "healthy"})


@app.route('/data')
def data():
    app.logger.info("data")
    results = sample(range(1, 10), 5)
    return jsonify({'results': results})


# @app.route('/members', methods=['GET'])
# def all_members():
#     app.logger.info("members")
#     return jsonify({'status': 'success', 'members': MEMBERS})


@app.route('/getall')
def get_all():
    # conn = mysql.connect()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    # try:
    #     cursor.execute("SELECT * from members order by id")
    #     userslist = cursor.fetchall()
    #     return jsonify({'status': 'success', 'members': userslist})
    # except Exception as e:
    #     print(e)
    # finally:
    #     cursor.close() 
    #     conn.close()
    return jsonify({'status': 'success', 'members': MEMBERS})


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    # conn = mysql.connect()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        firstname = post_data.get('firstname')
        lastname = post_data.get('lastname')
        address = post_data.get('address')
    #     sql = "INSERT INTO members(firstname,lastname,address) VALUES(%s, %s, %s)"
    #     data = (firstname, lastname, address)
    #     conn = mysql.connect()
    #     cursor = conn.cursor()
    #     cursor.execute(sql, data)
    #     conn.commit()
        MEMBERS.append({'id': len(MEMBERS) + 1, 'firstname': firstname, 'lastname': lastname, 'address': address})
        response_object['message'] = "Successfully Added"
    return jsonify(response_object)


@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    # conn = mysql.connect()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    # cursor.execute("SELECT * FROM members WHERE id = %s", [id])
    # row = cursor.fetchone() 
    row = [item for item in MEMBERS if item["id"] == id]
    return jsonify({'status': 'success', 'editmember': row[0]})


@app.route('/update', methods=['GET', 'POST'])
def update():
    # conn = mysql.connect()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        edit_id = post_data.get('edit_id')
        edit_firstname = post_data.get('edit_firstname')
        edit_lastname = post_data.get('edit_lastname')
        edit_address = post_data.get('edit_address')
        # cursor.execute ("UPDATE members SET firstname=%s, lastname=%s, address=%s WHERE id=%s",(edit_firstname, edit_lastname, edit_address, edit_id))
        # conn.commit()
        # cursor.close()
        for item in MEMBERS:
            if item["id"] == edit_id:
                item["firstname"] = edit_firstname
                item["lastname"] = edit_lastname
                item["address"] = edit_address
                break
        response_object['message'] = "Successfully Updated"
    return jsonify(response_object)


@app.route('/delete/<string:id>', methods=['GET', 'POST'])
def delete(id):
    # conn = mysql.connect()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    # cursor.execute("DELETE FROM members WHERE id = %s", [id])
    # conn.commit()
    # cursor.close()
    # MEMBERS = [item for item in MEMBERS if item["id"] != id]
    # MEMBERS = list(filter(lambda item: item['id'] != id, MEMBERS))
    for idx, item in enumerate(MEMBERS):  # enumerate(list(MEMBERS))
        if item['id'] == id:
            del MEMBERS[idx]  # MEMBERS.pop(idx)
            break
    response_object = {'status': 'success'}
    response_object['message'] = "Successfully Deleted"
    return jsonify(response_object)


@app.route("/arquivos", methods=["POST"])
def post_arquivo():
    arquivo = request.files.get("meuArquivo")
    nome_do_arquivo = arquivo.filename
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    # path = os.path.join(path, DIRETORIO) # esta dando erro # c:\output
    path = path + "\\output"
    path = os.path.join(path, nome_do_arquivo)
    arquivo.save(path)
    return '', 201


@app.route("/arquivos", methods=["GET"])
def lista_arquivos():
    arquivos = []
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    # path = os.path.join(path, DIRETORIO)  # esta dando erro # c:\output
    path = path + "\\output"
    for nome_do_arquivo in os.listdir(path):
        endereco_do_arquivo = os.path.join(path, nome_do_arquivo)
        if(os.path.isfile(endereco_do_arquivo)):
            arquivos.append(nome_do_arquivo)
    return jsonify(arquivos)


@app.route("/arquivos/<nome_do_arquivo>",  methods=["GET"])
def get_arquivo(nome_do_arquivo):
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    # path = os.path.join(path, DIRETORIO) # esta dando erro # c:\output
    path = path + "\\output"
    return send_from_directory(path, nome_do_arquivo, as_attachment=True)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True, threaded=True)


# python -m pip install --upgrade flask
# python main.py
