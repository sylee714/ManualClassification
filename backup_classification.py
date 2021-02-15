#Check images in a folder, and display image on python using opencv
#Check if the image contains a target
#If it does, classify the orientation, shape color, letter color, letter, and shape
#Test inputs to make sure they are valid
#If a mistake was done, allow user to go back and edit one of the classifications ^
#Check at the end of the code if everything works before saving to a text file
#Save text file in a separate folder, with the same name as the image

#look through images in a folder and display them one by one
import tkinter as tk
import os
import cv2
import time
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import ImageTk, Image

# Create a new directory to save all the manual classification text files.
def createNewDir(parentDir):
    newDirName = "manualClassification"
    newPath = os.path.join(parentDir, newDirName)
    try:
        os.mkdir(newPath)
    except OSError:
        print("The directory already existed.")
    return newPath

# Get the path to the parent directory.
def getParDir(dir):
    splitDir = dir.split("/")
    print("Split Dir: ", splitDir)
    # Remove empty str
    for i in range(len(splitDir)):
        if splitDir[i] == "":
            splitDir.pop(i)
    parentDir = ""
    for i in range(len(splitDir) - 1):
        # print("content: " + str(splitDir[i]))
        parentDir = parentDir + splitDir[i] + "/"
    return parentDir

# Change tne directory to your image file folder
directory = 'C:/Users/SYL/Desktop/CPP-AUVSI/img-recog/images/'
# Get the parent path of the image folder
parentDir = getParDir(directory)
print("Parent Dir: " + parentDir)

# Create a new directory to save manually entered classification for each image
manualClassDir = createNewDir(parentDir)
print("Manual Classification Dir: " + manualClassDir)

# List of absolute paths to each image
imagePaths = []
# List of image file names
imageFileNames = []

#goes inside folder and checks if its an image
for file in os.scandir(directory):
    if (file.path.endswith(".jpg")
            or file.path.endswith(".png")) or file.path.endswith(".jpeg") and file.is_file():
        # print(entry.path)
        # Add every path to an image
        imagePaths.append(file.path)
        # image = cv2.imread(entry.path, 1)
        #shows an image and once you press any key the window is closed
        # cv2.imshow('Test image', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        #this code will open all the images in the folder at once
        #image = Image.open(entry.path)
        #image.show()


        #print("Target? (y/n)" + target)
        #if(target == "y"):

print("Images Path")
for i, path in enumerate(imagePaths):
    print(path)
    x = path.split("/")
    # Add only the file name
    imageFileNames.append(x[len(x) - 1])

print("Image File Name")
for fileName in imageFileNames:
    print(fileName)

# List of image file names without file formats
fileNames = []
for i, imageFileName in enumerate(imageFileNames):
    temp = imageFileName.split(".")
    # Only get the file name with no ".[fileFormat]"
    fileNames.append(temp[0])

print("File name")
for fileName in fileNames:
    print(fileName)

print("-------------------------")
print("Start GUI")

# GUI
# Save the fields in a text with the same name as the image file
def save_file():
    if check_fields():
        global curIndex
        global fileNames
        global manualClassDir
        textFileName = fileNames[curIndex] + ".txt"
        print("Text file name: " + textFileName)
        path = os.path.join(manualClassDir, textFileName)
        print("Path to the text file: " + path)
        text = ""
        for i in range(len(entry_list)):
            if i == len(entry_list)-1:
                text += entry_list[i].get()
            else:
                text += entry_list[i].get() + ", "
        print(selectedOption.get())
        # for e in entry_list:
        #     text += e.get() + ", "
        # text = ent_orientation.get()
        # text += ", " + ent_shape.get()
        # text += ", " + ent_shapecolor.get()
        # text += ", " + ent_letter.get()
        # text += ", " + ent_lettercolor.get()
        f = open(path, "w")
        f.write(text)
        f.close()
        #----------------------------------
        # print(ent_orientation.get())
        # print(ent_shape.get())
        # print(ent_shapecolor.get())
        # print(ent_letter.get())
        # print(ent_lettercolor.get())
        # filepath = asksaveasfilename(
        #     defaultextension="txt",
        #     filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        # )
        # f = open()
        # if not filepath:
        #     return
        # with open(filepath, "w") as output_file:
        #     text = ent_orientation.get()
        #     text += ", " + ent_shape.get()
        #     text += ", " + ent_shapecolor.get()
        #     text += ", " + ent_letter.get()
        #     text += ", " + ent_lettercolor.get()
        #     output_file.write(text)
        # window.title(f"Backup Classification - {filepath}")
    else: # Display a popup error message
        print("Missing a field.")

def check_fields():
    # Check if every field is entered
    for e in entry_list:
        if not e.get():
            return False
    # Check if "Target" or "Emergent Target" is selected
    if selectedOption.get() == 0:
        return False
    return True

# Clear all the fields
def clear_fields():
    for e in entry_list:
        e.delete(0, "end")

# Display the next image
# Make it do auto-save
def next_img():
    clear_fields()
    global curIndex
    global numberOfPics
    global imagePaths
    curIndex = curIndex + 1
    if curIndex < numberOfPics-1:
        img = ImageTk.PhotoImage(Image.open(imagePaths[curIndex]))
        pic_label.configure(image=img)
        pic_label.image = img
    else:
        curIndex = curIndex - 1
    # print("Next picture")
    # print("Current Index: " + str(curIndex))

# Display the previous image
def prev_img():
    clear_fields()
    global curIndex
    global imagePaths
    if curIndex > 0:
        curIndex = curIndex-1
        img = ImageTk.PhotoImage(Image.open(imagePaths[curIndex]))
        pic_label.configure(image=img)
        pic_label.image = img
    # print("Previous picture")
    # print("Current Index: " + str(curIndex))

window = tk.Tk()
window.title("Backup Classification")
# window.columnconfigure([0,1], minsize=250)
# window.rowconfigure(0, minsize=100)
curIndex = 0
# print("Current Index: " + str(curIndex))
numberOfPics = len(imagePaths)

tempImg = cv2.imread(imagePaths[curIndex])
# wid = tempImg.shape[1]
# heig = tempImg.shape[0]
# print(wid)
# print(heig)

pic_frame = tk.Frame(master=window, borderwidth=5)
pic_frame.grid(row=0, column=0)
# Get the current image
img = ImageTk.PhotoImage(Image.open(imagePaths[curIndex]))

# Displaying images using label
pic_label = tk.Label(pic_frame, image=img)
pic_label.grid(row=0)

# Frame containing PREV and NEXT buttons
picBtn_frame = tk.Frame(master=pic_frame, borderwidth=5)
picBtn_frame.grid(row=1)

# PREV and NEXT buttons to navigate through images
btn_prev = tk.Button(master=picBtn_frame, text="PREV", command=prev_img, borderwidth=5)
btn_next = tk.Button(master=picBtn_frame, text="NEXT", command=next_img, borderwidth=5)
btn_prev.grid(row=0, column=0, sticky="w", padx=5)
btn_next.grid(row=0, column=1, sticky="e", padx=5)

labels = [
    "Orientation:",
    "Shape:",
    "Shape Color:",
    "Letter:",
    "Letter Color:"
]

# Frame containing both fields and button
frm_form = tk.Frame(master=window, borderwidth=5)
frm_form.grid(row=0, column=1)

# Frame containing only fields
fields_form = tk.Frame(frm_form, relief=tk.SUNKEN, borderwidth=5)
fields_form.grid(row=0)

# Fields
# Emergent Target/Target Dropdown List
# Just a place holder to invoke a method when a radio button is selected
# Disable entries when "Emergent Target" option is selected.
# Check that either "Emergent Target" or "Target" option has to be selected.
def sel():
    selection = "You selected the option " + str(selectedOption.get())
    print(selection)
    # Selected Target
    if selectedOption.get() == 1:
        for e in entry_list:
            e.config(state='normal')
    # Selected Emergent Target
    elif selectedOption.get() == 2:
        for e in entry_list:
            e.config(state='disabled')


selectedOption = tk.IntVar()
OPTIONS = ["Target", "Emergent Target"]
label_list = []
entry_list = []
CheckbuttonEmergentTarget = tk.IntVar()
CheckbuttonTarget = tk.IntVar()

# Target = 1
TargetButton = tk.Radiobutton(master=fields_form, text=OPTIONS[0],
                                       variable=selectedOption,
                                       value=1,
                                       command=sel)
TargetButton.grid(row=0, column=0, sticky="w")
# Emergent Target = 2
EmergentTargetButton = tk.Radiobutton(master=fields_form, text=OPTIONS[1],
                                       variable=selectedOption,
                                       value=2,
                                       command=sel)
EmergentTargetButton.grid(row=0, column=1, sticky="w")

for i in range(len(labels)):
    label = tk.Label(master=fields_form, text=labels[i])
    entry = tk.Entry(master=fields_form, width=20)
    label.grid(row=i+1, column=0, sticky="e")
    entry.grid(row=i+1, column=1)
    label_list.append(label)
    entry_list.append(entry)
# lbl_orientation = tk.Label(master=fields_form, text=labels[0])
# ent_orientation = tk.Entry(master=fields_form, width=20)
# lbl_orientation.grid(row=1, column=0, sticky="e")
# ent_orientation.grid(row=1, column=1)
#
# lbl_orientation = tk.Label(master=fields_form, text=labels[1])
# ent_orientation = tk.Entry(master=fields_form, width=20)
# lbl_orientation.grid(row=2, column=0, sticky="e")
# ent_orientation.grid(row=2, column=1)
#
# lbl_shape = tk.Label(master=fields_form, text=labels[2])
# ent_shape = tk.Entry(master=fields_form, width=20)
# lbl_shape.grid(row=3, column=0, sticky="e")
# ent_shape.grid(row=3, column=1)
#
# lbl_shapecolor = tk.Label(master=fields_form, text=labels[3])
# ent_shapecolor = tk.Entry(master=fields_form, width=20)
# lbl_shapecolor.grid(row=4, column=0, sticky="e")
# ent_shapecolor.grid(row=4, column=1)
#
# lbl_letter = tk.Label(master=fields_form, text=labels[4])
# ent_letter = tk.Entry(master=fields_form, width=20)
# lbl_letter.grid(row=5, column=0, sticky="e")
# ent_letter.grid(row=5, column=1)


# Frame containing SAVE and CLEAR buttons
fieldBtn_frame = tk.Frame(frm_form, borderwidth=5)
fieldBtn_frame.grid(row=1)

# Save button
btn_save = tk.Button(master=fieldBtn_frame, text="SAVE", command=save_file, borderwidth=5)
btn_save.grid(row=0, column=0, sticky="e", padx=5)

# Clear button
btn_clear = tk.Button(master=fieldBtn_frame, text="CLEAR", command=clear_fields, borderwidth=5)
btn_clear.grid(row=0, column=1, sticky="w", padx=5)


window.mainloop()

