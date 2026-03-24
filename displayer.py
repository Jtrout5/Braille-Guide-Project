import json
import os
import shutil
import zipfile
import urllib3
from tkinter import Tk, filedialog

try:
    import pdfplumber
    from docx import Document
    import textract
    import requests
    import pyautogui
except ImportError as e:
    os.system("pip3 install -r requirements.txt")
    import pdfplumber
    from docx import Document
    import textract
    import requests
    import pyautogui

def download_zip_file(url, destination_folder, filename):
    '''
    Takes 3 args, a url for the file, a destination folder, and a name to give the file
    Downloads the file found at url, gives it filename as a name and places it in the destination folder
    '''
    file_path = os.path.join(destination_folder, filename)
    response = requests.get(url, stream=True)
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            
def unzip_all(zip_file_path, destination_directory):
    """
    Takes 2 args, a path to a zip file and a path to the destination folder
    """
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_directory)

try: ## graphics package
    from cmu_graphics import *
except ImportError as e:
    zip_url = 'https://s3.amazonaws.com/cmu-cs-academy.lib.prod/desktop-cmu-graphics/cmu_graphics_installer.zip'  
    output_directory = "."
    output_filename = "cmu_graphics_installer.zip"
    download_zip_file(zip_url, output_directory, output_filename)
    unzip_all(output_directory+'/cmu_graphics_installer.zip', output_directory)
    shutil.move(output_directory+"/cmu_graphics_installer/cmu_graphics", ".")
    os.remove(output_filename)
    shutil.rmtree("cmu_graphics_installer")
    from cmu_graphics import *
    
def pick_file():
    Tk().withdraw() 
    path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[
            ("All files", "*.*"),
            ("Text files", "*.txt"),
            ("PDF files", "*.pdf"),
            ("Word documents", "*.docx *.doc")
        ]
    )
    return path

selected_delay = 45
app.time_delay = 45
app.index = -1
size = pyautogui.size()
width = size[0]
height = size[1]
app.width = width
app.height = height
app.autofs = 0

filepath = os.path.abspath(__file__)
directory_path = os.path.dirname(filepath)
os.chdir(directory_path)
currentFile =  os.path.basename(__file__)
filename = currentFile[:-3]


def generate():
    lowercase = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    uppercase = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    punctuation = ["!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "{", "}", "°", " "]
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    alpha_wordsigns = ["but", "can", "do", "every", "from", "go", "have", "just", "knowledge", "like", "more", "not", "people", "quite", "rather", "so", "that", "us", "very", "will", "it", "you", "as"]
    initial_letter_contractions = ["day", "ever", "father", "here", "know", "lord", "mother", "name", "one", "part", "question", "right", "some", "time", "under", "work", "young", "there", "character", "through", "where", "ought", "upon", "word", "these", "those", "whose", "cannot", "had", "many", "spirit", "world", "their"]
    strong_groupsigns = ["ch", "sh", "th", "wh", "ou", "st", "gh", "ed", "er", "ow", "ar", "in"]
    strong_contraction = ["and", "for", "of", "the", "with"]
    strong_wordsigns = ["child","shall","this","which","out","still"]
    lower_wordsigns = ["be","enough","were","his","in","was"]
    lower_groupsigns = ["ea", "bb", "cc", "ff", "gg", "be", "con", "dis", "en", "in"]
    shortform_words = ["about", "above", "according", "across", "after", "afternoon", "afterward", "again", "against", "almost", "already", "also", "although", "altogether", "always", "because", "before", "behind", "below", "beneath", "beside", "between", "beyond", "blind", "braille", "children", "could", "deceive", "declare", "either", "first", "friend", "good", "great", "herself", "him", "himself", "immediate", "its", "itself", "letter", "little", "much", "must", "myself", "necessary", "neither", "oneself", "ourselves", "paid", "perceive", "perhaps", "quick", "receive", "said", "should", "such", "themselves", "today", "together", "tomorrow", "tonight", "would", "your", "yourself", "yourselves"]
    final_letter_groupsigns = ["ound", "ance", "sion", "less", "ount", "ence", "ong", "ful", "tion", "ness", "ment", "ity"]


    categories = {
        "lowercase": lowercase,
        "uppercase": uppercase,
        "punctuation": punctuation,
        "digits": digits,
        "alpha_wordsigns": alpha_wordsigns,
        "initial_letter_contractions": initial_letter_contractions,
        "strong_groupsigns": strong_groupsigns,
        "strong_contraction": strong_contraction,
        "strong_wordsigns": strong_wordsigns,
        "lower_wordsigns": lower_wordsigns,
        "lower_groupsigns": lower_groupsigns,
        "shortform_words": shortform_words,
        "final_letter_groupsigns": final_letter_groupsigns
    }

    data = {}

    braille = {
    "a": {"type": "lowercase", "value": [(1,)]},
    "b": {"type": "lowercase", "value": [(1,2)]},
    "c": {"type": "lowercase", "value": [(1,4)]},
    "d": {"type": "lowercase", "value": [(1,4,5)]},
    "e": {"type": "lowercase", "value": [(1,5)]},
    "f": {"type": "lowercase", "value": [(1,2,4)]},
    "g": {"type": "lowercase", "value": [(1,2,4,5)]},
    "h": {"type": "lowercase", "value": [(1,2,5)]},
    "i": {"type": "lowercase", "value": [(2,4)]},
    "j": {"type": "lowercase", "value": [(2,4,5)]},
    "k": {"type": "lowercase", "value": [(1,3)]},
    "l": {"type": "lowercase", "value": [(1,2,3)]},
    "m": {"type": "lowercase", "value": [(1,3,4)]},
    "n": {"type": "lowercase", "value": [(1,3,4,5)]},
    "o": {"type": "lowercase", "value": [(1,3,5)]},
    "p": {"type": "lowercase", "value": [(1,2,3,4)]},
    "q": {"type": "lowercase", "value": [(1,2,3,4,5)]},
    "r": {"type": "lowercase", "value": [(1,2,3,5)]},
    "s": {"type": "lowercase", "value": [(2,3,4)]},
    "t": {"type": "lowercase", "value": [(2,3,4,5)]},
    "u": {"type": "lowercase", "value": [(1,3,6)]},
    "v": {"type": "lowercase", "value": [(1,2,3,6)]},
    "w": {"type": "lowercase", "value": [(2,4,5,6)]},
    "x": {"type": "lowercase", "value": [(1,3,4,6)]},
    "y": {"type": "lowercase", "value": [(1,3,4,5,6)]},
    "z": {"type": "lowercase", "value": [(1,3,5,6)]},
    "A": {"type": "uppercase", "value": [(6,), (1,)]},
    "B": {"type": "uppercase", "value": [(6,), (1,2)]},
    "C": {"type": "uppercase", "value": [(6,), (1,4)]},
    "D": {"type": "uppercase", "value": [(6,), (1,4,5)]},
    "E": {"type": "uppercase", "value": [(6,), (1,5)]},
    "F": {"type": "uppercase", "value": [(6,), (1,2,4)]},
    "G": {"type": "uppercase", "value": [(6,), (1,2,4,5)]},
    "H": {"type": "uppercase", "value": [(6,), (1,2,5)]},
    "I": {"type": "uppercase", "value": [(6,), (2,4)]},
    "J": {"type": "uppercase", "value": [(6,), (2,4,5)]},
    "K": {"type": "uppercase", "value": [(6,), (1,3)]},
    "L": {"type": "uppercase", "value": [(6,), (1,2,3)]},
    "M": {"type": "uppercase", "value": [(6,), (1,3,4)]},
    "N": {"type": "uppercase", "value": [(6,), (1,3,4,5)]},
    "O": {"type": "uppercase", "value": [(6,), (1,3,5)]},
    "P": {"type": "uppercase", "value": [(6,), (1,2,3,4)]},
    "Q": {"type": "uppercase", "value": [(6,), (1,2,3,4,5)]},
    "R": {"type": "uppercase", "value": [(6,), (1,2,3,5)]},
    "S": {"type": "uppercase", "value": [(6,), (2,3,4)]},
    "T": {"type": "uppercase", "value": [(6,), (2,3,4,5)]},
    "U": {"type": "uppercase", "value": [(6,), (1,3,6)]},
    "V": {"type": "uppercase", "value": [(6,), (1,2,3,6)]},
    "W": {"type": "uppercase", "value": [(6,), (2,4,5,6)]},
    "X": {"type": "uppercase", "value": [(6,), (1,3,4,6)]},
    "Y": {"type": "uppercase", "value": [(6,), (1,3,4,5,6)]},
    "Z": {"type": "uppercase", "value": [(6,), (1,3,5,6)]},
    "1": {"type": "digits", "value": [(3,4,5,6), (1,)]},
    "2": {"type": "digits", "value": [(3,4,5,6), (1,2)]},
    "3": {"type": "digits", "value": [(3,4,5,6), (1,4)]},
    "4": {"type": "digits", "value": [(3,4,5,6), (1,4,5)]},
    "5": {"type": "digits", "value": [(3,4,5,6), (1,5)]},
    "6": {"type": "digits", "value": [(3,4,5,6), (1,2,4)]},
    "7": {"type": "digits", "value": [(3,4,5,6), (1,2,4,5)]},
    "8": {"type": "digits", "value": [(3,4,5,6), (1,2,5)]},
    "9": {"type": "digits", "value": [(3,4,5,6), (2,4)]},
    "0": {"type": "digits", "value": [(3,4,5,6), (2,4,5)]},
    "!":  {"type": "punctuation", "value": [(2,3,5)]},          
    "\"": {"type": "punctuation", "value": [(5,), (2,3,5,6)]},  
    "#":  {"type": "punctuation", "value": [(3,4,5,6)]},   
    "$":  {"type": "punctuation", "value": [(4,),(2,3,4)]},        
    "%":  {"type": "punctuation", "value": [(4,6),(3,5,6)]},            
    "•":  {"type": "punctuation", "value": [(4,5,6),(2,5,6)]}, 
    "&":  {"type": "punctuation", "value": [(1,2,3,4,6)]},  
    "'":  {"type": "punctuation", "value": [(3,)]},    
    "(":  {"type": "punctuation", "value": [(5,), (1,2,6)]},    
    ")":  {"type": "punctuation", "value": [(5,), (3,4,5)]},   
    "*":  {"type": "punctuation", "value": [(5,),(3,5)]},  
    "+":  {"type": "punctuation", "value": [(3,4,6)]}, 
    ",":  {"type": "punctuation", "value": [(2,)]},
    "-":  {"type": "punctuation", "value": [(3,6)]}, 
    ".":  {"type": "punctuation", "value": [(2,5,6)]},
    "/":  {"type": "punctuation", "value": [(3,4)]}, 
    ":":  {"type": "punctuation", "value": [(2,5)]},
    ";":  {"type": "punctuation", "value": [(2,3)]}, 
    "<":  {"type": "punctuation", "value": [(4,),(1,2,6)]},
    "=":  {"type": "punctuation", "value": [(5,),(2,3,5,6)]}, 
    ">":  {"type": "punctuation", "value": [(4,),(3,4,5)]}, 
    "?":  {"type": "punctuation", "value": [(2,3,6)]}, 
    "@":  {"type": "punctuation", "value": [(4,),(1,)]}, 
    "[":  {"type": "punctuation", "value": [(5,), (1,2,6)]},
    "\\": {"type": "punctuation", "value": [((4,5,6),(1,6))]},   
    "]":  {"type": "punctuation", "value": [(5,), (3,4,5)]}, 
    "^":  {"type": "punctuation", "value": [(4,5),(1,4,6)]}, 
    "_":  {"type": "punctuation", "value": [(4,6),(3,6)]},  
    "{":  {"type": "punctuation", "value": [(4,5,6),(1,2,6)]}, 
    "}":  {"type": "punctuation", "value": [(4,5,6),(3,4,5)]}, 
    "°":  {"type": "punctuation", "value": [(4,5),(2,4,5)]}, 
    " ":  {"type": "punctuation", "value": [("space",)]},
    "ch": {"type": "strong_groupsigns", "value": [(1,6)]},
    "sh": {"type": "strong_groupsigns", "value": [(1,4,6)]},
    "th": {"type": "strong_groupsigns", "value": [(1,4,5,6)]},
    "wh": {"type": "strong_groupsigns", "value": [(1,5,6)]},
    "ou": {"type": "strong_groupsigns", "value": [(1,2,5,6)]},
    "st": {"type": "strong_groupsigns", "value": [(3,4)]},
    "gh": {"type": "strong_groupsigns", "value": [(1,2,6)]},
    "ed": {"type": "strong_groupsigns", "value": [(1,2,4,6)]},
    "er": {"type": "strong_groupsigns", "value": [(1,2,4,5,6)]},
    "ow": {"type": "strong_groupsigns", "value": [(2,4,6)]},
    "ar": {"type": "strong_groupsigns", "value": [(3,4,5)]},
    "in": {"type": "strong_groupsigns", "value": [(3,5)]},
    "and": {"type": "strong_contraction", "value": [(1,2,3,4,6)]},
    "for": {"type": "strong_contraction", "value": [(1,2,3,4,5,6)]},
    "of":  {"type": "strong_contraction", "value": [(1,2,3,5,6)]},
    "the": {"type": "strong_contraction", "value": [(2,3,4,6)]},
    "with": {"type": "strong_contraction", "value": [(2,3,4,5,6)]},
    "day":       {"type": "initial_letter_contractions", "value": [(5,),(1,4,5)]},
    "ever":      {"type": "initial_letter_contractions", "value": [(5,),(1,5)]},
    "father":    {"type": "initial_letter_contractions", "value": [(5,),(1,2,4)]},
    "here":      {"type": "initial_letter_contractions", "value": [(5,),(1,2,5)]},
    "know":      {"type": "initial_letter_contractions", "value": [(5,),(1,3)]},
    "lord":      {"type": "initial_letter_contractions", "value": [(5,),(1,2,3)]},
    "mother":    {"type": "initial_letter_contractions", "value": [(5,),(1,3,4)]},
    "name":      {"type": "initial_letter_contractions", "value": [(5,),(1,3,4,5)]},
    "one":       {"type": "initial_letter_contractions", "value": [(5,),(1,3,5)]},
    "part":      {"type": "initial_letter_contractions", "value": [(5,),(1,2,3,4)]},
    "question":  {"type": "initial_letter_contractions", "value": [(5,),(1,2,3,4,5)]},
    "right":     {"type": "initial_letter_contractions", "value": [(5,),(1,2,3,5)]},
    "some":      {"type": "initial_letter_contractions", "value": [(5,),(2,3,4)]},
    "time":      {"type": "initial_letter_contractions", "value": [(5,),(2,3,4,5)]},
    "under":     {"type": "initial_letter_contractions", "value": [(5,),(1,3,6)]},
    "work":      {"type": "initial_letter_contractions", "value": [(5,),(2,4,5,6)]},
    "young":     {"type": "initial_letter_contractions", "value": [(5,),(1,3,4,5,6)]},
    "there":     {"type": "initial_letter_contractions", "value": [(5,),(2,3,4,6)]},
    "character": {"type": "initial_letter_contractions", "value": [(5,),(1,6)]}, 
    "through":   {"type": "initial_letter_contractions", "value": [(5,),(1,4,5,6)]},
    "where":     {"type": "initial_letter_contractions", "value": [(5,),(1,5,6)]},
    "ought":     {"type": "initial_letter_contractions", "value": [(5,),(1,2,5,6)]},
    "upon":      {"type": "initial_letter_contractions", "value": [(4,5),(1,3,6)]},
    "word":      {"type": "initial_letter_contractions", "value": [(4,5),(2,4,5,6)]},
    "these":     {"type": "initial_letter_contractions", "value": [(4,5),(2,3,4,6)]},
    "those":     {"type": "initial_letter_contractions", "value": [(4,5),(1,4,5,6)]},
    "whose":     {"type": "initial_letter_contractions", "value": [(4,5),(1,5,6)]},
    "cannot":    {"type": "initial_letter_contractions", "value": [(4,5,6),(1,4)]},
    "had":       {"type": "initial_letter_contractions", "value": [(4,5,6),(1,2,5)]},
    "many":      {"type": "initial_letter_contractions", "value": [(4,5,6),(1,3,4)]},
    "spirit":    {"type": "initial_letter_contractions", "value": [(4,5,6),(2,3,4)]},
    "world":     {"type": "initial_letter_contractions", "value": [(4,5,6),(2,4,5,6)]},
    "their":     {"type": "initial_letter_contractions", "value": [(4,5,6),(2,3,4,6)]},
    "ea":  {"type": "lower_groupsigns", "value": [(2,)]},
    "bb":  {"type": "lower_groupsigns", "value": [(2,3)]},
    "cc":  {"type": "lower_groupsigns", "value": [(2,5)]},
    "ff":  {"type": "lower_groupsigns", "value": [(2,3,5)]},
    "gg":  {"type": "lower_groupsigns", "value": [(2,3,5,6)]},
    "be":  {"type": "lower_groupsigns", "value": [(2,3)]},      
    "con": {"type": "lower_groupsigns", "value": [(2,5)]},
    "dis": {"type": "lower_groupsigns", "value": [(2,5,6)]},
    "en":  {"type": "lower_groupsigns", "value": [(2,6)]},
    "in":  {"type": "lower_groupsigns", "value": [(3,5)]},
    "enough": {"type": "lower_wordsigns", "value": [(2,6)]},
    "were":   {"type": "lower_wordsigns", "value": [(2,3,5,6)]},
    "his":    {"type": "lower_wordsigns", "value": [(2,3,6)]},
    "in":     {"type": "lower_wordsigns", "value": [(3,5)]},
    "was":    {"type": "lower_wordsigns", "value": [(3,5,6)]},
    "child": {"type": "strong_wordsigns", "value": [(1,6)]},
    "shall": {"type": "strong_wordsigns", "value": [(1,4,6)]},
    "this":  {"type": "strong_wordsigns", "value": [(1,4,5,6)]},
    "which": {"type": "strong_wordsigns", "value": [(1,5,6)]},
    "out":   {"type": "strong_wordsigns", "value": [(1,2,5,6)]},
    "still": {"type": "strong_wordsigns", "value": [(3,4)]},
    "about":       {"type": "shortform_words", "value": [(1,), (1,2)]}, 
    "above":       {"type": "shortform_words", "value": [(1,), (1,2),(1,2,3,6)]}, 
    "according":   {"type": "shortform_words", "value": [(1,),(1,4)]},  
    "across":      {"type": "shortform_words", "value": [(1,),(1,4),(1,2,3,5)]},  
    "after":       {"type": "shortform_words", "value": [(1,),(1,2,4)]}, 
    "afternoon":   {"type": "shortform_words", "value": [(1,),(1,2,4),(1,3,4,5)]}, 
    "afterward":   {"type": "shortform_words", "value": [(1,),(1,2,4),(2,4,5,6)]},
    "again":       {"type": "shortform_words", "value": [(1,), (1,2,4,5)]}, 
    "against":     {"type": "shortform_words", "value": [(1,), (1,2,4,5), (3,4)]},
    "almost":      {"type": "shortform_words", "value": [(1,), (1,2,3), (1,3,4)]},
    "already":     {"type": "shortform_words", "value": [(1,), (1,2,3), (1,2,3,5)]},
    "also":        {"type": "shortform_words", "value": [(1,), (1,2,3)]},
    "although":    {"type": "shortform_words", "value": [(1,), (1,2,3),(1,4,5,6)]},
    "altogether":  {"type": "shortform_words", "value": [(1,),(1,2,3),(2,3,4,5)]},
    "always":      {"type": "shortform_words", "value": [(1,), (1,2,3), (2,4,5,6)]},
    "because":     {"type": "shortform_words", "value": [(2,3), (1,4)]}, 
    "before":      {"type": "shortform_words", "value": [(2,3), (1,2,4)]}, 
    "behind":      {"type": "shortform_words", "value": [(2,3), (1,2,5)]}, 
    "below":       {"type": "shortform_words", "value": [(2,3), (1,2,3)]}, 
    "beneath":     {"type": "shortform_words", "value": [(2,3), (1,3,4,5)]}, 
    "beside":      {"type": "shortform_words", "value": [(2,3), (2,3,4)]},
    "between":     {"type": "shortform_words", "value": [(2,3), (2,3,4,5)]}, 
    "beyond":      {"type": "shortform_words", "value": [(2,3), (1,3,4,5,6)]},
    "blind":       {"type": "shortform_words", "value": [(1,2), (1,2,3)]}, 
    "braille":     {"type": "shortform_words", "value": [(1,2),(1,2,3,5),(1,2,3)]}, 
    "children":    {"type": "shortform_words", "value": [(1,6), (1,3,4,5)]}, 
    "could":       {"type": "shortform_words", "value": [(1,4),(1,4,5)]}, 
    "deceive":     {"type": "shortform_words", "value": [(1,4,5), (1,4), (1,2,3,6)]}, 
    "declare":     {"type": "shortform_words", "value": [(1,4,5), (1,4), (1,2,3)]}, 
    "either":      {"type": "shortform_words", "value": [(1,5), (2,4)]},
    "first":      {"type": "shortform_words", "value":  [(1,2,4),(3,4)]}, 
    "friend":      {"type": "shortform_words", "value": [(1,2,4), (1,2,3,5)]},
    "good":        {"type": "shortform_words", "value": [(1,2,4,5), (1,4,5)]},
    "great":       {"type": "shortform_words", "value": [(1,2,4,5), (1,2,3,5),(2,3,4,5)]},
    "herself":     {"type": "shortform_words", "value": [(1,2,5), (1,2,4,5,6),(1,2,4)]}, 
    "him":         {"type": "shortform_words", "value": [(1,2,5), (1,3,4)]},
    "himself":     {"type": "shortform_words", "value": [(1,2,5), (1,3,4),(1,2,4)]}, 
    "immediate":   {"type": "shortform_words", "value": [(2,4), (1,3,4),(1,3,4)]}, 
    "its":         {"type": "shortform_words", "value": [(1,3,4,6),(2,3,4)]},  
    "itself":      {"type": "shortform_words", "value": [(1,3,4,6), (1,2,4)]},  
    "letter":      {"type": "shortform_words", "value": [(1,2,3), (1,2,3,5)]}, 
    "little":      {"type": "shortform_words", "value": [(1,2,3), (1,2,3)]}, 
    "much":        {"type": "shortform_words", "value": [(1,3,4), (1,6)]},
    "must":        {"type": "shortform_words", "value": [(1,3,4), (3,4)]}, 
    "myself":      {"type": "shortform_words", "value": [(1,3,4), (1,3,4,5,6),(1,2,4)]},
    "necessary":   {"type": "shortform_words", "value": [(1,3,4,5), (1,5),(1,4)]},
    "neither":     {"type": "shortform_words", "value": [(1,3,4,5), (1,5),(2,4)]}, 
    "oneself":     {"type": "shortform_words", "value": [(5,),(1,3,5), (1,2,4)]}, 
    "ourselves":   {"type": "shortform_words", "value": [(1,2,5,6), (1,2,3,5),(1,2,3,6),(2,3,4)]},
    "paid":        {"type": "shortform_words", "value": [(1,2,3,4), (1,4,5)]}, 
    "perceive":    {"type": "shortform_words", "value": [(1,2,3,4), (1,2,4,5,6),(1,4),(1,2,3,6)]},
    "perhaps":     {"type": "shortform_words", "value": [(1,2,3,4), (1,2,4,5,6),(1,2,5)]}, 
    "quick":       {"type": "shortform_words", "value": [(1,2,3,4,5), (1,3)]}, 
    "receive":     {"type": "shortform_words", "value": [(1,2,3,5), (1,4),(1,2,3,6)]}, 
    "said":        {"type": "shortform_words", "value": [(2,3,4), (1,4,5)]},
    "should":      {"type": "shortform_words", "value": [(1,4,6), (1,4,5)]},
    "such":        {"type": "shortform_words", "value": [(2,3,4), (1,6)]}, 
    "themselves":  {"type": "shortform_words", "value": [(2,3,4,6), (1,3,4),(1,2,3,6),(2,3,4)]}, 
    "today":       {"type": "shortform_words", "value": [(2,3,4,5), (1,4,5)]}, 
    "together":    {"type": "shortform_words", "value": [(2,3,4,5), (1,2,4,5),(1,2,3,5)]}, 
    "tomorrow":    {"type": "shortform_words", "value": [(2,3,4,5), (1,3,4)]}, 
    "tonight":     {"type": "shortform_words", "value": [(2,3,4,5), (1,3,4,5)]}, 
    "would":       {"type": "shortform_words", "value": [(2,4,5,6), (1,4,5)]}, 
    "your":        {"type": "shortform_words", "value": [(1,3,4,5,6), (1,2,3,5)]}, 
    "yourself":    {"type": "shortform_words", "value": [(1,3,4,5,6), (1,2,3,5),(1,2,4)]}, 
    "yourselves":  {"type": "shortform_words", "value": [(1,3,4,5,6), (1,2,3,5),(1,2,3,6),(2,3,4)]}, 
    "ound": {"type": "final_letter_groupsigns", "value": [(4,6),(1,4,5)]},
    "ance": {"type": "final_letter_groupsigns", "value": [(4,6),(1,5)]},
    "sion": {"type": "final_letter_groupsigns", "value": [(4,6),(1,3,4,5)]},
    "less": {"type": "final_letter_groupsigns", "value": [(4,6),(2,3,4)]},
    "ount": {"type": "final_letter_groupsigns", "value": [(4,6),(2,3,4,5)]},
    "ence": {"type": "final_letter_groupsigns", "value": [(5,6),(1,5)]},
    "ong":  {"type": "final_letter_groupsigns", "value": [(5,6),(1,2,4,5)]},
    "ful":  {"type": "final_letter_groupsigns", "value": [(5,6),(1,2,3)]},
    "tion": {"type": "final_letter_groupsigns", "value": [(5,6), (1,3,4,5)]},
    "ness": {"type": "final_letter_groupsigns", "value": [(5,6),(2,3,4)]},
    "ment": {"type": "final_letter_groupsigns", "value": [(5,6),(2,3,4,5)]},
    "ity":  {"type": "final_letter_groupsigns", "value": [(5,6),(1,3,4,5,6)]},
    "ing":  {"type": "strong_groupsigns", "value": [(3,4,6)]},
    "but":        { "type": "alpha_wordsigns", "value": [(1,2)] },
    "can":        { "type": "alpha_wordsigns", "value": [(1,4)] },
    "do":         { "type": "alpha_wordsigns", "value": [(1,4,5)] },
    "every":      { "type": "alpha_wordsigns", "value": [(1,5)] },
    "from":       { "type": "alpha_wordsigns", "value": [(1,2,4)] },
    "go":         { "type": "alpha_wordsigns", "value": [(1,2,4,5)] },
    "have":       { "type": "alpha_wordsigns", "value": [(1,2,5)] },
    "just":       { "type": "alpha_wordsigns", "value": [(2,4,5)] },
    "knowledge":  { "type": "alpha_wordsigns", "value": [(1,3)] },
    "like":       { "type": "alpha_wordsigns", "value": [(1,2,3)] },
    "more":       { "type": "alpha_wordsigns", "value": [(1,3,4)] },
    "not":        { "type": "alpha_wordsigns", "value": [(1,3,4,5)] },
    "people":     { "type": "alpha_wordsigns", "value": [(1,2,3,4)] },
    "quite":      { "type": "alpha_wordsigns", "value": [(1,2,3,4,5)] },
    "rather":     { "type": "alpha_wordsigns", "value": [(1,2,3,5)] },
    "so":         { "type": "alpha_wordsigns", "value": [(2,3,4)] },
    "that":       { "type": "alpha_wordsigns", "value": [(2,3,4,5)] },
    "us":         { "type": "alpha_wordsigns", "value": [(1,3,6)] },
    "very":       { "type": "alpha_wordsigns", "value": [(1,2,3,6)] },
    "will":       { "type": "alpha_wordsigns", "value": [(2,4,5,6)] },
    "it":         { "type": "alpha_wordsigns", "value": [(1,3,4,6)] },
    "you":        { "type": "alpha_wordsigns", "value": [(1,3,4,5,6)]},
    "as":         { "type": "alpha_wordsigns", "value": [(1,3,5,6)]}}


    for typename, items in categories.items():
        for key in items:
            data[key] = {
                "type": typename,
                "value": braille.get(key, [])
            }

    with open("brailledict.json", "w") as f:
        json.dump(data,f,indent = 4)


def check_existence(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.close()
            generate()

check_existence("brailledict.json")

with open("brailledict.json", "r") as f:
    raw = json.load(f)

legal_tokens = list(raw.keys())

def extract_text(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == ".pdf":
        
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    elif ext == ".docx":
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)

    else:
        return textract.process(path).decode("utf-8")


def match_keys(text, keys):
    return [k for k in keys if k in text]


def display(tuple_val):
    for button in buttons:
        if button.id in tuple_val:
            button.fill = 'lime'
        else:
            button.fill = 'grey'
            
app.matches = []

def from_device():
    text_file_path = pick_file()
    if text_file_path:
        text = extract_text(text_file_path)
        app.matches += match_keys(text,legal_tokens)



def onStep():
    if(app.autofs <= 3):
        app.autofs += 1
    if(app.autofs == 3):
        pyautogui.keyDown("command")
        pyautogui.keyDown('ctrl')
        pyautogui.press('f')
        pyautogui.keyUp("command")
        pyautogui.keyUp("ctrl")
    if(app.time_delay>0):
        app.time_delay-=1
    else:
        if(app.mode == 'auto'):
            if(app.index>=0):
                for j in range(len(app.matches[app.index])):
                    display(app.matches[app.index][j])

app.mode = 'selecting'

buttons = Group()

def create_button(locX, id):
    if(id == 'space'):
        new = Oval(locX, 3*app.height/4, app.width/4, app.height/10, fill='grey', border = 'black')
    else:
        new = Oval(locX, app.height/2, app.width/10, app.height/5, fill='grey', border = 'black')
    new.id = id
    new.label = (Label(id, locX, new.centerY, size = (app.width+app.height)/100))
    return new

def start():
    buttons.add(create_button(app.width/9, 3))
    buttons.add(create_button(2*app.width/9, 2))
    buttons.add(create_button(3*app.width/9, 1))
    buttons.add(create_button(6*app.width/9, 4))
    buttons.add(create_button(7*app.width/9, 5))
    buttons.add(create_button(8*app.width/9, 6))
    buttons.add(create_button(app.width/2, 'space'))

start()

typing_input_button = Rect(0,0,app.width/10, app.height/15, fill='white', border = 'black')
typing_input_label = Label("Type Your Input", typing_input_button.centerX, typing_input_button.centerY)
file_input_button = Rect(app.width,0,app.width/10, app.height/15, fill='white', border = 'black', align = 'top-right')
file_input_label = Label("Insert File", file_input_button.centerX, file_input_button.centerY)

def onMousePress(x,y):
    if(typing_input_button.contains(x,y)):
        text = app.getTextInput("Enter your text for braille conversion")
        app.matches+=match_keys(text, legal_tokens)
        for i in range(len(app.matches)):
            print(raw[app.matches[i]]["value"]["value"])
        app.matches.clear()
    if(file_input_button.contains(x,y)):
        from_device()

app.run()