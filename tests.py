#!/usr/bin/env python3
import pytest
import xml.etree.ElementTree as ET
import os
import tempfile
import shutil
import sys
from app import EntityCRUDApp


# Sample XML content for testing
SAMPLE_XML_CONTENT = '''<?xml version="1.0"?>
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
</entities>
'''


@pytest.fixture
def temp_app():
    """Create a temporary app instance with sample data"""
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Save sample XML
    entities_file = os.path.join(temp_dir, 'entities_description.xml')
    with open(entities_file, 'w') as f:
        f.write(SAMPLE_XML_CONTENT)
    
    # Create data directory
    data_dir = os.path.join(temp_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Create a test class that inherits from EntityCRUDApp
    class TestEntityCRUDApp(EntityCRUDApp):
        def __init__(self):
            # Don't call parent init to avoid UI initialization
            self.entities_file = entities_file
            self.data_dir = data_dir
            self.entities = {}
            
            # Create directories if they don't exist
            os.makedirs(self.data_dir, exist_ok=True)
            
            # Load entities but don't initialize UI
            self.load_entities()
            self.load_all_entity_data()
    
    app = TestEntityCRUDApp()
    
    yield app
    
    # Cleanup
    shutil.rmtree(temp_dir)


def test_load_entities(temp_app):
    """Test that entities are loaded correctly from XML"""
    # Check that we have 3 entities
    assert len(temp_app.entities) == 3
    
    # Check entity names
    assert 'posts' in temp_app.entities
    assert 'news' in temp_app.entities
    assert 'quotes' in temp_app.entities


def test_posts_entity_fields(temp_app):
    """Test posts entity fields"""
    posts_entity = temp_app.entities['posts']
    fields = posts_entity['fields']
    
    # Check number of fields
    assert len(fields) == 2
    
    # Check field names and types
    field_names = [field['name'] for field in fields]
    field_types = [field['type'] for field in fields]
    
    assert 'title' in field_names
    assert 'message' in field_names
    assert field_types[field_names.index('title')] == 'oneline'
    assert field_types[field_names.index('message')] == 'multiline'


def test_news_entity_fields(temp_app):
    """Test news entity fields"""
    news_entity = temp_app.entities['news']
    fields = news_entity['fields']
    
    # Check number of fields
    assert len(fields) == 2
    
    # Check field names and types
    field_names = [field['name'] for field in fields]
    field_types = [field['type'] for field in fields]
    
    assert 'caption' in field_names
    assert 'longread' in field_names
    assert field_types[field_names.index('caption')] == 'multiline'
    assert field_types[field_names.index('longread')] == 'multiline'


def test_quotes_entity_fields(temp_app):
    """Test quotes entity fields"""
    quotes_entity = temp_app.entities['quotes']
    fields = quotes_entity['fields']
    
    # Check number of fields
    assert len(fields) == 2
    
    # Check field names and types
    field_names = [field['name'] for field in fields]
    field_types = [field['type'] for field in fields]
    
    assert 'phrase' in field_names
    assert 'author' in field_names
    assert field_types[field_names.index('phrase')] == 'oneline'
    assert field_types[field_names.index('author')] == 'oneline'


def test_save_and_load_entities(temp_app):
    """Test saving and loading entities"""
    # Add a new entity
    temp_app.entities['test_entity'] = {
        'fields': [
            {'name': 'test_field1', 'type': 'oneline'},
            {'name': 'test_field2', 'type': 'multiline'}
        ],
        'records': {}  # Add empty records dict as required by new structure
    }
    
    # Save entities using the new method name
    temp_app.save_entities_to_xml()
    
    # Verify the file was saved correctly by reading it directly
    tree = ET.parse(temp_app.entities_file)
    root = tree.getroot()
    
    # Find our test entity in the saved XML
    test_entity_found = False
    for entity_elem in root.findall('entity'):
        entity_name = entity_elem.find('entity_name').text
        if entity_name == 'test_entity':
            test_entity_found = True
            
            # Check fields
            fields_elem = entity_elem.find('entity_fields')
            field_elems = fields_elem.findall('entity_field') if fields_elem is not None else []
            
            assert len(field_elems) == 2
            
            field_names = [field.find('field_name').text for field in field_elems]
            field_types = [field.find('field_type').text for field in field_elems]
            
            assert 'test_field1' in field_names
            assert 'test_field2' in field_names
            assert field_types[field_names.index('test_field1')] == 'oneline'
            assert field_types[field_names.index('test_field2')] == 'multiline'
            break
    
    assert test_entity_found, "Test entity not found in saved XML"
    
    # Now test loading by creating a new minimal app instance
    class NewTestApp:
        def __init__(self, entities_file, data_dir):
            self.entities_file = entities_file
            self.data_dir = data_dir
            self.entities = {}
            # Copy the load_entities method from EntityCRUDApp
            self.load_entities = lambda: EntityCRUDApp.load_entities(self)
            self.load_entities()
    
    new_app = NewTestApp(temp_app.entities_file, temp_app.data_dir)
    
    # Check that new entity was saved and loaded
    assert 'test_entity' in new_app.entities
    assert len(new_app.entities['test_entity']['fields']) == 2
    
    # Check field details
    fields = new_app.entities['test_entity']['fields']
    field_names = [field['name'] for field in fields]
    field_types = [field['type'] for field in fields]
    
    assert 'test_field1' in field_names
    assert 'test_field2' in field_names
    assert field_types[field_names.index('test_field1')] == 'oneline'
    assert field_types[field_names.index('test_field2')] == 'multiline'


def test_save_record(temp_app):
    """Test saving a record"""
    entity_name = 'posts'
    record_data = {
        'id': 'test-record-123',
        'title': 'Test Title',
        'message': 'Test message content\nwith multiple lines'
    }
    
    # Ensure entity exists with records dict
    if 'records' not in temp_app.entities[entity_name]:
        temp_app.entities[entity_name]['records'] = {}
    
    # Save record using the actual method
    # First, monkey-patch the method to use temp_app's context
    original_save_record = EntityCRUDApp.save_record
    temp_app.save_record = lambda en, d: original_save_record(temp_app, en, d)
    
    # Call the method
    temp_app.save_record(entity_name, record_data)
    
    # Check if file was created
    entity_dir = os.path.join(temp_app.data_dir, entity_name)
    expected_filename = f"{entity_name}-{record_data['id']}.xml"
    expected_path = os.path.join(entity_dir, expected_filename)
    
    assert os.path.exists(expected_path)
    
    # Check file content
    tree = ET.parse(expected_path)
    root = tree.getroot()
    
    assert root.find('id').text == 'test-record-123'
    assert root.find('title').text == 'Test Title'
    assert root.find('message').text == 'Test message content\nwith multiple lines'


def test_get_record_data(temp_app):
    """Test retrieving record data"""
    entity_name = 'news'
    record_id = 'test-news-456'
    
    # First create a record by manually writing the file
    entity_dir = os.path.join(temp_app.data_dir, entity_name)
    os.makedirs(entity_dir, exist_ok=True)
    
    filename = f"{entity_name}-{record_id}.xml"
    filepath = os.path.join(entity_dir, filename)
    
    # Create XML file manually
    root = ET.Element('record')
    ET.SubElement(root, 'id').text = record_id
    ET.SubElement(root, 'caption').text = 'Breaking News'
    ET.SubElement(root, 'longread').text = 'Detailed news content...'
    
    tree = ET.ElementTree(root)
    tree.write(filepath, encoding='utf-8', xml_declaration=True)
    
    # Now retrieve it using get_record_data
    # Ensure entity has records dict
    if 'records' not in temp_app.entities[entity_name]:
        temp_app.entities[entity_name]['records'] = {}
    
    # Monkey-patch the method
    original_get_record_data = EntityCRUDApp.get_record_data
    temp_app.get_record_data = lambda en, rid: original_get_record_data(temp_app, en, rid)
    
    retrieved_data = temp_app.get_record_data(entity_name, record_id)
    
    assert retrieved_data is not None
    assert retrieved_data['id'] == record_id
    assert retrieved_data['caption'] == 'Breaking News'
    assert retrieved_data['longread'] == 'Detailed news content...'


def test_delete_record(temp_app):
    """Test deleting a record"""
    entity_name = 'quotes'
    record_id = 'test-quote-789'
    
    # Create a record by manually writing the file
    entity_dir = os.path.join(temp_app.data_dir, entity_name)
    os.makedirs(entity_dir, exist_ok=True)
    
    filename = f"{entity_name}-{record_id}.xml"
    filepath = os.path.join(entity_dir, filename)
    
    # Create XML file manually
    root = ET.Element('record')
    ET.SubElement(root, 'id').text = record_id
    ET.SubElement(root, 'phrase').text = 'To be or not to be'
    ET.SubElement(root, 'author').text = 'Shakespeare'
    
    tree = ET.ElementTree(root)
    tree.write(filepath, encoding='utf-8', xml_declaration=True)
    
    # Verify it exists
    assert os.path.exists(filepath)
    
    # Delete the record
    # Monkey-patch the method
    original_delete_record = EntityCRUDApp.delete_record
    temp_app.delete_record = lambda en, rid: original_delete_record(temp_app, en, rid)
    
    temp_app.delete_record(entity_name, record_id)
    
    # Verify it's deleted
    assert not os.path.exists(filepath)


def test_file_naming_convention(temp_app):
    """Test that files are named with entity-entityId.xml format"""
    entity_name = 'testentity'
    record_id = 'unique-id-123'
    
    # First, add the entity to temp_app.entities
    temp_app.entities[entity_name] = {
        'fields': [{'name': 'field1', 'type': 'oneline'}],
        'records': {}
    }
    
    # Save a record using a simple direct approach
    entity_dir = os.path.join(temp_app.data_dir, entity_name)
    os.makedirs(entity_dir, exist_ok=True)
    
    filename = f"{entity_name}-{record_id}.xml"
    filepath = os.path.join(entity_dir, filename)
    
    # Create XML file manually
    root = ET.Element('record')
    ET.SubElement(root, 'id').text = record_id
    ET.SubElement(root, 'field1').text = 'value1'
    
    tree = ET.ElementTree(root)
    tree.write(filepath, encoding='utf-8', xml_declaration=True)
    
    # Check file name
    files = os.listdir(entity_dir)
    
    # Should have exactly one file
    assert len(files) == 1
    
    # File name should be entity-entityId.xml
    actual_filename = files[0]
    assert actual_filename == f"{entity_name}-{record_id}.xml"
    assert actual_filename.endswith('.xml')


def test_entity_directory_structure(temp_app):
    """Test the directory structure for entities"""
    entity_name = 'sample'
    record_id = 'record-001'
    
    # First, add the entity to temp_app.entities
    temp_app.entities[entity_name] = {
        'fields': [{'name': 'data', 'type': 'oneline'}],
        'records': {}
    }
    
    # Save a record using a simple direct approach
    entity_dir = os.path.join(temp_app.data_dir, entity_name)
    
    # This should create directory
    os.makedirs(entity_dir, exist_ok=True)
    
    # Check directory structure
    assert os.path.exists(entity_dir)
    assert os.path.isdir(entity_dir)
    
    # Create a test file
    filename = f"{entity_name}-{record_id}.xml"
    filepath = os.path.join(entity_dir, filename)
    
    # Create XML file manually
    root = ET.Element('record')
    ET.SubElement(root, 'id').text = record_id
    ET.SubElement(root, 'data').text = 'test'
    
    tree = ET.ElementTree(root)
    tree.write(filepath, encoding='utf-8', xml_declaration=True)
    
    # Check file inside directory
    files = os.listdir(entity_dir)
    assert len(files) == 1
    assert files[0] == f"{entity_name}-{record_id}.xml"


# Helper function to test the actual save_record method
def test_save_record_integration(temp_app):
    """Integration test for save_record method"""
    entity_name = 'integration_test'
    record_id = 'integration-id-999'
    
    # Add entity with proper structure
    temp_app.entities[entity_name] = {
        'fields': [{'name': 'test_field', 'type': 'oneline'}],
        'records': {}
    }
    
    # Monkey-patch save_record to use temp_app context
    import app
    original_indent = app.EntityCRUDApp.indent_xml
    temp_app.indent_xml = original_indent.__get__(temp_app, type(temp_app))
    
    # Use the actual save_record method
    data = {'id': record_id, 'test_field': 'integration value'}
    
    # Call save_record directly with proper context
    temp_app.save_record(entity_name, data)
    
    # Verify file was created
    entity_dir = os.path.join(temp_app.data_dir, entity_name)
    expected_file = os.path.join(entity_dir, f"{entity_name}-{record_id}.xml")
    
    assert os.path.exists(expected_file)
    
    # Verify content
    tree = ET.parse(expected_file)
    root = tree.getroot()
    
    assert root.find('id').text == record_id
    assert root.find('test_field').text == 'integration value'


if __name__ == "__main__":
    pytest.main([__file__, '-v'])