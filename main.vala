using Gtk;

public class BNote : Window {

  private TextView text_view;
  private Entry search_box;
  private TreeView note_list;

  public BNote () {
    this.title = "bNote";
    this.position = WindowPosition.CENTER;
    set_default_size (500, 600);

    this.text_view = new TextView ();
    this.text_view.editable = true;
    this.text_view.cursor_visible = true;

    this.search_box = new Entry();
    this.note_list = new TreeView();

    setup_search_box_signals();
    setup_treeview();

    var note_scroll = new ScrolledWindow (null, null);
    note_scroll.set_policy (PolicyType.AUTOMATIC, PolicyType.AUTOMATIC);
    note_scroll.add (this.text_view);
    
    var note_list_scroll = new ScrolledWindow (null, null);
    note_list_scroll.set_policy (PolicyType.AUTOMATIC, PolicyType.AUTOMATIC);
    note_list_scroll.add (this.note_list);

    var paned = new VPaned();
    paned.pack1(note_list_scroll,true,false);
    paned.pack2(note_scroll,true,false);
    paned.set_position(150);
  
    var vbox = new VBox (false, 0);
    vbox.pack_start (this.search_box, false, true, 0);
    vbox.pack_start (paned, true, true, 0);
    add (vbox);

  }

  private void setup_search_box_signals(){

  }

  private void setup_treeview () {
    var listmodel = new ListStore (4, typeof (string), typeof (string),
        typeof (string), typeof (string));
    note_list.set_model (listmodel);

    note_list.insert_column_with_attributes (-1, "Title", new CellRendererText (), "text", 0);
    note_list.insert_column_with_attributes (-1, "Date Added", new CellRendererText (), "text", 1);

    var cell = new CellRendererText ();
    cell.set ("foreground_set", true);

    TreeIter iter;
    listmodel.append (out iter);
    listmodel.set (iter, 0, "Blah Blah", 1, "Today at 10PM");

    listmodel.append (out iter);
    listmodel.set (iter, 0, "Note Test", 1, "Today at 9PM");
    listmodel.append (out iter);
    listmodel.set (iter, 0, "Note Test", 1, "Today at 8PM");
  } 

  public static int main (string[] args) {
    Gtk.init (ref args);

    var window = new BNote ();
    window.destroy.connect (Gtk.main_quit);
    window.show_all ();

    Gtk.main ();
    return 0;
  }
}
