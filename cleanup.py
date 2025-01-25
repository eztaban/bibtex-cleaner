from src import clear_folder

def main():
    # Define folders to clean
    folders = {
        "1": "tmp",
        "2": "output",
        "3": "input",
    }

    # Display options to the user
    print("Select folders to clean:")
    for num, folder in folders.items():
        print(f"{num}. {folder}")

    # Get user input
    choice = input("Enter the numbers of the folders to clean (e.g., 1 2 3): ").split()

    # Clean selected folders
    for num in choice:
        folder = folders.get(num)
        if folder:
            try:
                print(f"Clearing folder: {folder}")
                clear_folder(folder)
                print(f"Folder '{folder}' cleaned successfully.")
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected error while cleaning '{folder}': {e}")
        else:
            print(f"Invalid option: {num}")

if __name__ == "__main__":
    main()
