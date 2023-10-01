import json
from istorage import IStorage


class StorageJson(IStorage):
    """
    A class for storing and managing movie data in a JSON file.

    This class provides methods to interact with movie data stored in a
    JSON file.
    It inherits from the 'IStorage' interface.

    Args:
        filename (str): The name of the JSON file to store movie data.

    Methods:
        list_movies(): Retrieve and return a dictionary of movies from the
        JSON file.
        add_movie(movie_data): Add a new movie to the JSON file.
        delete_movie(movie_title): Delete a movie from the JSON file by title.
        update_movie(movie_data): Update the details of an existing movie in
        the JSON file.

    Private Methods:
        _load_data(): Load data from the JSON file.
        _save_data(data): Save data to the JSON file.

    Example:
        storage = StorageJson('data.json')
        movies = storage.list_movies()
        storage.add_movie({
            'title': 'Inception',
            'rating': '8.8',
            'year': '2010'
        })
        storage.delete_movie('The Matrix')
        storage.update_movie({
            'title': 'The Dark Knight',
            'rating': '9.0',
            'year': '2008'
        })
    """
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def _load_data(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        return data

    def _save_data(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def list_movies(self):
        """list movies in file"""
        data = self._load_data()
        return data

    def add_movie(self, movie_data):
        data = self._load_data()
        title = movie_data['title']
        data[title] = {
            'rating': movie_data['rating'],
            'year': movie_data['year'],
            'poster_url': movie_data.get('poster_url', '')
        }
        self._save_data(data)

    def delete_movie(self, movie_title):
        data = self._load_data()
        if movie_title in data:
            del data[movie_title]
            self._save_data(data)
            return movie_title
        else:
            return None

    def update_movie(self, movie_data):
        data = self._load_data()
        title = movie_data['title']
        if title in data:
            data[title]['rating'] = movie_data['rating']
            data[title]['year'] = movie_data['year']
            self._save_data(data)
