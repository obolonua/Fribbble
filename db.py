import sqlite3
import db
from flask import g

def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

def last_insert_id():
    return g.last_insert_id    
    
def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result

def add_picture(name, description, style, user_id, file_path):
    sql = "INSERT INTO pictures (title, description, style, user_id, image_path) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [name, description, style, user_id, file_path])

def get_pictures():
    sql = "SELECT id, title, description, style, image_path FROM pictures ORDER BY id DESC"
    return db.query(sql)

def get_picture(picture_id):
    sql = """SELECT pictures.id,
                    pictures.user_id,
                    pictures.title,
                    pictures.description,
                    pictures.style,
                    pictures.image_path
            FROM pictures 
            WHERE pictures.id = ?"""
    result = db.query(sql, [picture_id])    

    return result[0] if result else None

def update_picture(title, description, style, user_id, file_path, picture_id):
        sql = """
            UPDATE pictures
            SET title = ?, description = ?, style = ?, image_path = ?
            WHERE id = ? AND user_id = ?
        """
        execute(sql, [title, description, style, file_path, picture_id, user_id])

def delete_picture(picture_id, user_id):
    sql = "DELETE FROM pictures WHERE id = ? AND user_id = ?"
    execute(sql, [picture_id, user_id])

def search_pictures(query_text):
    sql = """
        SELECT id, title, description, style, image_path
        FROM pictures
        WHERE title LIKE ?
        ORDER BY id DESC
    """
    return query(sql, [f"%{query_text}%"])