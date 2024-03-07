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

def createUser(name, username, email, password):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        INSERT INTO brishna_user (name, username, email, password)
        VALUES (%s, %s, %s)
      """, (name, username, email, password,))

      conn.commit() #save data

def changePassword(password):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        SELECT * FROM brishna_user
        UPDATE brishna_user
        SET password = %s
        WHERE username = %s
      """, (password,))

      conn.commit()