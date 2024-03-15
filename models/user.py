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

def createUser(name, username, email, password, token, is_verified = False):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        INSERT INTO brishna_user (name, username, email, password, secret_code, is_verified)
        VALUES (%s, %s, %s, %s, %s, %s)
      """, (name, username, email, password, token, is_verified,))

      conn.commit() #save data

def getVerificationCode(token):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
          SELECT * FROM brishna_user
          WHERE secret_code = %s
      """, (token,))

      return cur.fetchone()
    
def isVerified(username, verified):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        UPDATE brishna_user 
        SET is_verified = %s
        WHERE username = %s
      """, (verified, username,))

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