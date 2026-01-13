#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import xml.etree.ElementTree as ET
import os
import uuid
from datetime import datetime
import shutil
import tempfile
import subprocess  # Added for launching processes

class EntityCRUDApp:
    def __init__(self):
        self.entities_file = './entities_description.xml'
        self.data_dir = './data'
        self.entities = {}

        # Create directories if they don't exist
        os.makedirs(self.data_dir, exist_ok=True)

        # Initialize XML file if it doesn't exist
        if not os.path.exists(self.entities_file):
            self.create_default_entities_file()

        # Load data first
        self.load_xml_data()

        # Initialize UI
        self.init_ui()

        # Render tabs after UI is initialized
        self.render_xml_data_state()

        # Show the window
        self.window.show_all()

    def create_default_entities_file(self):
        """Create a default entities XML file if it doesn't exist"""
        root = ET.Element('entities')
        tree = ET.ElementTree(root)
        tree.write(self.entities_file, encoding='utf-8', xml_declaration=True)

    def load_xml_data(self):
        """Load all data from XML files (entities_description.xml and data files)"""
        # Load entity definitions
        self.load_entities()

        # Load entity records data
        self.load_all_entity_data()

    def load_entities(self):
        """Load entity definitions from XML file"""
        try:
            tree = ET.parse(self.entities_file)
            root = tree.getroot()
            self.entities = {}

            for entity_elem in root.findall('entity'):
                entity_name = entity_elem.find('entity_name').text
                entity_data = {'fields': []}

                fields_elem = entity_elem.find('entity_fields')
                if fields_elem is not None:
                    for field_elem in fields_elem.findall('entity_field'):
                        field_name = field_elem.find('field_name').text
                        field_type = field_elem.find('field_type').text
                        entity_data['fields'].append({
                            'name': field_name,
                            'type': field_type
                        })

                self.entities[entity_name] = entity_data
        except Exception as e:
            print(f"Error loading entities: {e}")
            self.entities = {}

    def load_all_entity_data(self):
        """Load data for all entities from their XML files"""
        for entity_name in self.entities.keys():
            self.load_entity_data_from_files(entity_name)

    def load_entity_data_from_files(self, entity_name):
        """Load data for a specific entity from XML files (luassg format)"""
        entity_dir = os.path.join(self.data_dir, entity_name)
        if not os.path.exists(entity_dir):
            os.makedirs(entity_dir, exist_ok=True)
            self.entities[entity_name]['records'] = {}
            return

        records = {}
        # Get all XML files in entity directory
        for filename in os.listdir(entity_dir):
            if filename.endswith('.xml'):
                # Check if filename matches pattern: entity-id.xml
                # Remove .xml extension
                basename = filename[:-4]
                if '-' in basename:
                    file_entity_name, file_record_id = basename.split('-', 1)

                    # Only process files for this entity
                    if file_entity_name == entity_name:
                        filepath = os.path.join(entity_dir, filename)
                        try:
                            tree = ET.parse(filepath)
                            root = tree.getroot()

                            # Verify root element matches entity name
                            if root.tag != entity_name:
                                print(f"Warning: Root element '{root.tag}' doesn't match entity name '{entity_name}' in {filename}")
                                continue

                            # Extract ID from root element's id attribute (luassg format)
                            record_id = root.get('id')
                            if not record_id:
                                # Use the ID from filename as fallback
                                record_id = file_record_id
                                print(f"Warning: No id attribute found in {filename}, using filename ID: {record_id}")

                            # Extract field values
                            record_data = {'id': record_id}
                            for field in self.entities[entity_name]['fields']:
                                field_name = field['name']
                                field_elem = root.find(field_name)
                                record_data[field_name] = field_elem.text if field_elem is not None else ''

                            records[record_id] = record_data
                        except Exception as e:
                            print(f"Error loading {filepath}: {e}")

        self.entities[entity_name]['records'] = records

    def save_entities_to_xml(self):
        """Save entities to XML file"""
        root = ET.Element('entities')

        for entity_name, entity_data in self.entities.items():
            entity_elem = ET.SubElement(root, 'entity')

            # Entity name
            ET.SubElement(entity_elem, 'entity_name').text = entity_name

            # Entity fields
            fields_elem = ET.SubElement(entity_elem, 'entity_fields')
            for field in entity_data['fields']:
                field_elem = ET.SubElement(fields_elem, 'entity_field')
                ET.SubElement(field_elem, 'field_name').text = field['name']
                ET.SubElement(field_elem, 'field_type').text = field['type']

        # Format XML with indentation
        self.indent_xml(root)
        tree = ET.ElementTree(root)
        tree.write(self.entities_file, encoding='utf-8', xml_declaration=True)

    def init_ui(self):
        """Initialize the main UI components (window, notebook)"""
        # Create main window
        self.window = Gtk.Window(title="Entity CRUD Application")

        # Set window to 96% of screen width and 85% of screen height
        screen = Gdk.Screen.get_default()
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        window_width = int(screen_width * 0.96)
        window_height = int(screen_height * 0.85)

        self.window.set_default_size(window_width, window_height)

        # Center the window on screen
        self.window.set_position(Gtk.WindowPosition.CENTER)

        self.window.connect("destroy", Gtk.main_quit)

        # Connect window resize event to update table column widths
        self.window.connect("check-resize", self.on_window_resize)

        # Create main vertical box
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.window.add(main_vbox)

        # Create menu bar
        self.create_menu_bar()
        main_vbox.pack_start(self.menu_bar, False, False, 0)

        # Create notebook for tabs
        self.notebook = Gtk.Notebook()
        main_vbox.pack_start(self.notebook, True, True, 0)

    def create_menu_bar(self):
        """Create the main menu bar"""
        self.menu_bar = Gtk.MenuBar()

        # Configuration menu
        config_menu_item = Gtk.MenuItem(label="Configuration")
        self.menu_bar.append(config_menu_item)

        # Configuration submenu
        config_menu = Gtk.Menu()
        config_menu_item.set_submenu(config_menu)

        # Open CONST.xml menu item
        const_menu_item = Gtk.MenuItem(label="Open ./data/CONST.xml")
        const_menu_item.connect("activate", self.on_open_const_xml)
        config_menu.append(const_menu_item)

        # Open pagination.xml menu item
        pagination_menu_item = Gtk.MenuItem(label="Open ./data/pagination.xml")
        pagination_menu_item.connect("activate", self.on_open_pagination_xml)
        config_menu.append(pagination_menu_item)

    def on_window_resize(self, widget):
        """Handle window resize to update table column widths"""
        # Update column widths for all entity tabs
        for entity_name in self.entities.keys():
            self.update_table_column_widths(entity_name)

    def update_table_column_widths(self, entity_name):
        """Update column widths for a specific entity table"""
        if entity_name not in self.entities:
            return

        treeview = self.entities[entity_name].get('treeview')
        scrolled_window = self.entities[entity_name].get('scrolled_window')

        if not treeview or not scrolled_window:
            return

        # Get current allocation of the scrolled window
        allocation = scrolled_window.get_allocation()
        table_width = allocation.width

        # Calculate equal width for each column
        columns = treeview.get_columns()
        if columns and table_width > 0:
            # Calculate equal width for each column
            column_count = len(columns)
            equal_width = table_width / column_count

            # Set each column to equal width
            for column in columns:
                column.set_fixed_width(int(equal_width))
                column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)

    def on_open_const_xml(self, menu_item):
        """Handle opening CONST.xml in the XML tree editor"""
        const_file = os.path.join(self.data_dir, "CONST.xml")
        self.open_xml_in_editor(const_file)

    def on_open_pagination_xml(self, menu_item):
        """Handle opening pagination.xml in the XML tree editor"""
        pagination_file = os.path.join(self.data_dir, "pagination.xml")
        self.open_xml_in_editor(pagination_file)

    def open_xml_in_editor(self, xml_file_path):
        """Launch the XML tree editor as a new process"""
        # Check if the XML file exists
        if not os.path.exists(xml_file_path):
            # Create the file if it doesn't exist
            try:
                # Create a minimal XML structure
                root = ET.Element('root')
                tree = ET.ElementTree(root)
                # Ensure the directory exists
                os.makedirs(os.path.dirname(xml_file_path), exist_ok=True)
                tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)
                print(f"Created missing XML file: {xml_file_path}")
            except Exception as e:
                self.show_message(f"Failed to create XML file {xml_file_path}: {str(e)}", Gtk.MessageType.ERROR)
                return

        # Get the path to dialog_xml_tree_editor.py
        # Assuming it's in the same directory as app.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        editor_script = os.path.join(script_dir, "dialog_xml_tree_editor.py")

        # Check if the editor script exists
        if not os.path.exists(editor_script):
            self.show_message(f"XML tree editor not found: {editor_script}", Gtk.MessageType.ERROR)
            return

        try:
            # Launch the editor as a new process
            # Using python3 explicitly to ensure compatibility
            subprocess.Popen(['python3', editor_script, xml_file_path])
            print(f"Launched XML editor for: {xml_file_path}")
        except Exception as e:
            self.show_message(f"Failed to launch XML editor: {str(e)}", Gtk.MessageType.ERROR)

    def render_xml_data_state(self):
        """Clear UI and render tabs according to XML data content"""
        # Check if notebook exists and is attached to window
        if self.notebook and self.notebook.get_parent():
            # Clear all existing tabs from notebook only
            while self.notebook.get_n_pages() > 0:
                self.notebook.remove_page(0)

        # Create entity tabs
        for entity_name in self.entities.keys():
            self.create_entity_tab(entity_name)

        # Always create management tab as the last tab
        self.create_management_tab()

        # Force UI update
        if self.window:
            self.window.queue_draw()

    def create_entity_tab(self, entity_name):
        """Create a tab for a specific entity with filtering capability"""
        # Create main container box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_start(10)
        main_box.set_margin_end(10)
        main_box.set_margin_top(5)
        main_box.set_margin_bottom(5)

        # Create scrolled window for the table (98% width of parent)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        # Set initial size to 98% of parent width
        scrolled_window.set_size_request(-1, -1)  # Will be dynamically adjusted

        # Create filter controls container using Grid for precise control
        filter_grid = Gtk.Grid()
        filter_grid.set_column_spacing(5)
        filter_grid.set_row_spacing(5)
        main_box.pack_start(filter_grid, False, False, 0)

        # Get current window width for percentage calculations
        window_width = self.window.get_allocation().width

        # Filter label - 11% width
        filter_label = Gtk.Label(label="Filter by:")
        filter_label.set_halign(Gtk.Align.END)
        filter_label.set_hexpand(False)

        # Create a fixed width container for the label
        label_box = Gtk.Box()
        label_box.pack_start(filter_label, True, True, 0)
        filter_grid.attach(label_box, 0, 0, 1, 1)

        # Set width request for 11% of window width
        label_width = int(window_width * 0.11)
        label_box.set_size_request(label_width, -1)

        # Field selection dropdown - 15% width
        field_combo = Gtk.ComboBoxText()

        # Add "ID" as first option
        field_combo.append_text("ID")

        # Add all field names
        for field in self.entities[entity_name]['fields']:
            field_combo.append_text(field['name'])

        # Set default selection to ID
        field_combo.set_active(0)
        field_combo.set_hexpand(False)

        # Create a fixed width container for the dropdown
        combo_box = Gtk.Box()
        combo_box.pack_start(field_combo, True, True, 0)
        filter_grid.attach_next_to(combo_box, label_box, Gtk.PositionType.RIGHT, 1, 1)

        # Set width request for 15% of window width
        combo_width = int(window_width * 0.15)
        combo_box.set_size_request(combo_width, -1)

        # Filter entry - fills remaining space
        filter_entry = Gtk.Entry()
        filter_entry.set_placeholder_text("Enter filter text...")
        filter_entry.set_hexpand(True)
        filter_grid.attach_next_to(filter_entry, combo_box, Gtk.PositionType.RIGHT, 1, 1)

        # Clear filter button (fixed width)
        clear_filter_btn = Gtk.Button(label="Clear")
        clear_filter_btn.connect("clicked", self.on_clear_filter, entity_name)
        clear_filter_btn.set_hexpand(False)
        filter_grid.attach_next_to(clear_filter_btn, filter_entry, Gtk.PositionType.RIGHT, 1, 1)

        # Set fixed width for clear button
        clear_filter_btn.set_size_request(80, -1)

        # Create buttons for CRUD operations
        button_box = Gtk.Box(spacing=10)
        main_box.pack_start(button_box, False, False, 0)

        new_button = Gtk.Button(label="New Record")
        new_button.connect("clicked", self.on_new_record, entity_name)
        button_box.pack_start(new_button, False, False, 0)

        edit_button = Gtk.Button(label="Edit Record")
        edit_button.connect("clicked", self.on_edit_record, entity_name)
        button_box.pack_start(edit_button, False, False, 0)

        delete_button = Gtk.Button(label="Delete Record")
        delete_button.connect("clicked", self.on_delete_record, entity_name)
        button_box.pack_start(delete_button, False, False, 0)

        refresh_button = Gtk.Button(label="Refresh")
        refresh_button.connect("clicked", self.on_refresh_entity, entity_name)
        button_box.pack_start(refresh_button, False, False, 0)

        # Create tree view
        treeview = Gtk.TreeView()
        scrolled_window.add(treeview)

        # Connect double-click event
        treeview.connect("row-activated", self.on_row_double_click, entity_name)

        # Create list store
        columns = ['ID']
        for field in self.entities[entity_name]['fields']:
            columns.append(field['name'])

        types = [str] * len(columns)
        list_store = Gtk.ListStore(*types)

        # Create tree model filter for filtering
        filter_model = list_store.filter_new()
        filter_model.set_visible_func(self.filter_function, (entity_name, field_combo, filter_entry))
        treeview.set_model(filter_model)

        # Create columns (initial widths will be set by update_table_column_widths)
        for i, column_name in enumerate(columns):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_name, renderer, text=i)
            column.set_resizable(True)
            column.set_expand(False)  # Don't expand, use fixed width
            column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            treeview.append_column(column)

        # Pack the scrolled window (with table) into main box
        main_box.pack_start(scrolled_window, True, True, 0)

        # Store UI references
        self.entities[entity_name]['treeview'] = treeview
        self.entities[entity_name]['list_store'] = list_store
        self.entities[entity_name]['filter_model'] = filter_model
        self.entities[entity_name]['field_combo'] = field_combo
        self.entities[entity_name]['filter_entry'] = filter_entry
        self.entities[entity_name]['columns'] = columns
        self.entities[entity_name]['tab_widget'] = main_box
        self.entities[entity_name]['scrolled_window'] = scrolled_window

        # Connect filter entry changes
        filter_entry.connect('changed', self.on_filter_changed, entity_name)
        field_combo.connect('changed', self.on_filter_changed, entity_name)

        # Connect size allocate to adjust column widths
        scrolled_window.connect("size-allocate", self.on_table_size_allocate, entity_name)

        # Connect filter controls to adjust their widths on resize
        label_box.connect("size-allocate", self.on_filter_control_resize, entity_name, "label")
        combo_box.connect("size-allocate", self.on_filter_control_resize, entity_name, "combo")

        # Populate data
        self.populate_entity_tab_data(entity_name)

        # Initial column width update
        GLib.idle_add(self.update_table_column_widths, entity_name)

        # Add tab to notebook if it exists
        if self.notebook:
            label = Gtk.Label(label=entity_name)
            self.notebook.append_page(main_box, label)

    def on_row_double_click(self, treeview, path, column, entity_name):
        """Handle double-click on table row to open edit dialog"""
        # Get the selected row from the filter model
        filter_model = treeview.get_model()
        treeiter = filter_model.get_iter(path)

        if treeiter is not None:
            # Get the record ID from the filtered model
            record_id = filter_model[treeiter][0]

            # Open edit dialog
            dialog = RecordDialog(self, entity_name, record_id)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                self.save_record(entity_name, dialog.get_data())
                # Reload data and refresh UI
                self.load_entity_data_from_files(entity_name)
                self.populate_entity_tab_data(entity_name)
            dialog.destroy()

    def on_filter_control_resize(self, widget, allocation, entity_name, control_type):
        """Update filter control widths when window is resized"""
        if not self.window:
            return

        window_width = self.window.get_allocation().width
        if window_width <= 0:
            return

        if control_type == "label":
            # Update label width to 11% of window
            new_width = int(window_width * 0.11)
            widget.set_size_request(new_width, -1)
        elif control_type == "combo":
            # Update combo width to 15% of window
            new_width = int(window_width * 0.15)
            widget.set_size_request(new_width, -1)

    def on_table_size_allocate(self, widget, allocation, entity_name):
        """Adjust column widths when table size changes"""
        self.update_table_column_widths(entity_name)

    def filter_function(self, model, treeiter, data):
        """Filter function for TreeModelFilter"""
        entity_name, field_combo, filter_entry = data

        # Get filter text
        filter_text = filter_entry.get_text().strip().lower()

        # If filter is empty, show all records
        if not filter_text:
            return True

        # Get selected field
        field_name = field_combo.get_active_text()

        # Find the column index for the selected field
        columns = self.entities[entity_name]['columns']
        if field_name == "ID":
            col_index = 0  # ID is first column
        else:
            try:
                col_index = columns.index(field_name)
            except ValueError:
                # Field not found, show all
                return True

        # Get the value from the model
        value = model[treeiter][col_index]
        if value is None:
            return False

        # Check if filter text is contained in the value (case-insensitive)
        return filter_text in value.lower()

    def on_filter_changed(self, widget, entity_name):
        """Handle filter changes"""
        if entity_name in self.entities and 'filter_model' in self.entities[entity_name]:
            self.entities[entity_name]['filter_model'].refilter()

    def on_clear_filter(self, button, entity_name):
        """Clear the filter for a specific entity"""
        if entity_name in self.entities and 'filter_entry' in self.entities[entity_name]:
            self.entities[entity_name]['filter_entry'].set_text("")
            # Set dropdown back to ID
            if 'field_combo' in self.entities[entity_name]:
                self.entities[entity_name]['field_combo'].set_active(0)

    def populate_entity_tab_data(self, entity_name):
        """Populate the entity tab with data from memory"""
        if 'list_store' not in self.entities[entity_name]:
            return

        list_store = self.entities[entity_name]['list_store']
        list_store.clear()

        records = self.entities[entity_name].get('records', {})
        for record_id, record_data in records.items():
            row_data = [record_id]
            for field in self.entities[entity_name]['fields']:
                field_name = field['name']
                row_data.append(record_data.get(field_name, ''))
            list_store.append(row_data)

    def create_management_tab(self):
        """Create the management tab for entities"""
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        scrolled_window.add(vbox)

        # Create buttons
        button_box = Gtk.Box(spacing=10)
        vbox.pack_start(button_box, False, False, 0)

        new_entity_button = Gtk.Button(label="New Entity")
        new_entity_button.connect("clicked", self.on_new_entity)
        button_box.pack_start(new_entity_button, False, False, 0)

        edit_entity_button = Gtk.Button(label="Edit Entity")
        edit_entity_button.connect("clicked", self.on_edit_entity)
        button_box.pack_start(edit_entity_button, False, False, 0)

        delete_entity_button = Gtk.Button(label="Delete Entity")
        delete_entity_button.connect("clicked", self.on_delete_entity)
        button_box.pack_start(delete_entity_button, False, False, 0)

        refresh_button = Gtk.Button(label="Refresh All")
        refresh_button.connect("clicked", self.on_refresh_all)
        button_box.pack_start(refresh_button, False, False, 0)

        # Create tree view for entities
        self.entity_list_store = Gtk.ListStore(str, str)  # Entity name, Field count
        treeview = Gtk.TreeView(model=self.entity_list_store)
        vbox.pack_start(treeview, True, True, 0)

        # Create columns
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Entity Name", renderer, text=0)
        column.set_resizable(True)
        column.set_min_width(200)
        treeview.append_column(column)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Field Count", renderer, text=1)
        column.set_resizable(True)
        column.set_min_width(100)
        treeview.append_column(column)

        self.management_treeview = treeview

        # Populate entity list
        self.populate_management_tab_data()

        # Add tab to notebook if it exists
        if self.notebook:
            label = Gtk.Label(label="Entity Management")
            self.notebook.append_page(scrolled_window, label)

    def populate_management_tab_data(self):
        """Populate the management tab with entity list"""
        if not hasattr(self, 'entity_list_store') or self.entity_list_store is None:
            return

        self.entity_list_store.clear()
        for entity_name, entity_data in self.entities.items():
            field_count = len(entity_data['fields'])
            self.entity_list_store.append([entity_name, str(field_count)])

    def indent_xml(self, elem, level=0):
        """Helper function to format XML with indentation"""
        indent = "\n" + level * "\t"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = indent + "\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
            for child in elem:
                self.indent_xml(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = indent
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = indent

    def on_new_record(self, button, entity_name):
        """Handle new record creation"""
        dialog = RecordDialog(self, entity_name, None)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.save_record(entity_name, dialog.get_data())
            # Reload data and refresh UI
            self.load_entity_data_from_files(entity_name)
            self.populate_entity_tab_data(entity_name)
        dialog.destroy()

    def on_edit_record(self, button, entity_name):
        """Handle record editing"""
        if entity_name not in self.entities or 'treeview' not in self.entities[entity_name]:
            return

        treeview = self.entities[entity_name]['treeview']
        selection = treeview.get_selection()
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            # Get the record ID from the filtered model
            record_id = model[treeiter][0]
            dialog = RecordDialog(self, entity_name, record_id)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                self.save_record(entity_name, dialog.get_data())
                # Reload data and refresh UI
                self.load_entity_data_from_files(entity_name)
                self.populate_entity_tab_data(entity_name)
            dialog.destroy()
        else:
            self.show_message("Please select a record to edit", Gtk.MessageType.WARNING)

    def on_delete_record(self, button, entity_name):
        """Handle record deletion"""
        if entity_name not in self.entities or 'treeview' not in self.entities[entity_name]:
            return

        treeview = self.entities[entity_name]['treeview']
        selection = treeview.get_selection()
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            # Get the record ID from the filtered model
            record_id = model[treeiter][0]

            dialog = Gtk.MessageDialog(
                transient_for=self.window,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text=f"Delete record '{record_id}'?"
            )
            response = dialog.run()

            if response == Gtk.ResponseType.YES:
                self.delete_record(entity_name, record_id)
                # Reload data and refresh UI
                self.load_entity_data_from_files(entity_name)
                self.populate_entity_tab_data(entity_name)

            dialog.destroy()
        else:
            self.show_message("Please select a record to delete", Gtk.MessageType.WARNING)

    def on_refresh_entity(self, button, entity_name):
        """Refresh specific entity data"""
        # Reload data from files
        self.load_entity_data_from_files(entity_name)
        # Refresh UI
        self.populate_entity_tab_data(entity_name)

    def on_new_entity(self, button):
        """Handle new entity creation"""
        dialog = EntityDialog(self, None)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            entity_name, fields = dialog.get_data()
            if entity_name and entity_name not in self.entities:
                # Add to entities
                self.entities[entity_name] = {
                    'fields': fields,
                    'records': {}
                }
                # Save to XML
                self.save_entities_to_xml()
                # Re-render UI tabs only
                self.render_xml_data_state()
                # Show the updated window
                if self.window:
                    self.window.show_all()
        dialog.destroy()

    def on_edit_entity(self, button):
        """Handle entity editing"""
        if not hasattr(self, 'management_treeview') or self.management_treeview is None:
            return

        selection = self.management_treeview.get_selection()
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            entity_name = model[treeiter][0]
            old_entity_name = entity_name

            dialog = EntityDialog(self, entity_name)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                new_entity_name, new_fields = dialog.get_data()

                # Check if entity name changed
                if old_entity_name != new_entity_name:
                    # Rename directory
                    old_dir = os.path.join(self.data_dir, old_entity_name)
                    new_dir = os.path.join(self.data_dir, new_entity_name)
                    if os.path.exists(old_dir) and not os.path.exists(new_dir):
                        os.rename(old_dir, new_dir)

                        # Rename all files in the directory
                        if os.path.exists(new_dir):
                            for filename in os.listdir(new_dir):
                                if filename.startswith(f"{old_entity_name}-"):
                                    new_filename = filename.replace(f"{old_entity_name}-", f"{new_entity_name}-", 1)
                                    old_path = os.path.join(new_dir, filename)
                                    new_path = os.path.join(new_dir, new_filename)
                                    os.rename(old_path, new_path)

                # Update entity in memory
                # Preserve existing records if fields are compatible
                existing_records = self.entities[old_entity_name].get('records', {}) if old_entity_name in self.entities else {}

                if old_entity_name != new_entity_name:
                    del self.entities[old_entity_name]

                self.entities[new_entity_name] = {
                    'fields': new_fields,
                    'records': existing_records  # Keep existing records
                }

                # Save to XML
                self.save_entities_to_xml()
                # Re-render UI tabs only
                self.render_xml_data_state()
                # Show the updated window
                if self.window:
                    self.window.show_all()

            dialog.destroy()
        else:
            self.show_message("Please select an entity to edit", Gtk.MessageType.WARNING)

    def on_delete_entity(self, button):
        """Handle entity deletion"""
        if not hasattr(self, 'management_treeview') or self.management_treeview is None:
            return

        selection = self.management_treeview.get_selection()
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            entity_name = model[treeiter][0]

            dialog = Gtk.MessageDialog(
                transient_for=self.window,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text=f"Delete entity '{entity_name}' and all its data?"
            )
            response = dialog.run()

            if response == Gtk.ResponseType.YES:
                # Delete entity directory
                entity_dir = os.path.join(self.data_dir, entity_name)
                if os.path.exists(entity_dir):
                    shutil.rmtree(entity_dir)

                # Remove entity from memory
                del self.entities[entity_name]

                # Save to XML
                self.save_entities_to_xml()
                # Re-render UI tabs only
                self.render_xml_data_state()
                # Show the updated window
                if self.window:
                    self.window.show_all()

            dialog.destroy()
        else:
            self.show_message("Please select an entity to delete", Gtk.MessageType.WARNING)

    def on_refresh_all(self, button):
        """Refresh all data - reload from XML and re-render UI"""
        self.load_xml_data()
        self.render_xml_data_state()
        # Show the updated window
        if self.window:
            self.window.show_all()

    def save_record(self, entity_name, data):
        """Save a record to XML file in luassg compatible format"""
        entity_dir = os.path.join(self.data_dir, entity_name)
        os.makedirs(entity_dir, exist_ok=True)

        record_id = data.get('id', str(uuid.uuid4()))
        filename = f"{entity_name}-{record_id}.xml"
        filepath = os.path.join(entity_dir, filename)

        # Create root element with entity name and id attribute (luassg format)
        # Example: <product id="firstProduct">
        root = ET.Element(entity_name)
        root.set('id', record_id)

        # Add field elements as children
        # Example: <name>Product 1</name>
        for field_name, field_value in data.items():
            if field_name != 'id':
                field_elem = ET.SubElement(root, field_name)
                field_elem.text = field_value or ''

        # Format XML with indentation
        self.indent_xml(root)
        tree = ET.ElementTree(root)

        # Write with proper declaration
        tree.write(filepath, encoding='utf-8', xml_declaration=True)

        # Update in-memory data
        if 'records' not in self.entities[entity_name]:
            self.entities[entity_name]['records'] = {}
        self.entities[entity_name]['records'][record_id] = data

    def delete_record(self, entity_name, record_id):
        """Delete a record file"""
        entity_dir = os.path.join(self.data_dir, entity_name)
        filename = f"{entity_name}-{record_id}.xml"
        filepath = os.path.join(entity_dir, filename)

        if os.path.exists(filepath):
            os.remove(filepath)

        # Update in-memory data
        if 'records' in self.entities[entity_name] and record_id in self.entities[entity_name]['records']:
            del self.entities[entity_name]['records'][record_id]

    def get_record_data(self, entity_name, record_id):
        """Get data for a specific record from memory"""
        if entity_name not in self.entities:
            return None

        if 'records' in self.entities[entity_name] and record_id in self.entities[entity_name]['records']:
            return self.entities[entity_name]['records'][record_id]

        # Fallback to loading from file
        entity_dir = os.path.join(self.data_dir, entity_name)
        filename = f"{entity_name}-{record_id}.xml"
        filepath = os.path.join(entity_dir, filename)

        if os.path.exists(filepath):
            try:
                tree = ET.parse(filepath)
                root = tree.getroot()

                # Get id from attribute (luassg format)
                data = {'id': root.get('id', record_id)}

                # Get field values
                for field in self.entities[entity_name]['fields']:
                    field_name = field['name']
                    field_elem = root.find(field_name)
                    data[field_name] = field_elem.text if field_elem is not None else ''

                # Store in memory for future use
                if 'records' not in self.entities[entity_name]:
                    self.entities[entity_name]['records'] = {}
                self.entities[entity_name]['records'][record_id] = data

                return data
            except Exception as e:
                print(f"Error loading record from {filepath}: {e}")
                return None
        return None

    def show_message(self, message, message_type=Gtk.MessageType.INFO):
        """Show a message dialog"""
        if not hasattr(self, 'window') or self.window is None:
            return

        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=message_type,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()


class RecordDialog(Gtk.Dialog):
    def __init__(self, parent, entity_name, record_id=None):
        title = "New Record" if record_id is None else "Edit Record"
        super().__init__(title=title, transient_for=parent.window, flags=0)

        self.entity_name = entity_name
        self.record_id = record_id
        self.parent = parent
        self.fields = {}

        self.set_default_size(400, 300)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.init_ui()

        if record_id:
            self.load_data()

    def init_ui(self):
        area = self.get_content_area()
        area.set_spacing(10)

        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(10)
        self.grid.set_row_spacing(10)
        area.add(self.grid)

        row = 0
        for field in self.parent.entities[self.entity_name]['fields']:
            field_name = field['name']
            field_type = field['type']

            label = Gtk.Label(label=field_name + ":")
            label.set_halign(Gtk.Align.END)
            self.grid.attach(label, 0, row, 1, 1)

            if field_type == 'multiline':
                scrolled_window = Gtk.ScrolledWindow()
                scrolled_window.set_hexpand(True)
                scrolled_window.set_vexpand(True)
                scrolled_window.set_min_content_height(100)

                textview = Gtk.TextView()
                textview.set_wrap_mode(Gtk.WrapMode.WORD)
                scrolled_window.add(textview)

                self.grid.attach(scrolled_window, 1, row, 1, 1)
                self.fields[field_name] = textview
            else:  # oneline
                entry = Gtk.Entry()
                entry.set_hexpand(True)
                self.grid.attach(entry, 1, row, 1, 1)
                self.fields[field_name] = entry

            row += 1

        self.show_all()

    def load_data(self):
        if self.record_id:
            data = self.parent.get_record_data(self.entity_name, self.record_id)
            if data:
                for field_name, widget in self.fields.items():
                    if field_name in data:
                        value = data[field_name] or ''
                        if isinstance(widget, Gtk.TextView):
                            buffer = widget.get_buffer()
                            buffer.set_text(value)
                        else:  # Gtk.Entry
                            widget.set_text(value)

    def get_data(self):
        data = {}
        if self.record_id:
            data['id'] = self.record_id

        for field_name, widget in self.fields.items():
            if isinstance(widget, Gtk.TextView):
                buffer = widget.get_buffer()
                start_iter = buffer.get_start_iter()
                end_iter = buffer.get_end_iter()
                value = buffer.get_text(start_iter, end_iter, True)
            else:  # Gtk.Entry
                value = widget.get_text()

            data[field_name] = value

        return data


class EntityDialog(Gtk.Dialog):
    def __init__(self, parent, entity_name=None):
        title = "New Entity" if entity_name is None else "Edit Entity"
        super().__init__(title=title, transient_for=parent.window, flags=0)

        self.parent = parent
        self.entity_name = entity_name
        self.fields = []

        self.set_default_size(500, 400)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.init_ui()

        if entity_name:
            self.load_data()

    def init_ui(self):
        area = self.get_content_area()
        area.set_spacing(10)

        # Entity name
        name_box = Gtk.Box(spacing=10)
        area.pack_start(name_box, False, False, 0)

        name_label = Gtk.Label(label="Entity Name:")
        name_box.pack_start(name_label, False, False, 0)

        self.name_entry = Gtk.Entry()
        self.name_entry.set_hexpand(True)
        name_box.pack_start(self.name_entry, True, True, 0)

        # Fields frame
        frame = Gtk.Frame(label="Fields")
        area.pack_start(frame, True, True, 0)

        # Scrolled window for fields
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_min_content_height(200)
        frame.add(scrolled_window)

        # Fields container
        self.fields_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        scrolled_window.add(self.fields_container)

        # Buttons for field management
        button_box = Gtk.Box(spacing=10)
        area.pack_start(button_box, False, False, 0)

        add_field_button = Gtk.Button(label="Add Field")
        add_field_button.connect("clicked", self.on_add_field)
        button_box.pack_start(add_field_button, False, False, 0)

        self.show_all()

        # Add initial field if new entity
        if self.entity_name is None:
            self.on_add_field(None)

    def on_add_field(self, button):
        field_box = Gtk.Box(spacing=10)
        self.fields_container.pack_start(field_box, False, False, 0)

        # Field name
        name_entry = Gtk.Entry()
        name_entry.set_placeholder_text("Field Name")
        name_entry.set_hexpand(True)
        field_box.pack_start(name_entry, True, True, 0)

        # Field type
        type_combo = Gtk.ComboBoxText()
        type_combo.append_text("oneline")
        type_combo.append_text("multiline")
        type_combo.set_active(0)
        field_box.pack_start(type_combo, False, False, 0)

        # Remove button
        remove_button = Gtk.Button.new_from_icon_name("edit-delete", Gtk.IconSize.BUTTON)
        remove_button.connect("clicked", self.on_remove_field, field_box)
        field_box.pack_start(remove_button, False, False, 0)

        self.fields.append((field_box, name_entry, type_combo))
        self.show_all()

    def on_remove_field(self, button, field_box):
        # Remove from container
        self.fields_container.remove(field_box)

        # Remove from fields list
        self.fields = [f for f in self.fields if f[0] != field_box]

        self.show_all()

    def load_data(self):
        if self.entity_name and self.entity_name in self.parent.entities:
            self.name_entry.set_text(self.entity_name)

            # Clear existing fields
            for field_box, _, _ in self.fields:
                self.fields_container.remove(field_box)
            self.fields = []

            # Load fields
            entity_data = self.parent.entities[self.entity_name]
            for field in entity_data['fields']:
                self.on_add_field(None)
                field_box, name_entry, type_combo = self.fields[-1]
                name_entry.set_text(field['name'])

                # Set type
                if field['type'] == 'multiline':
                    type_combo.set_active(1)
                else:
                    type_combo.set_active(0)

            self.show_all()

    def get_data(self):
        entity_name = self.name_entry.get_text().strip()
        fields = []

        for field_box, name_entry, type_combo in self.fields:
            field_name = name_entry.get_text().strip()
            if field_name:
                field_type = type_combo.get_active_text()
                fields.append({
                    'name': field_name,
                    'type': field_type
                })

        return entity_name, fields


def main():
    app = EntityCRUDApp()
    Gtk.main()


if __name__ == "__main__":
    main()
