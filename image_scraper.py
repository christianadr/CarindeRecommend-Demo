import requests
from bs4 import BeautifulSoup

def search_image(query):
    url = "https://www.allrecipes.com/recipes/696/world-cuisine/asian/filipino/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        recipe_links = soup.find_all("a")

        for link in recipe_links:
            if link.string == query:
                recipe_url = link["href"]
                recipe_response = requests.get(recipe_url)

                if recipe_response.status_code == 200:
                    recipe_soup = BeautifulSoup(recipe_response.content, "html.parser")
                    image = recipe_soup.find("img")

                    if image is not None:
                        image_url = image["src"]
                        return image_url

    return None

# Example usage
meal = "Pancit Molo (Filipino Wonton Soup)"
image_url = search_image(meal)
if image_url is not None:
    print(f"Image URL for '{meal}': {image_url}")
else:
    print(f"No image found for '{meal}'")
