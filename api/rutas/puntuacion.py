from flask import Blueprint, jsonify, request
from db_connection import get_db_connection


puntuacion_bp = Blueprint('puntuacion', __name__)


#########################################################################################################################################

# GET /api/puntuaciones/:puntuacion_id

@puntuacion_bp.route('<int:puntuacion_id>', methods=['GET']) 
def get_puntuacion(puntuacion_id):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Obtenemos la puntucion con el id especificado
    cursor.execute(f"SELECT * FROM puntuacion WHERE puntuacion_id = '{puntuacion_id}';")
    puntuacion = cursor.fetchone()
    cursor.close()
    conn.close()
    
    # Comprobamos que la puntuacion existe
    if puntuacion is None:
      return jsonify({"message": "puntuacion no encontrado"}), 404
    
    # Damos formato a la puntuacion
    puntuacion = {
      "puntuacion_id": puntuacion[0],
      "fecha": puntuacion[1],
      "nota": puntuacion[2]
    }
    return jsonify(puntuacion), 200
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500
  
  
  
#########################################################################################################################################

# POST /api/puntuaciones

@puntuacion_bp.route('', methods=['POST'])
def post_puntuacion():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Comprobamos que se pasan los parámetros por el body de la petición
    try: 
      data = request.get_json()
    except:
      return jsonify({"message": "No se ha enviado ningun parametro"}), 400
    if data.get('username') is None:
      return jsonify({"message": "No se ha enviado el username"}), 400
    if data.get('receta_id') is None:
      return jsonify({"message": "No se ha enviado el id de la receta"}), 400
    if data.get('nota') is None:
      return jsonify({"message": "No se ha enviado la nota de la puntuacion"}), 400
    
    # Insertamos la puntuacion en la base de datos
    cursor.execute(f"INSERT INTO puntuacion (nota) VALUES ('{data['nota']}') RETURNING *;")
    nueva_puntuacion = cursor.fetchone()
    
    # Insertamos la interaccion en la base de datos
    cursor.execute(f"INSERT INTO interaccion (comentario_id, puntuacion_id, username, receta_id) VALUES (null, {nueva_puntuacion[0]}, '{data['username']}', {data['receta_id']}) RETURNING *;")
    nueva_interaccion = cursor.fetchone()
    
    # Damos formato a la puntuacion
    puntuacion = {
      "puntuacion_id": nueva_puntuacion[0],
      "fecha": nueva_puntuacion[1],
      "nota": nueva_puntuacion[2],
      "username": nueva_interaccion[3],
      "receta_id": nueva_interaccion[4]
    }
    
    conn.commit()
    cursor.close()
    conn.close()
    # retornamos el mensaje de exito y la puntuacion creada
    return jsonify({"message": "Puntuacion creada exitosamente", "puntuacion": puntuacion}), 201
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500


#########################################################################################################################################

# PUT /api/puntuaciones/:puntuacion_id

@puntuacion_bp.route('<int:puntuacion_id>', methods=['PUT'])
def put_puntuacion(puntuacion_id):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
      data = request.get_json()
    except:
      # si no se envia ningun parametro por el body de la peticion
      # se retorna un error
      return jsonify({"message": "No se ha enviado ningun parametro"}), 400

    # Se valida que el puntuacion_id no se pueda modificar
    if data.get("puntuacion_id") is not None:
      return jsonify({"message": "El puntuacion_id no puede ser modificado"}), 400
    
    # Puede que el usuario no pase todos los campos, por lo que se debe validar que campos se van a actualizar
    nota = data.get("nota") if (data is not None) else None
        
    # Realizamos la actualización de los campos que se hayan enviado
    if nota is not None:
      cursor.execute(f"UPDATE puntuacion SET nota = '{nota}' WHERE puntuacion_id = '{puntuacion_id}' RETURNING *;")
      puntuacion = cursor.fetchone()
      
      # Damos formato a la puntuacion
      puntuacion = {
        "puntuacion_id": puntuacion[0],
        "fecha": puntuacion[1],
        "contenido": puntuacion[2]
      }
      conn.commit()
      return jsonify({"message": "Puntuación actualizada exitosamente", "puntuacion": puntuacion}), 200
    else:
      return jsonify({"message": "No se ha enviado ningun campo para actualizar"}), 400 
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500
  finally:
    cursor.close()
    conn.close()



#########################################################################################################################################

# DELETE /api/puntuaciones/:puntuacion_id

@puntuacion_bp.route('<int:puntuacion_id>', methods=['DELETE'])
def delete_puntuacion(puntuacion_id):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()

    # Eliminamos la puntuacion de la base de datos
    cursor.execute(f"DELETE FROM puntuacion WHERE puntuacion_id = '{puntuacion_id}' RETURNING *;")
    puntuacion = cursor.fetchone()
    
    # Comprobamos que la puntuacion existe
    if puntuacion is None:
      return jsonify({"message": "Puntuación no encontrada"}), 404
    
    # Damos formato a la puntuacion
    puntuacion = {
      "puntuacion_id": puntuacion[0],
      "fecha": puntuacion[1],
      "nota": puntuacion[2]
    }
    conn.commit()
    return jsonify({"message": "Puntuación eliminada exitosamente", "puntuacion": puntuacion}), 200
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500
  
  finally:
    cursor.close()
    conn.close()
