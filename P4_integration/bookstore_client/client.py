#!/usr/bin/env python3
"""
Bookstore Client

A client application for interacting with the Bookstore API.
This client is intentionally incomplete and contains TODOs for implementation.
"""
import requests
import json
from tabulate import tabulate
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Constants
API_BASE_URL = "http://localhost:5000/api"
BOOKS_ENDPOINT = f"{API_BASE_URL}/books"

# Helper functions for formatting output
def print_success(message):
    """Print a success message in green."""
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

def print_error(message):
    """Print an error message in red."""
    print(f"{Fore.RED}Error: {message}{Style.RESET_ALL}")

def print_info(message):
    """Print an info message in blue."""
    print(f"{Fore.BLUE}{message}{Style.RESET_ALL}")

def format_book_table(books):
    """Format a list of books as a table."""
    if not books:
        return "No books found."
    
    # Convert single book to list if needed
    if isinstance(books, dict):
        books = [books]
    
    headers = ["ID", "Title", "Author", "Price", "In Stock"]
    rows = [
        [
            book.get("id", "N/A"),
            book.get("title", "N/A"),
            book.get("author", "N/A"),
            f"${book.get('price', 0):.2f}",
            "Yes" if book.get("in_stock", False) else "No"
        ]
        for book in books
    ]
    
    return tabulate(rows, headers=headers, tablefmt="grid")

# API client functions

def get_all_books():
    """Retrieve all books from the API."""
    try:
        response = requests.get(BOOKS_ENDPOINT)
        response.raise_for_status()
        books = response.json()
        return books
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to retrieve books: {e}")
        return []

def display_all_books():
    """Display all books in a formatted table."""
    print_info("Fetching all books...")
    books = get_all_books()
    print(format_book_table(books))

def get_book_by_id(book_id):
    """
    Retrieve a specific book by ID.
    
    Parameters:
        book_id (str): The ID of the book to retrieve
        
    Returns:
        dict: The book data if found, None otherwise
    """
    try:
        response = requests.get(f"{BOOKS_ENDPOINT}/{book_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        # Try to access status code from the error's response object
        if hasattr(http_err, 'response') and http_err.response is not None and http_err.response.status_code == 404:
            print_error("Book not found.")
        else:
            print_error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to retrieve book: {e}")
    return None

def display_book_details():
    """Display details for a specific book."""
    book_id = input("Enter book ID: ")
    
    book = get_book_by_id(book_id)
    if book:
        print(format_book_table(book))

def add_book():
    """
    Add a new book to the bookstore.
    
    Gather book details from the user and send them to the API.
    """
    title = input("Enter the book title: ").strip()
    author = input("Enter the book author: ").strip()
    price = input("Enter the book price: ").strip()
    
    # Validate in-stock input until y or n
    while True:
        in_stock_input = input("Is the book in stock? (yes/no): ").strip().lower()
        if in_stock_input in ("yes", "no", "y", "n"):
            break
        else:
            print("Please enter 'yes' or 'no'.")

    # Validate the title, author and price have values
    if not title or not author or not price:
        print_error("Title, author, and price are required fields.")
        return
    
    #Validate price is correct format
    try:
        price = float(price)
        if price < 0:
            raise ValueError("Price cannot be negative.")
    except ValueError:
        print_error("Invalid price. Please enter a valid number.")
        return

    # Prepare the data to be sent to the API
    new_book_data = {
        "title": title,
        "author": author,
        "price": price,
        "in_stock": in_stock_input
    }

    try:
        response = requests.post(BOOKS_ENDPOINT, json=new_book_data)
        response.raise_for_status()
        new_book = response.json()
        print_success(f"Book added successfully: {new_book['title']} by {new_book['author']}")
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to add book: {e}")

def update_book():
    """
    Update an existing book's information.
    
    Retrieve the current book information and allow the user to modify it.
    """
    book_id = input("Enter the ID of the book to update: ").strip()
    if not book_id:
        print_error("Book ID is required.")
        return

    book = get_book_by_id(book_id)
    if not book:
        print_error("Book not found.")
        return

    print_info("Leave input blank to keep existing value.")
    new_title = input(f"Title [{book['title']}]: ").strip()
    new_author = input(f"Author [{book['author']}]: ").strip()
    new_price_input = input(f"Price [{book['price']}]: ").strip()
    new_in_stock_input = input(f"In stock? (y/n) [{ 'y' if book['in_stock'] else 'n' }]: ").strip().lower()

    # Validate input IF entered
    if(new_price_input):
        try:
            price = float(new_price_input)
            if price < 0:
                raise ValueError("Price cannot be negative.")
        except ValueError:
            print_error("Invalid price. Please enter a valid number.")
        return

    if(new_in_stock_input):
        while True:
            if new_in_stock_input in ("yes", "no", "y", "n"):
                break
            else:
                print("Please enter 'yes' or 'no'.")
                new_in_stock_input = input(f"In stock? (y/n) [{ 'y' if book['in_stock'] else 'n' }]: ").strip().lower()


    # Use existing values if nothing entered
    updated_data = {
        "title": new_title if new_title else book["title"],
        "author": new_author if new_author else book["author"],
        "price": float(new_price_input) if new_price_input else book["price"],
        "in_stock": (
            book["in_stock"] if new_in_stock_input == ""
            else new_in_stock_input in ("y", "yes")
        )
    }

    try:
        response = requests.put(f"{BOOKS_ENDPOINT}/{book_id}", json=updated_data)
        response.raise_for_status()
        updated_book = response.json()
        print_success("Book updated successfully!")
        print(format_book_table(updated_book))
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to update book: {e}")

def delete_book():
    """
    Delete a book from the bookstore.
    
    Ask for confirmation before deleting.
    """
    book_id = input("Enter the ID of the book to delete: ").strip()
    if not book_id:
        print_error("Book ID is required.")
        return

    book = get_book_by_id(book_id)
    if not book:
        print_error("Book not found.")
        return

    # Confirmation to delete 
    print(format_book_table(book))
    confirm = input("Are you sure you want to delete this book? (y/n): ").strip().lower()
    if confirm not in ("y", "yes"):
        print_info("Delete operation cancelled.")
        return

    try:
        response = requests.delete(f"{BOOKS_ENDPOINT}/{book_id}")
        response.raise_for_status()
        print_success(f"Book with ID {book_id} deleted successfully.")
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to delete book: {e}")

def search_books():
    """
    Search for books by title or author.
    
    Send a search query to the API and display the results.
    """
    query = input("Enter a keyword to search by title or author: ").strip()
    if not query:
        print_error("Search query cannot be empty.")
        return

    try:
        response = requests.get(f"{BOOKS_ENDPOINT}/search", params={"query": query})
        response.raise_for_status()
        results = response.json()

        if results:
            print_success(f"Found {len(results)} matching book(s):")
            print(format_book_table(results))
        else:
            print_info("No books matched your search.")
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to perform search: {e}")

def display_menu():
    """Display the main menu options."""
    print("\n" + "=" * 50)
    print("             BOOKSTORE CLIENT              ")
    print("=" * 50)
    print("1. View All Books")
    print("2. View Book Details")
    print("3. Add New Book")
    print("4. Update Book")
    print("5. Delete Book")
    print("6. Search Books")
    print("7. Exit")
    print("=" * 50)

def main():
    """Main application function."""
    try:
        while True:
            display_menu()
            choice = input("Enter your choice (1-7): ")
            
            if choice == "1":
                display_all_books()
            elif choice == "2":
                display_book_details()
            elif choice == "3":
                add_book()
            elif choice == "4":
                update_book()
            elif choice == "5":
                delete_book()
            elif choice == "6":
                search_books()
            elif choice == "7":
                print_info("Exiting Bookstore Client. Goodbye!")
                break
            else:
                print_error("Invalid choice. Please enter a number between 1 and 7.")
            
            input("\nPress Enter to continue...")
            
    except KeyboardInterrupt:
        print_info("\nApplication terminated by user.")
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 