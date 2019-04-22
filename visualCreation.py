import createDB

import sqlite3

import matplotlib
import matplotlib.pyplot as plt
import json

# This function calls information from the table, Top20EventsinCities, specifically city and attendanceCount columns
# to calculate the average attendance per city
def calcAvgAttendance():
    conn = sqlite3.connect("finalProj.sqlite")
    cur = conn.cursor()

    cur.execute('SELECT City, AttendanceCount FROM Top20EventsinCities')

    totalAttendance = {}
    cityAppears = {}

    for row in cur:
        city = row[0]
        if city not in totalAttendance:
            totalAttendance[city] = 0
        totalAttendance[city] += row[1]
        if city not in cityAppears:
            cityAppears[city] = 0
        cityAppears[city] += 1

    avgAttendance = {}

    for item in totalAttendance.items():
        city = item[0]
        total = item[1]
        avg = total / cityAppears[city]
        avgAttendance[city] = avg
    
    return avgAttendance

# This function calls information from the table, NYT, specifically section and words columns to calculate 
# the average word count per section
def avg_wordcount():
    conn = sqlite3.connect('finalProj.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT section, words FROM NYT")

    section_count = {}
    word_total = {}

    for row in cur:
        if row[0] not in section_count:
            section_count[row[0]] = 0
        section_count[row[0]] += 1
        if row[0] not in word_total:
            word_total[row[0]] = 0
        word_total[row[0]] += row[1]
    
    count_avg = {}

    for x in word_total.items():
        count_avg[x[0]] = x[1] / section_count[x[0]]
    
    return count_avg

# This function calls information from the table, Weather, specifically clouds column to calculate 
# the frequencies of cloud statuses:
def cloud_status():
    conn = sqlite3.connect('finalProj.sqlite')
    cur = conn.cursor()
    
    cur.execute('SELECT clouds FROM Weather')
    descriptions = {}
    for row in cur:
        status = row[0]
        if status not in descriptions:
            descriptions[status] = 0
        else:
            descriptions[status] += 1
	
    return sorted(list(descriptions.items()), key = lambda x: x[1], reverse = True)

# This function calls the above calculations and inputs the information into a json file, which is then
# used to create the visualizations
def calcFile():
    yelp = calcAvgAttendance()
    nyt = avg_wordcount()
    weather = cloud_status()

    new_file = {}
    new_file['yelp'] = yelp
    new_file['nyt'] = nyt
    new_file['weather'] = weather

    with open('calcFile.json', 'w') as outfile:
        json.dump(new_file, outfile)

#calcFile()

# This function creates a bar chart that plots the city on the x axis and the average attendance on the y axis
def createAttendanceVisual():
    f1 = open('calcFile.json', 'r')
    f1_ = f1.read()
    f2 = json.loads(f1_)
    dict_ = f2['yelp']
    xvals = dict_.keys()
    yvals = dict_.values()

    plt.bar(xvals, yvals, align='center', color = 'red') #color = ['red', 'blue', 'green', 'yellow']

    plt.xticks(rotation=45)
    plt.ylabel('Avg Attendance')
    plt.xlabel('City')
    plt.title('Avg Attendance per City')
    plt.tight_layout()
    plt.savefig('attendancePerCity.png')
    plt.show()


# This function creates a bar chart that plots the section name on the x axis and the average word count on the y axis
def createWordCountVisual():
    f1 = open('calcFile.json', 'r')
    f1_ = f1.read()
    f2 = json.loads(f1_)
    dict_ = f2['nyt']
    xvals = dict_.keys()
    yvals = dict_.values()

    plt.bar(xvals, yvals, align = 'center', color = 'blue')

    plt.xticks(rotation = 90)
    plt.ylabel('Average Word Count')
    plt.xlabel('Section Name')
    plt.title('Average Word Count Per Section')
    plt.tight_layout()
    plt.savefig('avgwordcount.png')
    plt.show()

# This function creates a bar chart that plots the cloud status  on the x axis and the frequency on the y axis
def createCloudStatusVisual():
    f1 = open('calcFile.json', 'r')
    f1_ = f1.read()
    f2 = json.loads(f1_)
    d = f2['weather']
    
    x_list = []
    y_list = []
    for item in d:
        x_list.append(item[0])
        y_list.append(item[1])
    
    xvals = x_list
    yvals = y_list
    
    plt.bar(xvals, yvals, align='center', color = 'yellow')
    
    plt.xticks(rotation=90)
    plt.ylabel("Number of cities")
    plt.xlabel("Sky Statuses")
    plt.title("Sky descriptions for Cities")
    plt.tight_layout()
    plt.savefig("CitySkyDescriptions.png")
    plt.show()

# In order to create an updated visual, with updated calculations, run this file
createAttendanceVisual()
createWordCountVisual()
createCloudStatusVisual()