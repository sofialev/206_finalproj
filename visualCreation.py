import createDB

import sqlite3

import matplotlib
import matplotlib.pyplot as plt

# This function calls information from the city and attendanceCount columns to calculate the average attendance per city
def calcAvgAttendance():
    conn = sqlite3.connect("finalProj.sqlite")
    cur = conn.cursor()

    cur.execute('SELECT City, AttendanceCount FROM Top20EventsinCities')

    totalAttendance = {}

    for row in cur:
        city = row[0]
        if city not in totalAttendance:
            totalAttendance[city] = 0
        totalAttendance[city] += row[1]

    avgAttendance = {}

    for item in totalAttendance.items():
        city = item[0]
        total = item[1]
        avg = total / 20
        avgAttendance[city] = avg
    
    return avgAttendance

#print(calcAvg())

# This function creates a bar chart that plots the city on the x axis and the average attendance on the y axis
def createAttendanceVisual():
    dict_ = calcAvgAttendance()
    xvals = dict_.keys()
    yvals = dict_.values()

    plt.bar(xvals, yvals, align='center', color = 'red') #color = ['red', 'blue', 'green', 'yellow']

    plt.xticks(rotation=45)
    plt.ylabel('Avg Attendance')
    plt.xlabel('City')
    plt.title('Avg Attendance per City')
    plt.savefig('attendancePerCity.png')
    plt.show()


def avg_wordcount():
    # get a list of how many articles for each city (city_len)
    # get a count of how many views for each city (city_views)
    # divide the count by how many articles for each city (city_avg)
    # create a dictionary with city as keys and average as values (avg_dict)
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

    
def createWordCountVisual():
    dict_ = avg_wordcount()
    xvals = dict_.keys()
    yvals = dict_.values()

    plt.bar(xvals, yvals, align = 'center', color = 'blue')

    plt.xticks(rotation = 90)
    plt.ylabel('Average Word Count')
    plt.xlabel('Section Name')
    plt.title('Average Word Count Per Section')
    plt.savefig('avgwordcount.png')
    plt.show()


#calculate the frequencies of cloud statuses from the data base
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


#create a bar graph of the frequencies of cloud statuses for all the cities
def createCloudStatusVisual():
	d = cloud_status()
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

createAttendanceVisual()
createWordCountVisual()
createCloudStatusVisual()