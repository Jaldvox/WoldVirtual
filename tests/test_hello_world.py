import unittest

class TestHelloWorld(unittest.TestCase):
    
    def test_hello_world(self):
        """Test that hello world returns the expected string"""
        expected = "Hello, World!"
        actual = hello_world()
        self.assertEqual(actual, expected)
    
    def test_hello_world_type(self):
        """Test that hello world returns a string"""
        result = hello_world()
        self.assertIsInstance(result, str)

def hello_world():
    """Simple function that returns Hello, World!"""
    return "Hello, World!"

if __name__ == '__main__':
    unittest.main()