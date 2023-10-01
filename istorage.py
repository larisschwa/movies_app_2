class IStorage:
    """
    An abstract base class representing a movie storage interface.

    Attributes:
        movies (dict): A dictionary to store movie data.

    Methods:
        __init__:
            Initializes the storage class by creating an empty movies
            dictionary.

        list_movies:
            Retrieves and returns a dictionary containing movie data.

        add_movie:
            Adds a movie to the storage database.
            Args:
                movie_data (dict): A dictionary containing movie information,
                including title, rating, year, and poster URL.

        delete_movie:
            Deletes a movie from the storage database based on its title.
            Args:
                movie_title (str): The title of the movie to be deleted.
            Returns:
                str or None: The title of the deleted movie if successful, or
                None if the movie was not found.

        update_movie:
            Updates the information of a movie in the storage database.
            Args:
                movie_data (dict): A dictionary containing updated movie
                information.
                    It must include 'title', 'rating', 'year', and 'poster_url'
                    fields.

        get_movie:
            Retrieves a movie from the storage database based on its title.
            Args:
                movie_title (str): The title of the movie to retrieve.
            Returns:
                dict or None: A dictionary containing movie information if
                found, or None if the movie was not found.
    """
    def __init__(self):
        """initialize movies dictionary"""
        self.movies = {}

    def list_movies(self):
        """get list of movies"""
        return self.movies

    def add_movie(self, movie_data):
        """add movie to database"""
        title = movie_data['title']
        self.movies[title] = movie_data

    def delete_movie(self, movie_title):
        """delete movie from database"""
        if movie_title in self.movies:
            del self.movies[movie_title]
            return movie_title

    def update_movie(self, movie_data):
        """update movie title"""
        title = movie_data['title']
        if title in self.movies:
            self.movies[title] = movie_data

    def get_movie(self, movie_title):
        pass
