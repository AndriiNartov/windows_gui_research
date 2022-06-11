from PIL import ImageGrab

px = ImageGrab.grab().load()

print(px[0, 1000])