"""
INVENTORY MANAGEMENT SYSTEM

Purpose:
Manage products, sales, restocking and inventory reporting.

Components:
- Product: Represents a single product.
- ProductRepository: Stores and retrieves products.
- InventorySystem: Coordinates inventory operations.
- Custom Exceptions: Inventory-specific error handling.

Sale Flow:
1. User requests sale.
2. InventorySystem locates product.
3. Repository returns product.
4. Product.sell() validates stock.
5. Quantity is reduced.
6. Updated product remains stored.

Design Decisions:
1. Dictionary index for SKU lookups.
   Benefit: O(1) lookup.
   Tradeoff: More memory used.

2. Separate Repository and Controller.
   Benefit: Cleaner architecture.
   Tradeoff: More classes and complexity.

"""
class InventoryError(Exception):
    pass
class ProductNotFoundError(InventoryError):
    pass


class InsufficientStockError(InventoryError):
    pass


class DuplicateSKUError(InventoryError):
    pass

class Product:
    def __init__(self, sku, name, category, price, quantity, min_threshold):
        self.sku = sku
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.min_threshold = min_threshold

    @property
    def is_low_stock(self):
        return self.quantity < self.min_threshold

    @property
    def stock_value(self):
        return self.price * self.quantity

    def restock(self, amount):
        self.quantity += amount

    def sell(self, amount):
        if amount > self.quantity:
            raise InsufficientStockError("Not enough stock to sell.")
        self.quantity -= amount

    def __str__(self):
        return f"Product(SKU: {self.sku}, Name: {self.name}, Category: {self.category}, Price: {self.price}, Quantity: {self.quantity}, Min Threshold: {self.min_threshold})"

    def __repr__(self):
        return (
            f"Product("
            f"'{self.sku}', "  
            f"'{self.name}', "
            f"'{self.category}', "
            f"{self.price}, "
            f"{self.quantity}, "
            f"{self.min_threshold}"
            f")"
)    
    def __eq__(self, other):
        if isinstance(other, Product):
            return self.sku == other.sku
        return False

class ProductRepository:
    def __init__(self):
        self._products = []
        self._index = {}

    def add(self, product):
        if product.sku in self._index:
            raise DuplicateSKUError("Product with this SKU already exists.")
        self._products.append(product)
        self._index[product.sku] = product

    def find_by_sku(self, sku):
        return self._index.get(sku)

    def find_by_name(self, query):
        return [product for product in self._products if query.lower() in product.name.lower()]

    def find_by_category(self, category):
        return [product for product in self._products if product.category.lower() == category.lower()]

    def all(self):
        return self._products.copy()
    
class InventorySystem:
    def __init__(self):
        self.repository = ProductRepository()

    def add_product(self, product):
        self.repository.add(product)

    def restock(self, sku, amount):
        product = self.repository.find_by_sku(sku)
        if not product:
            raise ProductNotFoundError("Product not found.")
        product.restock(amount)
    def sell(self, sku, amount):
        product = self.repository.find_by_sku(sku)
        if not product:
            raise ProductNotFoundError("Product not found.")
        product.sell(amount)

    def get_low_stock(self):
        return [product for product in self.repository.all() if product.is_low_stock]

    def generate_report(self):
        total_value = sum(product.stock_value for product in self.repository.all())

        return {
            "total_products": len(self.repository.all()),
            "total_stock_value": total_value,
            "low_stock_products": [product for product in self.repository.all() if product.is_low_stock]
        }
    @classmethod
    def from_config(cls, config_list):
        inventory_system = cls()
        for config in config_list:
            product = Product(
                sku=config["sku"],
                name=config["name"],
                category=config["category"],
                price=config["price"],
                quantity=config["quantity"],
                min_threshold=config["min_threshold"]
            )
            inventory_system.add_product(product)
        return inventory_system 

def main():
    inventory = InventorySystem()

    while True:
        print("\n" + "=" * 35)
        print("INVENTORY MANAGEMENT SYSTEM")
        print("=" * 35)
        print("1. Add Product")
        print("2. Restock Product")
        print("3. Sell Product")
        print("4. Search Product By Name")
        print("5. Search Products By Category")
        print("6. Generate Report")
        print("7. Exit")

        choice = input("\nEnter your choice: ").strip()

        try:
            if choice == "1":
                print("\n--- Add Product ---")

                sku = input("SKU: ").strip()
                name = input("Name: ").strip()
                category = input("Category: ").strip()

                try:
                    price = float(input("Price: "))
                    quantity = int(input("Quantity: "))
                    min_threshold = int(input("Minimum Threshold: "))
                except ValueError:
                    print("Invalid numeric input.")
                    continue

                product = Product(
                    sku=sku,
                    name=name,
                    category=category,
                    price=price,
                    quantity=quantity,
                    min_threshold=min_threshold
                )

                inventory.add_product(product)
                print("Product added successfully.")

            elif choice == "2":
                print("\n--- Restock Product ---")

                sku = input("SKU: ").strip()

                try:
                    amount = int(input("Amount to restock: "))
                except ValueError:
                    print("Amount must be a number.")
                    continue

                inventory.restock(sku, amount)
                print("Product restocked successfully.")

            elif choice == "3":
                print("\n--- Sell Product ---")

                sku = input("SKU: ").strip()

                try:
                    amount = int(input("Quantity to sell: "))
                except ValueError:
                    print("Quantity must be a number.")
                    continue

                inventory.sell(sku, amount)
                print("Sale completed successfully.")

            elif choice == "4":
                print("\n--- Search By Name ---")

                query = input("Enter name to search: ").strip()

                products = inventory.repository.find_by_name(query)

                if not products:
                    print("No matching products found.")
                else:
                    for product in products:
                        print(product)

            elif choice == "5":
                print("\n--- Search By Category ---")

                category = input("Enter category: ").strip()

                products = inventory.repository.find_by_category(category)

                if not products:
                    print("No products found in that category.")
                else:
                    for product in products:
                        print(product)

            elif choice == "6":
                print("\n--- Inventory Report ---")

                report = inventory.generate_report()

                print(f"Total Products: {report['total_products']}")
                print(
                    f"Total Stock Value: ${report['total_stock_value']:.2f}"
                )

                low_stock = inventory.get_low_stock()

                print("\nLow Stock Products:")

                if not low_stock:
                    print("None")
                else:
                    for product in low_stock:
                        print(
                            f"{product.name} "
                            f"(SKU: {product.sku}) "
                            f"- Qty: {product.quantity}"
                        )

            elif choice == "7":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please select 1-7.")

        except InventoryError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()

