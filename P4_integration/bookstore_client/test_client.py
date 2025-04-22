#!/usr/bin/env python3
"""
Test script for the Bookstore Client
"""
import unittest
import requests
from unittest.mock import patch, MagicMock
from client import (
    get_all_books,
    get_book_by_id,
    add_book,
    update_book,
    delete_book,
    search_books
)

class TestBookstoreClient(unittest.TestCase):
    def setUp(self):
        self.sample_books = [
            {
                "id": "1",
                "title": "Test Book 1",
                "author": "Test Author 1",
                "price": 10.99,
                "in_stock": True
            },
            {
                "id": "2",
                "title": "Test Book 2",
                "author": "Test Author 2",
                "price": 12.99,
                "in_stock": False
            }
        ]
        self.single_book = self.sample_books[0]

    @patch('client.requests.get')
    def test_get_all_books(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_books
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_all_books()
        self.assertEqual(result, self.sample_books)
        mock_get.assert_called_once()

    @patch('client.requests.get')
    def test_get_book_by_id(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.single_book
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_book_by_id("1")
        self.assertEqual(result, self.single_book)
        mock_get.assert_called_once()

    @patch('client.requests.get')
    def test_get_book_by_id_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        http_error = requests.exceptions.HTTPError("404 Not Found")
        http_error.response = mock_response
        mock_get.side_effect = http_error

        result = get_book_by_id("999")
        self.assertIsNone(result)

    @patch('client.requests.post')
    @patch('builtins.input', side_effect=["Test Book", "Test Author", "9.99", "yes"])
    def test_add_book(self, mock_input, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "3",
            "title": "Test Book",
            "author": "Test Author",
            "price": 9.99,
            "in_stock": True
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        add_book()
        mock_post.assert_called_once()

    @patch('client.requests.put')
    @patch('client.get_book_by_id')
    @patch('builtins.input', side_effect=["1", "", "", "", ""])
    def test_update_book(self, mock_input, mock_get, mock_put):
        mock_get.return_value = self.single_book

        mock_response = MagicMock()
        mock_response.json.return_value = self.single_book
        mock_response.raise_for_status.return_value = None
        mock_put.return_value = mock_response

        update_book()
        mock_put.assert_called_once()

    @patch('client.requests.delete')
    @patch('client.get_book_by_id')
    @patch('builtins.input', side_effect=["1", "yes"])
    def test_delete_book(self, mock_input, mock_get, mock_delete):
        mock_get.return_value = self.single_book

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response

        delete_book()
        mock_delete.assert_called_once()

    @patch('client.requests.get')
    @patch('builtins.input', return_value="test")
    def test_search_books(self, mock_input, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [self.single_book]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        search_books()
        mock_get.assert_called_once()

if __name__ == '__main__':
    print("Running tests for Bookstore Client implementation...")
    unittest.main()
