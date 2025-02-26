"""
Minocrisy AI Tools - Basic Tests
Tests for the Flask application.
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

class TestApp(unittest.TestCase):
    """Test the Flask application."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a test configuration
        self.app = create_app({
            'TESTING': True,
            'SECRET_KEY': 'test-key',
            'ELEVENLABS_API_KEY': 'test-elevenlabs-key',
            'ELEVENLABS_VOICE_ID': 'test-voice-id',
            'OPENAI_API_KEY': 'test-openai-key',
            'RUNWAYML_API_KEY': 'test-runwayml-key'
        })
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Clean up the test environment."""
        self.app_context.pop()
    
    def test_index_page(self):
        """Test that the index page loads."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Minocrisy AI Tools', response.data)
    
    def test_talking_head_page(self):
        """Test that the talking head page loads."""
        response = self.client.get('/tools/talking-head/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Talking Head Generator', response.data)
    
    def test_hype_remover_page(self):
        """Test that the hype remover page loads."""
        response = self.client.get('/tools/hype-remover/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hype Remover', response.data)
    
    def test_api_status(self):
        """Test the API status endpoint."""
        response = self.client.get('/api/status')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('elevenlabs', data)
        self.assertIn('openai', data)
        self.assertIn('runwayml', data)
        # All should be True since we provided test keys
        self.assertTrue(data['elevenlabs'])
        self.assertTrue(data['openai'])
        self.assertTrue(data['runwayml'])
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
    
    @patch('app.tools.talking_head.service.generate_audio')
    @patch('app.tools.talking_head.service.generate_talking_head')
    def test_talking_head_generate(self, mock_generate_talking_head, mock_generate_audio):
        """Test the talking head generate endpoint."""
        # Mock the generate_audio and generate_talking_head functions
        mock_generate_audio.return_value = '/tmp/test.mp3'
        mock_generate_talking_head.return_value = '/tmp/test.mp4'
        
        # Mock the file operations
        with patch('builtins.open', MagicMock()):
            with patch('os.makedirs', MagicMock()):
                # Test the endpoint
                response = self.client.post('/tools/talking-head/generate', json={
                    'text': 'Test text'
                })
                
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertIn('video_url', data)
                self.assertIn('text', data)
                self.assertEqual(data['text'], 'Test text')
    
    @patch('app.tools.hype_remover.service.remove_hype')
    def test_hype_remover_process(self, mock_remove_hype):
        """Test the hype remover process endpoint."""
        # Mock the remove_hype function
        mock_remove_hype.return_value = {
            'original_text': 'Test text with AMAZING hype!',
            'processed_text': 'Test text with hype.',
            'changes': [
                {
                    'original': 'AMAZING hype',
                    'replacement': 'hype',
                    'reason': 'Removed exaggeration'
                }
            ]
        }
        
        # Test the endpoint
        response = self.client.post('/tools/hype-remover/process', json={
            'text': 'Test text with AMAZING hype!',
            'strength': 'moderate'
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('original_text', data)
        self.assertIn('processed_text', data)
        self.assertIn('changes', data)
        self.assertEqual(data['original_text'], 'Test text with AMAZING hype!')
        self.assertEqual(data['processed_text'], 'Test text with hype.')

if __name__ == '__main__':
    unittest.main()
