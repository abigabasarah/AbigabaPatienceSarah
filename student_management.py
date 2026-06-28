
import csv
import json
import logging
import os
from datetime import datetime
# File paths
CSV_FILE = "students.csv"
JSON_FILE = "students.json"
LOG_FILE = "student_system.log"

CSV_FIELDS = ["RegistrationNo", "Name", "Gender", "Age", "Course", "Score"]

# Logging set up
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def log(msg, level="info"):
    """Log a message to the log file."""
    if level == "error":
        logging.error(msg)
    elif level == "warning":
        logging.warning(msg)
    else:
        logging.info(msg)

# Custom exceptions


class StudentNotFoundError(Exception):
    """Raised when a student with the given registration number does not exist."""
    pass


class DuplicateRegistrationError(Exception):
    """Raised when trying to add a student with an existing registration number."""
    pass


class InvalidScoreError(Exception):
    """Raised when a score is not between 0 and 100."""
    pass


class InvalidAgeError(Exception):
    """Raised when an age is not a realistic student age (15–60)."""
    pass

# File helpers for CSV and JSON operations with exception handling


def load_csv():
    """Read all students from the CSV file and return as a list of dicts."""
    students = []
    if not os.path.exists(CSV_FILE):
        return students
    try:
        with open(CSV_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append(row)
    except Exception as e:
        log(f"Failed to read CSV: {e}", "error")
    return students


def save_csv(students):
    """Write the full list of student dicts back to the CSV file."""
    try:
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(students)
    except Exception as e:
        log(f"Failed to write CSV: {e}", "error")
        raise


def load_json():
    """Read additional student details from the JSON file."""
    if not os.path.exists(JSON_FILE):
        return {}
    try:
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        log(f"JSON decode error: {e}", "error")
        return {}
    except Exception as e:
        log(f"Failed to read JSON: {e}", "error")
        return {}


def save_json(data):
    """Write additional details dict back to the JSON file."""
    try:
        with open(JSON_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        log(f"Failed to write JSON: {e}", "error")
        raise

# Input validation


def validate_score(score_str):
    """Validate that score is a number between 0 and 100."""
    try:
        score = float(score_str)
    except ValueError:
        raise InvalidScoreError("Score must be a number.")
    if not (0 <= score <= 100):
        raise InvalidScoreError(
            f"Score {score} is out of range. Must be between 0 and 100.")
    return str(score)


def validate_age(age_str):
    """Validate that age is a realistic student age."""
    try:
        age = int(age_str)
    except ValueError:
        raise InvalidAgeError("Age must be a whole number.")
    if not (18 <= age <= 60):
        raise InvalidAgeError(
            f"Age {age} is not realistic for a student (expected 18–60).")
    return str(age)


def validate_gender(gender_str):
    """Validate gender input."""
    gender = gender_str.strip().capitalize()
    if gender not in ("Male", "Female"):
        raise ValueError("Gender must be Male or Female.")
    return gender
# Core functions


def add_student():
    """Collect student info from user and save to CSV + JSON."""
    print("\n── Add New Student ──")
    try:
        reg_no = input("Registration Number (e.g. 24/U/98877): ").strip()
        if not reg_no:
            raise ValueError("Registration number cannot be empty.")
        students = load_csv()
        for s in students:
            if s["RegistrationNo"].lower() == reg_no.lower():
                raise DuplicateRegistrationError(
                    f"Student '{reg_no}' already exists in the system."
                )

        name = input("Full Name: ").strip()
        if not name:
            raise ValueError("Name cannot be empty.")

        gender = validate_gender(input("Gender (Male/Female): "))
        age = validate_age(input("Age: "))
        course = input("Course: ").strip()
        if not course:
            raise ValueError("Course cannot be empty.")
        score = validate_score(input("Score (0–100): "))

        # Save basic info to CSV
        students.append({
            "RegistrationNo": reg_no,
            "Name": name,
            "Gender": gender,
            "Age": age,
            "Course": course,
            "Score": score
        })
        save_csv(students)

        # Save extra details to JSON
        address = input("Address: ").strip()
        contact = input("Contact (phone): ").strip()
        program = input("Program (e.g. BSc Software Engineering): ").strip()

        details = load_json()
        details[reg_no] = {
            "address": address,
            "contact": contact,
            "program": program,
            "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_json(details)

        print(f"\n Student '{name}' added successfully!")
        log(f"ADD | {reg_no} | {name}")

    except DuplicateRegistrationError as e:
        print(f"\n  Duplicate: {e}")
        log(f"ADD FAILED - Duplicate: {e}", "warning")
    except (InvalidScoreError, InvalidAgeError, ValueError) as e:
        print(f"\n Validation Error: {e}")
        log(f"ADD FAILED - Validation: {e}", "error")
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        log(f"ADD FAILED - Unexpected: {e}", "error")
    finally:
        print("End of Add Student")


def view_all_students():
    """Display all students from CSV in a formatted table."""
    print("\n All Students ")
    try:
        students = load_csv()
        if not students:
            print("No student records found.")
            log("VIEW ALL | No records found")
            return

        # Print table header
        print(
            f"\n{'No.':<5} {'Reg No':<15} {'Name':<25} {'Gender':<8} {'Age':<5} {'Course':<25} {'Score':<6}")
        print("─" * 95)

        for i, s in enumerate(students, 1):
            print(f"{i:<5} {s['RegistrationNo']:<15} {s['Name']:<25} {s['Gender']:<8} "
                  f"{s['Age']:<5} {s['Course']:<25} {s['Score']:<6}")

        print(f"\nTotal students: {len(students)}")
        log(f"VIEW ALL | {len(students)} records displayed")

    except Exception as e:
        print(f"\n Error reading records: {e}")
        log(f"VIEW ALL FAILED: {e}", "error")
    finally:
        print(" End of View Students ")


def search_student():
    """Search for a student by registration number and show full details."""
    print("\n Search Student ")
    try:
        reg_no = input("Enter Registration Number to search: ").strip()

        students = load_csv()
        found = None
        for s in students:
            if s["RegistrationNo"].lower() == reg_no.lower():
                found = s
                break

        if not found:
            raise StudentNotFoundError(
                f"No student found with registration number '{reg_no}'.")

        # Display CSV details
        print(f"\n{'─'*40}")
        print(f"  Registration No : {found['RegistrationNo']}")
        print(f"  Name            : {found['Name']}")
        print(f"  Gender          : {found['Gender']}")
        print(f"  Age             : {found['Age']}")
        print(f"  Course          : {found['Course']}")
        print(f"  Score           : {found['Score']}")

        # Display JSON extra details if available
        details = load_json()
        if found["RegistrationNo"] in details:
            extra = details[found["RegistrationNo"]]
            print(f"  Address         : {extra.get('address', 'N/A')}")
            print(f"  Contact         : {extra.get('contact', 'N/A')}")
            print(f"  Program         : {extra.get('program', 'N/A')}")
            print(f"  Date Added      : {extra.get('date_added', 'N/A')}")
        print(f"{'─'*40}")

        log(f"SEARCH | Found: {reg_no}")

    except StudentNotFoundError as e:
        print(f"\n  {e}")
        log(f"SEARCH FAILED - Not found: {reg_no}", "warning")
    except Exception as e:
        print(f"\n Error during search: {e}")
        log(f"SEARCH FAILED - Unexpected: {e}", "error")
    finally:
        print(" End of Search ")


def update_student():
    """Update an existing student's details."""
    print("\n Update Student ")
    try:
        reg_no = input(
            "Enter Registration Number of student to update: ").strip()

        students = load_csv()
        index = None
        for i, s in enumerate(students):
            if s["RegistrationNo"].lower() == reg_no.lower():
                index = i
                break

        if index is None:
            raise StudentNotFoundError(
                f"No student found with registration number '{reg_no}'.")

        student = students[index]
        print(f"\nUpdating record for: {student['Name']}")
        print("(Press Enter to keep existing value)\n")

        new_name = input(f"Name [{student['Name']}]: ").strip()
        if new_name:
            student["Name"] = new_name

        new_gender = input(f"Gender [{student['Gender']}]: ").strip()
        if new_gender:
            student["Gender"] = validate_gender(new_gender)

        new_age = input(f"Age [{student['Age']}]: ").strip()
        if new_age:
            student["Age"] = validate_age(new_age)

        new_course = input(f"Course [{student['Course']}]: ").strip()
        if new_course:
            student["Course"] = new_course

        new_score = input(f"Score [{student['Score']}]: ").strip()
        if new_score:
            student["Score"] = validate_score(new_score)

        students[index] = student
        save_csv(students)

        details = load_json()
        if reg_no not in details:
            details[reg_no] = {}

        new_address = input(
            f"Address [{details[reg_no].get('address', '')}]: ").strip()
        if new_address:
            details[reg_no]["address"] = new_address

        new_contact = input(
            f"Contact [{details[reg_no].get('contact', '')}]: ").strip()
        if new_contact:
            details[reg_no]["contact"] = new_contact

        new_program = input(
            f"Program [{details[reg_no].get('program', '')}]: ").strip()
        if new_program:
            details[reg_no]["program"] = new_program

        details[reg_no]["last_updated"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        save_json(details)

        print(f"\n Student '{reg_no}' updated successfully!")
        log(f"UPDATE | {reg_no}")

    except StudentNotFoundError as e:
        print(f"\n  {e}")
        log(f"UPDATE FAILED - Not found: {e}", "warning")
    except (InvalidScoreError, InvalidAgeError, ValueError) as e:
        print(f"\n Validation Error: {e}")
        log(f"UPDATE FAILED - Validation: {e}", "error")
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        log(f"UPDATE FAILED - Unexpected: {e}", "error")
    finally:
        print(" End of Update ")


def delete_student():
    """Delete a student record from both CSV and JSON."""
    print("\n Delete Student ")
    try:
        reg_no = input(
            "Enter Registration Number of student to delete: ").strip()

        students = load_csv()
        original_count = len(students)
        updated = [s for s in students if s["RegistrationNo"].lower()
                   != reg_no.lower()]

        if len(updated) == original_count:
            raise StudentNotFoundError(
                f"No student found with registration number '{reg_no}'.")

        # Confirm before deleting
        confirm = input(
            f"Are you sure you want to delete '{reg_no}'? (yes/no): ").strip().lower()
        if confirm != "yes":
            print(" Deletion cancelled.")
            log(f"DELETE CANCELLED | {reg_no}")
            return

        save_csv(updated)

        # Remove from JSON too
        details = load_json()
        if reg_no in details:
            del details[reg_no]
            save_json(details)

        print(f"\n Student '{reg_no}' deleted successfully!")
        log(f"DELETE | {reg_no}")

    except StudentNotFoundError as e:
        print(f"\n  {e}")
        log(f"DELETE FAILED - Not found: {e}", "warning")
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        log(f"DELETE FAILED - Unexpected: {e}", "error")
    finally:
        print(" End of Delete ")


def show_menu():
    print("\n" + "═" * 45)
    print("   STUDENT RECORD MANAGEMENT SYSTEM")
    print("═" * 45)
    print("  1. Add New Student")
    print("  2. View All Students")
    print("  3. Search Student by Reg. Number")
    print("  4. Update Student Details")
    print("  5. Delete Student Record")
    print("  6. Exit")
    print("═" * 45)


def main():
    log(" SYSTEM STARTED ")
    print("\nWelcome to the Student Record Management System!")

    while True:
        show_menu()
        try:
            choice = input("Enter your choice (1–6): ").strip()
            log(f"MENU CHOICE | {choice}")

            if choice == "1":
                add_student()
            elif choice == "2":
                view_all_students()
            elif choice == "3":
                search_student()
            elif choice == "4":
                update_student()
            elif choice == "5":
                delete_student()
            elif choice == "6":
                print("\n System exiting...")
                log(" SYSTEM EXITED ")
                break
            else:
                print("  Invalid choice. Please enter a number between 1 and 6.")
                log(f"INVALID MENU CHOICE | {choice}", "warning")

        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!")
            log(" SYSTEM INTERRUPTED (Ctrl+C) ", "warning")
            break


if __name__ == "__main__":
    main()
