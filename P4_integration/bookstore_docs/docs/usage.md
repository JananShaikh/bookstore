# Usage Guide

Once you run the client, you'll see a menu like:

```
1. View All Books
2. View Book Details
3. Add New Book
4. Update Book
5. Delete Book
6. Search Books
7. Exit
```

---

## Commands

### View All Books

- Shows all books in a table
- Data comes from API `/api/books`

### View Book by ID

- Prompts for book ID
- Displays details or error if not found

### Add Book

- Requires title, author, price
- Validates yes/no input for stock

### Update Book

- Prompts for ID and shows current values
- User can modify or keep existing ones

### Delete Book

- Prompts for ID
- Requires confirmation (`yes` or `no`)

### Search Books

- Search by keyword (in title or author)
- Shows matches in table format
