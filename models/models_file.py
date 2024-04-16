import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
#   with conn.cursor() as cur:
#     cur.execute(
#         'SELECT * FROM users'
#     )
#     cur.fetchall()

def getUser():
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
          SELECT * 
          FROM "userAuthdb".users
          WHERE username = 'bribak'
      """)
      return cur.fetchone()

print(getUser())