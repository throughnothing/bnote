import sqlite3
import datetime

class Note:
  def __init__(self,id,title,body,created_str,modified_str):
    self.id = id
    self.title = title
    self.body = body
    #TODO Convert these to actual datetime objects
    self.created = created_str
    self.modified = modified_str

  def set_text(self,text):
    self.body = text


class BNoteDataStore:
  def __init__(self):
    # TODO make this use a file later on
    self.conn = sqlite3.connect(':memory:')
    self.cursor = self.conn.cursor()

    self.cursor.execute("""
      CREATE TABLE notes (
        id integer primary key,
        title text,
        body text,
        created datetime,
        modified datetime
      )"""
    );

  def __del__(self):
    self.cursor.close()
    self.conn.close()

  def search(self, search):
    print "Searching for notes matching: %s" % (search)
    #TODO use full text search obviously
    self.cursor.execute("SELECT * FROM notes WHERE title like '%" + search + "%'")
    for row in self.cursor:
      print row

  def create(self,title):
    print "Creating new note: %s" % (title)
    self.cursor.execute("INSERT INTO notes (title,created,modified) VALUES ('%s',DATETIME('NOW'),DATETIME('NOW'))" % (title))
    id = self.cursor.lastrowid
    self.cursor.execute("SELECT * FROM notes WHERE id = '%i'" % (id))
    for row in self.cursor:
      reval = Note(row[0],row[1],row[2],row[3],row[4])

    return reval
    

  def save(self,note):
    print "Updating note: %s" % (note.title)
    self.cursor.execute("REPLACE INTO notes (id,title,body,created,modified) VALUES (%i,'%s','%s','%s',DATETIME('NOW'))"
                        % (note.id, note.title, note.body, note.created))

  def get_all(self):
    pass
