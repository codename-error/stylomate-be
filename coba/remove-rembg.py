from rembg import remove
from PIL import Image

input_path = '/Users/macbook/Library/CloudStorage/OneDrive-UniversitasTeknologiYogyakarta/file-document-macbook/fast_api/arkfidia_hackaton/coba/image-testing-2.jpg'
output_path = './output.png'

input = Image.open(input_path)
output = remove(input)
output.save(output_path)