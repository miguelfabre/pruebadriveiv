import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed
from pruebadriveiv import Test

class InsertTestCase(unittest.TestCase):
    def setUp(self):
    	print "zapatos"
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_urlfetch_stub()

    def tearDown(self):
    	print "zapatos"
        self.testbed.deactivate()

    def test(self):
	print "zapatos"
	test = Test()
	response = test.Inserta('OK')
	self.assertEqual(response, 'OK')

if __name__ == "__main__":
	unittest.main()
