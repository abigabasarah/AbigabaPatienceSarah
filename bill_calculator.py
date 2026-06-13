
print("===== Bill Split Calculator =====")

bill_amount = float(input("\nEnter total bill amount: "))
if bill_amount <= 0:
    print("Invalid amount! Please enter a positive number.")
    bill_amount = float(input("Enter total bill amount again: "))

num_people = int(input("Enter number of people: "))
if num_people <= 0:
    print("Invalid number! Must be at least 1 person.")
    num_people = int(input("Enter number of people again: "))

print("\nSelect tip percentage:")
print("1. 10%")
print("2. 15%")
print("3. 20%")
print("4. Custom")

choice = input("Enter choice (1-4): ")

if choice == "1":
    tip_percent = 10
elif choice == "2":
    tip_percent = 15
elif choice == "3":
    tip_percent = 20
elif choice == "4":
    tip_percent = float(input("Enter custom tip percentage: "))
else:
    print("Invalid choice, defaulting to 10%")
    tip_percent = 10

# Calculations
tip_amount = bill_amount * (tip_percent / 100)
total_bill = bill_amount + tip_amount
per_person = total_bill / num_people

# Output receipt
print("\n========== RECEIPT ==========")
print(f"  Original Bill:    {bill_amount:.2f}")
print(f"  Tip ({tip_percent}%):          {tip_amount:.2f}")
print(f"  Total Bill:       {total_bill:.2f}")
print(f"  Number of People: {num_people}")
print("-----------------------------")
print(f"  Each Person Pays:UGX {per_person:.2f}")
print("=============================")
