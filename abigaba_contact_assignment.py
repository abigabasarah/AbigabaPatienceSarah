
class ContactManager:
    def __init__(self):
        # self.contacts holds tuples of (name, phone, email)
        self.contacts = []
    # Validation helpers

    def is_valid_phone(self, phone):
        """
        A phone number is valid if it only contains digits, hyphens (-),
        and an optional leading plus sign (+), e.g. "+256-701-234567".
        """
        if phone == "":
            return False

        for index in range(len(phone)):
            char = phone[index]
            if char.isdigit() or char == "-":
                continue
            elif char == "+" and index == 0:
                continue
            else:
                return False
        return True

    def is_valid_email(self, email):
        """
        An email is valid if it contains both '@' and '.'.
        An empty email is allowed since email is optional.
        """
        if email == "":
            return True

        if "@" in email and "." in email:
            return True
        return False
    # Add or Update with validation

    def add_contact(self, name, phone, email=""):
        if not self.is_valid_phone(phone):
            print(
                "Error: Phone number can only contain digits, hyphens (-), and an optional leading '+'.")
            return False

        if not self.is_valid_email(email):
            print("Error: Email must contain an '@' symbol and a '.' (period).")
            return False

        new_contact = (name, phone, email)
        self.contacts.append(new_contact)
        print(f"Contact '{name}' added successfully.")
        return True

    def update_contact(self, name, new_phone=None, new_email=None):
        index = self.find_index_by_name(name)

        if index == -1:
            print(f"No contact found with the name '{name}'.")
            return False

        old_name, old_phone, old_email = self.contacts[index]

        # Decide what the updated values should be
        phone_to_use = old_phone
        email_to_use = old_email

        if new_phone is not None and new_phone != "":
            if not self.is_valid_phone(new_phone):
                print(
                    "Error: Phone number can only contain digits, hyphens (-), and an optional leading '+'.")
                return False
            phone_to_use = new_phone

        if new_email is not None and new_email != "":
            if not self.is_valid_email(new_email):
                print("Error: Email must contain an '@' symbol and a '.' (period).")
                return False
            email_to_use = new_email

        # Tuples are immutable, so we replace the whole tuple in the list
        self.contacts[index] = (old_name, phone_to_use, email_to_use)
        print(f"Contact '{name}' updated successfully.")
        return True

    def delete_contact(self, name):
        index = self.find_index_by_name(name)

        if index == -1:
            print(f"No contact found with the name '{name}'.")
            return False

        del self.contacts[index]
        print(f"Contact '{name}' deleted successfully.")
        return True

    def view_contact(self, name):
        index = self.find_index_by_name(name)

        if index == -1:
            print(f"No contact found with the name '{name}'.")
            return None

        self.display_results([self.contacts[index]])
        return self.contacts[index]
    # find a contact's index by exact name (case-insensitive)

    def find_index_by_name(self, name):
        for index in range(len(self.contacts)):
            current_name = self.contacts[index][0]
            if current_name.lower() == name.lower():
                return index
        return -1
    # Advanced search (name, phone, OR email) + clean display

    def search_contacts(self, keyword):
        keyword = keyword.lower()
        results = []

        for contact in self.contacts:
            name, phone, email = contact
            if keyword in name.lower() or keyword in phone.lower() or keyword in email.lower():
                results.append(contact)

        if len(results) == 0:
            print(f"No contacts matched '{keyword}'.")
        else:
            print(f"Found {len(results)} match(es) for '{keyword}':")
            self.display_results(results)

        return results

    def list_all_contacts(self):
        if len(self.contacts) == 0:
            print("Your contact list is empty.")
        else:
            self.display_results(self.contacts)

    def display_results(self, contact_list):
        """
        Helper method that prints a list of contact tuples in a clean,
        readable format instead of raw tuples.
        """
        print("-" * 40)
        for contact in contact_list:
            name, phone, email = contact
            email_display = email if email != "" else "N/A"
            print(f"Name : {name}")
            print(f"Phone: {phone}")
            print(f"Email: {email_display}")
            print("-" * 40)
# Interactive CLI Menu


def main():
    manager = ContactManager()
    while True:
        print("\n=== Contact Manager Menu ===")
        print("1. Add Contact")
        print("2. View Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Search Contacts")
        print("6. List All Contacts")
        print("7. Exit")

        choice = input("Choose an option (1-7): ")

        if choice == "1":
            name = input("Enter name: ")
            phone = input("Enter phone (digits and hyphens only): ")
            email = input("Enter email (optional, press Enter to skip): ")
            manager.add_contact(name, phone, email)

        elif choice == "2":
            name = input("Enter the name of the contact to view: ")
            manager.view_contact(name)

        elif choice == "3":
            name = input("Enter the name of the contact to update: ")
            new_phone = input(
                "Enter new phone (press Enter to keep current): ")
            new_email = input(
                "Enter new email (press Enter to keep current): ")
            manager.update_contact(name, new_phone, new_email)

        elif choice == "4":
            name = input("Enter the name of the contact to delete: ")
            confirm = input(
                f"Are you sure you want to delete '{name}'? (y/n): ")
            if confirm.lower() == "y":
                manager.delete_contact(name)
            else:
                print("Deletion cancelled.")

        elif choice == "5":
            keyword = input("Enter a name, phone, or email to search for: ")
            manager.search_contacts(keyword)

        elif choice == "6":
            manager.list_all_contacts()

        elif choice == "7":
            print("Exiting....")
            break

        else:
            print("Invalid option. Please choose a number between 1 and 7.")


if __name__ == "__main__":
    main()
