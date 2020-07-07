import json
import logging
import pprint
import webbrowser

import requests

DEFAULT_BASE_URL = "https://www.thecocktaildb.com"
DEFAULT_KEY = 1


class CocktailDbAPI:
    def __init__(self, key=DEFAULT_KEY, base_url=DEFAULT_BASE_URL):
        self.key = key
        self.base_url = base_url
        self.logger = logging.getLogger("CocktailDbApi")

    def _request(self, url):
        self.logger.debug(f"Requesting: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.error(f"Got code: {response.status_code} on request {url}")
        data = json.loads(response.text)
        return data

    def show_image(self, data):
        try:
            url = data["strDrinkThumb"]
            webbrowser.open(url)
        except:
            pass

    def print(self, data):
        data = {k: v for (k, v) in data.items() if v}
        pprint.pprint(data)
        print(f"{data.get('strDrink')} - ({data.get('strCategory')}) - Image:{data.get('strDrinkThumb', None)}")

    def _make_url(self, action=None, extra=None):
        extra = f"?{extra}" if extra else ""
        return f"{self.base_url}/api/json/v1/{self.key}/{action}.php{extra}"

    def search_by_name(self, name):
        """ Search cocktail by name
        https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita
        """
        url = self._make_url(action="search", extra=f"s={name}")
        return self._request(url)

    def list_by_letter(self, letter):
        """
        List all cocktails by first letter
        https://www.thecocktaildb.com/api/json/v1/1/search.php?f=a
        """
        url = self._make_url(action="search", extra=f"f={letter}")
        return self._request(url)

    def search_ingred_by_name(self, name):
        """
        Search ingredient by name
        https://www.thecocktaildb.com/api/json/v1/1/search.php?i=vodka
        """
        url = self._make_url(action="search", extra=f"i={name}")
        return self._request(url)

    def get_by_id(self, id):
        """
        Lookup full cocktail details by id
        https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=11007
        """
        url = self._make_url(action="lookup", extra=f"i={id}")
        return self._request(url)

    def get_ingred_by_id(self, id):
        """
        Lookup ingredient by ID
        https://www.thecocktaildb.com/api/json/v1/1/lookup.php?iid=552
        """
        url = self._make_url(action="lookup", extra=f"ii={id}")
        return self._request(url)

    def get_random(self):
        """
        Lookup a random cocktail
        https://www.thecocktaildb.com/api/json/v1/1/random.php
        """
        url = self._make_url(action="random")
        return self._request(url)

    def get_10_random(self):
        """
        Lookup a selection of 10 random cocktails (only available to $2+ Patreon supporters)
        https://www.thecocktaildb.com/api/json/v1/1/randomselection.php
        """
        url = self._make_url(action="randomselection")
        return self._request(url)

    def get_popular(self):
        """
        List Popular cocktails (only available to $2+ Patreon supporters)
        https://www.thecocktaildb.com/api/json/v1/1/popular.php
        """
        url = self._make_url(action="popular")
        return self._request(url)


#
# List most latest cocktails (only available to $2+ Patreon supporters)
# https://www.thecocktaildb.com/api/json/v1/1/latest.php
#
# Search by ingredient
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=Gin
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=Vodka
#
# Filter by multi-ingredient (only available to $2+ Patreon supporters)
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=Dry_Vermouth,Gin,Anis
#
# Filter by alcoholic
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Alcoholic
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic
#
# Filter by Category
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=Ordinary_Drink
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=Cocktail
#
# Filter by Glass
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?g=Cocktail_glass
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?g=Champagne_flute
#
# List the categories, glasses, ingredients or alcoholic filters
# https://www.thecocktaildb.com/api/json/v1/1/list.php?c=list
# https://www.thecocktaildb.com/api/json/v1/1/list.php?g=list
# https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list
# https://www.thecocktaildb.com/api/json/v1/1/list.php?a=list
#
#
# Images
# Drink thumbnails
# Add /preview to the end of the cocktail image URL
# https://www.thecocktaildb.com/images/media/drink/vrwquq1478252802.jpg/preview (100x100 pixels)
#
#
# Ingredient Thumbnails
# https://www.thecocktaildb.com/images/ingredients/gin-Small.png (100x100 pixels)
# https://www.thecocktaildb.com/images/ingredients/gin-Medium.png (350x350 pixels)
# https://www.thecocktaildb.com/images/ingredients/gin.png (700x700 pixels)
#

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    api = CocktailDbAPI()
    drinks = api.get_random()
    drink = drinks["drinks"][0]

    api.print(drink)
    # api.show_image(drink)
