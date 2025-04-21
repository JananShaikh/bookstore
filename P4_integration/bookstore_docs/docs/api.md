# API Reference

Base URL: `http://localhost:5000/api/books`

---

## Endpoints

### GET `/api/books`
- Returns a list of all books

### GET `/api/books/<id>`
- Returns details of a specific book
- Returns 404 if not found

### POST `/api/books`
- Creates a new book
- JSON payload:
  ```json
  {
    "title": "New Book",
    "author": "Author Name",
    "price": 9.99,
    "in_stock": true
  }
  ```

### PUT `/api/books/<id>`
- Updates an existing book
- Accepts any subset of fields above

### DELETE `/api/books/<id>`
- Deletes the book
- Returns a success message

### GET `/api/books/search?query=<keyword>`
- Searches books by title or author
