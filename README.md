# Braille Typing Project

Project Author: Jeramiah Trout
<details>
<summary>Quick Information</summary>
This repository hosts content which began as a learning tool to type properly contracted UEB braille on a Perkins Brailler, which is just one of many brailling tools. In its current form, it handles all known UEB contractions but does not follow every single rule. For example, it doesn't do a double capital indicator for words which are completely capital. This section will be updated as new rules are properly implemented

 <br>
In this readme, you will find info on installing python, as well as getting this project to run on your system. As new features are added, there will be updates to the readme providing details on the new releases. Please enjoy.

<br>

I have personally tested this project on Windows and Mac devices and believe everything to be fully functional and bug free. However, if you find crashes, launch failures, or bugs during use, please submit a bug report on the github page for this repository. Thank you for taking the time to read this document and for showing your interest in my project.

________
</details>
<details>
<summary> Getting Started </summary>
<details>
<summary>Python Installation</summary>

# Python 3.14 is now supported!!!

You may download the most recent release of Python 3.14 (3.13.4) at https://www.python.org/downloads/release/python-3144/ and then navigate to your specific platform and download the installer from there. I personally recommend scrolling all the way down to the files portion of the site and downloading the recommended installer directly instead of the using the install manager as the manager introduced some annoyance. After the download is complete, open the installer, and click "Install Now" or "Upgrade" (Upgrade is only available if you have an older release of the same version). Once installation is complete, you can use the rest of this guide to get started.
</details>

<details>
<summary>Graphics Installtion</summary>

## Graphics Package (Now Installed Automatically on First Launch)

This project is built using the CMU graphics library which can be found at https://academy.cs.cmu.edu/desktop. This project will install the most updated version of the graphics package for you on your 1st running of the displayer. If this process fails (which should not happen), then you should follow the above link, download the package as a zip, extract/expand, and then copy the cmu_graphics folder from the cmu_graphics_installer folder, and place it into the project directory. It is important to only copy and move the cmu_graphics folder, not the entire cmu_graphics_installer folder. 
</details>

<details>
<summary>Launching the Project</summary>

<details>
<summary>MacOs</summary>

## MacOS Instructions for PretendLauncher.py
If you are on MacOS, you have 3 options for running the launcher:

1. Open displayer.py with VS code, and run through the play button at the top right  
or  
2. Open in Python Launcher (NOT IDLE) and run the script  
or  
3. Open a terminal window, navigate to the directory the displayer is in and run the displayer.


```bash
cd path/to/this/repository
python3 displayer.py
```
Note that if you have multiple versions of python3 installed, (such as 3.6.4, 3.9.3, 3.13.7, 3.14.2), you may need to specify version in your command as shown below:

To check installed versions, simply run 

```bash
which -a python3
```
or 

```bash
python3 --vesion
```
____
For example, if you have vesion 3.13.7 and 3.14.1 and 3.12.9, and wanted to run the 3.13.7 version, you would run:

```bash
cd path/to/this/repository
python3.13 displayer.py
```
____
</details>
<details>
<summary> Windows </summary>

## Windows Instructions for displayer.py

If you are on Windows you have 2 simple options to run the displayer:

1. Double click the displayer.py file as if it were an executable  
or  
2. Open the repository folder through VS code and click the play button at the top right while having the displayer file selected <br>
or
3. Open command prompt and navigate to the directory displayer.py is stored in, type "python3 displayer.py" and press Enter
____

</details>
</details>
</details>

<details>
<summary>Using the Project</summary>

Once you have the displayer running, you can either type your text input (by pressing t or clicking the upper left button) which will open a grpahics window with limited options, or input a file (by pressing f or clicking the upper right button) which will open a file picker menu. If you are typing your input, be aware that you will only be able to type text directly into the input box, no formatting is available, and you will be unable to copy/paste into this window. Once you press enter, your input will be converted to braille. This input is never sent or stored anyhere and disappears upon the displayer being closed. This also means that what you type cannot be recovered if you close the displayer before you finish. The benefit to this approach is being able to just quickly enter words/sentences for quick conversion, but is limited compared to file inputs. If you choose to input a file, then your formatting will be maintained as best as possible, and the file is never sent or stored anywhere except on your local device where you created it. This method is recommended for longer texts, paragraphs, etc. The text will be converted, and then the braille to replicate the text will be displayed in order as well as the buttons to press on a brailler to get that result, and the english text related to what is being typed. This will hekp users create accurate braille and learn as they do. You can control page width, speed in auto mode, whether the program is in auto or manual mode, and whether it is paused or running either with mouse clicks or button presses which will be explained in the next paragraph.

<details>
<summary>Hotkeys:</summary>

## Text entry, mode control, speed control, display control

### X: Closes the displayer entirely, removes all entries and converted braille

### T: Opens typing menu for your text input. No copy/paste ability. Deletes converted braille from any previous entries of text or file input

### F: Opens file select menu for your file input. Deletes converted braille from any previous entries of text or file input

### M: Toggles manual mode and auto mode for displaying braille. When toggling to automode, it will be paused automatically

### P: Toggles Pause if auto mode is active, does nothing otherwise. Spacebar acheives the same behavior

### +: Increases the speed of the displayer in auto mode, measured in cells per minute

### -: Decreases the speed of the displayer in auto mode, measured in cells per minute

### LeftArrow: Move back one cell

### RightArrow: Move forward one cell


## Page Width Hotkeys:

#### Minumum Page Width: 10 cells

#### Maximum Page Width: Infinite

#### Maximum Non-Infinite Page Width: 60 Cells

#### Default Page Width: 42 Cells

#### No key presses will take the user outside the bounds of page width

### 1: Sets page width to 10 cells

### 2: Decreases page width by 10 cells

### 3: Decreases page width by 1 cell

### 4: Increases page width by 1 cell:

### 5: Increases page width by 10 cells:

### 6: Increases page with to Infinite
</details>

<details>
<summary> Extra Information</summary>


<details>
<summary>displayer.py</summary>
This file acts as the displayer of the braille to type on a brailler. It has several helpful features for users. You can either type your input in a text input window or input a file, from which the text will be extracted. It will interpret the text, and convert it to UEB braille, showing the user how to type it on a brailler for blind people to read. This serves as a good learning tool for users with vision as they will internalize the contractions as well as the dot patterns of those letters, numbers, punctuation, and contractions. It follows most of the UEB rules with some new rules being poperly added later. Also allows the user to select the speed at which to display the braille cells, and the width of the paper being used. Users can use the displayer in manual mode, advancing forwards with arrow keys, or in auto mode, where the speed controls become relveant. 
</details>

<details>
<summary>braille_generator.py</summary>
This file will create a json file of all of the letters, numbers, punctuation, and contractions recognized in UEB. It will provide the dot patters for each entry, and the type of entry that it is, whether it be a letter, strong groupsign, alphabetic wordsign, etc. This file can be run on it's own to make the json file, but will be run automatically by the displayer file if the json file doesn't exist.
</details>

<details>
<summary>file_helper.py</summary>
This file is used to allow users to select a file to input into the displayer to have the text extracted and converted. Uses tkinter to open a file dialogue menu.
</details>

<details>
<summary>Changelog</summary>
Allows users to track changes over time, and understand when and how features were added
</details>

<details>
<summary>requirements.txt</summary>
List of required python packages not included in a default python installation.
</details>