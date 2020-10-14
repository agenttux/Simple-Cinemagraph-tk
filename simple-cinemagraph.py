import argparse
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import os
from tqdm import tqdm

x1, y1, x2, y2, pointCount = 0, 0, 0, 0, 0
rect = None


def on_button_press(event):
    global pointCount, x1, x2, y1, y2, rect
    if pointCount == 0:
        x1 = cv.canvasx(event.x)
        y1 = cv.canvasy(event.y)
        pointCount += 1
    elif pointCount == 1:
        x2 = cv.canvasx(event.x)
        y2 = cv.canvasy(event.y)
        pointCount += 1
    else:
        pointCount = 1
        x1 = cv.canvasx(event.x)
        y1 = cv.canvasy(event.y)
        x2 = 0
        y2 = 0
        cv.delete(rect)
    if pointCount == 2:
        rect = cv.create_rectangle(x1, y1, x2, y2, outline="red")
    else:
        pass


def exit_loop(event):
    root.destroy()


parser = argparse.ArgumentParser(
    description='Make a cinemagraph from a video file.')
parser.add_argument('inputPath', help='path to video file')
parser.add_argument('-o', '--outputPath',
                    help='path to output file (default is current directory)')
parser.add_argument('-f', '--outputFile', default="output.mp4",
                    help='name of output file (default is "output.mp4")')

args = parser.parse_args()

if os.path.isfile(args.inputPath) != 1:
    print("Not a vaild input file!")
    exit()

os.system("rm -rf tmp-cine-files")
os.system("mkdir tmp-cine-files")
os.system("ffmpeg  -hide_banner -i " + args.inputPath +
          " -filter:v fps=fps=24 tmp-cine-files/$filename%05d.png")
try:
    im = Image.open("tmp-cine-files/00001.png")
except:
    print("Invalid video file!")
    os.system("rm -rf tmp-cine-files")
    exit()

imw, imh = im.size  # get height and width of image

root = tk.Tk()
root.title("Cinemagraph Maker")
photo = ImageTk.PhotoImage(im)
cv = tk.Canvas(width=imw, height=imh, cursor="cross")
cv.create_image(0, 0, image=photo, anchor='nw')
cv.pack(fill='both', expand='False')
cv.bind("<ButtonPress-1>", on_button_press)
cv.bind("<ButtonPress-3>", exit_loop)

root.mainloop()

print("First corner coordinates: ({0}, {1})".format(x1, y1))
print("Second corner coordinates: ({0}, {1})".format(x2, y2))


pixArray = np.array(im)
cutArray = pixArray[int(y1):int(y2), int(x1):int(x2)]

fileList = os.listdir("tmp-cine-files")

print("\nGenerating cinemagraph frames:")

for file in tqdm(fileList):
    photoPath = "tmp-cine-files/" + str(file)
    currentImage = np.array(Image.open(photoPath))
    currentImage.setflags(write=1)
    currentImage[int(y1):int(y2), int(x1):int(x2)] = cutArray
    arr2im = Image.fromarray(currentImage)
    arr2im.save(photoPath)

os.system("ffmpeg -r 24 -f image2 -s 1920x1080 -start_number 1 -i tmp-cine-files/%05d.png -vframes 1000 -vcodec libx264 -crf 25  -pix_fmt yuv420p " + args.outputFile)

os.system("rm -rf tmp-cine-files")
