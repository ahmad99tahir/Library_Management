from Book import Book,FictionBook,NonFictionBook
from Borrower import Borrower
import csv 
from helpers import log_timestamp

class Library:
    """Class representing a library with books and borrowers."""

    def __init__(self):
        """Initialize an empty library with no books and borrowers."""
        self.books = []
        self.borrowers = []

    def check_copy(self, book):
        """Check if a copy of the given book already exists in the library.

        Args:
            book (Book): The book to check.

        Returns:
            bool: True if a copy is found, otherwise return False.
        """
        for i in self.books:
            if i.isbn == book.isbn and i.title == book.title and i.author == book.author: 
                i.quantity_available += book.quantity_available #Add the quantity_available of the new book to that of the old book if the new book is a copy of the old book.
                return True
            elif i.isbn == book.isbn and (i.title != book.title or i.author != book.author):
                print("We already have a book with this ISBN. It is also possible that you are writing the name and address in the wrong format.") #if the isbn is same but title or author is different it means the input is wrong.
                return True
        else:
          return False

    def add_book(self, book):
        """Add a new book to the library.

        Args:
            book (Book): The book to add.

        Returns:
            None
        """
        check = self.check_copy(book) #if the new book is not a copy of already existing book and is also the input is correct, then add it as a new book.
        if bool(check) is False:
          self.books.append(book)
          print("New Book Added Successfully")

    def add_borrower(self, borrower):
        """Add a new borrower to the library.

        Args:
            borrower (Borrower): The borrower to add.

        Returns:
            None
        """
        for b in self.borrowers:
            if (b.name == borrower.name and b.address == borrower.address): #check if a borrower with this name and address already exists.
                print("We already have a Borrower with the same name and address.")
                return
            
        self.borrowers.append(borrower)
        print("New Borrower Added Successfully")

    @log_timestamp
    def borrow_book(self, borrower, book):
        """Borrow a book from the library.

        Args:
            borrower (Borrower): The borrower borrowing the book.
            book (Book): The book being borrowed.

        Returns:
            None
        """
        if book.quantity_available >= 1: #Make sure that to borrow a book atleast 1 copy should be available in the library.
          if book not in borrower.borrowed_books: #Also the should not have already been borrowed by the user.
            borrower.borrowed_books.append(book)
            book.quantity_available -= 1 #If successfully borrowed by user then reduce the count in library.
            print(borrower.name, "has borrowed" , book.title)
          else:
            print("You already have a copy of this book.")
        else:
          print("Sorry, this book is out of stock")

    @log_timestamp
    def return_book(self, borrower, book):
        """Return a borrowed book to the library.

        Args:
            borrower (Borrower): The borrower returning the book.
            book (Book): The book being returned.

        Returns:
            None
        """
        if book in borrower.borrowed_books: #Check if user has borrowed this book from the library or not.
            borrower.borrowed_books.remove(book) #If yes then let him return it and remove it from his list.
            book.quantity_available += 1 #Add it back to the library's inventory.
            print(borrower.name,"returned",book.title)
        else:
            print(borrower.name,"did not borrow",book.title,"from this Library.")

    def average_books_borrowed_per_borrower(self):
        """Calculate the average number of books borrowed per borrower.

        Returns:
            float: Average number of books borrowed per borrower.
        """
        total_borrowed_books = sum(len(borrower.borrowed_books) for borrower in self.borrowers) #calculate the count of all the books borrowed by all the users
        total_borrowers = len(self.borrowers) #Calculate the total number of users
        return total_borrowed_books / total_borrowers if total_borrowers > 0 else 0 #Calculate average books borrowed per borrower, also avoid zerodivisionerror

    def save_inventory(self, filename):
        """Save the library's inventory to a CSV file.

        Args:
            filename (str): The name of the file to save the inventory to.

        Returns:
            None
        """

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for book in self.books:
                #save the inventory into a csv file, save genre if it is a Fiction Book and subject if it is a NonFiction Book
                writer.writerow([book.title, book.author, book.isbn, book.quantity_available, book.genre if isinstance(book, FictionBook) else (book.subject if isinstance(book, NonFictionBook) else None)])

    def save_borrowers(self, filename):
        """Save the list of borrowers to a CSV file.

        Args:
            filename (str): The name of the file to save the borrowers to.

        Returns:
            None
        """
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for borrower in self.borrowers:
                writer.writerow([borrower.name, borrower.address, ','.join(book.title for book in borrower.borrowed_books)]) #save borrower info into a file

    def load_inventory(self, filename):
        """Load the library's inventory from a CSV file.

        Args:
            filename (str): The name of the file to load the inventory from.

        Returns:
            None
        """
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.add_book(Book(row[0], row[1], row[2], int(row[3]))) #create a book object for all the books loaded from file. 

    def load_borrowers(self, filename):
        """Load the list of borrowers from a CSV file.

        Args:
            filename (str): The name of the file to load the borrowers from.

        Returns:
            None
        """
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                borrower = Borrower(row[0], row[1]) #load a borrower using borrower's title and address 
                borrowed_books = row[2].split(',')
                for title in borrowed_books:
                    book = next((book for book in self.books if book.title == title), None) #Seperate the titles of books and save them into the borrowed books list of the borrower.
                    if book:
                        borrower.borrowed_books.append(book)
                self.add_borrower(borrower)

    def print_books(self):
        """Print the list of Books Available in the Library."""
        print("The books in the inventory are: ")
        for book in self.books:
            if isinstance(book, FictionBook):
                print(book.title, "by", book.author, ", ISBN:" ,book.isbn,", Quantity:" ,book.quantity_available,", Genre:" , book.genre)
            elif isinstance(book, NonFictionBook):
                print(book.title, "by", book.author, ", ISBN:" ,book.isbn,", Quantity:" ,book.quantity_available,", Subject:" , book.subject)
            else:
                print(book.title, "by", book.author, ", ISBN:" ,book.isbn,", Quantity:" ,book.quantity_available)