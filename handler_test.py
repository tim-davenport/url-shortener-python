import unittest
from unittest.mock import patch

from handler import post, get

class HandlerTest(unittest.TestCase):

    @patch('handler.boto3')
    @patch('handler.os')
    def test_returns_http_201(self, mock_boto3, mock_os):
        response = post({'body': {'url':'https://www.test.com'}}, None)
        self.assertTrue(response['statusCode'], 201)
        self.assertIsNotNone(response['headers']['Location'])

    def test_returns_http_400(self):
        response = post({'body': {'url':'foobar'}}, None)
        self.assertTrue(response['statusCode'], 400)

    def test_get_returns_302(self):
        response = get({'queryStringParameters':{"code":"abcdef"}}, None)
        self.assertTrue(response['statusCode'], 302)

if __name__ == "__main__":
    unittest.main()