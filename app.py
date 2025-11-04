import datetime
import json
import os

SNACKS = [
    {"id": 1, "name": "Popcorn", "price": 1000},
    {"id": 2, "name": "Soda", "price": 1000},
    {"id": 3, "name": "Crunchys", "price": 7000},
    {"id": 4, "name": "Chips", "price": 6000},
    {"id": 5, "name": "Hotdog", "price": 8000},
]

ORDERS_JSON = "orders.json"
ORDERS_TXT = "orders.txt"

orders = []


# ---------- Utilities ----------
def fmt_price(amount: int) -> str:
    """Format integer price with thousand separators."""
    return f"TSh {amount:,}"


def load_orders():
    """Load orders from JSON file (if present) into memory."""
    global orders
    if os.path.exists(ORDERS_JSON):
        try:
            with open(ORDERS_JSON, "r", encoding="utf-8") as f:
                orders = json.load(f)
        except Exception as e:
            print(f"⚠️ Couldn't load saved orders ({e}) — starting fresh.")
            orders = []
    else:
        orders = []


def save_orders_json():
    """Save current orders list to JSON file."""
    try:
        with open(ORDERS_JSON, "w", encoding="utf-8") as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ Error saving orders to JSON: {e}")


def append_receipt_to_txt(order: dict):
    """Append a receipt to ORDERS_TXT."""
    try:
        with open(ORDERS_TXT, "a", encoding="utf-8") as f:
            f.write(f"User: {order['user']}\n")
            f.write(f"Time: {order['time']}\n")
            for item in order["cart"]:
                f.write(f"  - {item['name']} x{item['qty']} = {fmt_price(item['total'])}\n")
            f.write(f"Total: {fmt_price(order['total'])}\n")
            f.write("-" * 40 + "\n")
    except Exception as e:
        print(f"⚠️ Error writing receipt to text file: {e}")


def header():
    print("*+*+*+*+*+*+*+* Welcome to Cinema Snack Ordering System +*+*+*+*++*+*+*")


def show_snacks():
    print("\n🍿 Available Snacks 🍿 :")
    print("-" * 40)
    for item in SNACKS:
        print(f"{item['id']}. {item['name']} - {fmt_price(item['price'])}")
    print("-" * 40)


# ---------- User actions ----------
def login():
    while True:
        header()
        username = input("Enter your username: ").strip()
        if username:
            username = username.capitalize()
            print(f" Hello, {username}! Let's get started.\n")
            return username
        print("⚠️ Username cannot be empty. Try again.\n")


def place_order():
    cart = []
    while True:
        show_snacks()
        print("0. Finish ordering")
        if cart:
            print("R. Remove last item from cart")
            print("\nCurrent cart:")
            for idx, it in enumerate(cart, start=1):
                print(f"{idx}. {it['name']} x{it['qty']} = {fmt_price(it['total'])}")
            subtotal = sum(i["total"] for i in cart)
            print(f"Subtotal: {fmt_price(subtotal)}\n")

        choice = input("Select a snack number (or 0 to finish): ").strip().lower()
        if choice == "0":
            break
        if choice == "r" and cart:
            removed = cart.pop()
            print(f"Removed last item: {removed['name']} x{removed['qty']}")
            continue

        # validate integer choice
        if not choice.isdigit():
            print("⚠️ Enter a number corresponding to a snack (or 0 to finish).")
            continue

        choice_id = int(choice)
        snack = next((s for s in SNACKS if s["id"] == choice_id), None)
        if not snack:
            print("❌ Invalid snack ID. Try again.")
            continue

        qty_str = input(f"How many {snack['name']}? ").strip()
        if not qty_str.isdigit():
            print("⚠️ Quantity must be a positive integer.")
            continue
        qty = int(qty_str)
        if qty <= 0:
            print("⚠️ Quantity must be greater than 0.")
            continue

        total_price = snack["price"] * qty
        cart.append({"name": snack["name"], "qty": qty, "total": total_price})
        print(f"✅ Added {qty} x {snack['name']} — {fmt_price(total_price)}")

    if not cart:
        print("🛒 No items were ordered.")
        return None

    order_total = sum(item["total"] for item in cart)
    print(f"\n💰 Order Total: {fmt_price(order_total)}")
    # show cart one more time before returning
    print("Final cart:")
    for item in cart:
        print(f"- {item['name']} x{item['qty']} = {fmt_price(item['total'])}")
    return cart, order_total


def checkout(username, cart, total):
    while True:
        confirm = input("Confirm purchase? (y/n): ").strip().lower()
        if confirm == "y":
            order = {
                "user": username,
                "cart": cart,
                "total": total,
                "time": datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
            }
            orders.append(order)
            save_orders_json()
            append_receipt_to_txt(order)
            print(f"💳 Payment successful! Receipt saved to '{ORDERS_TXT}'. Enjoy your snacks! 🎥🍿")
            return
        elif confirm == "n":
            print("❌ Order cancelled.")
            return
        else:
            print("Please enter 'y' or 'n'.")


def view_orders():
    if not orders:
        print("\n🕒 No orders made yet.")
        return
    print("\n📋 Order History:")
    for i, order in enumerate(orders, start=1):
        print(f"\nOrder #{i} by {order['user']} at {order['time']}")
        for item in order["cart"]:
            print(f"- {item['name']} x{item['qty']} = {fmt_price(item['total'])}")
        print(f"Total: {fmt_price(order['total'])}")


# ---------- Main ----------
def main():
    load_orders()
    username = login()
    while True:
        print("\nMain Menu")
        print("1. Place an Order")
        print("2. View Order History")
        print("3. Exit")
        choice = input("Select an option: ").strip()
        if not choice.isdigit():
            print("⚠️ Please enter a number (1-3).")
            continue
        option = int(choice)
        if option == 1:
            result = place_order()
            if result:
                cart, total = result
                checkout(username, cart, total)
        elif option == 2:
            view_orders()
        elif option == 3:
            print("Goodbye!, Welcome Again")
            break
        else:
            print("⚠️ Invalid option. Choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
