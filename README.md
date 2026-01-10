# Entity XML CRUD Application

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![GTK](https://img.shields.io/badge/GTK-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Tests](https://img.shields.io/badge/Tests-11%20passed-brightgreen)

A modern GTK3 desktop application for managing entity-based data with XML storage. This application provides a user-friendly interface for performing CRUD (Create, Read, Update, Delete) operations on entities defined in an XML configuration file.

## ✨ Features

- **Multi-Entity Management**: Automatically creates tabs for each entity defined in XML
- **CRUD Operations**: Full Create, Read, Update, Delete functionality for records
- **Dynamic Entity Definition**: Define custom entities with configurable fields
- **Field Type Support**: Two field types supported: `oneline` (single-line text) and `multiline` (multi-line text area)
- **Entity Management**: Create, edit, and delete entities with automatic file system updates
- **Persistent XML Storage**: All data stored in structured XML files
- **Clean Architecture**: Clear separation between data loading and UI rendering
- **Comprehensive Testing**: 11 tests with full coverage using pytest

## 📁 File Structure

```
./
├── app.py                      # Main application
├── tests.py                    # Pytest test suite (11 tests)
├── entities_description.xml    # Entity definitions
├── README.md                   # This file
└── data/                       # Data storage directory
    ├── posts/                  # Example entity directory
    │   ├── posts-[uuid].xml    # Entity files follow: entity-entityId.xml format
    │   └── ...
    ├── news/
    └── quotes/
```

## 🚀 Quick Start

### 1. Clone and install
```bash
# For Arch Linux
git clone https://github.com/ArtNazarov/entity_xml_crud_app.git
cd entity_xml_crud_app
sudo pacman -S python python-gobject gtk3 python-pytest
python app.py
```

### 2. Run tests
```bash
python -m pytest tests.py -v
```

## 🛠️ Requirements

### Arch Linux
```bash
sudo pacman -S python python-gobject gtk3 python-pytest
```

### Ubuntu/Debian
```bash
sudo apt-get install python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0 python3-pytest
```

### Fedora
```bash
sudo dnf install python3 python3-gobject gtk3 python3-pytest
```

### Using pip
```bash
pip install PyGObject pytest
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

### Key Benefits
- **No UI flickering**: Tabs don't disappear during refresh
- **Robust updates**: Entity structure changes handled gracefully
- **Clean separation**: Data operations separate from UI rendering

## 🎮 Using the Application

### Initial Setup
The application automatically creates necessary directories and files:
- Creates `./data/` directory if it doesn't exist
- Creates `./entities_description.xml` with default structure if missing
- Loads existing entities and data on startup

### Entity Definition Format
Entities are defined in `entities_description.xml`:

```xml
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

## 💾 Data Storage

### File Naming Convention
```
./data/{entity_name}/{entity_name}-{unique_id}.xml
```
Example: `./data/posts/posts-550e8400-e29b-41d4-a716-446655440000.xml`

### Record XML Format
```xml
<?xml version="1.0"?>
<record>
    <id>550e8400-e29b-41d4-a716-446655440000</id>
    <title>Sample Post</title>
    <message>This is a sample message with multiple lines.</message>
</record>
```

## 🧪 Testing

The project includes 11 comprehensive pytest tests:

```bash
# Run all tests
python -m pytest tests.py -v

# Run specific test category
python -m pytest tests.py::test_load_entities -v

# Test coverage includes:
# ✓ Entity loading and parsing
# ✓ Field type validation  
# ✓ File naming conventions
# ✓ Directory structure
# ✓ CRUD operations
# ✓ Integration tests
```

## 🔧 Key Implementation Details

### Fixed Bugs
1. **Empty window on startup** - Proper initialization sequence
2. **Tabs disappearing on refresh** - Separate data loading from UI rendering
3. **Entity Management tab position** - Always appears as last tab
4. **Window blanking on entity updates** - Added safety checks and proper UI refresh

### Performance Optimizations
- In-memory data caching for quick access
- Selective UI updates (entity vs full refresh)
- Efficient XML parsing with error handling

### User Experience
- Confirmation dialogs for destructive actions
- Real-time data synchronization
- Clear error messages
- Responsive UI with proper scrolling

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
- Maintain backward compatibility
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

### Data Flow
```
User Action → Load XML Data → Update Memory → Render UI State → Show Window
```

## 🚀 Example Workflow

1. **Launch application**: `python app.py`
2. **Add new entity**: Go to "Entity Management" tab → "New Entity"
   - Name: "tasks"
   - Fields: "name" (oneline), "description" (multiline)
3. **Add records**: Go to "tasks" tab → "New Record"
   - Fill in fields and save
4. **Edit structure**: Go to "Entity Management" → Select "tasks" → "Edit Entity"
   - Add field: "priority" (oneline)
   - UI automatically updates with new column
5. **Refresh data**: Click "Refresh All" to reload from disk

That's it! Your data is automatically saved in the correct XML format.