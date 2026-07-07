import os
import pytest
from unittest.mock import patch, MagicMock

os.environ.setdefault('DB_PORT_27017_TCP_ADDR', 'localhost')

from flask_brevets import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_submit_success(client):
    """Test that a valid list of control times is successfully inserted into MongoDB."""
    with patch('flask_brevets.db.brevets_list') as mock_collection:
        mock_collection.insert_one.return_value = MagicMock()
        
        test_payload = {
            "items": [
                {"km": "20.0", "open": "Wed 5/6 1:00", "close": "Wed 5/6 2:00"},
                {"km": "40.0", "open": "Wed 5/6 2:00", "close": "Wed 5/6 4:00"}
            ]
        }
        
        response = client.post('/_insert', json=test_payload)
        
        assert response.status_code == 200
        assert response.get_json()["result"] == "Successfully Added Entry to Database"
        mock_collection.insert_one.assert_called_once_with({"times": test_payload["items"]})

def test_submit_empty_error(client):
    """Test that submitting an empty list returns a 400 error as required by the spec."""
    response = client.post('/_insert', json={"items": []})
    
    assert response.status_code == 400
    assert "Error: No Control Times to Submit" in response.get_json()["result"]

def test_display_page_retrieval(client):
    """Test that the display page successfully fetches documents from MongoDB and renders."""
    with patch('flask_brevets.db.brevets_list') as mock_collection:
        mock_collection.find.return_value = [
            {
                "_id": "mocked_object_id_123",
                "times": [{"km": "20.0", "open": "Wed 5/6 1:00", "close": "Wed 5/6 2:00"}]
            }
        ]
        
        response = client.get('/display')
        
        assert response.status_code == 200
        assert b"All Submitted Control Times" in response.data
        mock_collection.find.assert_called_once()