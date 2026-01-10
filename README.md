# Entity XML CRUD Application

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![GTK](https://img.shields.io/badge/GTK-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Tests](https://img.shields.io/badge/Tests-10%20passed-brightgreen)

A modern GTK3 desktop application for managing entity-based data with XML storage. This application provides a user-friendly interface for performing CRUD (Create, Read, Update, Delete) operations on entities defined in an XML configuration file.

## ✨ Features

- **Multi-Entity Management**: Automatically creates tabs for each entity defined in XML
- **CRUD Operations**: Full Create, Read, Update, Delete functionality for records
- **Dynamic Entity Definition**: Define custom entities with configurable fields
- **Field Type Support**: Two field types supported: `oneline` (single-line text) and `multiline` (multi-line text area)
- **Entity Management**: Create, edit, and delete entities with automatic file system updates
- **Persistent XML Storage**: All data stored in structured XML files
- **Comprehensive Testing**: Full test coverage with pytest

## 📁 File Structure

```
./
├── app.py                      # Main application
├── tests.py                    # Pytest test suite
├── entities_description.xml    # Entity definitions
├── README.md                   # This file
└── data/                       # Data storage directory
    ├── posts/                  # Example entity directory
    │   ├── posts-[uuid].xml    # Entity files follow: entity-entityId.xml format
    │   └── ...
    ├── news/
    └── quotes/
```

## 📋 Requirements

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

### Using pip (cross-platform)
```bash
pip install PyGObject pytest
```

## 🚀 Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/ArtNazarov/entity_xml_crud_app.git
cd entity_xml_crud_app
```

### 2. Install dependencies
```bash
# For Arch Linux
sudo pacman -S python python-gobject gtk3 python-pytest

# Or using pip
pip install PyGObject pytest
```

### 3. Run the application
```bash
python app.py
```

### 4. Run tests
```bash
python -m pytest tests.py -v
```

## 🛠️ Configuration

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
- **`oneline`**: Single-line text input field
- **`multiline`**: Multi-line text area with scrollbars

## 🎮 Using the Application

### Main Interface
- **Entity Tabs**: Each entity gets its own tab with a data table
- **Management Tab**: Central location for managing entity definitions

### Record Operations (per entity)
- **New Record**: Create a new record with all defined fields
- **Edit Record**: Modify selected record (double-click or button)
- **Delete Record**: Remove selected record with confirmation
- **Refresh**: Reload data from disk

### Entity Operations
- **New Entity**: Define a new entity with custom fields
- **Edit Entity**: Modify entity structure (renames files automatically)
- **Delete Entity**: Remove entity and all associated data files
- **Refresh All**: Reload all entity definitions and data

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

The project includes comprehensive pytest coverage:

```bash
# Run all tests
python -m pytest tests.py -v

# Run specific test
python -m pytest tests.py::test_load_entities -v

# Test coverage includes:
# - Entity loading and parsing
# - Field type validation
# - CRUD operations
# - File naming conventions
# - Directory structure
```

## 🔧 Development

### Project Structure
- `app.py`: Main application class with GTK interface
- `tests.py`: Pytest test suite with 10 comprehensive tests
- `EntityCRUDApp`: Main application class
- `RecordDialog`: Dialog for creating/editing records
- `EntityDialog`: Dialog for managing entity definitions

### Key Features Implemented
- ✅ Automatic XML file creation if missing
- ✅ Proper file path handling with entity-entityId.xml format
- ✅ Entity renaming with automatic file renaming
- ✅ Multi-line text support with scrollable text areas
- ✅ Confirmation dialogs for deletions
- ✅ Real-time data refresh
- ✅ Error handling for file operations

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

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- GTK3 team for the excellent GUI toolkit
- Python community for amazing libraries
- Pytest team for robust testing framework

## 📧 Contact

Artem Nazarov - [GitHub](https://github.com/ArtNazarov)

Project Link: [https://github.com/ArtNazarov/entity_xml_crud_app](https://github.com/ArtNazarov/entity_xml_crud_app)

## 🚀 Quick Start Example

1. **Clone and install:**
```bash
git clone https://github.com/ArtNazarov/entity_xml_crud_app.git
cd entity_xml_crud_app
sudo pacman -S python python-gobject gtk3 python-pytest
```

2. **Run the app:**
```bash
python app.py
```

3. **Create your first entity:**
   - Go to "Entity Management" tab
   - Click "New Entity"
   - Name: "tasks"
   - Add fields: "name" (oneline), "description" (multiline)
   - Click OK

4. **Add records:**
   - Go to "tasks" tab
   - Click "New Record"
   - Fill in fields and save

That's it! Your data is automatically saved in XML format.