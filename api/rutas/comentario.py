from flask import Blueprint, jsonify, request
from db_connection import get_db_connection


comentario_bp = Blueprint('comentario', __name__)



@comentario_bp.route('<int:comentario_id>', methods=['GET']) 
def get_comentario(comentario_id):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM comentario WHERE comentario_id = '{comentario_id}';")
    comentario = cursor.fetchone()
    cursor.close()
    conn.close()
    if comentario is None:
      return jsonify({"message": "comentario no encontrado"}), 404
    
    comentario = {
      "comentario_id": comentario[0],
      "fecha": comentario[1],
      "contenido": comentario[2]
    }
    return jsonify(comentario), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500


#########################################################################################################################################


@comentario_bp.route('', methods=['GET'])
def get_comentarios():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()   
    try:
      data = request.get_json()
    except:
      # si no se envia ningun parametro por el body de la peticion, data sera None
      data = None
    receta_id = data.get("receta_id") if (data is not None) else None
    if receta_id is not None:
      cursor.execute(f"SELECT * from interaccion where receta_id = {receta_id} and puntuacion_id is NULL;")
    else:
      return jsonify({"message": "No se ha enviado el id de la receta"}), 400
    comentarios = cursor.fetchall()
    # convertimos la lista de tuplas en una lista de diccionarios
        # INSERT INTO comentario(contenido) VALUES ('La receta del pastel de chocolate estaba deliciosa, muy rica en sabores.');

    comentarios = [{"comentario_id": comentario[1], "username": comentario[3], "receta_id": comentario[4]} for comentario in comentarios]
    return jsonify(comentarios), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500
  finally:
    cursor.close()
    conn.close()

#########################################################################################################################################



# recibimos parametros por el body de la peticion
@comentario_bp.route('', methods=['POST'])
def post_comentario():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()
    if data.get('username') is None:
      return jsonify({"message": "No se ha enviado el username"}), 400
    if data.get('receta_id') is None:
      return jsonify({"message": "No se ha enviado el id de la receta"}), 400
    if data.get('contenido') is None:
      return jsonify({"message": "No se ha enviado el contenido del comentario"}), 400
    

    cursor.execute(f"INSERT INTO comentario (contenido) VALUES ('{data['contenido']}') RETURNING *;")
    nuevo_comentario = cursor.fetchone()
    cursor.execute(f"INSERT INTO interaccion (comentario_id, puntuacion_id, username, receta_id) VALUES ({nuevo_comentario[0]}, null, '{data['username']}', {data['receta_id']}) RETURNING *;")
    nueva_interaccion = cursor.fetchone()
    
    comentario = {
      "comentario_id": nuevo_comentario[0],
      "fecha": nuevo_comentario[1],
      "contenido": nuevo_comentario[2],
      "username": nueva_interaccion[3],
      "receta_id": nueva_interaccion[4]
    }
    
    conn.commit()
    cursor.close()
    conn.close()
    # retonarmos el mensaje de exito y el comentario creado
    return jsonify({"message": "comentario creado exitosamente", "comentario": comentario}), 201
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500


