import httpx

TMDB_API_KEY = "bf44969be4cff25fe948f33c7210b6f1"  # 🔑 جایگزین کن با API Key از سایت themoviedb.org

def search_movie(movie_title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title,
        "language": "en-US"
    }

    try:
        response = httpx.get(url, params=params, timeout=10)
        response.raise_for_status()  # اگر خطای HTTP بود، متوقف می‌شود
        data = response.json()

        if data["results"]:
            movie = data["results"][0]
            title = movie["title"]
            overview = movie.get("overview", "No summary available.")
            poster_path = movie.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

            return {
                "title": title,
                "overview": overview,
                "poster_url": poster_url
            }

    except httpx.RequestError as e:
        print("TMDB Request Error:", e)
    except httpx.HTTPStatusError as e:
        print("TMDB Response Error:", e)

    return None

