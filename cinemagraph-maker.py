import argparse
import tkinter as tk
from PIL import Image, ImageTk
import os

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
        cv.delete(rect)
    if pointCount == 2:
        rect = cv.create_rectangle(x1, y1, x2, y2, outline="red")
    else:
        pass


parser = argparse.ArgumentParser(
    description='Make a cinemagraph from a video file.')
parser.add_argument('inputPath', help='path to video file')
parser.add_argument('-o', '--outputPath',
                    help='path to output file (default is current directory)')
parser.add_argument('-f', '--outputFile', default="output.png",
                    help='name of output file (default is "output.png")')

args = parser.parse_args()

if os.path.isfile(args.inputPath) != 1:
    print("Not a vaild input file!")
    exit()

im = Image.open(args.inputPath)
imw, imh = im.size  # get height and width of image

root = tk.Tk()
root.title("Cinemagraph Maker")
photo = ImageTk.PhotoImage(im)
cv = tk.Canvas(width=imw, height=imh, cursor="cross")
cv.create_image(0, 0, image=photo, anchor='nw')
cv.pack(fill='both', expand='False')
cv.bind("<ButtonPress-1>", on_button_press)

root.mainloop()
