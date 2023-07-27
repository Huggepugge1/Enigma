# This is just awful to implement
from PIL import Image
from PIL.ExifTags import TAGS


def get_img_metadata(img: string):


print(TAGS)
img = Image.open('IMG_20230716_142432.jpg')
img_tags = img._getexif()
print(img_tags)
exif = {
    TAGS[k]: v
    for k, v in img_tags.items()
}

print(exif)