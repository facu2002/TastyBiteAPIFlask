from flask import Blueprint, jsonify, request
from db_connection import get_db_connection

receta_bp = Blueprint('receta', __name__)


#########################################################################################################################################

# GET /api/recetas/:receta_id

@receta_bp.route('<int:receta_id>', methods=['GET'])
def get_receta(receta_id):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Obtenemos la receta desde la tabla receta
    cursor.execute(f"SELECT * FROM receta WHERE receta_id = {receta_id}")
    receta = cursor.fetchone()
    
    # Comprobamos que la receta existe
    if receta is None:
      return jsonify({"message": "Receta no encontrada"}), 404
    
    # Obtenemos el usuario que ha creado la receta
    cursor.execute(f"SELECT username FROM receta JOIN usuario_receta ON receta.receta_id = usuario_receta.receta_id WHERE receta.receta_id = {receta_id};")
    username = cursor.fetchone()
    
    # Obtenemos los ingredientes de la receta
    cursor.execute(f"SELECT nombre, ingrediente.ingrediente_id FROM receta JOIN receta_ingrediente ON receta.receta_id = receta_ingrediente.receta_id JOIN ingrediente ON ingrediente.ingrediente_id = receta_ingrediente.ingrediente_id WHERE receta.receta_id = {receta_id};")
    ingredientes = cursor.fetchall()
    ingredientes = [{ "nombre": ingrediente[0], "ingrediente_id": ingrediente[1] } for ingrediente in ingredientes]
    
    # Obtenemos los comentarios de la receta
    cursor.execute(f"SELECT comentario.comentario_id, username, contenido FROM interaccion JOIN comentario ON comentario.comentario_id = interaccion.comentario_id WHERE receta_id = {receta_id} AND puntuacion_id IS NULL;")
    comentarios = cursor.fetchall()
    comentarios = [{ "comentario_id": comentario[0], "username": comentario[1], "contenido": comentario[2] } for comentario in comentarios] 
    
    # Obtenemos las puntuaciones de la receta
    cursor.execute(f"SELECT puntuacion.puntuacion_id, username, nota FROM interaccion JOIN puntuacion ON puntuacion.puntuacion_id = interaccion.puntuacion_id WHERE receta_id = {receta_id} AND comentario_id IS NULL;")
    puntuaciones = cursor.fetchall()
    puntuaciones = [{ "puntuacion_id": puntuacion[0], "username": puntuacion[1], "puntuacion": puntuacion[2] } for puntuacion in puntuaciones]
    
    cursor.close()
    conn.close()
 
    # Creamos el objeto receta que vamos a devolver
    receta = {
      "receta_id": receta[0],
      "titulo": receta[1],
      "categoria_id": receta[2],
      "instrucciones": receta[3],
      "tiempo": receta[4],
      "raciones": receta[5],
      "dificultad": receta[6],
      "username": username[0],
      "ingredientes": ingredientes, 
      "comentarios": comentarios,
      "puntuaciones": puntuaciones
    }
    
    return jsonify(receta), 200
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500
  

#########################################################################################################################################

# GET /api/recetas

@receta_bp.route('', methods=['GET'])
def get_recetas():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()   
    
    try:
      # Obtenemos el numero de recetas que se quieren obtener
      data = request.get_json()
    except:
      # si no se envia ningun parametro por el body de la peticion, data sera None
      data = None
    
    # Obtenemos el numero de recetas que se quieren obtener  
    numero = data.get("numero") if (data is not None) else None
    
    # Obtenemos las recetas desde la tabla receta
    if numero is not None:
      cursor.execute(f"SELECT * FROM receta LIMIT {numero};")
    else:
      # En caso de no pasar ningun parametro, se obtienen 10 recetas
      cursor.execute("SELECT * FROM receta LIMIT 10;")
    
    recetas = cursor.fetchall()
    
    recetas = [{
      "receta_id": receta[0],
      "titulo": receta[1],
      "categoria_id": receta[2],
      "instrucciones": receta[3],
      "tiempo": receta[4],
      "raciones": receta[5],
      "dificultad": receta[6]
    } for receta in recetas]
    
    return jsonify(recetas), 200
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500
  
  finally:
    cursor.close()
    conn.close()


#########################################################################################################################################

# POST /api/recetas


@receta_bp.route('', methods=['POST'])
def post_receta():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()
    
    # Realizamos la insercion de la receta en la tabla receta
    cursor.execute(f"INSERT INTO receta (titulo, categoria_id, instrucciones, tiempo, raciones, dificultad) VALUES ('{data['titulo']}', {data['categoria_id']}, '{data['instrucciones']}', {data['tiempo']}, {data['raciones']}, {data['dificultad']}) RETURNING *;")
    
    receta = cursor.fetchone()
    receta = {
      "receta_id": receta[0],
      "nombre": receta[1],
      "apellidos": receta[2],
      "descripcion_perfil": receta[3],
      "email": receta[4]
    }
    conn.commit()
    cursor.close()
    conn.close()
    
    # retonarmos el mensaje de exito y el receta creado
    return jsonify({"message": "Receta creada exitosamente", "receta": receta}), 201
  except Exception as e:
    if 'duplicate key value violates unique constraint' in str(e):
      return jsonify({"message": "La receta ya existe"}), 409
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500


#########################################################################################################################################

# PUT /api/recetas/:receta_id

@receta_bp.route('<int:receta_id>', methods=['PUT'])
def put_receta(receta_id):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
      data = request.get_json()
    except:
      # si no se envia ningun parametro por el body de la peticion
      # se retorna un error
      return jsonify({"message": "No se ha enviado ningun parametro"}), 400

    # se valida que receta_id no se pueda modificar
    if data.get("receta_id") is not None:
      return jsonify({"message": "El receta_id no puede ser modificado"}), 400

    # puede que el receta no pase todos los campos, por lo que se debe validar que campos se van a actualizar
    titulo = data.get("titulo") if (data is not None) else None
    categoria_id = data.get("categoria_id") if (data is not None) else None
    instrucciones = data.get("instrucciones") if (data is not None) else None
    tiempo = data.get("tiempo") if (data is not None) else None
    raciones = data.get("raciones") if (data is not None) else None
    dificultad = data.get("dificultad") if (data is not None) else None
    
    # realizamos la actualizacion de los campos que se hayan enviado
    if titulo is not None:
      cursor.execute(f"UPDATE receta SET titulo = '{titulo}' WHERE receta_id = {receta_id};")
    if categoria_id is not None:
      cursor.execute(f"UPDATE receta SET categoria_id = {categoria_id} WHERE receta_id = {receta_id};")
    if instrucciones is not None:
      cursor.execute(f"UPDATE receta SET instrucciones = '{instrucciones}' WHERE receta_id = {receta_id};")
    if tiempo is not None:
      cursor.execute(f"UPDATE receta SET tiempo = {tiempo} WHERE receta_id = {receta_id};")
    if raciones is not None:
      cursor.execute(f"UPDATE receta SET raciones = {raciones} WHERE receta_id = {receta_id};")
    if dificultad is not None:
      cursor.execute(f"UPDATE receta SET dificultad = {dificultad} WHERE receta_id = {receta_id};")
    
    cursor.execute(f"SELECT * FROM receta WHERE receta_id = '{receta_id}';")
    receta = cursor.fetchone()
    receta = {
      "receta_id": receta[0],
      "titulo": receta[1],
      "categoria_id": receta[2],
      "instrucciones": receta[3],
      "tiempo": receta[4],
      "raciones": receta[5],
      "dificultad": receta[6]
    }
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Receta actualizado exitosamente", "receta": receta}), 200
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500


#########################################################################################################################################

# DELETE /api/recetas/:receta_id

@receta_bp.route('<int:receta_id>', methods=['DELETE'])
def delete_receta(receta_id):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    # INSERT INTO receta (titulo, categoria_id, instrucciones, tiempo, raciones, dificultad) VALUES ('Barritas energéticas', 1, 'Mezclar todos los ingredientes en un bol. Hornear durante 50 minutos a 180 grados.', 50, 10, 4);
    
    cursor.execute(f"SELECT * FROM receta WHERE receta_id = '{receta_id}';")
    receta = cursor.fetchone()
    receta = {
      "receta_id": receta[0],
      "titulo": receta[1],
      "categoria_id": receta[2],
      "instrucciones": receta[3],
      "tiempo": receta[4],
      "raciones": receta[5],
      "dificultad": receta[6]
    }
    
    cursor.execute(f"DELETE FROM receta WHERE receta_id = '{receta_id}';")
    
    conn.commit()
    cursor.close()
    conn.close()
    if receta is None:
      return jsonify({"message": "receta no encontrado"}), 404
    return jsonify({"message": "Receta eliminada exitosamente", "receta": receta}), 200
  
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500
  
