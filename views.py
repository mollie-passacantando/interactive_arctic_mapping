from django.shortcuts import render,redirect
# from .forms import TrackForm
import modules.ATL03_trackfinder as tf
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from laserviz.forms import PickTimesForm , PickTrackForm
from mainapp.models import DataModel

@csrf_exempt
def plot_data(request):
	context={}
	trackform = PickTrackForm()
	context["trackform"]=trackform
	print('plot data initiated')
	if request.method == 'POST':
		timeform = PickTimesForm(request.POST)
		print('post request confirmed')
		if timeform.is_valid():
			print('timeform valid')
			target_directory= '/home/bitnami/htdocs/projects/laserviz/data/'
			start_date = timeform.cleaned_data.get("start_date")
			end_date = timeform.cleaned_data.get("end_date")
			
			[data,lats,lons,heights,dist_corrected] = tf.getTracks(start_date,end_date,target_directory)
			print(lats.shape)
			[fig_html, track_info]= tf.makeMap(lons,lats)

			# create a model instance and fill with lats,lons,and trackid
			i=0
			for track in track_info:
				record = DataModel(TrackID = track)
				print(isinstance(track,int))
				# track_info = track_info.tolist()
				current_lats = lats[i,:]
				current_lons = lons[i,:]
				current_heights = heights[i,:]
				current_dist = dist_corrected[i,:]

				listlats = current_lats.tolist()
				listlons = current_lons.tolist()
				listheight = current_heights.tolist()
				listdist = current_dist.tolist()
				print('converted to list')
				# setattr(record,"TrackID",track)
				setattr(record,"lats",listlats)
				setattr(record,"lons",listlons)
				setattr(record,"heights",listheight)
				setattr(record,"dist_along_track",listdist)
				record.save()
				print('setattributes')
				
				i=i+1

			context["figure"]=fig_html
			context["track_info"]=track_info
			context["timeform"]=timeform
			context["start_date"]=start_date
			context["end_date"]=end_date
			context["data"]=data


			
	else:
		print('hit else statement')
		timeform = PickTimesForm()
		context['timeform']=timeform

	return render(request,'extend_template.html',context)

		
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

		mytrack = DataModel.objects.get(TrackID=track_number)
		mydists = getattr(mytrack,'dist_along_track')
		myheights = getattr(mytrack,'heights')
		fig_html = tf.plotchl(mydists,myheights)
		context['chlfig'] = fig_html
		context['popup'] = True
		
	context['trackform']=trackform
	context['timeform']=timeform
	
	return render(request,'index.html',context)

# def plot_chl(request):



