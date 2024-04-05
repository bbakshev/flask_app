import os, uuid
from datetime import datetime, timezone 
import psycopg2, psycopg2.extras

psycopg2.extras.register_uuid()
timestamp = datetime.now(timezone.utc)


def getByUsername(username):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        SELECT * FROM brishna_user
        WHERE username = %s
      """, (username,))

      return cur.fetchone()

def createUser(name, username, email, password, is_verified = False):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        INSERT INTO brishna_user (name, username, email, password, is_verified)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING user_id
      """, (name, username, email, password, is_verified,))
      user_id = cur.fetchone()[0]
      conn.commit() #save data
      return user_id

def createEmailUUID(email_uuid, user_id):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        INSERT INTO brishna_email_ver_uuid (email_uuid, time_stamp, user_id)
        VALUES (%s, NOW(), %s)
      """, (email_uuid, user_id,))
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