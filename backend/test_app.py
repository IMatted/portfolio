# AI Wrote these

import unittest
import json
from app import app, client, releases_collection

class ReleaseArchitectTestCase(unittest.TestCase):

    def setUp(self):
        """
        Set up a temporary testing context before each test executes.
        Swaps the production collection out for an isolated test collection.
        """
        app.config['TESTING'] = True
        self.app = app.test_client()
        
        # Override collection to point to a temporary test namespace
        self.db = client.get_database("test_release_db")
        self.collection = self.db.releases
        import app as app_module
        app_module.releases_collection = self.collection

    def tearDown(self):
        """
        Clean up and wipe the test database after each test finishes.
        """
        client.drop_database("test_release_db")

    # 1. Test Health Check Route
    def test_health_check(self):
        response = self.app.get('/api/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')

    # 2. Test CREATE (POST Route) & AI Classification Parsing Logic
    def test_create_release_success(self):
        payload = {
            "version": "v1.2.3",
            "title": "Authentication Hotfix",
            "raw_input": "fixed login timeout bug\nadded secondary verification ui\nupdated database string"
        }
        response = self.app.post('/api/releases', 
                                 data=json.dumps(payload), 
                                 content_type='application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['version'], 'v1.2.3')
        self.assertFalse(data['is_published']) # Draft defaults to False
        
        # Verify AI Parsing sorted keywords correctly into categories
        self.assertIn("Fixed login timeout bug", data['changelog']['bug_fixes'])
        self.assertIn("Added secondary verification ui", data['changelog']['features'])
        self.assertIn("Updated database string", data['changelog']['maintenance'])

    # 3. Test CREATE Data Validation Boundaries
    def test_create_release_missing_fields(self):
        incomplete_payload = {
            "version": "v1.0.0"
            # Missing title and raw_input fields
        }
        response = self.app.post('/api/releases', 
                                 data=json.dumps(incomplete_payload), 
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", json.loads(response.data))

    # 4. Test READ (GET Routes)
    def test_get_releases(self):
        # Insert a mock document into test collection directly
        self.collection.insert_one({
            "version": "v1.0.0", "title": "Old Release", "raw_input": "minor fix",
            "changelog": {"features":[], "bug_fixes":["Minor fix"], "maintenance":[]},
            "is_published": True, "created_at": "2026-05-28T00:00:00"
        })

        # Test Main Feed
        response = self.app.get('/api/releases')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), 1)

    # 5. Test UPDATE Publication States (PUT Route)
    def test_update_release_status(self):
        doc = self.collection.insert_one({
            "version": "v2.0.0", "title": "Beta Build", "raw_input": "added dashboard",
            "changelog": {"features":["Added dashboard"], "bug_fixes":[], "maintenance":[]},
            "is_published": False, "created_at": "2026-05-28T00:00:00"
        })
        release_id = str(doc.inserted_id)

        # Fire put update request to change draft to published
        response = self.app.put(f'/api/releases/{release_id}',
                                data=json.dumps({"is_published": True}),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        # Verify state flipped inside test database
        updated_doc = self.collection.find_one({"_id": doc.inserted_id})
        self.assertTrue(updated_doc['is_published'])

    # 6. Test DELETE (DELETE Route)
    def test_delete_release(self):
        doc = self.collection.insert_one({
            "version": "v3.0.0", "title": "Trash Build", "raw_input": "test text",
            "changelog": {"features":[], "bug_fixes":[], "maintenance":[]},
            "is_published": False, "created_at": "2026-05-28T00:00:00"
        })
        release_id = str(doc.inserted_id)

        response = self.app.delete(f'/api/releases/{release_id}')
        self.assertEqual(response.status_code, 200)
        
        # Confirm it's gone from database entirely
        self.assertIsNone(self.collection.find_one({"_id": doc.inserted_id}))

if __name__ == '__main__':
    unittest.main()