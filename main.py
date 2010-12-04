import pygtk,gtk,os
import datetime
from sqliteds import BNoteDataStore,Note

class BNote:
  def __init__(self):
    # Initialize datastore (sqlite for now)
    self.notes = BNoteDataStore()
    self.cur_note = None
    self.filtered_notes = self.notes.get_all()

    # For detecting keyboard shortcuts
    self.ctrl_down = False

    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_default_size(500,600)
    self._setup_global_keyboard_shortcuts()

    # Search Text Box
    self.search_box = gtk.Entry()  
    self._setup_search_box_signals()


    # Main TextView for notes
    self.note_text = gtk.TextView()
    self.note_buffer = self.note_text.get_buffer();
    self.note_text.editable = True;
    self.note_text.cursor_visible = True;
    self._setup_note_signals()

    self._setup_note_list()

    # Scroll For Note Body
    self.note_scroll = gtk.ScrolledWindow()
    self.note_scroll.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
    self.note_scroll.add(self.note_text)
    
    # Scroll For Note List
    self.note_list_scroll = gtk.ScrolledWindow()
    self.note_list_scroll.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
    self.note_list_scroll.add(self.note_list_view)


    # Resizable VPaned
    vpaned = gtk.VPaned()
    vpaned.add1(self.note_list_scroll)
    vpaned.add2(self.note_scroll)
    # Set the default position of the resizer
    vpaned.set_position(160)

    # VBox for search box + VPaned
    vbox = gtk.VBox(False,0)
    vbox.pack_start(self.search_box,False,True,0) 
    vbox.pack_start(vpaned,True,True,0) 


    self.note_scroll.show()
    self.note_list_scroll.show()
    vpaned.show()
    self.note_text.show()
    self.note_list_view.show()
    self.search_box.show()
    vbox.show()
    self.window.add(vbox)
    self.window.show()

  def _update_notes_list(self):
    self.note_list_store.clear()
    if self.filtered_notes:
      i = 0
      for note in self.filtered_notes:
        if i == 0:
          print "updating buffer text for : %s" % (note.title)
          self.note_buffer.set_text(note.body)

        self.note_list_store.append([note.title,note.get_modified(),note.get_created(),i])
        i = i + 1

  def _setup_note_list(self):
    self.note_list_store = gtk.ListStore(str,str,str,int)

    self.note_list_view = gtk.TreeView(self.note_list_store)
    self.title_column = gtk.TreeViewColumn('Title')
    self.date_created_column = gtk.TreeViewColumn('Date Created')
    self.date_modified_column = gtk.TreeViewColumn('Date Modified')
    self.note_list_view.append_column(self.title_column)
    self.note_list_view.append_column(self.date_created_column)
    self.note_list_view.append_column(self.date_modified_column)

    self.cell = gtk.CellRendererText()

    self.title_column.pack_start(self.cell,True)
    self.title_column.add_attribute(self.cell,'text',0)

    self.date_modified_column.pack_start(self.cell,True)
    self.date_modified_column.add_attribute(self.cell,'text',1)

    self.date_created_column.pack_start(self.cell,True)
    self.date_created_column.add_attribute(self.cell,'text',2)
  
    self._update_notes_list()

  def _setup_global_keyboard_shortcuts(self):
    self.window.connect("key-press-event",self.global_key_press)
    self.window.connect("key-release-event",self.global_key_release)

  def global_key_press(self, widget, event):
    keyname = gtk.gdk.keyval_name(event.keyval)
    if keyname.find("Escape") == 0:
      self.search_box.set_text('')
      self.search_box.grab_focus()
    if keyname.find("Control") == 0:
      self.ctrl_down = True
    if keyname == "l" and self.ctrl_down:
      self.search_box.grab_focus()

  def global_key_release(self, widget, event):
    keyname = gtk.gdk.keyval_name(event.keyval)
    if keyname.find("Control") == 0:
      self.ctrl_down = False

  def _setup_search_box_signals(self):
    self.search_box.connect("changed",self.search_modified)
    self.search_box.connect("activate",self.search_activated)

  def search_modified(self,widget,delete_type=None,delete_count=0):
    text = self.search_box.get_text()
    if text != "":
      self.filtered_notes = self.notes.search(text)
    else:
      self.filtered_notes = self.notes.get_all()

    self._update_notes_list()

  def search_activated(self,widget):
    text = self.search_box.get_text()
    #TODO need to also check that an item isn't highlighted in the notes list
    if text != "":
      self.cur_note = self.notes.create(text)
      self.note_buffer.set_text('')
      self.note_text.grab_focus()

  def _setup_note_signals(self):
    self.note_buffer.connect("changed",self.note_modified)

  def note_modified(self,widget,delete_type=None,delete_count=0):
    s_iter = self.note_buffer.get_start_iter()
    e_iter = self.note_buffer.get_end_iter()
    text = self.note_buffer.get_text(s_iter,e_iter)
    self.cur_note.set_text(text)
    self.notes.save(self.cur_note)

  def main(self):
    gtk.main()


if __name__ == "__main__":
  bnote = BNote()
  bnote.main()
