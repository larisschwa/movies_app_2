import csv
from istorage import IStorage


class StorageCsv(IStorage):
    """
    A class that implements the IStorage interface using a CSV file for
    data storage.

    Args:
        csv_file (str): The path to the CSV file used for storage.

    Methods:
        list_movies:
            Retrieves and returns a dictionary of movies from the CSV file.
            Returns:
                dict: A dictionary containing movie data with titles as keys.

        add_movie:
            Adds a new movie to the CSV file.
            Args:
                movie_data (dict): A dictionary containing movie information,
                including title, rating, year, and poster URL.

        delete_movie:
            Deletes a movie from the CSV file based on its title.
            Args:
                movie_title (str): The title of the movie to be deleted.
            Returns:
                str or None: The title of the deleted movie if successful, or
                None if the movie was not found.

        update_movie:
            Updates the rating and year of a movie in the CSV file.
            Args:
                movie_data (dict): A dictionary containing updated movie
                information.
                    It must include 'title', 'rating', and 'year' fields.

    Private Methods:
        _save_movies:
            Writes the movie data to the CSV file.
            Args:
                movies (dict): A dictionary containing movie data with titles
                as keys.
    """
    def __init__(self, csv_file):
        super().__init__()
        self.csv_file = csv_file

    def list_movies(self):
        movies = {}
        with open(self.csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row['title']
                rating = row.get('rating', 'N/A')
                year = row.get('year', 'N/A')
                poster_url = row.get('poster_url',
                                     'N/A')
                movies[title] = {
                    'rating': rating,
                    'year': year,
                    'poster_url': poster_url
                }
        return movies

    def add_movie(self, movie_data):
        title = movie_data['title']
        rating = movie_data['rating']
        year = movie_data['year']
        poster_url = movie_data['poster_url']

        with open(self.csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([title, rating, year, poster_url])

    def delete_movie(self, movie_title):
        movies = self.list_movies()
        if movie_title in movies:
            del movies[movie_title]
            self._save_movies(movies)
            return movie_title

    def update_movie(self, movie_data):
        movies = self.list_movies()
        title = movie_data['title']
        if title in movies:
            movies[title]['rating'] = movie_data['rating']
            movies[title]['year'] = movie_data['year']
            self._save_movies(movies)

    def _save_movies(self, movies):
        with open(self.csv_file, 'w', newline='') as file:
            fieldnames = ['title', 'rating', 'year', 'poster_url']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for movie_title, movie_data in movies.items():
                writer.writerow({
                    'title': movie_title,
                    'rating': movie_data['rating'],
                    'year': movie_data['year'],
                    'poster_url': movie_data['poster_url']
                })
