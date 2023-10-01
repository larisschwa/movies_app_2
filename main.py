from storage_csv import StorageCsv
from storage_json import StorageJson
from movie_app import MovieApp


def main():
    """
    Allow the user to select the file storage type for the movie app.

    Displays a menu for the user to choose between two storage options: CSV and JSON.
    Depending on the user's choice, it initializes the selected storage type and
    proceeds with the movie app using the chosen storage method.

    Returns:
        None
    """
    print("Choose the storage type:")
    print("1. CSV")
    print("2. JSON")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        storage = StorageCsv('movies.csv')
    elif choice == "2":
        storage = StorageJson('data.json')
    else:
        print("Invalid choice. Please choose 1 or 2.")
        return

    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
