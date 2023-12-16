import psycopg2

def get_db_connection():
  try:
    conn = psycopg2.connect(host='localhost',
        database="tastybite",
        user="postgres",
        password="12345")
  except psycopg2.Error as e:
    print("Fallo en la conexión con la base de datos", e)
    raise e
  except Exception as e:
    print("Ha ocurrido un error", e)
    raise e
  return conn