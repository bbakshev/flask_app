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
