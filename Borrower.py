class Borrower:
    def __init__(self, name, address):
        """Initialize a Borrower object with a name, address, and an empty list of borrowed books.

        Args:
            name (str): The name of the borrower.
            address (str): The address of the borrower.

        Returns:
            None
        """
        self.name = name
        self.address = address
        self.borrowed_books = []

    def info(self):
        return f"{self.name} ({self.address}) - Borrowed Books: {', '.join(book.title for book in self.borrowed_books)}"