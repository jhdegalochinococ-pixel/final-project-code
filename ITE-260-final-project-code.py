import csv
import os                                                   

FILENAME = "inventory_data.csv"

# Structure: {item_name: {"quantity": int, "description": str}}
inventory = {}


def load_data():
    """Load inventory data from the CSV file."""
    inventory.clear()

    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)

                for row in reader:
                    if len(row) == 2:
                        name, quantity = row
                        description = "No description provided."
                    elif len(row) == 3:
                        name, quantity, description = row
                    else:
                        continue

                    try:
                        quantity = int(quantity)

                        if quantity < 0:
                            print(
                                f"Invalid quantity for '{name}'. "
                                "Skipping entry."
                            )
                            continue

                        inventory[name] = {
                            "quantity": quantity,
                            "description": description.strip()
                        }

                    except ValueError:
                        print(
                            f"Invalid quantity for '{name}'. "
                            "Skipping entry."
                        )

        except OSError as error:
            print(f"Error loading data: {error}")


def save_data():
    """Save inventory data to the CSV file."""
    try:
        with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            for name, data in inventory.items():
                writer.writerow([
                    name,
                    data["quantity"],
                    data["description"]
                ])

    except OSError as error:
        print(f"Error saving data: {error}")


def get_valid_quantity(prompt):
    """Accept only non-negative integers."""
    while True:
        try:
            value = int(input(prompt))

            if value < 0:
                print("Quantity cannot be negative. Please try again.")
            else:
                return value

        except ValueError:
            print("Invalid input. Please enter a whole number.")


def find_item_key(input_name):
    """Find an item without considering uppercase or lowercase."""
    return next(
        (
            key for key in inventory
            if key.lower() == input_name.strip().lower()
        ),
        None
    )


def register_item():
    """1. Register a new school supply."""
    print("\n--- Register New Item ---")
    name = input("Enter item name: ").strip()

    if not name:
        print("Item name cannot be empty.")
        return

    if find_item_key(name) is not None:
        print(f"Item '{name}' already exists.")
        print("Use Add Quantity or Edit Item Details instead.")
        return

    quantity = get_valid_quantity("Enter initial quantity: ")
    description = input("Enter description (optional): ").strip()

    if not description:
        description = "No description provided."

    inventory[name] = {
        "quantity": quantity,
        "description": description
    }

    save_data()
    print(f"'{name}' registered successfully.")


def view_stock_list():
    """2. Display all supplies and their quantities."""
    if not inventory:
        print("\nInventory is empty.")
        return

    print("\n--- School Supplies Inventory Stock List ---")
    print(f"{'Item Name':<25} | {'Quantity':<10} | Description")
    print("-" * 75)

    for name, data in inventory.items():
        print(
            f"{name:<25} | "
            f"{data['quantity']:<10} | "
            f"{data['description']}"
        )


def search_supply():
    """3. Search by item name or description."""
    keyword = input(
        "Enter supply name, description, or keyword: "
    ).strip().lower()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    found = False

    print("\n--- Search Results ---")
    print(f"{'Item Name':<25} | {'Quantity':<10} | Description")
    print("-" * 75)

    for name, data in inventory.items():
        if (
            keyword in name.lower()
            or keyword in data["description"].lower()
        ):
            print(
                f"{name:<25} | "
                f"{data['quantity']:<10} | "
                f"{data['description']}"
            )
            found = True

    if not found:
        print("No matching supplies found.")


def add_quantity():
    """4. Increase stock when new supplies arrive."""
    print("\n--- Add Stock / Restock ---")
    input_name = input("Enter item name to restock: ").strip()
    key = find_item_key(input_name)

    if key is None:
        print("Item not found.")
        return

    print(f"Current stock for '{key}': {inventory[key]['quantity']}")

    add_qty = get_valid_quantity("Enter quantity to add: ")
    inventory[key]["quantity"] += add_qty

    save_data()
    print(
        f"Stock updated. New quantity for '{key}': "
        f"{inventory[key]['quantity']}"
    )


def release_quantity():
    """5. Decrease stock when supplies are issued."""
    print("\n--- Release Stock / Issue Items ---")
    input_name = input("Enter item name to release: ").strip()
    key = find_item_key(input_name)

    if key is None:
        print("Item not found.")
        return

    current_qty = inventory[key]["quantity"]
    print(f"Current stock for '{key}': {current_qty}")

    release_qty = get_valid_quantity("Enter quantity to release: ")

    if release_qty > current_qty:
        print(
            "Error: Cannot release more than the "
            f"available stock ({current_qty})."
        )
        return

    inventory[key]["quantity"] -= release_qty

    save_data()
    print(
        f"Stock released. Remaining quantity for '{key}': "
        f"{inventory[key]['quantity']}"
    )


def edit_item_details():
    """6. Update an item's name or description."""
    print("\n--- Edit Item Details ---")
    input_name = input("Enter item name to edit: ").strip()
    key = find_item_key(input_name)

    if key is None:
        print("Item not found.")
        return

    current_item = inventory[key]

    print(f"\nCurrent Name: {key}")
    print(f"Current Description: {current_item['description']}")

    print("\nWhat details would you like to edit?")
    print("1. Update Item Name")
    print("2. Update Item Description")
    print("3. Update Both Name and Description")

    sub_choice = input("Select option (1-3): ").strip()

    if sub_choice not in ("1", "2", "3"):
        print("Invalid choice. Edit cancelled.")
        return

    new_name = key
    new_desc = current_item["description"]

    if sub_choice in ("1", "3"):
        new_name = input("Enter new item name: ").strip()

        if not new_name:
            print("Name cannot be empty. Edit cancelled.")
            return

        target_key = find_item_key(new_name)

        if target_key is not None and target_key != key:
            print(f"Another item named '{target_key}' already exists.")
            return

    if sub_choice in ("2", "3"):
        new_desc = input("Enter new description: ").strip()

        if not new_desc:
            new_desc = "No description provided."

    data = inventory.pop(key)
    data["description"] = new_desc
    inventory[new_name] = data

    save_data()
    print("Item details updated successfully.")


def remove_item():
    """7. Delete a supply from the inventory."""
    print("\n--- Remove Item ---")
    input_name = input("Enter item name to remove: ").strip()
    key = find_item_key(input_name)

    if key is None:
        print("Item not found.")
        return

    confirm = input(
        f"Are you sure you want to delete '{key}'? (y/n): "
    ).strip().lower()

    if confirm == "y":
        del inventory[key]
        save_data()
        print(f"'{key}' removed successfully.")
    else:
        print("Deletion cancelled.")


def view_low_stock_items():
    """8. Display supplies with five or fewer items."""
    print("\n--- Low-Stock Items (5 or fewer) ---")
    found = False

    print(f"{'Item Name':<25} | {'Quantity':<10} | Description")
    print("-" * 75)

    for name, data in inventory.items():
        if data["quantity"] <= 5:
            print(
                f"{name:<25} | "
                f"{data['quantity']:<10} | "
                f"{data['description']}"
            )
            found = True

    if not found:
        print("No supplies are running low in stock.")


def main():
    """Run the School Supplies Inventory System."""
    load_data()

    while True:
        print("\n===== SCHOOL SUPPLIES INVENTORY SYSTEM =====")
        print("1. Register Item")
        print("2. View Stock List")
        print("3. Search Supply")
        print("4. Add Quantity")
        print("5. Release Quantity")
        print("6. Edit Item Details")
        print("7. Remove Item")
        print("8. View Low-Stock Items")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            register_item()
        elif choice == "2":
            view_stock_list()
        elif choice == "3":
            search_supply()
        elif choice == "4":
            add_quantity()
        elif choice == "5":
            release_quantity()
        elif choice == "6":
            edit_item_details()
        elif choice == "7":
            remove_item()
        elif choice == "8":
            view_low_stock_items()
        elif choice == "9":
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()