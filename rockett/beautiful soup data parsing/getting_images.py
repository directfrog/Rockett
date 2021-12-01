import requests

def get_image(image_link):
	response = requests.get(image_link)
	file = open("sample_image.png", "wb")
	file.write(response.content)
	file.close()