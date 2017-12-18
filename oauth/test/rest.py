import unittest
import importlib
import requests
#from app import create_app
from flask.ext.testing import LiveServerTestCase

# Testing with LiveServer

class MyTest(LiveServerTestCase):
    # if the create_app is not implemented NotImplementedError will be raised
    def create_app(self):
        from app import app
        app.config['TESTING'] = True
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 8943
        return app

    def test_flask_application_is_up_and_running(self):
            url = self.get_server_url() + '/test'
            print url
            response = urllib2.urlopen(url)
            self.assertEqual(response.code, 200)

if __name__ == '__main__':
    unittest.main()
