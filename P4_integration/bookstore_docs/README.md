# Bookstore Client & API

This project includes a command-line **client application** that interacts with a RESTful **Bookstore API**. It allows users to manage a collection of books through a user-friendly interface with full CRUD capabilities.

---

## Features

- List all books  
- View details of a book by ID  
- Add a new book  
- Update existing book information  
- Delete a book  
- Search books by title or author  
- Input validation and user-friendly error handling  
- Clean table formatting and colored feedback

---

## Project Structure

```
bookstore_api/
├── app.py               # Flask REST API for books
├── books.json           # JSON file storing book data

bookstore_client/
├── client.py            # Interactive CLI client
├── test_client.py       # Unit tests for client functions
```

---

## Requirements

- Python 3.7+
- `pip install` the following packages:
  ```
  pip install requests tabulate colorama flask flask-cors
  ```

---

## How to Run

### 1. Start the Bookstore API
```bash
cd bookstore_api
python app.py
```

This runs a Flask server on `http://localhost:5000`.

---

### 2. Launch the Bookstore Client
In a separate terminal:
```bash
cd bookstore_client
python client.py
```

You’ll be presented with a menu to:
- View books
- Add/update/delete
- Search for titles/authors

---

## Running Tests

To run unit tests for client functionality:
```bash
cd bookstore_client
python test_client.py
```

---

## Notes

- Book data is stored in `books.json` and persists between runs.
- The client validates inputs like price and yes/no prompts.
- The API includes realistic error handling and delay simulation.

---

## Full Documentation

- [Project Overview](docs/index.md)
- [Setup Guide](docs/setup.md)
- [Usage Instructions](docs/usage.md)
- [API Reference](docs/api.md)
- [Testing Guide](docs/testing.md)
---

## Acknowledgements

This project was developed as part of an integration exercise to demonstrate working with REST APIs, client interaction design, and Python development best practices.
