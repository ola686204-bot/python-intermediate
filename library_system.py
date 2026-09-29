"""All-in-one library management system."""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta


# ============================================================
# CUSTOM EXCEPTIONS
# ============================================================

class LibraryError(Exception):
    """Base exception for library-related errors."""


class BookUnavailableError(LibraryError):
    """Raised when a book has no available copies."""


class LoanLimitExceededError(LibraryError):
    """Raised when a member has reached their loan limit."""


# ============================================================
# BOOK CLASS
# ============================================================

class Book:
    """Represent a book in the library catalogue."""

    def __init__(
        self,
        title,
        author,
        isbn,
        genre,
        total_copies,
    ):
        """Initialize a book.

        Args:
            title (str): Book title.
            author (str): Book author.
            isbn (str): Unique ISBN.
            genre (str): Book genre.
            total_copies (int): Total number of copies.
        """
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title must be a non-empty string.")

        if not isinstance(author, str) or not author.strip():
            raise ValueError("Author must be a non-empty string.")

        if not isinstance(isbn, str) or not isbn.strip():
            raise ValueError("ISBN must be a non-empty string.")

        if not isinstance(genre, str) or not genre.strip():
            raise ValueError("Genre must be a non-empty string.")

        if not isinstance(total_copies, int) or total_copies <= 0:
            raise ValueError(
                "Total copies must be a positive integer."
            )

        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()
        self.genre = genre.strip()
        self.total_copies = total_copies
        self.available_copies = total_copies

    @property
    def is_available(self):
        """Return True when at least one copy is available."""
        return self.available_copies > 0

    def checkout(self):
        """Check out one copy of the book.

        Raises:
            BookUnavailableError: If no copies are available.
        """
        if not self.is_available:
            raise BookUnavailableError(
                f"'{self.title}' has no available copies."
            )

        self.available_copies -= 1

    def return_book(self):
        """Return one copy of the book."""
        if self.available_copies >= self.total_copies:
            raise LibraryError(
                f"All copies of '{self.title}' are already available."
            )

        self.available_copies += 1

    def __str__(self):
        """Return a readable string representation."""
        return (
            f"{self.title} by {self.author} "
            f"(ISBN: {self.isbn})"
        )

    def __repr__(self):
        """Return a detailed representation."""
        return (
            f"Book(title={self.title!r}, "
            f"author={self.author!r}, "
            f"isbn={self.isbn!r}, "
            f"genre={self.genre!r}, "
            f"total_copies={self.total_copies!r}, "
            f"available_copies={self.available_copies!r})"
        )

    def __eq__(self, other):
        """Compare books using their ISBN."""
        if not isinstance(other, Book):
            return NotImplemented

        return self.isbn == other.isbn


# ============================================================
# MEMBER ABSTRACT BASE CLASS
# ============================================================

class Member(ABC):
    """Abstract base class for library members."""

    def __init__(
        self,
        member_id,
        name,
        email,
        membership_tier,
    ):
        """Initialize a library member.

        Args:
            member_id (str): Unique member ID.
            name (str): Member name.
            email (str): Member email.
            membership_tier (str): Membership level.
        """
        if not isinstance(member_id, str) or not member_id.strip():
            raise ValueError(
                "Member ID must be a non-empty string."
            )

        if not isinstance(name, str) or not name.strip():
            raise ValueError(
                "Name must be a non-empty string."
            )

        if not isinstance(email, str) or not email.strip():
            raise ValueError(
                "Email must be a non-empty string."
            )

        self.member_id = member_id.strip()
        self.name = name.strip()
        self.email = email.strip()
        self.membership_tier = membership_tier

    @property
    @abstractmethod
    def loan_duration_days(self):
        """Return the number of days a member may borrow a book."""

    @property
    @abstractmethod
    def fine_per_day(self):
        """Return the fine charged per overdue day."""

    @property
    @abstractmethod
    def loan_limit(self):
        """Return the maximum number of active loans."""

    def __str__(self):
        """Return a readable member representation."""
        return (
            f"{self.name} ({self.member_id}) - "
            f"{self.membership_tier}"
        )

    def __repr__(self):
        """Return a detailed member representation."""
        return (
            f"{self.__class__.__name__}("
            f"member_id={self.member_id!r}, "
            f"name={self.name!r}, "
            f"email={self.email!r})"
        )


# ============================================================
# BASIC MEMBER
# ============================================================

class BasicMember(Member):
    """Represent a basic library member."""

    def __init__(self, member_id, name, email):
        """Initialize a basic member."""
        super().__init__(
            member_id,
            name,
            email,
            "Basic",
        )

    @property
    def loan_duration_days(self):
        """Return the basic member loan duration."""
        return 14

    @property
    def fine_per_day(self):
        """Return the basic member daily fine."""
        return 50

    @property
    def loan_limit(self):
        """Return the basic member loan limit."""
        return 3


# ============================================================
# PREMIUM MEMBER
# ============================================================

class PremiumMember(Member):
    """Represent a premium library member."""

    def __init__(self, member_id, name, email):
        """Initialize a premium member."""
        super().__init__(
            member_id,
            name,
            email,
            "Premium",
        )

    @property
    def loan_duration_days(self):
        """Return the premium member loan duration."""
        return 21

    @property
    def fine_per_day(self):
        """Return the premium member daily fine."""
        return 30

    @property
    def loan_limit(self):
        """Return the premium member loan limit."""
        return 5


# ============================================================
# LOAN CLASS
# ============================================================

class Loan:
    """Represent a book borrowed by a library member."""

    def __init__(self, book, member, borrow_date):
        """Initialize a loan.

        Args:
            book (Book): Book being borrowed.
            member (Member): Member borrowing the book.
            borrow_date (datetime): Date and time of borrowing.
        """
        if not isinstance(book, Book):
            raise TypeError("book must be a Book object.")

        if not isinstance(member, Member):
            raise TypeError(
                "member must be a Member object."
            )

        if not isinstance(borrow_date, datetime):
            raise TypeError(
                "borrow_date must be a datetime object."
            )

        self.book = book
        self.member = member
        self.borrow_date = borrow_date
        self.return_date = None

    @property
    def due_date(self):
        """Calculate and return the loan due date."""
        return self.borrow_date + timedelta(
            days=self.member.loan_duration_days
        )

    @property
    def is_overdue(self):
        """Return True if the active loan is overdue."""
        if self.return_date is not None:
            return False

        return datetime.now() > self.due_date

    @property
    def days_overdue(self):
        """Return the number of days the loan is overdue."""
        if not self.is_overdue:
            return 0

        difference = datetime.now() - self.due_date
        return difference.days

    @property
    def fine_amount(self):
        """Calculate the current overdue fine."""
        return self.days_overdue * self.member.fine_per_day

    def __str__(self):
        """Return a readable loan representation."""
        status = "Returned" if self.return_date else "Active"

        return (
            f"{self.book.title} -> {self.member.name} "
            f"(Due: {self.due_date.strftime('%Y-%m-%d')}, "
            f"Status: {status})"
        )

    def __repr__(self):
        """Return a detailed loan representation."""
        return (
            f"Loan(book={self.book!r}, "
            f"member={self.member!r}, "
            f"borrow_date={self.borrow_date!r})"
        )


# ============================================================
# LIBRARY CLASS
# ============================================================

class Library:
    """Manage books, members, and loans."""

    def __init__(
        self,
        name,
        catalogue=None,
        members=None,
        loans=None,
    ):
        """Initialize a library.

        Args:
            name (str): Library name.
            catalogue (dict, optional): ISBN-to-book dictionary.
            members (dict, optional): ID-to-member dictionary.
            loans (list, optional): List of loans.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError(
                "Library name must be a non-empty string."
            )

        self.name = name.strip()
        self.catalogue = catalogue if catalogue is not None else {}
        self.members = members if members is not None else {}
        self.loans = loans if loans is not None else []

    @classmethod
    def from_config(cls, config_dict):
        """Create a Library object from a configuration dictionary.

        Args:
            config_dict (dict): Configuration data.

        Returns:
            Library: A configured library instance.
        """
        if not isinstance(config_dict, dict):
            raise TypeError("Configuration must be a dictionary.")

        name = config_dict.get("name")

        if not name:
            raise ValueError(
                "Configuration must contain a library name."
            )

        return cls(name)

    def add_book(self, book):
        """Add a book to the library catalogue.

        Args:
            book (Book): Book to add.

        Raises:
            LibraryError: If the ISBN already exists.
        """
        if not isinstance(book, Book):
            raise TypeError("book must be a Book object.")

        if book.isbn in self.catalogue:
            raise LibraryError(
                f"A book with ISBN {book.isbn} already exists."
            )

        self.catalogue[book.isbn] = book

    def register_member(self, member):
        """Register a member.

        Args:
            member (Member): Member to register.

        Raises:
            LibraryError: If the member ID already exists.
        """
        if not isinstance(member, Member):
            raise TypeError(
                "member must be a Member object."
            )

        if member.member_id in self.members:
            raise LibraryError(
                f"Member ID {member.member_id} already exists."
            )

        self.members[member.member_id] = member

    def _get_member(self, member_id):
        """Find a member by ID."""
        if member_id not in self.members:
            raise LibraryError(
                f"Member {member_id} was not found."
            )

        return self.members[member_id]

    def _get_book(self, isbn):
        """Find a book by ISBN."""
        if isbn not in self.catalogue:
            raise LibraryError(
                f"Book with ISBN {isbn} was not found."
            )

        return self.catalogue[isbn]

    def _active_loans_for_member(self, member_id):
        """Return all active loans for a member."""
        return [
            loan
            for loan in self.loans
            if (
                loan.member.member_id == member_id
                and loan.return_date is None
            )
        ]

    def borrow_book(self, member_id, isbn):
        """Borrow a book for a member.

        Args:
            member_id (str): Member ID.
            isbn (str): Book ISBN.

        Raises:
            LoanLimitExceededError: If member reached their limit.
            BookUnavailableError: If no copy is available.
            LibraryError: If member or book does not exist.

        Returns:
            Loan: The newly created loan.
        """
        member = self._get_member(member_id)
        book = self._get_book(isbn)

        active_loans = self._active_loans_for_member(
            member_id
        )

        if len(active_loans) >= member.loan_limit:
            raise LoanLimitExceededError(
                f"{member.name} has reached the "
                f"{member.loan_limit}-book loan limit."
            )

        if not book.is_available:
            raise BookUnavailableError(
                f"'{book.title}' has no available copies."
            )

        # Prevent the same member from borrowing
        # the same book twice at the same time.
        for loan in active_loans:
            if loan.book.isbn == isbn:
                raise LibraryError(
                    "This member already has an active "
                    "loan for this book."
                )

        book.checkout()

        loan = Loan(
            book=book,
            member=member,
            borrow_date=datetime.now(),
        )

        self.loans.append(loan)

        return loan

    def return_book(self, member_id, isbn):
        """Return a book borrowed by a member.

        Args:
            member_id (str): Member ID.
            isbn (str): Book ISBN.

        Returns:
            Loan: The returned loan.

        Raises:
            LibraryError: If no matching active loan exists.
        """
        self._get_member(member_id)
        book = self._get_book(isbn)

        for loan in self.loans:
            if (
                loan.member.member_id == member_id
                and loan.book.isbn == isbn
                and loan.return_date is None
            ):
                loan.return_date = datetime.now()
                book.return_book()
                return loan

        raise LibraryError(
            "No active loan was found for this member and book."
        )

    def get_overdue_loans(self):
        """Return all currently overdue loans.

        Returns:
            list: List of overdue Loan objects.
        """
        return [
            loan
            for loan in self.loans
            if loan.is_overdue
        ]

    def generate_report(self):
        """Generate a report describing the library.

        Returns:
            str: Formatted library report.
        """
        active_loans = [
            loan
            for loan in self.loans
            if loan.return_date is None
        ]

        overdue_loans = self.get_overdue_loans()

        total_fines = sum(
            loan.fine_amount
            for loan in overdue_loans
        )

        lines = [
            "",
            "=" * 60,
            f"LIBRARY REPORT - {self.name}",
            "=" * 60,
            f"Books in catalogue: {len(self.catalogue)}",
            f"Registered members: {len(self.members)}",
            f"Total loans: {len(self.loans)}",
            f"Active loans: {len(active_loans)}",
            f"Overdue loans: {len(overdue_loans)}",
            f"Outstanding fines: ₦{total_fines:,.2f}",
            "",
            "BOOKS:",
        ]

        if self.catalogue:
            for book in self.catalogue.values():
                lines.append(
                    f"- {book.title} | "
                    f"ISBN: {book.isbn} | "
                    f"Available: "
                    f"{book.available_copies}/"
                    f"{book.total_copies}"
                )
        else:
            lines.append("- No books registered.")

        lines.append("")
        lines.append("MEMBERS:")

        if self.members:
            for member in self.members.values():
                member_loans = self._active_loans_for_member(
                    member.member_id
                )

                lines.append(
                    f"- {member.name} | "
                    f"ID: {member.member_id} | "
                    f"Tier: {member.membership_tier} | "
                    f"Active loans: {len(member_loans)}/"
                    f"{member.loan_limit}"
                )
        else:
            lines.append("- No members registered.")

        lines.append("=" * 60)

        return "\n".join(lines)

    def __len__(self):
        """Return the number of books in the catalogue."""
        return len(self.catalogue)

    def __contains__(self, isbn):
        """Check whether an ISBN exists in the catalogue."""
        return isbn in self.catalogue


# ============================================================
# INPUT VALIDATION FUNCTIONS
# ============================================================

def get_non_empty_input(prompt):
    """Get a non-empty string from the user.

    Args:
        prompt (str): Input prompt.

    Returns:
        str: Validated user input.
    """
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("Input cannot be empty.")


def get_positive_integer(prompt):
    """Get a positive integer from the user.

    Args:
        prompt (str): Input prompt.

    Returns:
        int: Positive integer entered by the user.
    """
    while True:
        value = input(prompt).strip()

        try:
            number = int(value)

            if number <= 0:
                print("Please enter a positive number.")
                continue

            return number

        except ValueError:
            print("Please enter a valid whole number.")


def get_membership_type():
    """Get a valid membership type from the user.

    Returns:
        str: Either 'basic' or 'premium'.
    """
    while True:
        membership = input(
            "Membership type (basic/premium): "
        ).strip().lower()

        if membership in ("basic", "premium"):
            return membership

        print("Please enter 'basic' or 'premium'.")


# ============================================================
# DISPLAY FUNCTIONS
# ============================================================

def display_books(library):
    """Display all books in the library."""
    if not library.catalogue:
        print("\nNo books have been added yet.")
        return

    print("\n" + "=" * 70)
    print("BOOK CATALOGUE")
    print("=" * 70)

    for book in library.catalogue.values():
        print(f"Title: {book.title}")
        print(f"Author: {book.author}")
        print(f"ISBN: {book.isbn}")
        print(f"Genre: {book.genre}")
        print(
            f"Copies: {book.available_copies}/"
            f"{book.total_copies}"
        )
        print(
            f"Available: "
            f"{'Yes' if book.is_available else 'No'}"
        )
        print("-" * 70)


def display_members(library):
    """Display all registered members."""
    if not library.members:
        print("\nNo members have been registered yet.")
        return

    print("\n" + "=" * 70)
    print("REGISTERED MEMBERS")
    print("=" * 70)

    for member in library.members.values():
        active_loans = library._active_loans_for_member(
            member.member_id
        )

        print(f"Name: {member.name}")
        print(f"Member ID: {member.member_id}")
        print(f"Email: {member.email}")
        print(f"Tier: {member.membership_tier}")
        print(
            f"Active loans: "
            f"{len(active_loans)}/{member.loan_limit}"
        )
        print(
            f"Loan duration: "
            f"{member.loan_duration_days} days"
        )
        print(
            f"Fine per day: "
            f"₦{member.fine_per_day}"
        )
        print("-" * 70)


def display_overdue_loans(library):
    """Display all overdue loans."""
    overdue_loans = library.get_overdue_loans()

    if not overdue_loans:
        print("\nThere are no overdue loans.")
        return

    print("\n" + "=" * 70)
    print("OVERDUE LOANS")
    print("=" * 70)

    for loan in overdue_loans:
        print(f"Book: {loan.book.title}")
        print(f"Member: {loan.member.name}")
        print(f"Member ID: {loan.member.member_id}")
        print(
            f"Due date: "
            f"{loan.due_date.strftime('%Y-%m-%d')}"
        )
        print(f"Days overdue: {loan.days_overdue}")
        print(f"Fine: ₦{loan.fine_amount:,.2f}")
        print("-" * 70)


# ============================================================
# CLI ACTIONS
# ============================================================

def add_book_cli(library):
    """Handle adding a book through the CLI."""
    print("\n--- ADD BOOK ---")

    title = get_non_empty_input("Title: ")
    author = get_non_empty_input("Author: ")
    isbn = get_non_empty_input("ISBN: ")
    genre = get_non_empty_input("Genre: ")
    total_copies = get_positive_integer(
        "Total copies: "
    )

    try:
        book = Book(
            title,
            author,
            isbn,
            genre,
            total_copies,
        )

        library.add_book(book)

        print(
            f"\nBook '{book.title}' added successfully."
        )

    except (ValueError, LibraryError, TypeError) as error:
        print(f"\nError: {error}")


def register_member_cli(library):
    """Handle member registration through the CLI."""
    print("\n--- REGISTER MEMBER ---")

    member_id = get_non_empty_input("Member ID: ")
    name = get_non_empty_input("Name: ")
    email = get_non_empty_input("Email: ")
    membership = get_membership_type()

    try:
        if membership == "basic":
            member = BasicMember(
                member_id,
                name,
                email,
            )
        else:
            member = PremiumMember(
                member_id,
                name,
                email,
            )

        library.register_member(member)

        print(
            f"\nMember '{member.name}' registered "
            "successfully."
        )

    except (ValueError, LibraryError, TypeError) as error:
        print(f"\nError: {error}")


def borrow_book_cli(library):
    """Handle book borrowing through the CLI."""
    print("\n--- BORROW BOOK ---")

    member_id = get_non_empty_input("Member ID: ")
    isbn = get_non_empty_input("Book ISBN: ")

    try:
        loan = library.borrow_book(
            member_id,
            isbn,
        )

        print("\nBook borrowed successfully.")
        print(f"Book: {loan.book.title}")
        print(f"Member: {loan.member.name}")
        print(
            f"Borrow date: "
            f"{loan.borrow_date.strftime('%Y-%m-%d')}"
        )
        print(
            f"Due date: "
            f"{loan.due_date.strftime('%Y-%m-%d')}"
        )

    except (
        LibraryError,
        BookUnavailableError,
        LoanLimitExceededError,
    ) as error:
        print(f"\nError: {error}")


def return_book_cli(library):
    """Handle returning a book through the CLI."""
    print("\n--- RETURN BOOK ---")

    member_id = get_non_empty_input("Member ID: ")
    isbn = get_non_empty_input("Book ISBN: ")

    try:
        loan = library.return_book(
            member_id,
            isbn,
        )

        print("\nBook returned successfully.")
        print(f"Book: {loan.book.title}")
        print(f"Member: {loan.member.name}")

        if loan.fine_amount > 0:
            print(
                f"Overdue fine: "
                f"₦{loan.fine_amount:,.2f}"
            )
        else:
            print("No overdue fine.")

    except LibraryError as error:
        print(f"\nError: {error}")


# ============================================================
# MAIN MENU
# ============================================================

def display_menu():
    """Display the main library menu."""
    print("\n")
    print("=" * 50)
    print("LIBRARY MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. Add Book")
    print("2. Register Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. View Overdue Loans")
    print("6. Generate Library Report")
    print("7. Exit")
    print("=" * 50)


def main():
    """Run the library management system."""
    config = {
        "name": "Community Library"
    }

    library = Library.from_config(config)

    print("=" * 50)
    print(f"Welcome to {library.name}")
    print("=" * 50)

    while True:
        display_menu()

        choice = input("Choose an option (1-7): ").strip()

        try:
            if choice == "1":
                add_book_cli(library)

            elif choice == "2":
                register_member_cli(library)

            elif choice == "3":
                borrow_book_cli(library)

            elif choice == "4":
                return_book_cli(library)

            elif choice == "5":
                display_overdue_loans(library)

            elif choice == "6":
                print(library.generate_report())

            elif choice == "7":
                print("\nThank you for using the library system.")
                break

            else:
                print(
                    "\nInvalid choice. "
                    "Please select a number from 1 to 7."
                )

        except Exception as error:
            # Prevent unexpected input/runtime errors
            # from crashing the CLI.
            print(f"\nUnexpected error: {error}")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
