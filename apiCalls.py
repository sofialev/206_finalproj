import requests
import json
import secret


# This function makes a call to the yelp api using the city inputted by the user and 
# returns no more than 20 events
def yelpRequest(city):
    header = {'Authorization': "Bearer %s" % secret.yelp_api_key}
    params= {}
    params['limit'] = 20
    params['location'] = city
    url = 'https://api.yelp.com/v3/events'
    response = requests.get(url, params=params, headers=header)
    new = json.loads(response.text)
    return new

# This function goes through the dictionary returned by yelpRequest to create a list of 
# dictionaries, where each dictionary contains information about an individual event
def cityInfo():
    city = inputCity()
    data = yelpRequest(city)

    cityEvents = []

    for event in data['events']: 
        indivEvent = {}
        indivEvent['city'] = city
        indivEvent['name'] = event['name']
        indivEvent['attending'] = event['attending_count']
        indivEvent['cost'] = event['cost']
        cityEvents.append(indivEvent)

    return cityEvents

# This function asks the user to input a city name
def inputCity():
    user = input('Please enter a city name ')
    return user

# This function makes a call to the NYT API using the provided search term
def nytRequest(search_term):
    my_key = secret.nyt_api_key
    type_of_material = "Article"
    #filter_ = input_filter()
    #base_url = 'https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key='
    base_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
    params = {'q': search_term, 'fq': type_of_material, 'api-key': my_key}
    response = requests.get(url = base_url, params = sorted(params.items()))
    new = json.loads(response.text)
    return new['response']['docs']

# This function asks the user to enter a search term
def input_term():
    user = input("Please enter a search term: ")
    return user

# This function calls the function input_term, and then uses it to make a call to nytRequest,
# it then returns a list of dictionaries. Each dictionary contains information about one of the 
# articles returned by nytRequest
def NYT_parse_request():
    search_term = input_term()
    data = nytRequest(search_term)
    search_articles = []
    for item in data:
        indivResult = {}
        indivResult['search term'] = search_term
        indivResult['title'] = item['headline']['main']
        indivResult['author'] = item['byline']['original']
        indivResult['section'] = item['section_name']
        indivResult['word count'] = item['word_count']
        search_articles.append(indivResult)
    return search_articles

# This function makes a call to the Open Weather API using the inputted city
def ow_make_request(city):
	key = secret.ow_api
	url = "http://api.openweathermap.org/data/2.5/weather?"
	response = requests.get(url + "q=" + city + "&units=imperial" + "&appid=" + key)
	new = json.loads(response.text)

	return new

# This function asks the user to input a city 
def input_city():
	user = input("Please enter a city name ")
	return user

# This function goes through the  object returned by ow_make_request and returns a
# dictionary that includes certain information
def city_info():
	city = input_city()
	data = ow_make_request(city)
	new_dict = {}
	new_dict['city'] = city	
	new_dict['temp'] = data['main']["temp"]
	new_dict['humidity'] = data['main']['humidity']
	new_dict['wind_speed'] = data['wind']['speed']
	for i in data['weather']:
		new_dict['clouds'] = i['description']
	return new_dict
	

