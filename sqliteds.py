from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, create_engine
from sqlalchemy.orm import mapper
import sqlite3
import datetime

engine = create_engine('sqlite:///:memory', echo=True)

metadata = MetaData()
notes_table = Table('notes', metadata,
                    Column('id', Integer, primary_key = True),
                    Column('title', String),
                    Column('body', String),
                    Column('created', DateTime),
                    Column('modified', DateTime),
                    sqlite_autoincrement = True
                   )
metadata.create_all(engine)

class Note(object):
  def __init__(self,title,body='',created='',modified=''):
    self.title = title
    self.body = body
    self.created = created
    self.modified = modified

mapper(Note, notes_table)

class BNoteDataStore:
  def search(self, search):
    print "Searching for notes matching: %s" % (search)
    #TODO use full text search obviously
    #self.cursor.execute("SELECT * FROM notes WHERE title like '%" + search + "%'")

    #results = []
    #for row in self.cursor:
      #results.append(Note(row[0],row[1],row[2],row[3],row[4]))

    #return results

  def create(self,title):
    print "Creating new note: %s" % (title)
    return Note(title)

    

  def save(self,note):
    print "Updating note: %s" % (note.title)
    #self.cursor.execute("REPLACE INTO notes (id,title,body,created,modified) VALUES (%i,'%s','%s','%s',DATETIME('NOW'))"
                        #% (note.id, note.title, note.body, note.created))

  def get_all(self):
    pass
