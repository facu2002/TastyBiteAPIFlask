from flask import Blueprint, jsonify, request
from db_connection import get_db_connection


ingrediente_bp = Blueprint('ingrediente', __name__)


#########################################################################################################################################


@ingrediente_bp.route('<int:ingrediente_id>', methods=['GET']) 
def get_ingrediente(ingrediente_id):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM ingrediente WHERE ingrediente_id = '{ingrediente_id}';")
    ingrediente = cursor.fetchone()
    
    cursor.execute(f"SELECT titulo, receta.receta_id FROM (SELECT receta_id FROM receta_ingrediente WHERE ingrediente_id = {ingrediente_id}) AS subquery JOIN receta ON receta.receta_id = subquery.receta_id;")
    recetas = cursor.fetchall()
    recetas = [{"titulo": receta[0], "receta_id": receta[1]} for receta in recetas]
    
  
    cursor.close()
    conn.close()
    if ingrediente is None:
      return jsonify({"message": "Ingrediente no encontrado"}), 404
    ingrediente = {
      "ingrediente_id": ingrediente[0],
      "nombre": ingrediente[1],
      "descripcion": ingrediente[2],
      "unidad_medida": ingrediente[3],
      "recetas": recetas
    }
    return jsonify(ingrediente), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500


#########################################################################################################################################


@ingrediente_bp.route('', methods=['GET'])
def get_ingredientes():
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
      cursor.execute(f"SELECT * FROM ingrediente LIMIT {numero};")
    else:
      cursor.execute("SELECT * FROM ingrediente LIMIT 10;")
    ingredientes = cursor.fetchall()
    return jsonify(ingredientes), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500
  finally:
    cursor.close()
    conn.close()


#########################################################################################################################################


# recibimos parametros por el body de la peticion
@ingrediente_bp.route('', methods=['POST'])
def post_ingrediente():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()
    cursor.execute(f"INSERT INTO ingrediente (nombre, descripcion, unidad_medida) VALUES ('{data['nombre']}', '{data['descripcion']}', '{data['unidad_medida']}');")
    cursor.execute(f"SELECT * FROM ingrediente WHERE nombre = '{data['nombre']}' AND descripcion = '{data['descripcion']}' AND unidad_medida = '{data['unidad_medida']}';")
    ingrediente = cursor.fetchone()
    ingrediente = {
      "ingrediente_id": ingrediente[0],
      "nombre": ingrediente[1],
      "descripcion": ingrediente[2],
      "unidad_medida": ingrediente[3]
    }
    conn.commit()
    cursor.close()
    conn.close()
    # retonarmos el mensaje de exito y el ingrediente creado
    return jsonify({"message": "Ingrediente creado exitosamente", "ingrediente": ingrediente}), 201
  except Exception as e:
    if 'duplicate key value violates unique constraint' in str(e):
      return jsonify({"message": "El ingrediente_id ya existe"}), 409
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500



#########################################################################################################################################

# @ingrediente_bp.route('<int:ingrediente_id>', methods=['PUT'])
# def put_ingrediente(ingrediente_id):
#   try:
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     try:
#       data = request.get_json()
#     except:
#       # si no se envia ningun parametro por el body de la peticion
#       # se retorna un error
#       return jsonify({"message": "No se ha enviado ningun parametro"}), 400

#     # se valida que el ingrediente_id no se pueda modificar
#     if data.get("ingrediente_id") is not None:
#       return jsonify({"message": "El ingrediente_id no puede ser modificado"}), 400
    
#     # puede que el usuario no pase todos los campos, por lo que se debe validar que campos se van a actualizar
#     nombre = data.get("nombre") if (data is not None) else None
#     descripcion = data.get("descripcion") if (data is not None) else None
#     unidad_medida = data.get("unidad_medida") if (data is not None) else None
    
#     # realizamos la actualizacion de los campos que se hayan enviado
#     if nombre is not None:
#       cursor.execute(f"UPDATE ingrediente SET nombre = '{nombre}' WHERE ingrediente_id = '{ingrediente_id}';")
#     if descripcion is not None:
#       cursor.execute(f"UPDATE ingrediente SET descripcion = '{descripcion}' WHERE ingrediente_id = '{ingrediente_id}';")
#     if unidad_medida is not None:
#       cursor.execute(f"UPDATE ingrediente SET unidad_medida = '{unidad_medida}' WHERE ingrediente_id = '{ingrediente_id}';")

    
#     cursor.execute(f"SELECT * FROM ingrediente WHERE ingrediente_id = '{ingrediente_id}';")
#     ingrediente = cursor.fetchone()
#     ingrediente = {
#       "imgrediente_id": ingrediente[0],
#       "nombre": ingrediente[1],
#       "descripcion": ingrediente[2],
#       "unidad_medida": ingrediente[3],
#     }
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return jsonify({"message": "Ingrediente actualizado exitosamente", "ingrediente": ingrediente}), 200
#   except Exception as e:
#     return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500
  

#########################################################################################################################################


# @ingrediente_bp.route('<int:ingrediente_id>', methods=['DELETE'])
# def delete_ingrediente(ingrediente_id):
#   try:
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     cursor.execute(f"SELECT * FROM ingrediente WHERE ingrediente_id = '{ingrediente_id}';")
#     ingrediente = cursor.fetchone()
#     ingrediente = {
#       "ingrediente_id": ingrediente[0],
#       "nombre": ingrediente[1],
#       "descripcion": ingrediente[2],
#       "unidad_medida": ingrediente[3]
#     }
    
#     cursor.execute(f"DELETE FROM ingrediente WHERE ingrediente_id = '{ingrediente_id}';")
    
#     conn.commit()
#     cursor.close()
#     conn.close()
#     if ingrediente is None:
#       return jsonify({"message": "Ingrediente no encontrado"}), 404
#     return jsonify(ingrediente), 200
#   except Exception as e:
#     print("Ha ocurrido un error", e)
#     return jsonify({"message": "Ha ocurrido un error"}), 500
