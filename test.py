import os

image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images")
for image in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image)
    print(image_path)