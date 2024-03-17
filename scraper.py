import requests
import re
from bs4 import BeautifulSoup
from textblob import TextBlob

BASE_URL = 'https://www.yelp.com/biz/'

class EscapeRoom:
    def __init__(self, room_url):
        self.base_url = BASE_URL
        self.room_url = room_url
        self.full_url = f'{self.base_url}{self.room_url}'
        self.soup = BeautifulSoup(requests.get(self.full_url).text, 'html.parser')

        # Abstracted intializations
        self.name, self.city, self.rating = self.set_room_info()
        self.upper_bound = self.set_reviews_loop_upper_bound()
        self.all_reviews = self.set_all_page_reviews()
    
    # Returns the upper bound for looping through the review pages.
    # Example: If the review page consists of 20 pages, then the search query will
    # append '?start=190' to the URL to get to the last review page. This function will
    # return 191, the upper bound needed for a for-loop to go through all the review pages.
    def set_reviews_loop_upper_bound(self):
        upper_bound = 0
        # 'css-chan6m' elements contain a "# of #", with the former being the current review page
        # and the latter being the last review page.
        chan6m_elems = self.soup.find_all(class_='css-chan6m')
        for chan6m_elem in chan6m_elems:
            if 'of' in chan6m_elem.text:
                upper_bound = (int(chan6m_elem.text.split()[-1]) - 1) * 10 + 1 # get last review page
                return upper_bound
        return upper_bound
    
    # Takes in a soup object and retuns the escape room's name and the city the room is in
    def set_room_info(self):
        room_title_info = self.soup.title.text.split('-')
        
        # Title is the 0th element in the list with trailing white spaces
        room_name = room_title_info[0].strip().lower()

        # Address is the 2nd elemnt in the list, city is the second to last element in list with trailing white spaces
        room_city = room_title_info[2].split(',')[-2].strip()

        # Get the overall rating of the escape room
        overall_rating_pattern = re.compile(r'(?:[1-4](?:\.5)?|5(?:\.0)?) star rating')
        # seems like 2 of the same gets extracted, pick the 0th element
        room_overall_element = self.soup.find_all('div', {'aria-label': overall_rating_pattern, 'class': 'css-1v6kfrx'})[0]
        room_overall_rating = float(room_overall_element['aria-label'].split()[0])

        return room_name, room_city, room_overall_rating
    
    # Gets every review of an escape room and returns it in a list
    def set_all_page_reviews(self):
        # Helper function that takes in a soup object and returns the reviews of
        # that "page" as a list of reviews
        def get_page_reviews(soup_obj):
            page_reviews = []
            # Class='raw__09f24__T4Ezm' and lang='en' tags specifies reviews
            review_elements = soup_obj.find_all(class_='raw__09f24__T4Ezm', lang='en')
            for review_element in review_elements:
                review = review_element.text
                page_reviews.append(review)
            return page_reviews
        
        # Helper function that takes in a soup object and returns the rating of
        # that "page" as a list of ratings
        def get_page_ratings(soup_obj):        
            # regex pattern to capture review ratings
            user_rating_pattern = re.compile(r'(?:[1-4](?:\.5)?|5(?:\.0)?) star rating')
            page_ratings = []
            rating_elements = soup_obj.find_all('div', {'aria-label': user_rating_pattern, 'class': 'css-14g69b3'})
            for rating_element in rating_elements:
                rating_value = rating_element['aria-label'].split()[0] # just want the number
                page_ratings.append(rating_value)

            # list comp to convert strings to ints (user ratings have no decimals)
            return [int(page_rating) for page_rating in page_ratings[:10]]

        all_reviews = []
        #### CHANGE UPPER BOUND LATER ####
        for i in range(0, 11, 10): # loop through all review pages
            curr_full_url = self.full_url
            if i != 0: # append appropriate search query for review page
                curr_full_url += f'?start={i}' 
            
            # Make html request on full_url and create soup object
            curr_html = requests.get(curr_full_url)
            curr_soup_obj = BeautifulSoup(curr_html.text, 'html.parser')

            # .extend instead of .append because get_page_reviews returns a list
            all_reviews.extend(get_page_reviews(curr_soup_obj))
        return all_reviews
