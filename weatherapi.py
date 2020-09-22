import os
from tkinter import *
from PIL import ImageTk, Image
import requests
import datetime
from texttable import Texttable
from urllib.request import urlopen
from io import BytesIO
import matplotlib.pyplot as plt
from geopandas import *
from geopy import *
import folium  
from IPython.display import HTML, display
import webbrowser



# create the main tkinter window
window = Tk()
# set main tkinter window title
window.title('3-DAY WEATHER FORECAST API')
window.configure(background="lightblue")

#set icon image for the MAIN Tk WINDOW 
# Image should be in the same folder in which script is saved 
p1 = PhotoImage(file = 'corekara_image.png') 
# Setting icon of master window 
window.iconphoto(False, p1) 

# create text box entries
post_code = Entry(window, width=30)
post_code.insert(0, 'Enter Valid JP post code')
post_code.bind("<FocusIn>", lambda args: post_code.delete('0', 'end'))
post_code.grid(row=0,column=1, pady=(10,0), padx=10)

# create text box entry labels
post_code_label = Label(window, text="Post Code", width=30)
post_code_label.grid(row=0, column=0, pady=(10,0), padx=10, sticky=W+E)




def weatherAPI():
	# create a coordinates variable to be used in the api
	coordniates = post_code.get()

	params = {
	  'postal_code': coordniates,
	  'country':'JP',
	  'key':'aa48ad88872540c2b629a07581fda25f',
	}

	# handle errors in connecting to api
	try:
		api_result = requests.get('https://api.weatherbit.io/v2.0/forecast/daily?', params)
		api_output = api_result.json()
	except Exception as e:
		api_output = "Error connecting to API, please check your parameters"

	# create api output variables
	latitude = api_output['lat']
	longitude = api_output['lon']
	timezone = api_output['timezone']
	city = api_output['city_name']
	day_1 = api_output['data'][0]
	day_2 = api_output['data'][1]
	day_3 = api_output['data'][2]


	# create LISTS of results
	dates = [day_1['datetime'], day_2['datetime'], day_3['datetime']]
	icons = [day_1['weather']['icon'], day_2['weather']['icon'], day_3['weather']['icon']]
	dscrpts = [day_1['weather']['description'], day_2['weather']['description'], day_3['weather']['description']]
	maxtemp= [day_1['max_temp'], day_2['max_temp'], day_3['max_temp']]
	mintemp = [day_1['min_temp'], day_2['min_temp'], day_3['min_temp']]
	days = []

	# print(dates)

	# print(days)

	for dy in dates:
		values = dy.split('-')

		# print(values)
		day, month, year = (int(values[2]), int(values[1]), int(values[0]))
		new_values = datetime.date(year, month, day)
		list.append(days, new_values.strftime('%a'))

	# print(days)
	# print(timezone)

	new_maxtemp = [str(int(maxtemp[0])) + " °", str(int(maxtemp[1])) + " °", str(int(maxtemp[2])) + " °"]
	new_mintemp = [str(int(mintemp[0])) + " °", str(int(mintemp[1])) + " °", str(int(mintemp[2])) + " °"]

	#print address location
	# print(city)

	#print required values date, day, weather icon, weather description, max temp and min temp
	t = Texttable()
	t.add_rows([['Date', 'Day', 'Weather icon', 'Description', 'Max temp', 'Min temp'], 
		[dates[0], days[0], icons[0], dscrpts[0], new_maxtemp[0], new_mintemp[0]], 
		[dates[1], days[1], icons[1], dscrpts[1], new_maxtemp[1], new_mintemp[1]],
		[dates[2], days[2], icons[2], dscrpts[2], new_maxtemp[2], new_mintemp[2]]
		])


	

	address_label = Label(window, text=city + "\n" + "3-day forecast")
	address_label.grid(row=1, column=0, columnspan=3, pady=(10,0))

	# print(type(icons[0]))
	
	#SET FRAME 1 FOR DAY 1 
	# create frame label
	frame_1 = LabelFrame(window)
	#display frame on main window
	frame_1.grid(row=2, column=0, pady=(10,0), padx=(10,0))

	# GET THE WEATHER ICON FOR DAY 1
	# open day 1 weather icon 
	url_1 = "https://www.weatherbit.io/static/img/icons/" + icons[0] + ".png"
	u_1 = urlopen(url_1)
	raw_data_1 = u_1.read()
	u_1.close()
	
	icon_1 = ImageTk.PhotoImage(Image.open(BytesIO(raw_data_1)))
	#create day 1 weather icon label
	icon_1_label = Label(frame_1, image=icon_1)
	#display day 1 weather icon label
	icon_1_label.grid(row=0, column=0, columnspan=2)

	# SET DATE FOR DAY 1
	# create date label
	date_1_label = Label(frame_1, text=dates[0], anchor=W)
	#display date on frame
	date_1_label.grid(row=1, column=0)

	# SET DAY FOR DAY 1
	# create day label
	day_1_label = Label(frame_1, text=days[0], anchor=E)
	#display day on frame
	day_1_label.grid(row=1, column=1)

	# SET WEATHER DESCRIPTION FOR DAY 1
	# create description label
	descrption_1_label = Label(frame_1, text=dscrpts[0], anchor=W)
	#display description on frame
	descrption_1_label.grid(row=2, column=0, columnspan=2)

	# SET MAX TEMP OR DAY 1
	# create max temp label
	max_temp_1_label = Label(frame_1, text="max " + new_maxtemp[0], anchor=E)
	#display max temp on frame
	max_temp_1_label.grid(row=3, column=0, columnspan=2)

	# SET MIN TEMP OR DAY 1
	# create max temp label
	min_temp_1_label = Label(frame_1, text="min " + new_mintemp[0], anchor=W)
	#display max temp on frame
	min_temp_1_label.grid(row=3, column=2, columnspan=2)


	#SET FRAME 2 FOR DAY 2
	frame_2 = LabelFrame(window)
	frame_2.grid(row=2, column=1, pady=(10,0), padx=(10,0))

	# GET THE WEATHER ICON FOR DAY 2
	# open day 2 weather icon 
	url_2 = "https://www.weatherbit.io/static/img/icons/" + icons[1] + ".png"
	u_2 = urlopen(url_2)
	raw_data_2 = u_2.read()
	u_2.close()
	
	icon_2 = ImageTk.PhotoImage(Image.open(BytesIO(raw_data_2)))

	# create day 1 weather icon label
	icon_2_label = Label(frame_2, image=icon_2)
	# display day 1 weather icon label
	icon_2_label.grid(row=0, column=0, columnspan=2)

	# SET DATE FOR DAY 2
	# create date label
	date_2_label = Label(frame_2, text=dates[1], anchor=W)
	#display date on frame
	date_2_label.grid(row=1, column=0)

	# SET DAY FOR DAY 2
	# create day label
	day_2_label = Label(frame_2, text=days[1], anchor=E)
	#display day on frame
	day_2_label.grid(row=1, column=1)

	# SET WEATHER DESCRIPTION FOR DAY 2
	# create description label
	descrption_2_label = Label(frame_2, text=dscrpts[1], anchor=W)
	#display description on frame
	descrption_2_label.grid(row=2, column=0, columnspan=2)

	# SET MAX TEMP OR DAY 2
	# create max temp label
	max_temp_2_label = Label(frame_2, text="max " + new_maxtemp[1], anchor=E)
	#display max temp on frame
	max_temp_2_label.grid(row=3, column=0, columnspan=2)

	# SET MIN TEMP OR DAY 2
	# create max temp label
	min_temp_2_label = Label(frame_2, text="min " + new_mintemp[1], anchor=W)
	#display max temp on frame
	min_temp_2_label.grid(row=3, column=2, columnspan=2)


	#SET FRAME 3 FOR DAY 3 
	frame_3 = LabelFrame(window)
	frame_3.grid(row=2, column=2, pady=(10,0), padx=(10,10))

	# GET THE WEATHER ICON FOR DAY 3
	# open day 2 weather icon 
	url_3 = "https://www.weatherbit.io/static/img/icons/" + icons[2] + ".png"
	u_3 = urlopen(url_3)
	raw_data_3 = u_3.read()
	u_3.close()

	icon_3 = ImageTk.PhotoImage(Image.open(BytesIO(raw_data_2)))

	# create day 1 weather icon label
	icon_3_label = Label(frame_3, image=icon_3)
	# display day 1 weather icon label
	icon_3_label.grid(row=0, column=0, columnspan=2)

	# SET DATE FOR DAY 3
	# create date label
	date_3_label = Label(frame_3, text=dates[2], anchor=W)
	#display date on frame
	date_3_label.grid(row=1, column=0)

	# SET DAY FOR DAY 3
	# create day label
	day_3_label = Label(frame_3, text=days[2], anchor=E)
	#display day on frame
	day_3_label.grid(row=1, column=1)

	# SET WEATHER DESCRIPTION FOR DAY 3
	# create description label
	descrption_3_label = Label(frame_3, text=dscrpts[2], anchor=W)
	#display description on frame
	descrption_3_label.grid(row=2, column=0, columnspan=2)

	# SET MAX TEMP OR DAY 3
	# create max temp label
	max_temp_3_label = Label(frame_3, text="max " + new_maxtemp[2], anchor=E)
	#display max temp on frame
	max_temp_3_label.grid(row=3, column=0, columnspan=2)

	# SET MIN TEMP OR DAY 3
	# create max temp label
	min_temp_3_label = Label(frame_3, text="min " + new_mintemp[2], anchor=W)
	#display max temp on frame
	min_temp_3_label.grid(row=3, column=2, columnspan=2)

	#SET FRAME 4 FOR MAP
	frame_4 = LabelFrame(window)
	frame_4.grid(row=3, column=0, columnspan=2, pady=(10,10), padx=(10,0))

	
	# VISUALISE MAP
	map1 = folium.Map(
    location=[latitude,longitude],
    tiles='cartodbpositron',
    zoom_start=12,
	)
	lambda row:folium.CircleMarker(location=[latitude, longitude]).add_to(map1)
	

	# mapWidth, mapHeight = (400,500) # width and height of the displayed iFrame, in pixels
	# srcdoc = map1._repr_html_()
	# embed = HTML('<iframe srcdoc="{}" '
 #             'style="width: {}px; height: {}px; display:block; width: 50%; margin: 0 auto; '
 #             'border: none"></iframe>'.format(srcdoc, mapWidth, mapHeight))


	map1.save('1.html')

	map_label = Label(frame_4, text=webbrowser.open('1.html'))
	# map_label = Label(frame_4, text=display(embed))
	map_label.grid(row=0, column=0, columnspan=2, sticky=W+E)




	#SET FRAME 5 FOR FREE SPACE
	frame_5 = LabelFrame(window)
	frame_5.grid(row=3, column=1, columnspan=2, pady=(10,10), padx=(0,10))

	


	def plotGraph():
		# Make a data frame
		bars = [(str(days[0]) + " " + str(dates[0])), (str(days[1]) + " " + str(dates[1])), (str(days[2]) + " " + str(dates[2]))]

		df=pd.DataFrame({'x': bars, 'max_temp': [int(maxtemp[0]), int(maxtemp[0]), int(maxtemp[0])], 
			'min_temp': [int(mintemp[0]), int(mintemp[1]), int(mintemp[2])]})
		 
		# Initialize the figure
		plt.style.use('seaborn-darkgrid')
			 
		# create a color palette
		palette = plt.get_cmap('Set1')
		 
		# multiple line plot
		num=0
		for column in df.drop('x', axis=1):
			num+=1
		 
			# Find the right spot on the plot
			plt.subplot(2,1, num)
		 
		    # Plot the lineplot
			plt.plot(df['x'], df[column], marker='', color=palette(num), linewidth=1.9, alpha=0.9, label=column)
			
		 
		    # Same limits for everybody!
			# plt.xlim(0,100)
			plt.ylim(-11,40)

			# Not ticks everywhere
			plt.tick_params(axis ='both', which ='major',  
               labelsize = 9, pad = 10,  
               colors ='black')
			# plt.tick_params(labelleft='off')
		 
		    # Add title
			plt.title(column, loc='left', fontsize=10, fontweight=0, color=palette(num) )
		 
		# general title
		plt.suptitle(city + "\n3-day Temperature forecast", fontsize=9, fontweight=0, color='black', style='italic', y=0.99)
		 
		# Axis title
		plt.text(1, -25, 'Date', fontsize=10)
		plt.text(-0.30, 40, 'Temperature', fontsize=10, rotation='vertical')

		plt.show()

	button_plot = Button(frame_5, text="View Temperature graph", command=plotGraph)
	button_plot.grid(row=0, column=0, pady=(10,0), padx=10)



button_submit = Button(window, text="Submit", command=weatherAPI)
button_submit.grid(row=0, column=3, pady=(10,0), padx=10)

def closeProgram():
	window.destroy()

quit_button = Button(window, text="close", comman=closeProgram)
quit_button.grid(row=4, column=3, pady=(10,10), padx=10)



window.mainloop()
