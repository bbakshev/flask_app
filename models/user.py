import os, uuid
from datetime import datetime, timezone 
import psycopg2, psycopg2.extras

psycopg2.extras.register_uuid()
timestamp = datetime.now(timezone.utc)


def getByUsername(username):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        SELECT * FROM "userAuthdb".users
        WHERE username = %s
      """, (username,))
      return cur.fetchone()

def getByEmail(email):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        SELECT user_id, is_verified
        FROM "userAuthdb".users
        WHERE email = %s
      """, (email,))
      return cur.fetchone()

def createUser(name, username, email, password, is_verified = False):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        INSERT INTO "userAuthdb".users (name, username, email, password, is_verified)
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
        INSERT INTO "userAuthdb".email_ver_uuid (email_uuid, time_stamp, user_id)
        VALUES (%s, NOW(), %s)
      """, (email_uuid, user_id,))
      conn.commit() #save data

def updateEmailUUID(user_id, new_email_uuid):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        UPDATE "userAuthdb".email_ver_uuid
        SET email_uuid = %s, time_stamp = NOW()
        WHERE user_id = %s
        """, (new_email_uuid, user_id,))
      conn.commit()

def confirmVerificationCode(token):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
          SELECT "userAuthdb".users.user_id, "userAuthdb".users.is_verified, "userAuthdb".email_ver_uuid.email_uuid, 
          FROM "userAuthdb".users
          INNER JOIN "userAuthdb".email_ver_uuid
          ON "userAuthdb".users.user_id = "userAuthdb".email_ver_uuid.user_id
          WHERE "userAuthdb".email_ver_uuid.email_uuid = %s
      """,(token,))
      return cur.fetchone()

def isVerified(user_id, verified):
  with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
    with conn.cursor() as cur:
      cur.execute("""
        UPDATE "userAuthdb".users 
        SET is_verified = %s
        WHERE user_id = %s
      """, (verified, user_id,))

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