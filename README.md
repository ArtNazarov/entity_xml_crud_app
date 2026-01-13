# Entity XML CRUD Application

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![GTK](https://img.shields.io/badge/GTK-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Tests](https://img.shields.io/badge/Tests-11%20passed-brightgreen)

A modern GTK3 desktop application for managing entity-based data with XML storage. This application provides a user-friendly interface for performing CRUD (Create, Read, Update, Delete) operations on entities defined in an XML configuration file, following the [Lua ArtNazarov/luassg site generator](https://github.com/ArtNazarov/luassg) XML format.

## 🌟 New Feature: Configuration Menu with XML Tree Editor Integration

### XML Tree Editor Integration

The application now includes a **Configuration** menu that allows you to directly edit XML configuration files using an integrated XML tree editor:

#### Added Features:
- **Configuration Menu**: Main menu with "Configuration" dropdown
- **Direct XML Editing**: Two menu items for editing common configuration files:
  - **Open ./data/CONST.xml**: Edit the CONST.xml configuration file
  - **Open ./data/pagination.xml**: Edit the pagination.xml configuration file
- **Integrated Editor**: Launches `dialog_xml_tree_editor.py` as a standalone process
- **Automatic File Creation**: Missing XML files are automatically created if they don't exist

#### How It Works:
1. Click **Configuration** in the main menu bar
2. Select either **"Open ./data/CONST.xml"** or **"Open ./data/pagination.xml"**
3. The application automatically:
   - Checks if the XML file exists (creates it if missing)
   - Verifies the XML tree editor script is available
   - Launches the editor in a new process with the selected file
4. Edit the XML file in a dedicated tree-based editor interface
5. Changes are saved back to the original file

#### Technical Details:
- **Process Isolation**: XML editor runs as a separate process, keeping the main app responsive
- **File Validation**: Ensures XML files follow proper structure before editing
- **Path Resolution**: Automatically finds the editor script in the same directory as app.py
- **Error Handling**: Comprehensive error messages if files or editor are missing

#### Benefits:
- 🔧 **Direct Configuration Editing**: Edit XML configs without leaving the application
- 🌳 **Visual XML Editing**: Use a tree-based editor for complex XML structures
- 🔄 **Live Updates**: Changes made in the editor are immediately saved
- ⚡ **Non-blocking**: Main application remains responsive while editing

## Screenshots

![List of data, main menu](https://dl.dropbox.com/scl/fi/qpis5l2a0i60bleplqib1/scrI_updated.png?rlkey=9kilfk6xc11sdxtmfvbit3xpx&st=qm3pgh0e)

![Menu items for config editor](https://dl.dropbox.com/scl/fi/1kkgx5n11cfsggrh52a41/scrI_main_menu.png?rlkey=0ukgju14f1bt6uu7yqbsjswf7&st=q7x1nn4t)

![Editing ./data/CONST.xml](https://dl.dropbox.com/scl/fi/swdj2f2tc0xdcs5i6yv0d/scr_const_dialog.png?rlkey=xub8wspme6u8dj5rqrl2tpde3&st=qka4q901)

![Editing ./data/pagination.xml](https://dl.dropbox.com/scl/fi/k4bln7amtr28v3d6l1tzs/scr_pagination_dialog.png?rlkey=aeepp5yrh8knefrjm7lggs7w6&st=dz2oozss)

![Editing some data](https://dl.dropbox.com/scl/fi/4so1ovazk58gsvag2ynyc/scrII.png?rlkey=21xhbk42zox5crp9e3w1sce5p&st=vtpwier6)

![List of entities](https://dl.dropbox.com/scl/fi/r1i2f01mkwz0ghfgxount/scrIII.png?rlkey=ck9iipaqqg56niqerg3if0o26&st=0f2s9p6d)

![Editing some entity structure](https://dl.dropbox.com/scl/fi/hvvuz01r4div7g439pwhd/scrIV.png?rlkey=phkk07rykx1p9ng66z5wxjrea&st=2hlq1nsi)

## ✨ Features

- **Multi-Entity Management**: Automatically creates tabs for each entity defined in XML
- **CRUD Operations**: Full Create, Read, Update, Delete functionality for records
- **Dynamic Entity Definition**: Define custom entities with configurable fields
- **Field Type Support**: Two field types supported: `oneline` (single-line text) and `multiline` (multi-line text area)
- **Entity Management**: Create, edit, and delete entities with automatic file system updates
- **luassg XML Format**: Compatible with **ArtNazarov/luassg** XML structure
- **Persistent XML Storage**: All data stored in structured XML files
- **Clean Architecture**: Clear separation between data loading and UI rendering
- **Comprehensive Testing**: 11 tests with full coverage using pytest
- **Configuration Menu**: Integrated XML tree editor for editing configuration files

## 📁 File Structure

```
./
├── app.py                      # Main application
├── tests.py                    # Pytest test suite (11 tests)
├── dialog_xml_tree_editor.py   # XML tree editor for configuration files
├── entities_description.xml    # Entity definitions
├── README.md                   # This file
└── data/                       # Data storage directory
    ├── CONST.xml               # Configuration file (editable via menu)
    ├── pagination.xml          # Configuration file (editable via menu)
    ├── posts/                  # Example entity directory
    │   ├── posts-[uuid].xml    # Entity files follow: entity-entityId.xml format
    │   └── ...
    ├── news/
    ├── quotes/
    └── gallery/
        └── gallery-37158403-3cfe-4922-92e2-46326f0eb571.xml  # Example file
```

## 🚀 Quick Start

### 1. Clone and install
```bash
# For Arch Linux
git clone https://github.com/ArtNazarov/entity_xml_crud_app.git
cd entity_xml_crud_app
sudo pacman -S python python-gobject gtk3 python-pytest python-lxml
python app.py
```

### 2. Run tests
```bash
python -m pytest tests.py -v
```

## 🛠️ Requirements

### Arch Linux
```bash
sudo pacman -S python python-gobject gtk3 python-pytest python-lxml
```

### Ubuntu/Debian
```bash
sudo apt-get install python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0 python3-pytest python3-lxml
```

### Fedora
```bash
sudo dnf install python3 python3-gobject gtk3 python3-pytest python3-lxml
```

### Using pip
```bash
pip install PyGObject pytest lxml
```

## 🏗️ Architecture

The application follows a clean architecture with clear separation of concerns:

### Data Layer
- `load_xml_data()`: Loads all data from XML files into memory
- `save_entities_to_xml()`: Saves entity definitions to XML
- In-memory data structure with entities, fields, and records

### Presentation Layer
- `render_xml_data_state()`: Clears UI and renders tabs based on in-memory data
- `create_entity_tab()`: Creates individual entity tabs
- `create_management_tab()`: Creates the management tab (always last)
- `create_menu_bar()`: Creates the main menu with configuration options

### Configuration Management
- `on_open_const_xml()`: Handles opening CONST.xml in the XML tree editor
- `on_open_pagination_xml()`: Handles opening pagination.xml in the XML tree editor
- `open_xml_in_editor()`: Common method for launching the XML tree editor

### Key Benefits
- **No UI flickering**: Tabs don't disappear during refresh
- **Robust updates**: Entity structure changes handled gracefully
- **Clean separation**: Data operations separate from UI rendering
- **Integrated configuration**: Edit XML files directly from the application

## 🎮 Using the Application

### Initial Setup
The application automatically creates necessary directories and files:
- Creates `./data/` directory if it doesn't exist
- Creates `./entities_description.xml` with default structure if missing
- Loads existing entities and data on startup

### Editing Configuration Files
1. Click **Configuration** in the main menu bar
2. Select **"Open ./data/CONST.xml"** to edit the CONST.xml file
3. Select **"Open ./data/pagination.xml"** to edit the pagination.xml file
4. The XML tree editor opens in a new window for visual XML editing
5. Make changes and save - they are immediately reflected in the file

### Entity Definition Format
Entities are defined in `entities_description.xml` following the luassg format:

```xml
<?xml version='1.0' encoding='utf-8'?>
<entities>
    <entity>
        <entity_name>gallery</entity_name>
        <entity_fields>
            <entity_field>
                <field_name>title</field_name>
                <field_type>oneline</field_type>
            </entity_field>
            <entity_field>
                <field_name>description</field_name>
                <field_type>multiline</field_type>
            </entity_field>
            <entity_field>
                <field_name>alt</field_name>
                <field_type>oneline</field_type>
            </entity_field>
            <entity_field>
                <field_name>src</field_name>
                <field_type>oneline</field_type>
            </entity_field>
            <entity_field>
                <field_name>comment</field_name>
                <field_type>multiline</field_type>
            </entity_field>
        </entity_fields>
    </entity>
    <!-- More entities... -->
</entities>
```

### Supported Field Types
- **`oneline`**: Single-line text input field (Gtk.Entry)
- **`multiline`**: Multi-line text area with scrollbars (Gtk.TextView in Gtk.ScrolledWindow)

### Record Operations (per entity tab)
- **New Record**: Create new record with dialog
- **Edit Record**: Modify selected record
- **Delete Record**: Remove selected record with confirmation
- **Refresh**: Reload data for this entity only

### Entity Operations (management tab)
- **New Entity**: Define new entity with custom fields
- **Edit Entity**: Modify entity structure (automatically renames files)
- **Delete Entity**: Remove entity and all associated data with confirmation
- **Refresh All**: Reload all data and refresh entire UI

### Configuration Operations (main menu)
- **Open CONST.xml**: Edit the CONST.xml configuration file
- **Open pagination.xml**: Edit the pagination.xml configuration file

## 💾 Data Storage

### File Naming Convention
```
./data/{entity_name}/{entity_name}-{unique_id}.xml
```
Example: `./data/gallery/gallery-37158403-3cfe-4922-92e2-46326f0eb571.xml`

### Configuration Files
- `./data/CONST.xml`: Application configuration constants
- `./data/pagination.xml`: Pagination settings and configuration

### Record XML Format (luassg compatible)
The application saves records in the **ArtNazarov/luassg** XML format:

```xml
<?xml version='1.0' encoding='utf-8'?>
<gallery id="37158403-3cfe-4922-92e2-46326f0eb571">
    <title>The kitten</title>
    <description>Some description</description>
    <alt>Some alt text</alt>
    <src>https://upload.wikimedia.org/wikipedia/commons/9/9b/Photo_of_a_kitten.jpg</src>
    <comment>my comment</comment>
</gallery>
```

**Key characteristics:**
- Root element name matches entity name
- `id` attribute on root element contains the record identifier
- Field elements as direct children of root
- XML declaration with encoding
- Proper indentation for readability

### Example Files Structure

**entities_description.xml:**
```xml
<?xml version='1.0' encoding='utf-8'?>
<entities>
    <entity>
        <entity_name>posts</entity_name>
        <entity_fields>
            <entity_field>
                <field_name>title</field_name>
                <field_type>oneline</field_type>
            </entity_field>
            <entity_field>
                <field_name>message</field_name>
                <field_type>multiline</field_type>
            </entity_field>
        </entity_fields>
    </entity>
    <entity>
        <entity_name>news</entity_name>
        <entity_fields>
            <entity_field>
                <field_name>caption</field_name>
                <field_type>multiline</field_type>
            </entity_field>
            <entity_field>
                <field_name>longread</field_name>
                <field_type>multiline</field_type>
            </entity_field>
        </entity_fields>
    </entity>
    <entity>
        <entity_name>quotes</entity_name>
        <entity_fields>
            <entity_field>
                <field_name>phrase</field_name>
                <field_type>oneline</field_type>
            </entity_field>
            <entity_field>
                <field_name>author</field_name>
                <field_type>oneline</field_type>
            </entity_field>
        </entity_fields>
    </entity>
    <entity>
        <entity_name>gallery</entity_name>
        <entity_fields>
            <entity_field>
                <field_name>title</field_name>
                <field_type>oneline</field_type>
            </entity_field>
            <entity_field>
                <field_name>description</field_name>
                <field_type>multiline</field_type>
            </entity_field>
            <entity_field>
                <field_name>alt</field_name>
                <field_type>oneline</field_type>
            </entity_field>
            <entity_field>
                <field_name>src</field_name>
                <field_type>oneline</field_type>
            </entity_field>
            <entity_field>
                <field_name>comment</field_name>
                <field_type>multiline</field_type>
            </entity_field>
        </entity_fields>
    </entity>
</entities>
```

**data/gallery/gallery-37158403-3cfe-4922-92e2-46326f0eb571.xml:**
```xml
<?xml version='1.0' encoding='utf-8'?>
<gallery id="37158403-3cfe-4922-92e2-46326f0eb571">
    <title>The kitten</title>
    <description>Some description</description>
    <alt>Some alt text</alt>
    <src>https://upload.wikimedia.org/wikipedia/commons/9/9b/Photo_of_a_kitten.jpg</src>
    <comment>my comment</comment>
</gallery>
```

## 🧪 Testing

The project includes 11 comprehensive pytest tests that verify:

```bash
# Run all tests
python -m pytest tests.py -v

# Run specific test category
python -m pytest tests.py::test_load_entities -v

# Test coverage includes:
# ✓ Entity loading and parsing
# ✓ Field type validation  
# ✓ File naming conventions (entity-entityId.xml)
# ✓ Directory structure
# ✓ CRUD operations with luassg format
# ✓ Integration tests
# ✓ Loading existing luassg format files
```

## 🔧 Key Implementation Details

### luassg XML Format Compatibility
The application is specifically designed to work with the **ArtNazarov/luassg** XML format:
- Records are saved with root element name = entity name
- `id` attribute on root element contains record identifier
- Field values are stored as child elements
- Automatic handling of filename pattern: `{entity_name}-{entity_id}.xml`

### Configuration Menu Implementation
The new configuration menu feature integrates seamlessly:
- **Menu Bar Integration**: Added to main window without disrupting existing layout
- **Process Management**: Uses `subprocess.Popen` to launch editor independently
- **File Validation**: Checks if XML files exist and creates them if missing
- **Error Handling**: Provides user feedback if editor script is not found
- **Path Resolution**: Automatically locates `dialog_xml_tree_editor.py` in the same directory

### Fixed Bugs
1. **Empty window on startup** - Proper initialization sequence
2. **Tabs disappearing on refresh** - Separate data loading from UI rendering
3. **Entity Management tab position** - Always appears as last tab
4. **Window blanking on entity updates** - Added safety checks and proper UI refresh

### Performance Optimizations
- In-memory data caching for quick access
- Selective UI updates (entity vs full refresh)
- Efficient XML parsing with error handling
- Proper handling of luassg format files
- Independent process for XML editing (non-blocking)

### User Experience
- Confirmation dialogs for destructive actions
- Real-time data synchronization
- Clear error messages
- Responsive UI with proper scrolling
- Automatic file renaming when entity names change
- Integrated configuration editing via menu
- Visual XML tree editing for complex structures

## 🐛 Troubleshooting

### Common Issues

**Issue**: "ModuleNotFoundError: No module named 'gi'"
**Solution**: Install python-gobject package
```bash
sudo pacman -S python-gobject  # Arch
sudo apt-get install python3-gi  # Ubuntu/Debian
```

**Issue**: Window appears empty on startup
**Solution**: Ensure `entities_description.xml` exists and is valid XML

**Issue**: Tabs disappear after refresh
**Solution**: This bug has been fixed in current version. Update to latest code.

**Issue**: XML files not loading correctly
**Solution**: Ensure files follow luassg format with `id` attribute on root element

**Issue**: "XML tree editor not found" error
**Solution**: Ensure `dialog_xml_tree_editor.py` is in the same directory as `app.py`

**Issue**: Configuration menu items don't work
**Solution**: Install python-lxml: `pip install lxml` or `sudo pacman -S python-lxml`

### Debug Mode
Add debug prints to `load_entities()` method to see XML parsing issues.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Write tests for new features
- Maintain backward compatibility with luassg format
- Follow Python PEP 8 style guide
- Update documentation as needed
- Ensure all 11 tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- GTK3 team for the excellent GUI toolkit
- Python community for amazing libraries
- Pytest team for robust testing framework
- All contributors who helped fix bugs and improve the application
- **ArtNazarov/luassg** for the XML format specification

## 📧 Contact

Artem Nazarov - [GitHub](https://github.com/ArtNazarov)

Project Link: [https://github.com/ArtNazarov/entity_xml_crud_app](https://github.com/ArtNazarov/entity_xml_crud_app)

## 🎯 Quick Reference

### Key Classes
- `EntityCRUDApp`: Main application class
- `RecordDialog`: Dialog for creating/editing records
- `EntityDialog`: Dialog for managing entity definitions

### Key Methods
- `load_xml_data()`: Master data loader
- `render_xml_data_state()`: Master UI renderer
- `on_refresh_all()`: Refresh everything (management tab)
- `on_refresh_entity()`: Refresh single entity
- `open_xml_in_editor()`: Launch XML tree editor

### Data Flow
```
User Action → Load XML Data → Update Memory → Render UI State → Show Window
Configuration Menu → Launch Editor → Edit XML → Save Changes
```

## 🚀 Example Workflow

1. **Launch application**: `python app.py`
2. **Edit configuration**: Click **Configuration** → **Open ./data/CONST.xml**
   - XML tree editor opens in a new window
   - Edit the XML structure visually
   - Save changes
3. **Add new entity**: Go to "Entity Management" tab → "New Entity"
   - Name: "tasks"
   - Fields: "name" (oneline), "description" (multiline)
4. **Add records**: Go to "tasks" tab → "New Record"
   - Fill in fields and save (creates `tasks-{uuid}.xml` in luassg format)
5. **Edit structure**: Go to "Entity Management" → Select "tasks" → "Edit Entity"
   - Add field: "priority" (oneline)
   - UI automatically updates with new column
6. **Refresh data**: Click "Refresh All" to reload from disk
7. **Edit pagination**: Click **Configuration** → **Open ./data/pagination.xml**
   - Configure pagination settings for your data

That's it! Your data is automatically saved in the **luassg XML format** and configuration files can be edited directly from the application menu.