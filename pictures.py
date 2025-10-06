import db

def add_picture(name, description, style, user_id, file_path):
    sql = "INSERT INTO pictures (title, description, style, user_id, image_path) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [name, description, style, user_id, file_path])

def get_pictures():
    sql = "SELECT id, title, description, style, image_path FROM pictures ORDER BY id DESC"
    return db.query(sql)

def get_picture(picture_id):
    sql = """SELECT users.username,
                    pictures.id,
                    pictures.user_id,
                    pictures.title,
                    pictures.description,
                    pictures.style,
                    pictures.image_path
            FROM pictures
            JOIN users ON pictures.user_id = users.id
            WHERE pictures.id = ?"""
    result = db.query(sql, [picture_id])    

    return result[0] if result else None

def update_picture(title, description, style, user_id, file_path, picture_id):
        sql = """
            UPDATE pictures
            SET title = ?, description = ?, style = ?, image_path = ?
            WHERE id = ? AND user_id = ?
        """
        db.execute(sql, [title, description, style, file_path, picture_id, user_id])

def delete_picture(picture_id, user_id):
    sql = "DELETE FROM pictures WHERE id = ? AND user_id = ?"
    db.execute(sql, [picture_id, user_id])

def search_pictures(query_text):
    sql = """
        SELECT id, title, description, style, image_path
        FROM pictures
        WHERE title LIKE ?
        ORDER BY id DESC
    """
    return db.query(sql, [f"%{query_text}%"])