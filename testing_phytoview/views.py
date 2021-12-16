from django.shortcuts import render,redirect
# from .forms import TrackForm
import modules.ATL03_trackfinder as tf
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from laserviz.forms import PickTimesForm , PickTrackForm
# def homepage(request):
# 	return render(request,'index.html')

# def homepage(request):
# 	import modules.ATL03_trackfinder as tf
# 	url_data = tf.map_init()
# 	return render(request,'index.html',{'url_data':url_data})

# def homepage(request):
# 	import modules.ATL03_trackfinder as tf
# 	import matplotlib
# 	import plotly.graph_objects as go
# 	import matplotlib.pyplot as plt 
# 	import cartopy.crs as ccrs

# 	# make your base arctic map people see on the homepage
# 	fig = go.Figure(figsize=(7,7))
# 	axs = plt.axes(projection=ccrs.NorthPolarStereo())
# 	axs.coastlines(resolution='10m')
# 	axs.gridlines()
# 	axs.set_extent([-40,150,75,89.9],crs=ccrs.PlateCarree())

# 	## testing ability for template to take python event handling

# 	points = axs.scatter(180,80,picker=True,transform=ccrs.NorthPolarStereo())
# 	fig.write_html("test")
# 	return render(request,'index.html',{'chart':chart})

# def plot_data(request):
# 	import modules.ATL03_trackfinder as tf
# 	import os
# 	import h5py

# 	# dates = request.GET['requested_dates']
# 	start_date = request.POST.get('start_input','This is a default value')
# 	end_date = request.POST.get('end_input','This is a default value')
# 	[data,lats,lons] = tf.getTracks(start_date,end_date)

# 	[fig_html, track_info]= tf.makeMap(lons,lats)
# 	# context = {
# 	# 	"data":data,
# 	# 	"lats":ilat,
# 	# 	"lons":ilon,
# 	# }

# 	print(lats)
# 	return render(request,'index.html',{'data':data,'figure':fig_html,'track_info':track_info})

# def plot_data(request):
# 	import modules.ATL03_trackfinder as tf
# 	import os
# 	import h5py

# 	timeform = PickTimesForm(request.POST)
# 	trackform = PickTrackForm(None)
# 	target_directory= '/home/bitnami/htdocs/projects/laserviz/data/'

# 	context = {}
# 	if timeform.is_valid():
# 		timeform.save()
# 		print('yes')
# 		start_date = timeform.cleaned_data.get("start_date")
# 		print(start_date)
# 		end_date = timeform.cleaned_data.get("end_date")
# 		print(end_date)
# 		context["start_date"]=start_date
# 		context["end_date"]=end_date
# 		[data,lats,lons] = tf.getTracks(start_date,end_date,target_directory)
# 		context["data"]=data
# 		[fig_html, track_info]= tf.makeMap(lons,lats)
# 		context["figure"]=fig_html
# 		context["track_info"]=track_info
		
# 	# dates = request.GET['requested_dates']

	
# 	context["timeform"]=timeform
# 	context["trackform"]=trackform


# 	return render(request,'index.html',context)

def plot_data(request,pk):
    filename = get_object_or_404(DisplayData, pk=pk)
	context={}
	trackform = PickTrackForm()
	context["trackform"]=trackform

	if request.method == 'POST':
		timeform = PickTimesForm(request.POST)
		if timeform.is_valid():
			target_directory= '/home/bitnami/htdocs/projects/laserviz/data/'
			start_date = timeform.cleaned_data.get("start_date")
			end_date = timeform.cleaned_data.get("end_date")
			
			[data,lats,lons] = tf.getTracks(start_date,end_date,target_directory)
			[fig_html, track_info]= tf.makeMap(lons,lats)
			
			# context["figure"]=fig_html
			# context["track_info"]=track_info
			# context["timeform"]=timeform
			# context["start_date"]=start_date
			# context["end_date"]=end_date
			# context["data"]=data

            filename.TestModelField = form.cleaned_data("start_date")
            filename.save()

			return HttpResponseRedirect(request,'index.html',context)
	else:
		timeform = PickTimesForm()
		context['timeform']=timeform
	return render(request,'index.html',context)

		
	


def homepage(request):

	timeform = PickTimesForm(None)
	trackform = PickTrackForm(None)
	[fig_html,track_info] = tf.makeMap()

	context = {
		'figure':fig_html,
		'timeform':timeform,
		'trackform':trackform,
	}

	return render(request,'index.html',context)

# @csrf_exempt
# def pick_track(request):
# 	if request.method == 'POST':
# 		form = TrackForm(request.POST)

# 		if form.is_valid():
# 			track_number = form.cleaned_data['your_track']
			
# 	else:
# 		track_number = 'fuck'
	
# 	return render(request,'plot_popup.html',{'track_number':track_number})

@csrf_exempt
def track(request):
	trackform = PickTrackForm(request.POST)
	timeform = PickTimesForm(None)
	context = {}
	if trackform.is_valid():
		print('yes')
		track_number = trackform.cleaned_data.get("track_number")
		print(track_number)
		context['track_number']=track_number
		
	context['trackform']=trackform
	context['timeform']=timeform
	return render(request,'plot_popup.html',context)


# def homepage(request):
# 	import matplotlib.pyplot as plt
# 	import numpy as np

# 	import mpld3 
# 	from mpld3 import plugins, fig_to_html

# 	import modules.ATL03_trackfinder as tf
# 	import cartopy.crs as ccrs

# 	# make your base arctic map people see on the homepage
# 	fig = plt.figure()
# 	ax=plt.axes(projection=ccrs.NorthPolarStereo())

	

# 	ax.set_extent([-150,150,50,90],crs=ccrs.PlateCarree())
# 	# ax.coastlines()
# 	ax.stock_img()
	
# 	points = ax.scatter([20,30,50,80],[78,80,88,87],transform = ccrs.PlateCarree())
# 	# labels = ['point label']

# 	# tooltip = plugins.PointLabelTooltip(points,labels)
# 	plugins.connect(fig,plugins.PointLabelTooltip(points))

# 	fig_html = mpld3.fig_to_html(fig)

# 	return render(request,'index.html',{'figure':fig_html})




