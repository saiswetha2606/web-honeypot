import unittest
import socket
import time
from threading import Thread
from honeypot.server import SimpleHoneypot

class TestHoneypot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Start the honeypot in a separate thread for testing"""
        cls.honeypot = SimpleHoneypot(config_file='../honeypot/config.json')
        cls.server_thread = Thread(target=cls.honeypot.run)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)  # Give server time to start

    def test_connection(self):
        """Test that the honeypot accepts connections"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 2222))
            banner = sock.recv(1024)
            self.assertTrue(banner.startswith(b'220'))
            sock.send(b'TEST\n')
            sock.close()
        except socket.error as e:
            self.fail(f"Connection failed: {str(e)}")

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        # Normally the server would keep running, but for testing we can exit
        pass

if __name__ == '__main__':
    unittest.main()