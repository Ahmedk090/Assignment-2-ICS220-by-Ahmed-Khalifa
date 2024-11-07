ebook.py
class Ebook:
    """
    Represents an e-book in the catalog with details such as title, author,
    publication date, genre, and price.
    """
    def __init__(self, title, author, publication_date, genre, price):
        self._title = title
        self._author = author
        self._publication_date = publication_date
        self._genre = genre
        self._price = price

    # Getters and Setters
    def get_title(self):
        return self._title

    def set_title(self, title):
        self._title = title

    def get_author(self):
        return self._author

    def set_author(self, author):
        self._author = author

    def get_price(self):
        return self._price

    def set_price(self, price):
        self._price = price

    def __str__(self):
        return f"{self._title} by {self._author}, Genre: {self._genre}, Price: ${self._price}"
catalog.py
class Catalog:
    """
    Catalog to manage a collection of e-books available in the store.
    """
    def __init__(self):
        self._ebooks = []

    def add_ebook(self, ebook):
        """Adds a new e-book to the catalog."""
        self._ebooks.append(ebook)

    def remove_ebook(self, title):
        """Removes an e-book from the catalog by title."""
        self._ebooks = [ebook for ebook in self._ebooks if ebook.get_title() != title]

    def find_ebook(self, title):
        """Finds an e-book by title."""
        for ebook in self._ebooks:
            if ebook.get_title() == title:
                return ebook
        return None
customer.py
class Customer:
    """
    Customer class representing a user with personal details and loyalty status.
    """
    def __init__(self, name, contact_information, is_loyalty_member=False):
        self._name = name
        self._contact_information = contact_information
        self._is_loyalty_member = is_loyalty_member

    # Getters and Setters
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def is_loyalty_member(self):
        return self._is_loyalty_member

    def set_loyalty_member(self, status):
        self._is_loyalty_member = status
shopping_cart.py
class ShoppingCart:
    """
    ShoppingCart class for managing items selected by the customer.
    """
    def __init__(self):
        self._items = []
        self._total_price = 0.0

    def add_to_cart(self, ebook):
        """Adds an e-book to the shopping cart."""
        self._items.append(ebook)
        self._total_price += ebook.get_price()

    def remove_from_cart(self, title):
        """Removes an e-book from the cart by title."""
        for ebook in self._items:
            if ebook.get_title() == title:
                self._items.remove(ebook)
                self._total_price -= ebook.get_price()
                break

    def apply_discounts(self, customer):
        """Applies discounts based on loyalty and bulk purchase."""
        discount = 0.10 if customer.is_loyalty_member() else 0.0
        if len(self._items) >= 5:
            discount += 0.20
        self._total_price -= self._total_price * discount
order.py
from invoice import Invoice

class Order:
    """
    Order class for managing e-books purchased by a customer.
    """
    def __init__(self, customer, order_date):
        self._customer = customer
        self._order_date = order_date
        self._ebooks = []
        self._total_amount = 0.0

    def add_ebook(self, ebook):
        """Adds an e-book to the order."""
        self._ebooks.append(ebook)
        self._total_amount += ebook.get_price()

    def generate_invoice(self):
        """Generates an invoice for the order."""
        return Invoice(self, self._total_amount)
invoice.py
class Invoice:
    """
    Invoice class to generate details of a completed order, including VAT and discounts.
    """
    def __init__(self, order, total_amount):
        self._invoice_number = f"INV-{id(order)}"
        self._items = [(ebook.get_title(), ebook.get_price()) for ebook in order._ebooks]
        discount_amount = total_amount * (0.10 if order._customer.is_loyalty_member() else 0.0)
        discounted_total = total_amount - discount_amount
        self._VAT = discounted_total * 0.08  # 8% VAT
        self._total = discounted_total + self._VAT

    def generate_details(self):
        """Returns the invoice details."""
        return {
            "Invoice Number": self._invoice_number,
            "Items": self._items,
            "VAT": self._VAT,
            "Total": self._total
        }
payment.py
class Payment:
    """
    Payment class to process the payment for an order.
    """
    def __init__(self, payment_method, amount_paid):
        self._payment_method = payment_method
        self._amount_paid = amount_paid
        self._payment_status = "Pending"

    def process_payment(self, total_amount):
        """Processes the payment based on the total amount."""
        if self._amount_paid >= total_amount:
            self._payment_status = "Completed"
        else:
            self._payment_status = "Failed"

    def get_payment_status(self):
        """Returns the status of the payment."""
        return self._payment_status
test_cases.py
from ebook import Ebook
from catalog import Catalog
from customer import Customer
from shopping_cart import ShoppingCart
from order import Order
from payment import Payment

def test_ebook_management():
    # Add, modify, and remove e-books in catalog
    catalog = Catalog()
    ebook = Ebook("Python Programming", "Author A", "2021-01-01", "Programming", 50)
    catalog.add_ebook(ebook)
    assert catalog.find_ebook("Python Programming") == ebook

    # Remove the ebook
    catalog.remove_ebook("Python Programming")
    assert catalog.find_ebook("Python Programming") is None

def test_customer_management():
    # Create and modify customer
    customer = Customer("Alice", "alice@example.com")
    customer.set_loyalty_member(True)
    assert customer.is_loyalty_member() == True

def test_shopping_cart_operations():
    # Test adding and removing items in shopping cart and applying discounts
    cart = ShoppingCart()
    ebook1 = Ebook("Data Science", "Author B", "2022-01-01", "Data Science", 100)
    cart.add_to_cart(ebook1)
    customer = Customer("Bob", "bob@example.com", True)
    cart.apply_discounts(customer)
    assert cart._total_price == 90  # 10% loyalty discount applied

def test_order_and_invoice():
    # Generate an order and create invoice with VAT and discounts
    customer = Customer("Carol", "carol@example.com", True)
    order = Order(customer, "2024-11-07")
    ebook = Ebook("Cybersecurity", "Author C", "2023-03-03", "Security", 120)
    order.add_ebook(ebook)
    invoice = order.generate_invoice()
    details = invoice.generate_details()
    assert "Total" in details

def test_payment_processing():
    # Test processing of payment
    payment = Payment("Credit Card", 100)
    payment.process_payment(100)
    assert payment.get_payment_status() == "Completed"