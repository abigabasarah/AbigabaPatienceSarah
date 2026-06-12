# E-commerce Price Calculator with Login System
#  USER CREDENTIALS
users = {
    "admin":    {"password": "admin123",    "role": "Admin"},
    "Grace":  {"password": "gracemonic256",  "role": "Cashier"},
    "John": {"password": "@john90", "role": "Customer"},
}
print("   WELCOME TO SHOPEASE E-COMMERCE SYSTEM  ")
#  LOGIN WITH 3 ATTEMPTS
print("===== LOGIN =====")
attempts = 0
max_attempts = 3
logged_in = False
while attempts < max_attempts:
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users:
        if password == users[username]["password"]:
            role = users[username]["role"]
            print(f"\nLogin successful! Welcome, {username}.\n")
            logged_in = True
            break
        else:
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"Incorrect password. {remaining} attempt(s) left.\n")
            else:
                print("Too many failed attempts. Access denied.")
    else:
        attempts += 1
        remaining = max_attempts - attempts
        if remaining > 0:
            print(f"Username not found. {remaining} attempt(s) left.\n")
        else:
            print("Too many failed attempts. Access denied.")

if not logged_in:
    exit()
# ACCESS LEVEL MENU
if role == "Admin":
    print("===== ADMIN MENU =====")
    print("1. Buy products")
    print("2. Process orders")
    print("3. Manage system")
    choice = input("\nSelect an option (1/2/3): ")
    if choice == "1":
        action = "buy"
    elif choice == "2":
        action = "process"
    elif choice == "3":
        print("Opening system management...")
        exit()
    else:
        print("Invalid option.")
        exit()

elif role == "Cashier":
    print("===== CASHIER MENU =====")
    print("1. Process a customer order")
    print("2. View products")
    choice = input("\nSelect an option (1/2): ")
    if choice == "1":
        action = "process"
    elif choice == "2":
        print("Displaying products...")
        exit()
    else:
        print("Invalid option.")
        exit()
elif role == "Customer":
    print("Welcome! Redirecting you to the shop...\n")

# PRICE CALCULATOR
print("\n===== E-COMMERCE PRICE CALCULATOR =====")
while True:
    try:
        subtotal = float(input("Enter subtotal (UGX): "))
        if subtotal <= 0:
            print("Please enter a positive amount.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a number.")
#  DISCOUNT BASED ON SUBTOTAL
if subtotal >= 500000:
    discount_rate = 0.20
    print("Discount applied: 20% (purchase above UGX 500,000)")
elif subtotal >= 200000:
    discount_rate = 0.10
    print("Discount applied: 10% (purchase above UGX 200,000)")
elif subtotal >= 50000:
    discount_rate = 0.05
    print("Discount applied: 5% (purchase above UGX 50,000)")
else:
    discount_rate = 0.0
    print("No discount applied.")

# COUPON CODE
coupon = input("Enter coupon code (or press Enter to skip): ")

if coupon == "SAVE10":
    coupon_discount = 0.10
    print("Coupon SAVE10 applied: extra 10% off")
elif coupon == "SAVE20":
    coupon_discount = 0.20
    print("Coupon SAVE20 applied: extra 20% off")
elif coupon == "":
    coupon_discount = 0.0
    print("No coupon used.")
else:
    coupon_discount = 0.0
    print("Invalid coupon code. No coupon discount applied.")
# ---- TAX BASED ON LOCATION ----
print("\nSelect your location:")
print("1. Kampala")
print("2. Other Uganda cities")
print("3. Outside Uganda")
location = input("Enter 1, 2, or 3: ")

if location == "1":
    tax_rate = 0.18
    print("Tax rate: 18% (Kampala)")
elif location == "2":
    tax_rate = 0.15
    print("Tax rate: 15% (Other Uganda cities)")
elif location == "3":
    tax_rate = 0.05
    print("Tax rate: 5% (Outside Uganda)")
else:
    print("Invalid location. Defaulting to 18% tax.")
    tax_rate = 0.18

# FINAL CALCULATION
total_discount = (discount_rate + coupon_discount) * subtotal
discounted_price = subtotal - total_discount
tax_amount = tax_rate * discounted_price
final_price = discounted_price + tax_amount
# RECEIPT
print("\n===== RECEIPT =====")
print(f"Subtotal:          UGX {subtotal:,.0f}")
print(f"Discount:          UGX {total_discount:,.0f}")
print(f"After Discount:    UGX {discounted_price:,.0f}")
print(f"Tax:               UGX {tax_amount:,.0f}")
print(f"Final Price:       UGX {final_price:,.0f}")
print("===================")
