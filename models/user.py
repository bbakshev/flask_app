import os
import psycopg2


def getByUsername(username):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        SELECT * FROM brishna_user
        WHERE username = %s
      """, (username,))

      return cur.fetchone()

def createUser(username, email, password, name):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        INSERT INTO brishna_user
        VALUES (%s, %s, %s, %s)
      """, (username, email, password, name,))

      conn.commit() #save data