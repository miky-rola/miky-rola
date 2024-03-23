import csv
from sys import exit

class BookInventory:
    def __init__(self):
        self.books = {}  # Dictionary to store book inventory
        self.filename = "books_inventory.csv"  # CSV file to store inventory data

    # Method to load existing inventory data from CSV file
    def load_inventory(self):
        try:
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.books[row["Title"]] = {"title": row["Title"], "author": row["Author"]}
        except FileNotFoundError:
            print("No existing inventory found. Starting with empty inventory.")

    # Method to save current inventory data to CSV file
    def save_inventory(self):
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Title", "Author"])
            writer.writeheader()
            for book_info in self.books.values():
                writer.writerow({"Title": book_info["title"], "Author": book_info["author"]})



    # Method to list all books in the inventory
    def list_books(self):
        if self.books:
            print("="*10, "List of Books", "="*10)
            for title, book_info in self.books.items():
                print(f"Title: {title}, Author: {book_info['author']}")
        else:
            print("No books available in the inventory.")

    # Method to add a new book to the inventory
    def add_book(self):
        while True:
            title = input("Enter title of book: ").strip().title()
            if title:
                author = input(f"Enter author of the book titled {title}: ")
                if author:
                    if title in self.books:
                        print("Book with this title already exists.")
                        break
                    else:
                        self.books[title] = {"title": title, "author": author}
                        print("Book added successfully.")
                        self.save_inventory()
                        break
                else:
                    print("Author cannot be blank")
                    continue
            else:
                print("Title cannot be blank")
                continue


    # Method to update information of an existing book
    def update_book(self):
        while True:
            title_update = input("Enter the title of the book you want to update: ").strip().title()
            if title_update in self.books:
                new_title = input("Enter the new title (leave blank to keep existing): ").strip().title()
                new_author = input("Enter the new author (leave blank to keep existing): ")
                
                if new_title:
                    self.books[new_title] = self.books.pop(title_update)
                    self.books[new_title]["title"] = new_title
                if new_author:
                    self.books[new_title]["author"] = new_author
                
                print("Book updated successfully.")
                self.save_inventory()
                break
            else:
                print("Book not found.")
                continue

    # Method to display information of a specific book
    def display_book(self):
        while True:
            title = input("Enter the title of the book you want to display: ").strip().title()
            if title in self.books:
                book_info = self.books[title]
                print(f"Title: {title}, Author: {book_info['author']}")
                break
            else:
                print("Book not found.")
                continue

    # Method to delete a book from the inventory
    def delete_book(self):
        title = input("Enter the title of the book you want to delete: ").strip().title()
        if title in self.books:
            confirmation = input(f"Are you sure you want to delete '{title}'? (yes/no): ").strip().lower()
            if confirmation == "yes":
                del self.books[title]
                print("Book deleted successfully.")
                self.save_inventory()
            else:
                print("Deletion canceled.")
        else:
            print("Book not found.")

    # Main method to run the book inventory system
    def main(self):
            self.load_inventory()  # Load existing inventory data
            
            while True:
                user_name = input("Enter your name: ").strip().title()

                if user_name:
                    print(f"Hello {user_name}! Welcome to the book inventory")

                    while True:
                        # Display menu options
                        print("Enter\t 1. To add a new book to the inventory\n2. To update book\n3. To list all books\n4. To display book\n5. To delete book\n6. To exit")
                        user_choice = input("Your choice: ")
                        if user_choice == "1":
                            self.add_book()
                        elif user_choice == "2":
                            self.update_book()
                        elif user_choice == "3":
                            self.list_books()
                        elif user_choice == "4":
                            self.display_book()
                        elif user_choice == "5":
                            self.delete_book()
                        elif user_choice == "6":
                            print("Exiting the book inventory...")
                            self.save_inventory()
                            exit()
                        else:
                            print("Invalid choice. Please enter a valid option.")
                            continue
                else:
                    print("Name cannot be blank")
                    continue


if __name__ == "__main__":
    inventory = BookInventory()
    inventory.main()
