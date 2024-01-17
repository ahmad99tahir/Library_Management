from helpers import validate_isbn

class Book:
    def __init__(self, title, author, isbn, quantity_available):
        """Initialize a Book object with title, author, ISBN, and quantity available.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            isbn (str): The ISBN of the book.
            quantity_available (int): The quantity of the book available in the library.

        Returns:
            None
        """

        if validate_isbn(isbn) is True:
          self.title = title
          self.author = author
          self.isbn = isbn
          self.quantity_available = quantity_available
        else:
          print("Invalid ISBN, can't add this book to inventory")

    def info(self):
        print(self.title , "by " ,self.author, ", ISBN: " ,self.isbn, "In stock:",self.quantity_available)

class FictionBook(Book):
    def __init__(self, title, author, isbn, quantity_available, genre):
        super().__init__(title, author, isbn, quantity_available)
        self.genre = genre

class NonFictionBook(Book):
    def __init__(self, title, author, isbn, quantity_available, subject):
        super().__init__(title, author, isbn, quantity_available)
        self.subject = subject
