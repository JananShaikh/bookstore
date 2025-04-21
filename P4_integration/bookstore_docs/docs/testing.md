# Testing Guide

### File: `bookstore_client/test_client.py`

- Uses Python `unittest` and `unittest.mock`
- Tests:
  - Get all books
  - Get book by ID
  - Handle errors (e.g., 404 Not Found)
- Mocks the `requests` module to avoid real API calls

---

## Running the Tests

```bash
cd bookstore_client
python test_client.py
```

---

## How to Extend

You can add tests for:
- `add_book()`
- `update_book()`
- `delete_book()`
- `search_books()`

Use `patch('client.requests.method')` to simulate API behavior.
