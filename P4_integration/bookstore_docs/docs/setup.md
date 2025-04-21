# Setup Guide

## Requirements

- Python 3.7+
- Pip packages:
  ```
  pip install requests tabulate colorama flask flask-cors
  ```

---

## Folder Structure

```
bookstore_api/
    app.py
    books.json

bookstore_client/
    client.py
    test_client.py
```

---

## Running the Project

### 1. Start the API

```bash
cd bookstore_api
python app.py
```

This launches the Flask server at `http://localhost:5000`.

### 2. Start the Client

In a new terminal:

```bash
cd bookstore_client
python client.py
```
