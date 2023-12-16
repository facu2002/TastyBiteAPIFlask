from flask import Blueprint, jsonify, request
from db_connection import get_db_connection

receta_bp = Blueprint('receta', __name__)

#########################################################################

@receta_bp.route('<int:receta_id>', methods=['GET'])
def get_receta(receta_id):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM receta WHERE receta_id = {receta_id}")
    receta = cursor.fetchone()
    cursor.close()
    conn.close()
    if receta is None:
      return jsonify({"message": "Receta no encontrado"}), 404    
    receta = {
      "receta_id": receta[0],
      "titulo": receta[1],
      "categoria_id": receta[2],
      "instrucciones": receta[3],
      "tiempo": receta[4],
      "raciones": receta[5],
      "dificultad": receta[6]
    }
    return jsonify(receta), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500



#########################################################################

@receta_bp.route('', methods=['GET'])
def get_recetas():
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
      cursor.execute(f"SELECT * FROM receta LIMIT {numero};")
    else:
      cursor.execute("SELECT * FROM receta LIMIT 10;")
    recetas = cursor.fetchall()
    return jsonify(recetas), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500
  finally:
    cursor.close()
    conn.close()


#########################################################################


@receta_bp.route('', methods=['POST'])
def post_receta():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()
    cursor.execute(f"INSERT INTO receta (titulo, categoria_id, instrucciones, tiempo, raciones, dificultad) VALUES ('{data['titulo']}', {data['categoria_id']}, '{data['instrucciones']}', {data['tiempo']}, {data['raciones']}, {data['dificultad']});")
    cursor.execute(f"SELECT * FROM receta WHERE receta_id = {data['receta_id']};")
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


#########################################################################


@receta_bp.route('<int:receta_id>', methods=['PUT'])
def put_receta(recipe_id):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
      data = request.get_json()
    except:
      # si no se envia ningun parametro por el body de la peticion
      # se retorna un error
      return jsonify({"message": "No se ha enviado ningun parametro"}), 400

    # se valida que el recipe_id no se pueda modificar
    if data.get("recipe_id") is not None:
      return jsonify({"message": "El recipe_id no puede ser modificado"}), 400

    # puede que el receta no pase todos los campos, por lo que se debe validar que campos se van a actualizar
    titulo = data.get("titulo") if (data is not None) else None
    categoria_id = data.get("categoria_id") if (data is not None) else None
    instrucciones = data.get("instrucciones") if (data is not None) else None
    tiempo = data.get("tiempo") if (data is not None) else None
    raciones = data.get("raciones") if (data is not None) else None
    dificultad = data.get("dificultad") if (data is not None) else None
    
    # realizamos la actualizacion de los campos que se hayan enviado
    if titulo is not None:
      cursor.execute(f"UPDATE receta SET titulo = '{titulo}' WHERE recipe_id = {recipe_id};")
    if categoria_id is not None:
      cursor.execute(f"UPDATE receta SET categoria_id = {categoria_id} WHERE recipe_id = {recipe_id};")
    if instrucciones is not None:
      cursor.execute(f"UPDATE receta SET instrucciones = '{instrucciones}' WHERE recipe_id = {recipe_id};")
    if tiempo is not None:
      cursor.execute(f"UPDATE receta SET tiempo = {tiempo} WHERE recipe_id = {recipe_id};")
    if raciones is not None:
      cursor.execute(f"UPDATE receta SET raciones = {raciones} WHERE recipe_id = {recipe_id};")
    if dificultad is not None:
      cursor.execute(f"UPDATE receta SET dificultad = {dificultad} WHERE recipe_id = {recipe_id};")
    
    cursor.execute(f"SELECT * FROM receta WHERE recipe_id = '{recipe_id}';")
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
    return jsonify(receta), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500
