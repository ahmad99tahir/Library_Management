from Library import Library
import threading
import time
from Book import Book,FictionBook,NonFictionBook
from Borrower import Borrower
from helpers import validate_isbn,log_timestamp,concurrent_borrow_return

def main_menu(library):
    while True:
        print("\n*** Library Management System Menu ***")
        print("1. Add a book")
        print("2. Add a borrower")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Print inventory")
        print("6. Print borrowers")
        print("7. Search for a book by its title")
        print("8. Search for a book by its isbn")
        print("9. Save inventory to file")
        print("10. Load inventory from file")
        print("11. Save borrowers to file")
        print("12. Load borrowers from file")
        print("13. Average books borrowed per borrower")
        print("14. Simulate Concurrent Borrow Return")
        print("15. Exit")

        choice = input("Enter your choice (1-15): ")

        if choice == "1":
            add_book_menu(library)
        elif choice == "2":
            add_borrower_menu(library)
        elif choice == "3":
            borrow_book_menu(library)
        elif choice == "4":
            return_book_menu(library)
        elif choice == "5":
            library.print_books()
        elif choice == "6":
            print_borrowers_menu(library)
        elif choice == "7":
            search_book_title(library)
        elif choice == "8":
            search_book_isbn(library)    
        elif choice == "9":
            save_inventory_menu(library)
        elif choice == "10":
            load_inventory_menu(library)
        elif choice == "11":
            save_borrowers_menu(library)
        elif choice == "12":
            load_borrowers_menu(library)
        elif choice == "13":
            print("Average books borrowed per borrower:", library.average_books_borrowed_per_borrower())
        elif choice == "14":
            simulate_concurrent_actions(library)
        elif choice == "15":
            print("Exiting the Library Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 15.")


def get_formatted_name():
    """Ask the user to enter a borrower's name and change it into the appropriate format.

    Returns:
        str: The formatted name entered by the user.
    """
    full_name = input("Enter Borrower Name: ") 
    parts = full_name.split() #Seperate the words
    capitalized = [part.capitalize() for part in parts] #Capitalize the first letter of every word
    formatted_name = ' '.join(capitalized) #join the words back together
    return formatted_name

def get_formatted_address():
    """Ask the user to enter a borrower's address and change it into the appropriate format.

    Returns:
        str: The formatted name entered by the user.
    """
    address = input("Enter Borrower Address: ")
    parts = address.split() #Seperate the words
    capitalized = [part.capitalize() for part in parts] #Capitalize the first letter of every word
    formatted_address = ' '.join(capitalized) #join the words back together
    return formatted_address

def get_formatted_title():
    """Ask the user to enter the book title and change it into the appropriate format.

    Returns:
        str: The formatted name entered by the user.
    """
    title = input("Enter Book Title: ")
    parts = title.split() #Seperate the words
    capitalized = [part.capitalize() for part in parts] #Capitalize the first letter of every word
    formatted_title = ' '.join(capitalized) #join the words back together
    return formatted_title

def get_formatted_author():
    """Ask the user to enter the author's name and change it into the appropriate format.

    Returns:
        str: The formatted name entered by the user.
    """
    author = input("Enter Author's Name: ")
    parts = author.split() #Seperate the words
    capitalized = [part.capitalize() for part in parts] #Capitalize the first letter of every word
    formatted_author = ' '.join(capitalized) #join the words back together
    return formatted_author

def add_book_menu(library):
    """Menu for adding a book to the library.

    Args:
        library (Library): Instance of the library.

    Returns:
        None
    """
    title = get_formatted_title()
    author = get_formatted_author()

    while True:
        isbn = input("Enter the ISBN of the book (format: xxx-xx-xxxxx-xx-x): ")
        if validate_isbn(isbn):
            break
        else:
            print("Invalid ISBN format. Please enter a valid ISBN.")

    while True:
        try:
            quantity_available = int(input("Enter the quantity available: "))
            if quantity_available < 0:
                raise ValueError("Quantity can not be a negative number.")
            break
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid quantity.")

    while True:
        book_type = input("Enter the type of book (Fiction or Non-Fiction): ").lower()
        if book_type in {"fiction", "non-fiction"}:
            break
        else:
            print("Invalid book type. Please enter either 'Fiction' or 'Non-Fiction'.")
    
    #Seperating the books into their sub-classes
    if validate_isbn(isbn):
        if book_type == "fiction":
            genre = input("Enter the genre of the book (format: First Last): ")
            fiction_book = FictionBook(title, author, isbn, quantity_available, genre)
            library.add_book(fiction_book)
        elif book_type == "non-fiction":
            subject = input("Enter the subject of the book (format: First Last):")
            non_fiction_book = NonFictionBook(title, author, isbn, quantity_available, subject)
            library.add_book(non_fiction_book)
        else:
            print("Invalid book type, please enter either 'Fiction' or 'Non-Fiction'. Book not added to inventory.")
    else:
        print("Invalid ISBN, book not added to inventory.")

def add_borrower_menu(library):
    """Menu for adding a borrower to the library.

    Args:
        library (Library): Instance of the library.

    Returns:
        None
    """
    name = get_formatted_name()
    address = get_formatted_address()
    new_borrower = Borrower(name, address)
    library.add_borrower(new_borrower)

def borrow_book_menu(library):
    """Menu for Borrowing a book from the library.

    Args:
        library (Library): Instance of the library.

    Returns:
        None
    """
    borrower_name = get_formatted_name()
    borrower_address = get_formatted_address()

    borrower = next((b for b in library.borrowers if b.name == borrower_name and b.address == borrower_address), None) #check if borrower is present in library

    if borrower: 
        title = get_formatted_title()
        isbn = input("Enter ISBN of the book to borrow (format: xxx-xx-xxxxx-xx-x):") 
        book = next((book for book in library.books if book.title == title and book.isbn == isbn), None) #check if book is present in library

        if book:
            library.borrow_book(borrower, book)
        else:
            print("Book not found in the inventory.")
    else:
        print("Borrower not found. Please register using the 'Add a borrower' option.")

def return_book_menu(library):
    """Menu for returning a book to the library.

    Args:
        library (Library): Instance of the library.

    Returns:
        None
    """
    borrower_name = get_formatted_name()
    borrower_address = get_formatted_address()
    borrower = next((b for b in library.borrowers if b.name == borrower_name and b.address == borrower_address), None) #check if borrower is present in library

    if borrower:
        title = get_formatted_title()
        isbn = input("Enter the ISBN of the book to return (format: xxx-xx-xxxxx-xx-x): ")
        book = next((book for book in borrower.borrowed_books if book.title == title and book.isbn == isbn), None) #check if the user has borrowed this book or not.

        if book:
            library.return_book(borrower, book)
        else:
            print("Book not found in the borrowed books list.")
    else:
        print("Borrower not found.")

def print_borrowers_menu(library):
    for borrower in library.borrowers:
        print(borrower.info())

def save_inventory_menu(library):
    """Menu for saving the library inventory into a CSV file.

    Args:
        library (Library): Instance of the library.

    Returns:
        None
    """
    filename = input("Enter the filename to save the inventory (format: Filename.csv): ")
    library.save_inventory(filename)
    print("Inventory saved to", filename)

def load_inventory_menu(library):
    """Menu for loading the library inventory from a CSV file.

    Args:
        library (Library): Instance of the library.

    Returns:
        None
    """
    filename = input("Enter the filename to load the inventory: (format: Filename.csv): ")

    try:
        library.load_inventory(filename)
        print("Inventory loaded from", filename)
    except FileNotFoundError:
        print("Sorry this file can not be found.")

def save_borrowers_menu(library):
    """Menu for saving the borrower's list into a CSV file.

    Args:
        library (Library): Instance of the library.

    Returns:
        None
    """
    filename = input("Enter the filename to save the borrowers (format: Filename.csv): ")
    library.save_borrowers(filename)
    print("Borrowers saved to", filename)

def load_borrowers_menu(library):
    """Menu for loading the borrower's list from a CSV file.

    Args:
        library (Library): Instance of the library.

    Returns:
        None
    """
    filename = input("Enter the filename to load the borrowers (format: Filename.csv): ")

    try:
        library.load_borrowers(filename)
        print("Borrowers loaded from", filename)
    except FileNotFoundError:
        print("Sorry this file can not be found.")

def simulate_concurrent_actions(library):
    """Simulate concurrent borrow and return actions for a specific borrower and book.
    Ask the user to enter the number of concurrent borrow and return actions to simulate.
    Ask the user to enter the borrower's name and address, and the book title.
    It creates two threads for concurrent borrowing and returning, and prints the result.

    Args:
        library (Library): The library instance.

    Returns:
        None
    """
    num_borrowers = int(input("Enter the number of borrowers to perform simulation: ")) 
    borrow_count = int(input("Enter the number of concurrent borrow actions to simulate: "))
    return_count = int(input("Enter the number of concurrent return actions to simulate: "))

    for _ in range(num_borrowers): #Run the function for the specified borrowers
        borrower_name = get_formatted_name()
        borrower_address = get_formatted_address()

        borrower = next((b for b in library.borrowers if b.name == borrower_name and b.address == borrower_address), None) #check if borrower is registered or not

        if borrower:
            book_title = get_formatted_title()
            isbn = input("Enter the isbn of the book you want to borrow (format: xxx-xx-xxxxx-xx-x): ")
            book = next((book for book in library.books if book.title == book_title and book.isbn == isbn), None) #check if book is in the library.

            if book:
                threads = []

                borrow_thread = threading.Thread(target=concurrent_borrow_return, args=(library, borrower, book, borrow_count, 0)) #Thread for borrowing the book
                return_thread = threading.Thread(target=concurrent_borrow_return, args=(library, borrower, book, 0, return_count)) #Thread for returning the book

                threads.append(borrow_thread)
                threads.append(return_thread)

                for thread in threads:
                    thread.start()

                time.sleep(1) 

                for thread in threads:
                    thread.join() #wait for the other thread to complete

                print("Concurrent borrow and return simulation completed for", borrower_name)
            else:
                print("Book", book_title,"or",isbn, "not found in the inventory.")
        else:
            print("Borrower" ,borrower_name, "not found. Please register using the 'Add a borrower' option.")

def search_book_title(library):
    """Search for a book in the library by its title.

    Args:
        library (Library): The library instance.

    Returns:
        None
    """
    title = get_formatted_title()
    found_books = [book for book in library.books if book.title == title] #check if a book with this title is in library.

    if found_books:
        print(f"Found {len(found_books)} book(s) with the title '{title}':") #print how many books with this title are there.
        for i, book in enumerate(found_books, start=1): #List all the books with this title and print their title and authors.
            print(f"{i}. {book.title} by {book.author}")
    else:
        print(f"No books found with the title '{title}'.")

def search_book_isbn(library):
    """Search for a book in the library by its ISBN.

    Args:
        library (Library): The library instance.

    Returns:
        None
    """
    isbn = input("Enter the ISBN of the book to search (format: xxx-xx-xxxxx-xx-x): ")
    found_books = [book for book in library.books if book.isbn == isbn] #check if book with this isbn is in library.

    if found_books:
        for book in found_books:
            print(f"{book.title} by {book.author}") #if book is there print its title and author.
    else:
        print(f"No books found with the ISBN '{isbn}'.")


if __name__ == "__main__":
    library_system = Library()
    main_menu(library_system)
