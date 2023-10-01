import requests
from istorage import IStorage


OMDB_API_URL = 'http://www.omdbapi.com/'
OMDB_API_KEY = '5eeb20d'


def fetch_movie_info(title):
    """
    Fetches movie information from OMDB API based on the given title.

    Args:
        title (str): The title of the movie to search for on OMDB.

    Returns:
        dict or None: A dictionary containing movie information if found,
                      or None if the movie is not found or there is an issue
                      with the API.
    """
    params = {'apikey': OMDB_API_KEY, 't': title}
    response = requests.get(OMDB_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def print_menu():
    """
    Displays the movie app's options menu to the user.

    Returns:
        None
    """
    print("Movie App Menu:")
    print("1. List Movies")
    print("2. Add Movie")
    print("3. Delete Movie")
    print("4. Update Movie")
    print("5. Movie Statistics")
    print("6. Random Movie")
    print("7. Search Movies")
    print("8. Sort Movies")
    print("9. Generate Website")
    print("0. Exit")


class MovieApp:
    """
    Initializes and manages the movie app.

    Args:
        storage (IStorage): An instance of a storage class implementing
        the IStorage interface.

    Methods:
        command_list_movies: Display a list of movies.
        command_movie_stats: Show statistics of movies in the file.
        command_add_movie: Add a movie to the storage based on OMDB
        information.
        command_delete_movie: Delete a movie from the storage.
        command_update_movie: Update movie information in the storage.
        command_random_movie: Display a random movie.
        command_search_movies: Allow the user to search for movies.
        command_sort_movies: Sort movies by rating.
        command_generate_website: Generate a website displaying movie
        information.
        run: Accept user input from the menu and execute corresponding
        commands.
    """
    def __init__(self, storage: IStorage):
        self._storage = storage

    def command_list_movies(self):
        """show user a list of movies"""
        movies = self._storage.list_movies()
        if movies:
            print("Movie List:")
            for movie, data in movies.items():
                print(f"{movie}: {data['rating']}")
        else:
            print("No movies found.")

    def command_movie_stats(self):
        """show user stats of movies in file"""
        movies = self._storage.list_movies()
        if movies:
            num_movies = len(movies)
            total_rating = sum(
                float(data['rating']) for data in movies.values())
            avg_rating = total_rating / num_movies

            ratings = [float(data['rating']) for data in movies.values()]
            sorted_ratings = sorted(ratings)
            mid = num_movies // 2
            if num_movies % 2 == 0:
                median_rating = (sorted_ratings[mid - 1] + sorted_ratings[
                    mid]) / 2
            else:
                median_rating = sorted_ratings[mid]

            best_movie = max(movies, key=lambda x: float(movies[x]['rating']))
            worst_movie = min(movies, key=lambda x: float(movies[x]['rating']))

            print("Movie Statistics:")
            print(f"Number of movies: {num_movies}")
            print(f"Average rating: {avg_rating:.2f}")
            print(f"Median rating: {median_rating:.1f}")
            print(f"Best movie: {best_movie} ({movies[best_movie]['rating']})")
            print(
                f"Worst movie: {worst_movie} "
                f"({movies[worst_movie]['rating']})")
        else:
            print("No movies found.")

    def command_add_movie(self):
        movie_title = input("Enter the title of the movie: ")

        movie_info = fetch_movie_info(movie_title)

        if movie_info:
            movie_rating = movie_info.get('imdbRating', 'N/A')
            movie_year = movie_info.get('Year', 'N/A')
            poster_url = movie_info.get('Poster', 'N/A')

            movie_data = {
                'title': movie_title,
                'rating': movie_rating,
                'year': movie_year,
                'poster_url': poster_url
            }

            self._storage.add_movie(movie_data)
            print("Movie added successfully!")
        else:
            print("Movie not found on OMDB.")

    def command_delete_movie(self, movie_title=None):
        """delete movie from list"""
        self._storage.delete_movie(movie_title)
        movie_title = input("Enter the title of the movie to delete: ")
        deleted_movie = self._storage.delete_movie(movie_title)

        if deleted_movie:
            print(f"Movie '{deleted_movie}' deleted successfully!")
        else:
            print("Movie not found.")

    def command_update_movie(self):
        movie_title = input("Enter the title of the movie to update: ")
        updated_movie = self._storage.get_movie(movie_title)

        if updated_movie:
            print(f"Current movie details: {updated_movie}")
            updated_rating = input("Enter the updated rating: ")
            updated_year = input("Enter the updated year: ")

            # Update the movie details in the `updated_movie` dictionary
            updated_movie['rating'] = updated_rating
            updated_movie['year'] = updated_year

            self._storage.update_movie(updated_movie)
            print(f"Movie '{movie_title}' updated successfully!")
        else:
            print("Movie not found.")

    def command_random_movie(self):
        """show user a random movie"""
        movies = self._storage.list_movies()
        if movies:
            import random
            random_movie = random.choice(list(movies.keys()))
            print(
                f"Random Movie: {random_movie} "
                f"({movies[random_movie]['rating']})")
        else:
            print("No movies found.")

    def command_search_movies(self):
        """allow user to search the list of movies"""
        movies = self._storage.list_movies()
        search_term = input("Enter a search term: ")
        found_movies = []
        for movie in movies:
            if search_term.lower() in movie.lower():
                found_movies.append(movie)
        if found_movies:
            print(f"Found movies containing '{search_term}':")
            for movie in found_movies:
                print(f"- {movie} ({movies[movie]['rating']})")
        else:
            print("No movies found.")

    def command_sort_movies(self):
        """sort movies by ranking"""
        movies = self._storage.list_movies()
        sort_order = input(
            "Enter 'asc' for ascending order or 'desc' for descending order: ")
        sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'],
                               reverse=(sort_order.lower() == 'desc'))
        print("Sorted movies:")
        for movie, data in sorted_movies:
            print(f"{movie}: {data['rating']}")

    def command_generate_website(self):
        movies = self._storage.list_movies()

        # Generate the HTML content for movie cards
        movie_cards = ""
        for movie_title, movie_data in movies.items():
            rating = movie_data.get('rating', '')
            year = movie_data.get('year', '')
            poster_url = movie_data.get('poster_url', '')

            movie_card = f"""
            <div class="movie-card">
                <img src="{poster_url}" alt="{movie_title} Poster"/>
                <h2>{movie_title}</h2>
                <p>Rating: {rating}</p>
                <p>Year: {year}</p>
            </div>
            """
            movie_cards += movie_card

        # Generate the complete HTML file
        website_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Movie Website</title>
            <link rel="stylesheet" type="text/css" href="style.css">
        </head>
        <body>
            <h1>Movie List</h1>
            <div class="movie-list">
                {movie_cards}
            </div>
        </body>
        </html>
        """

        # Write the website HTML content to a file (index.html)
        with open('index.html', 'w') as f:
            f.write(website_html)

        print("Website generated successfully!")

    def run(self):
        """accept user input from menu"""
        while True:
            # Print menu
            print_menu()

            # Get user command
            command = input("Enter your choice: ")

            # Execute command based on user input
            if command == "0":
                break
            elif command == "1":
                self.command_list_movies()
            elif command == "2":
                self.command_add_movie()
            elif command == "3":
                self.command_delete_movie()
            elif command == "4":
                self.command_update_movie()
            elif command == "5":
                self.command_movie_stats()
            elif command == "6":
                self.command_random_movie()
            elif command == "7":
                self.command_search_movies()
            elif command == "8":
                self.command_sort_movies()
            elif command == "9":
                self.command_generate_website()
            else:
                print("Invalid command. Please try again.")

            print()  # Add an empty line for readability
