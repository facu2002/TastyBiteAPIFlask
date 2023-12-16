from flask import Blueprint, jsonify, request
from db_connection import get_db_connection


usuario_bp = Blueprint('usuario', __name__)


#########################################################################################################################################


@usuario_bp.route('<string:username>', methods=['GET']) 
def get_usuario(username):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM usuario WHERE username = '{username}';")
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    if usuario is None:
      return jsonify({"message": "Usuario no encontrado"}), 404
    usuario = {
      "username": usuario[0],
      "nombre": usuario[1],
      "apellidos": usuario[2],
      "descripcion_perfil": usuario[3],
      "email": usuario[4]
    }
    return jsonify(usuario), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500



#########################################################################################################################################


@usuario_bp.route('', methods=['GET'])
def get_usuarios():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()   
    try:
      data = request.get_json()
    except:
      # si no se envia ningun parametro por el body de la peticion, data sera None
      data = None
    numero = data.get("numero") if (data is not None) else None
    if numero is not None:
      cursor.execute(f"SELECT * FROM usuario LIMIT {numero};")
    else:
      cursor.execute("SELECT * FROM usuario LIMIT 10;")
    usuarios = cursor.fetchall()
    return jsonify(usuarios), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500
  finally:
    cursor.close()
    conn.close()


#########################################################################################################################################


# recibimos parametros por el body de la peticion
@usuario_bp.route('', methods=['POST'])
def post_usuario():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()
    cursor.execute(f"INSERT INTO usuario (username, nombre, apellidos, descripcion_perfil, email) VALUES ('{data['username']}', '{data['nombre']}', '{data['apellidos']}', '{data['descripcion_perfil']}', '{data['email']}');")
    cursor.execute(f"SELECT * FROM usuario WHERE username = '{data['username']}';")
    usuario = cursor.fetchone()
    usuario = {
      "username": usuario[0],
      "nombre": usuario[1],
      "apellidos": usuario[2],
      "descripcion_perfil": usuario[3],
      "email": usuario[4]
    }
    conn.commit()
    cursor.close()
    conn.close()
    # retonarmos el mensaje de exito y el usuario creado
    return jsonify({"message": "Usuario creado exitosamente", "usuario": usuario}), 201
  except Exception as e:
    if 'duplicate key value violates unique constraint' in str(e):
      return jsonify({"message": "El username ya existe"}), 409
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500


#########################################################################################################################################

@usuario_bp.route('<string:username>', methods=['PUT'])
def put_usuario(username):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
      data = request.get_json()
    except:
      # si no se envia ningun parametro por el body de la peticion
      # se retorna un error
      return jsonify({"message": "No se ha enviado ningun parametro"}), 400

    # se valida que el username no se pueda modificar
    if data.get("username") is not None:
      return jsonify({"message": "El username no puede ser modificado"}), 400
    
    # puede que el usuario no pase todos los campos, por lo que se debe validar que campos se van a actualizar
    nombre = data.get("nombre") if (data is not None) else None
    apellidos = data.get("apellidos") if (data is not None) else None
    descripcion_perfil = data.get("descripcion_perfil") if (data is not None) else None
    email = data.get("email") if (data is not None) else None
    
    # realizamos la actualizacion de los campos que se hayan enviado
    if nombre is not None:
      cursor.execute(f"UPDATE usuario SET nombre = '{nombre}' WHERE username = '{username}';")
    if apellidos is not None:
      cursor.execute(f"UPDATE usuario SET apellidos = '{apellidos}' WHERE username = '{username}';")
    if descripcion_perfil is not None:
      cursor.execute(f"UPDATE usuario SET descripcion_perfil = '{descripcion_perfil}' WHERE username = '{username}';")
    if email is not None:
      cursor.execute(f"UPDATE usuario SET email = '{email}' WHERE username = '{username}';")
    
    
    cursor.execute(f"SELECT * FROM usuario WHERE username = '{username}';")
    usuario = cursor.fetchone()
    usuario = {
      "username": usuario[0],
      "nombre": usuario[1],
      "apellidos": usuario[2],
      "descripcion_perfil": usuario[3],
      "email": usuario[4]
    }
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Usuario actualizado exitosamente", "usuario": usuario}), 200
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500
  
  
#########################################################################################################################################


@usuario_bp.route('<string:username>', methods=['DELETE'])
def delete_usuario(username):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * FROM usuario WHERE username = '{username}';")
    usuario = cursor.fetchone()
    usuario = {
      "username": usuario[0],
      "nombre": usuario[1],
      "apellidos": usuario[2],
      "descripcion_perfil": usuario[3],
      "email": usuario[4]
    }
    
    cursor.execute(f"DELETE FROM usuario WHERE username = '{username}';")
    
    conn.commit()
    cursor.close()
    conn.close()
    if usuario is None:
      return jsonify({"message": "Usuario no encontrado"}), 404
    return jsonify(usuario), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500
