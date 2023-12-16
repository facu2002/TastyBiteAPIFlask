from flask import Blueprint, jsonify, request
from db_connection import get_db_connection


ranking_bp = Blueprint('ranking', __name__)



#########################################################################################################################################


@ranking_bp.route('', methods=['GET'])
def get_ranking():
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
      cursor.execute(f"SELECT * FROM ranking GROUP BY username, n_recetas ORDER BY n_recetas DESC LIMIT {numero};")
    else:
      cursor.execute("SELECT * FROM ranking GROUP BY username, n_recetas ORDER BY n_recetas DESC LIMIT 10;")
    ranking = cursor.fetchall()
    ranking = [{"username": user[0], "n_recetas": user[1]} for user in ranking]
    return jsonify(ranking), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500
  finally:
    cursor.close()
    conn.close()


