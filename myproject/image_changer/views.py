from django.shortcuts import render, redirect
from .models import Image
from .forms import LoadImageForm, ChangeSizeForm
from io import BytesIO
from django.contrib import messages
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as img
import sys
import requests

def home(request):
	images = Image.objects.exclude(name__startswith = 'copy')
	return render(request, 'index.html', {'images': images})

def get_image_by_url(url, image):
	response = requests.get(url, stream=True)
	file_name = url.split('/')[-1]
	lf = NamedTemporaryFile()
	for block in response.iter_content(1024 * 8):
		if not block:
			break
		lf.write(block)
	image.picture.save(file_name, File(lf))

def check_both_fill(form, request):
		value1 = form.cleaned_data['image_url']
		value2 = form.cleaned_data['image_file']
		if value1 and value2:
			messages.error(request, 'Выберите только один способ.')
			return True
		elif not value1 and not value2:
			messages.error(request, 'Воспользуйтесь одним из способов.')
			return True
		return False

def load_image(request):
	if request.method == 'POST':
		form = LoadImageForm(request.POST, request.FILES)
		if form.is_valid():
			if check_both_fill(form, request):
				return redirect('load-image')
			image = Image.objects.create()
			url = form.cleaned_data.get('image_url')
			if url:
				get_image_by_url(url, image)
			else:
				image.picture = form.cleaned_data['image_file']
			image.name = image.picture.name
			image.save()
			return redirect('change-size/{}/'.format(image.id))
	form = LoadImageForm()
	return render(request, 'load.html', {'form': form})

def size_changer(x, y, old_image, new_image):
	im = img.open(old_image.picture)
	output = BytesIO()
	if x and not y:
		wpercent = (x / float(im.size[0]))
		y = int((float(im.size[1]) * float(wpercent)))
	elif y and not x:
		hpercent = (y / float (im.size[1]))
		x = int ((float (im.size[0]) * float (hpercent)))
	im = im.resize( (x,y) )
	im.save(output, format='JPEG', quality=100)
	output.seek(0)
	new_image.picture = InMemoryUploadedFile(output,'ImageField',
		"%s.jpg" %old_image.picture.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

def check_xy_fill(form, request):
		value1 = form.cleaned_data['x']
		value2 = form.cleaned_data['y']
		if not value1 and not value2:
			messages.error(request, 'Заполните одно из полей.')
			return True
		return False

def change_size(request, pk):
	new_image = None
	image =Image.objects.get(id=pk)
	if request.method == 'POST':
		form = ChangeSizeForm(request.POST)
		if form.is_valid():
			if check_xy_fill(form, request):
				return redirect('change-size/{}/'.format(pk))
			print(image)
			x = form.cleaned_data['x']
			y = form.cleaned_data['y']
			new_image = Image.objects.create()
			size_changer(x, y, image, new_image)
			print('test1', new_image.picture)
			print('test2', image.picture)
			new_image.name = 'copy_' + image.name
			new_image.save()
	form = ChangeSizeForm()
	context = {'image':image, 'form':form, 'new_image':new_image}
	return render(request, 'change.html', context)