#!/usr/bin/env python3
import pytest
import xml.etree.ElementTree as ET
import os
import tempfile
import shutil
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
    
    # Monkey patch the app to use temp directory
    original_entities_file = EntityCRUDApp.__init__.__defaults__
    original_data_dir = None
    
    # Create a test class that inherits from EntityCRUDApp
    class TestEntityCRUDApp(EntityCRUDApp):
        def __init__(self):
            self.entities_file = entities_file
            self.data_dir = data_dir
            self.entities = {}
            
            # Create directories if they don't exist
            os.makedirs(self.data_dir, exist_ok=True)
            
            self.load_entities()
            # Don't initialize UI for tests
    
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
        ]
    }
    
    # Save entities
    temp_app.save_entities()
    
    # Create new app instance to load from saved file
    class NewTestApp(EntityCRUDApp):
        def __init__(self, entities_file, data_dir):
            self.entities_file = entities_file
            self.data_dir = data_dir
            self.entities = {}
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
    
    # Save record
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
    
    # First create a record
    record_data = {
        'id': record_id,
        'caption': 'Breaking News',
        'longread': 'Detailed news content...'
    }
    
    temp_app.save_record(entity_name, record_data)
    
    # Now retrieve it
    retrieved_data = temp_app.get_record_data(entity_name, record_id)
    
    assert retrieved_data is not None
    assert retrieved_data['id'] == record_id
    assert retrieved_data['caption'] == 'Breaking News'
    assert retrieved_data['longread'] == 'Detailed news content...'


def test_delete_record(temp_app):
    """Test deleting a record"""
    entity_name = 'quotes'
    record_id = 'test-quote-789'
    
    # Create a record
    record_data = {
        'id': record_id,
        'phrase': 'To be or not to be',
        'author': 'Shakespeare'
    }
    
    temp_app.save_record(entity_name, record_data)
    
    # Verify it exists
    entity_dir = os.path.join(temp_app.data_dir, entity_name)
    expected_filename = f"{entity_name}-{record_id}.xml"
    expected_path = os.path.join(entity_dir, expected_filename)
    
    assert os.path.exists(expected_path)
    
    # Delete the record
    temp_app.delete_record(entity_name, record_id)
    
    # Verify it's deleted
    assert not os.path.exists(expected_path)


def test_file_naming_convention(temp_app):
    """Test that files are named with entity-entityId.xml format"""
    entity_name = 'testentity'
    record_id = 'unique-id-123'
    
    # Save a record
    temp_app.save_record(entity_name, {'id': record_id, 'field1': 'value1'})
    
    # Check file name
    entity_dir = os.path.join(temp_app.data_dir, entity_name)
    files = os.listdir(entity_dir)
    
    # Should have exactly one file
    assert len(files) == 1
    
    # File name should be entity-entityId.xml
    filename = files[0]
    assert filename == f"{entity_name}-{record_id}.xml"
    assert filename.endswith('.xml')


def test_entity_directory_structure(temp_app):
    """Test the directory structure for entities"""
    entity_name = 'sample'
    record_id = 'record-001'
    
    # Save a record (this should create directory)
    temp_app.save_record(entity_name, {'id': record_id, 'data': 'test'})
    
    # Check directory structure
    entity_dir = os.path.join(temp_app.data_dir, entity_name)
    assert os.path.exists(entity_dir)
    assert os.path.isdir(entity_dir)
    
    # Check file inside directory
    files = os.listdir(entity_dir)
    assert len(files) == 1
    assert files[0] == f"{entity_name}-{record_id}.xml"


if __name__ == "__main__":
    pytest.main([__file__, '-v'])