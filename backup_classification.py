# Check images in a folder, and display image on python using opencv
# Check if the image contains a target
# If it does, classify the orientation, shape color, letter color, letter, and shape
# Test inputs to make sure they are valid
# If a mistake was done, allow user to go back and edit one of the classifications ^
# Check at the end of the code if everything works before saving to a text file
# Save text file in a separate folder, with the same name as the image

# look through images in a folder and display them one by one
import tkinter as tk
from tkinter import messagebox
import os
import cv2
import time
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import ImageTk, Image


# Create a new directory to save all the manual classification text files.
def create_new_dir(parentDir):
    newDirName = "manualClassification"
    newPath = os.path.join(parentDir, newDirName)
    try:
        os.mkdir(newPath)
    except OSError:
        print("The directory already existed.")
    return newPath


# Get the path to the parent directory.
def get_par_dir(dir):
    split_dir = dir.split("/")
    print("Split Dir: ", split_dir)
    # Remove empty str
    for i in range(len(split_dir)):
        if split_dir[i] == "":
            split_dir.pop(i)
    par_dir = ""
    for i in range(len(split_dir) - 1):
        # print("content: " + str(splitDir[i]))
        par_dir = par_dir + split_dir[i] + "/"
    return par_dir


# Change tne directory to your image file folder
directory = 'C:/Users/SYL/Desktop/CPP-AUVSI/img-recog/images/'
# Get the parent path of the image folder
parent_dir = get_par_dir(directory)
print("Parent Dir: " + parent_dir)

# Create a new directory to save manually entered classification for each image
manualClassDir = create_new_dir(parent_dir)
print("Manual Classification Dir: " + manualClassDir)

# List of absolute paths to each image
imagePaths = []
# List of image file names
imageFileNames = []

# goes inside folder and checks if its an image
for file in os.scandir(directory):
    if (file.path.endswith(".jpg")
        or file.path.endswith(".png")) or file.path.endswith(".jpeg") and file.is_file():
        # print(entry.path)
        # Add every path to an image
        imagePaths.append(file.path)
        # image = cv2.imread(entry.path, 1)
        # shows an image and once you press any key the window is closed
        # cv2.imshow('Test image', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # this code will open all the images in the folder at once
        # image = Image.open(entry.path)
        # image.show()

        # print("Target? (y/n)" + target)
        # if(target == "y"):

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
file_names = []
for i, imageFileName in enumerate(imageFileNames):
    temp = imageFileName.split(".")
    # Only get the file name with no ".[fileFormat]"
    file_names.append(temp[0])

print("File name")
for fileName in file_names:
    print(fileName)

print("-------------------------")
print("Start GUI")


# Display an error message.
def display_error_msg(message):
    messagebox.showerror("Error", message)


# GUI
# Save the fields in a text with the same name as the image file
def save_file():
    if check_fields():
        global curIndex
        global file_names
        global manualClassDir
        textFileName = file_names[curIndex] + ".txt"
        print("Text file name: " + textFileName)
        file_path = os.path.join(manualClassDir, textFileName)
        print("Path to the text file: " + file_path)
        text = ""
        if selectedOption.get() == 1:
            for i in range(len(entryList)):
                if i == len(entryList) - 1:
                    text += entryList[i].get()
                else:
                    text += entryList[i].get() + ", "
        elif selectedOption.get() == 2:
            text = "emergent target"
        f = open(file_path, "w")
        f.write(text)
        f.close()
        return True
    else:  # Display a popup error message
        display_error_msg("Missing a field")
        return False


# Check if required fields are provided before saving.
def check_fields():
    # Check if "Target" or "Emergent Target" is selected
    if selectedOption.get() == 0:
        return False
    # "Target" is selected
    elif selectedOption.get() == 1:
        # Check if every field is entered
        for e in entryList:
            if not e.get():
                return False
        return True
    # "Emergent Target" selected. No need to check other entries
    elif selectedOption.get() == 2:
        return True


# Reset all the fields and radio buttons.
def reset():
    clear_fields()
    enable_entries()
    selectedOption.set(0)


# Clear all the fields.
def clear_fields():
    for e in entryList:
        e.delete(0, "end")
        # e.config(state='normal')
    # selectedOption.set(0)


# Disable entries
def disable_entries():
    for e in entryList:
        # e.delete(0, "end")
        e.config(state='disabled')


# Enable entries
def enable_entries():
    for e in entryList:
        # e.delete(0, "end")
        e.config(state='normal')


# Display the next image
# Make it do auto-save
def next_img():
    global curIndex
    global numberOfPics
    global imagePaths
    if curIndex < numberOfPics - 1:
        if save_file():
            reset()
            curIndex = curIndex + 1
            image = ImageTk.PhotoImage(Image.open(imagePaths[curIndex]))
            pic_label.configure(image=image)
            pic_label.image = img
    else:
        display_error_msg("No Next Image")
    # print("Next picture")
    # print("Current Index: " + str(curIndex))


# Display the previous image
def prev_img():
    # clear_fields()
    # reset()
    global curIndex
    global imagePaths
    if curIndex > 0:
        reset()
        curIndex = curIndex - 1
        img = ImageTk.PhotoImage(Image.open(imagePaths[curIndex]))
        pic_label.configure(image=img)
        pic_label.image = img
    else:
        display_error_msg("No Previous Image")
    # print("Previous picture")
    # print("Current Index: " + str(curIndex))


# Enable entries when "Target" option is selected.
# Disable entries when "Emergent Target" option is selected.
def sel():
    selection = "You selected the option " + str(selectedOption.get())
    print(selection)
    # Selected Target
    if selectedOption.get() == 1:
        enable_entries()
    # Selected Emergent Target
    elif selectedOption.get() == 2:
        disable_entries()


# Create the window
window = tk.Tk()
window.title("Backup Classification")
# window.columnconfigure([0,1], minsize=250)
# window.rowconfigure(0, minsize=100)
curIndex = 0
# print("Current Index: " + str(curIndex))
numberOfPics = len(imagePaths)
# print(imagePaths)
# print("Num of Images: " + str(numberOfPics))

# tempImg = cv2.imread(imagePaths[curIndex])
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

LABEL_OPTIONS = [
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

RADIO_BUTTON_OPTIONS = ["Target", "Emergent Target"]
selectedOption = tk.IntVar()
labelList = []
entryList = []
radioButtonList = []

# Add radio buttons for Target and Emergent Target
# Target = 1 and Emergent Target = 2
for i in range(len(RADIO_BUTTON_OPTIONS)):
    radioButton = tk.Radiobutton(master=fields_form, text=RADIO_BUTTON_OPTIONS[i],
                                 variable=selectedOption,
                                 value=i + 1,
                                 command=sel)
    radioButton.grid(row=0, column=i, sticky="w")
    radioButtonList.append(radioButton)

# Add labels and entries
for i in range(len(LABEL_OPTIONS)):
    label = tk.Label(master=fields_form, text=LABEL_OPTIONS[i])
    entry = tk.Entry(master=fields_form, width=20)
    label.grid(row=i + 1, column=0, sticky="e")
    entry.grid(row=i + 1, column=1)
    labelList.append(label)
    entryList.append(entry)

# Frame containing SAVE and CLEAR buttons
fieldBtn_frame = tk.Frame(frm_form, borderwidth=5)
fieldBtn_frame.grid(row=1)

# Save button
btn_save = tk.Button(master=fieldBtn_frame, text="SAVE", command=save_file, borderwidth=5)
btn_save.grid(row=0, column=0, sticky="e", padx=5)

# Clear button
btn_clear = tk.Button(master=fieldBtn_frame, text="RESET", command=reset, borderwidth=5)
btn_clear.grid(row=0, column=1, sticky="w", padx=5)

window.mainloop()
