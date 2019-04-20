import apiCalls
import sqlite3

# This function calls cityInfo and inputs the data into the DB if it is not already there
def yelp_info():
    cityEventsList = apiCalls.cityInfo()

    try:
        conn = sqlite3.connect('finalProj.sqlite')
        cur = conn.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS Top20EventsinCities(City TEXT, EventName TEXT UNIQUE, AttendanceCount INTEGER, Cost INTEGER)')
        conn.commit()

        for event in cityEventsList:
            vals = list(event.values())
            city_ = vals[0]
            name_ = vals[1]
            attendance_ = vals[2]
            cost_ = vals[3]

            cur.execute('INSERT INTO Top20EventsinCities(City, EventName, AttendanceCount, Cost) VALUES (?,?,?,?)', (city_, name_, attendance_, cost_, ))
            conn.commit()
    except:
        print('Events already in DB, please enter a different city')

#yelp_info()

def nyt_info():
    nytInfo = apiCalls.NYT_parse_request()

    conn = sqlite3.connect('finalProj.sqlite')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS NYT (Search TEXT, Title TEXT, Author TEXT, Section TEXT, Words INTEGER)')
    conn.commit()
    try:
        for article in nytInfo:
            vals = list(article.values())
            search_term = vals[0]
            title_ = vals[1]
            author_ = vals[2]
            section_ = vals[3]
            wordcount_ = vals[4]

            cur.execute('INSERT INTO NYT (Search, Title, Author, Section, Words) VALUES (?, ?, ?, ?, ?)', (search_term, title_, author_, section_, wordcount_))
            conn.commit()
    except:
        print("Search term already in database. Please enter a new one")

#nyt_info()

def openweather_sqlite():

	try:
		city_weather = apiCalls.city_info()
	
		conn = sqlite3.connect('finalProj.sqlite')
		cur = conn.cursor()
		cur.execute('CREATE TABLE IF NOT EXISTS Weather(city TEXT UNIQUE, temp REAL, humidity INTEGER , wind_speed REAL, clouds TEXT)')

		city = city_weather['city']
		temp = city_weather['temp']
		humidity = city_weather['humidity']
		wind_speed = city_weather['wind_speed']
		clouds = city_weather['clouds']
		cur.execute('INSERT OR IGNORE INTO Weather (city, temp, humidity, wind_speed, clouds) VALUES (?, ?, ?, ?, ?)',
                	(city, temp, humidity, wind_speed, clouds))
	
		conn.commit()
		return city_weather
	
	except:
		print("Not a valid city or you already entered that city")

openweather_sqlite()