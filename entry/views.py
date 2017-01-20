import os

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from doctor.functions import finddata
from patients.models import Patient

from .models import Entry
from .forms import EntryForm

# Create your views here.
def index(request):
	return render(request, "main.html")

def entry_detail(request, id):

	instance = get_object_or_404(Entry, id=id)

	context = {
		"title" : instance.title,
		"instance" : instance,
	}

	return render(request, "entry_detail.html", context)


def entry_create(request):
	form = EntryForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

		# Set the user field to the current logged in patient 
		# 	data_pat = {"id": int(request.session.get("pat_id", None))}
   		# res = finddata(Patient, data_pat)
		# instance.user = res.id

		# define if on heroku environment
		ON_HEROKU = 'ON_HEROKU' in os.environ

		if ON_HEROKU: 

			base_url = "https://photodiary2.herokuapp.com"
			img_url = base_url + instance.image.url

			app = ClarifaiApp()
			model = app.models.get('food-items-v1.0')
			imgdata = model.predict_by_url(img_url)
			datalist = imgdata['outputs'][0]['data']['concepts']

			if datalist[0]['name'] == 'no person':
				datalist.pop(0)

			smart_content = ""
			for data in datalist:
				smart_content += data['name']
				smart_content += " "
			instance.content = smart_content

			smart_title = datalist[0]['name']
			instance.title = smart_title.title()
			
			instance.save()

		else:
			base = '/Users/marcus/Developer/capstone/TeamLegion/media_cdn'
			imgurl = instance.image.url
			imgurl = imgurl[6:]

			print imgurl

			app = ClarifaiApp()
			model = app.models.get('food-items-v1.0')

			image = ClImage(file_obj=open(base+imgurl, 'rb'))

			imgdata = model.predict([image])
			datalist = imgdata['outputs'][0]['data']['concepts']

			if datalist[0]['name'] == 'no person':
				datalist.pop(0)

			smart_content = ""
			for data in datalist:
				smart_content += data['name']
				smart_content += " "
			instance.content = smart_content

			smart_title = datalist[0]['name']
			instance.title = smart_title.title()
			
			instance.save()
	
		messages.success(request, "Successfully Created!")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"form" : form,
	}

	return render(request, "entry_form.html", context)


def entry_list(request):

	queryset_list = Entry.objects.all().order_by("-timestamp")

	for item in queryset_list:
		print(item.timestamp)

	# if request.session.get("pat_id"):
	# 	data_pat = {"id": int(request.session.get("pat_id", None))}
	# 	res = finddata(Patient, data_pat)
	# 	queryset_list = Entry.objects.filter(user_id=res.id)
	# else:
	# 	queryset_list = Entry.objects.filter(user_id=0)

	

	paginator = Paginator(queryset_list, 5) 
	page_request_var = "page"

	page = request.GET.get(page_request_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    queryset = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list" : queryset,
		"title" : "List",
		"page_request_var":page_request_var
	}

	return render(request, "entry_list.html", context)