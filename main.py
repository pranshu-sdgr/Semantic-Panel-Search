from data import reader

def main():
    print("Loading movie data...")
    movies = reader.get_movies_data()
    if movies:
        print(f"Loaded {len(movies)} movies.")
        for movie in movies[:5]:  # Print first 5 movies as a sample
            print(movie)
        movie_with_description_and_title = 0
        for movie in movies:
            if movie.get('description') and movie.get('title'):
                movie_with_description_and_title += 1
        print(f"Number of movies with both description and title: {movie_with_description_and_title}")
    else:
        print("No movie data available.")


if __name__ == "__main__":
    main()