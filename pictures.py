import db

def add_picture(name, description, style, classes, user_id, file_path):
    sql = "INSERT INTO pictures (title, description, style, user_id, image_path) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [name, description, style, user_id, file_path])

    picture_id = db.last_insert_id()

    for title, value in classes:
        sql = "INSERT INTO picture_classes (picture_id, title, style) VALUES (?, ?, ?)"
        db.execute(sql, [picture_id, title, value])

def get_pictures():
    sql = "SELECT id, title, description, style, image_path FROM pictures ORDER BY id DESC"
    return db.query(sql)

def get_specs(picture_id):
    sql =  """SELECT title, style FROM picture_classes WHERE picture_id =?"""
    return db.query(sql, [picture_id])
     
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

def update_picture(title, description, style, user_id, file_path, picture_id, classes):
    
    sql = "DELETE FROM picture_classes WHERE picture_id =?"
    db.execute(sql, [picture_id])

    for title, value in classes:
        sql = "INSERT INTO picture_classes (picture_id, title, style) VALUES (?, ?, ?)"
        db.execute(sql, [picture_id, title, value])        

    sql = """
        UPDATE pictures
        SET title = ?, description = ?, style = ?, image_path = ?
        WHERE id = ? AND user_id = ?
        """
    db.execute(sql, [title, description, style, file_path, picture_id, user_id])

def delete_picture(picture_id, user_id):
    sql2 = "DELETE FROM picture_classes WHERE picture_id = ?"
    db.execute(sql2, [picture_id])
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

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes