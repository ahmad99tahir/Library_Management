import time
import re
from datetime import datetime

def validate_isbn(isbn):
    """Check if the given ISBN follows the format '###-##########'.

    Args:
        isbn (str): The ISBN to validate.

    Returns:
        bool: True if the ISBN is valid, False otherwise.
    """
    pattern = re.compile(r"^\d{3}-\d{2}-\d{5}-\d{2}-\d{1}$") #ISBN standard format is xxx-xx-xxxxx-xx-x
    return bool(pattern.match(isbn)) 

def log_timestamp(func):
    """Decorator to log the timestamp when a function is executed.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.
    """
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = func(*args, **kwargs)
        print(f"[{timestamp}] {func.__name__}  is executed.")
        return result
    return wrapper

def concurrent_borrow_return(library, borrower, book, borrow_count, return_count):
    """Simulate concurrent borrowing and returning of a book by a borrower.

    Args:
        library (Library): Instance of library.
        borrower (Borrower): The borrower borrowing and returning the book.
        book (Book): The book being borrowed and returned.
        borrow_count (int): The number of times the book should be borrowed.
        return_count (int): The number of times the book should be returned.

    Returns:
        None
    """
    for _ in range(borrow_count):
        library.borrow_book(borrower, book)
        time.sleep(1)

    for _ in range(return_count):
        library.return_book(borrower, book)
        time.sleep(1)