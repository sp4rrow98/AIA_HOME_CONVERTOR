from django.shortcuts import render
from PIL import Image, UnidentifiedImageError
from django.conf import settings as django_settings
from django.http import FileResponse, HttpResponse

# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request, 'index.html')

    if request.method == "POST" or "FILES":
        try:
            # Get data from inputs
            name = request.POST["name"]
            photos = request.FILES.getlist('photos')

            count = 1
            if (len(photos) > 1):
                # For multiple photos
                imglist = []
                counter = 0

                # Write buffers and append to the list
                for photo in photos:
                    print(photo.temporary_file_path())
                    bytes = photo.read() # Read files in memory
                    path = django_settings.MEDIA_ROOT + f"buffer{counter}.png" # auto path
                    counter = counter + 1 # counter
                    file = open(path, 'wb')
                    file.write(bytes)
                    file.close()
                    imglist.append(file)

                # CONVERT
                listconv = []
                counter = 0
                for img in imglist:
                    path = django_settings.MEDIA_ROOT + f"buffer{counter}.png"
                    img = Image.open(path)
                    img = img.convert('RGB')
                    listconv.append(img)
                    counter=counter+1
                img.save(django_settings.MEDIA_ROOT + f"{name}.pdf", save_all=True, append_images=listconv[:-1])

                # Return response
                img = open(django_settings.MEDIA_ROOT + f"{name}.pdf", 'rb')
                response = FileResponse(img)
                return response

            elif (len(photos) == 1):
                # For single photo
                photos = request.FILES["photos"]
                # WRITE FILE
                bytes = photos.read() # CONTENT UPLOADED FILE
                path = django_settings.MEDIA_ROOT + "buffer"
                file=open(path,'wb')
                file.write(bytes)
                file.close()

                # CONVERT
                image1 = Image.open(path)
                im1 = image1.convert('RGB')
                im1.save(django_settings.MEDIA_ROOT + f"{name}.pdf")
                img = open(django_settings.MEDIA_ROOT + f"{name}.pdf", 'rb')
                # Return response
                response = FileResponse(img)
                return response
            else:
                print("ERROR")
        except UnidentifiedImageError:
            return render(request, 'error.html')
        return render(request, 'index.html')