import os
import shutil
categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".pptx", ".xlsx", ".csv"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Programs": [".exe", ".msi", ".apk"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c"],
    "Others": []  # anything that doesn't fit above
}


def get_category(extension):
    for category, extensions in categories.items():
        if extension.lower() in extensions:
            return category
    return "Others"


def organise_downloads():
    # Path to Downloads folder on Windows
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    print("===== FILE ORGANISER =====")
    print(f"Organising: {downloads_path}\n")
    moved = 0
    skipped = 0

    for filename in os.listdir(downloads_path):
        file_path = os.path.join(downloads_path, filename)
        # Skip folders
        if os.path.isdir(file_path):
            skipped += 1
            continue
        # Get the file extension
        _, extension = os.path.splitext(filename)

        if not extension:
            skipped += 1
            continue
        category = get_category(extension)
        category_folder = os.path.join(downloads_path, category)
        os.makedirs(category_folder, exist_ok=True)

        destination = os.path.join(category_folder, filename)

        if os.path.exists(destination):
            print(f"Skipped (already exists): {filename}")
            skipped += 1
            continue

        shutil.move(file_path, destination)
        print(f"Moved: {filename} → {category}/")
        moved += 1

    print(f"\n DONE")
    print(f"Files moved : {moved}")
    print(f"Files skipped: {skipped}")


organise_downloads()
