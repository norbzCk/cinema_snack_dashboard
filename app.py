# Cinema Snack Ordering System
# Author: norbzCk

import datetime

# Database of snacks
snacks = [
    {"id": 1, "name": "Popcorn", "price": 5000},
    {"id": 2, "name": "Soda", "price": 1000},
    {"id": 3, "name": "Nachos", "price": 7000},
    {"id": 4, "name": "Chips", "price": 6000},
    {"id": 5, "name": "Hotdog", "price": 8000}
]

# Store all orders
orders = []

# --- Authentication system ---
def login():
    print("🎫 Welcome to Cinema Snack Ordering System 🎫")
    username = input("Enter your username: ").strip()
    if not username:
        print("⚠️ Username cannot be empty!")
        return login()
    print(f"✅ Hello, {username.capitalize()}! Let's get started.\n")
    return username

# --- Show available snacks ---
def show_snacks():
    print("\n🍿 Available Snacks:")
    print("-" * 30)
    for item in snacks:
        print(f"{item['id']}. {item['name']} - TSh {item['price']}")
    print("-" * 30)

# --- Add an order ---
def place_order():
    cart = []
    while True:
        show_snacks()
        try:
            choice = int(input("Select a snack number (0 to finish): "))
            if choice == 0:
                break
            snack = next((s for s in snacks if s["id"] == choice), None)
            if not snack:
                print("❌ Invalid snack ID.")
                continue
            qty = int(input(f"How many {snack['name']}s? "))
            if qty <= 0:
                print("⚠️ Quantity must be greater than 0.")
                continue
            total_price = snack["price"] * qty
            cart.append({"name": snack["name"], "qty": qty, "total": total_price})
            print(f"Successfully added {qty} {snack['name']}(s) to order (TSh {total_price})")
        except ValueError:
            print("⚠️ Enter numbers only!")

    if not cart:
        print("🛒 No items were ordered.")
        return None

    order_total = sum(item["total"] for item in cart)
    print(f"\n💰 Order Total: TSh {order_total}")
    return cart, order_total

# --- Checkout and save order ---
def checkout(username, cart, total):
    confirm = input("Confirm purchase? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Order cancelled.")
        return

    # Create order record
    order = {
        "user": username,
        "cart": cart,
        "total": total,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    orders.append(order)

    # Save to file (receipt)
    with open("orders.txt", "a") as f:
        f.write(f"User: {order['user']}\n")
        f.write(f"Time: {order['time']}\n")
        for item in cart:
            f.write(f"  - {item['name']} x{item['qty']} = TSh {item['total']}\n")
        f.write(f"Total: TSh {order['total']}\n")
        f.write("-" * 40 + "\n")

    print("💳 Payment successful! Receipt saved to 'orders.txt'. Enjoy your snacks! 🎥🍿") # later i will implement that user gets receipt

# --- View past orders ---
def view_orders():
    if not orders:
        print("\n🕒 No orders made yet.")
        return
    print("\n📋 Order History:")
    for i, order in enumerate(orders, start=1):
        print(f"\nOrder #{i} by {order['user']} at {order['time']}")
        for item in order["cart"]:
            print(f"- {item['name']} x{item['qty']} = TSh {item['total']}")
        print(f"Total: TSh {order['total']}")

# --- Main program ---
def main():
    username = login()
    while True:
        print("\n Main Menu")
        print("1. Place an Order")
        print("2. View Order History")
        print("3. Exit")
        try:
            option = int(input("Select an option: "))
            if option == 1:
                result = place_order()
                if result:
                    cart, total = result
                    checkout(username, cart, total)
            elif option == 2:
                view_orders()
            elif option == 3:
                print("👋 Goodbye!")
                break
            else:
                print("⚠️ Invalid option.")
        except ValueError:
            print("⚠️ Please enter a number.")


if __name__ == "__main__":
    main()
