from refreshbooks import api
from refreshbooks.client import FailedRequest
from django.shortcuts import render
from django.http import HttpResponse
import csv
from django.core.files.storage import default_storage
from uberimport.forms import UploadCSVForm

def index(request):
	greeting = "Hello"
	form = UploadCSVForm()
	return render(request, 'index.html', {'greeting' : greeting, 'form' : form})

def importer(request):
	resource = request.POST.get('resource')
	successes = []
	errors = []

	# Get API Creds
	subdomain = request.POST.get('subdomain').strip() + '.freshbooks.com'
	token = request.POST.get('token').strip()
	apiClient = api.TokenClient(subdomain, token)

	# Get the CSV Headers
	reader = csv.reader(request.FILES['file'], delimiter=",")
	headers = reader.next()
	headers = [x.strip() for x in headers]

	# Import all the things
	for row in reader:
		values = getDictionaryOfValues(row, headers)
		try:
			response = eval("getattr(apiClient, resource).create(" + resource + " = values)")
			successes.append(values)
		except FailedRequest as error:
			values['message'] = error.error
			errors.append(values)

	return render(request, 'results.html', {'successes' : successes, 'errors' : errors})

def getDictionaryOfValues(values, columns):
	mapping = {}

	for index, val in enumerate(columns):
		try:
			mapping[val] = values[index].strip()
		except:
			pass

	return mapping