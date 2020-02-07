import unittest
from unittest.mock import patch

from handler import post, get

class HandlerTest(unittest.TestCase):

    @patch('handler.boto3')
    @patch('handler.os')
    def test_post_returns_http_201(self, mock_boto3, mock_os):
        response = post({'body': '{"url":"https://www.test.com"}'}, None)
        self.assertTrue(response['statusCode'], 201)
        self.assertIsNotNone(response['headers']['Location'])

    def test_post_returns_http_400_with_invalid_url(self):
        response = post({'body': '{"url":"foobar"}'}, None)
        self.assertTrue(response['statusCode'], 400)

    def test_post_returns_http_400_with_no_url_supplied(self):
        response = post({'body': "{}"}, None)
        self.assertTrue(response['statusCode'], 400)

    @patch('handler.boto3')
    @patch('handler.os')
    def test_get_returns_302(self, mock_boto3, mock_os):
        response = get({'queryStringParameters':{'code':'abcdef'}}, None)
        self.assertTrue(response['statusCode'], 302)
        self.assertIsNotNone(response['headers']['Location'])

    def test_get_returns_400_without_code_query_string(self):
        response = get({'queryStringParameters':{}}, None)
        self.assertTrue(response['statusCode'], 400)

if __name__ == "__main__":
    unittest.main()