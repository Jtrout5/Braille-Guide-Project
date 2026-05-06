import json
import os
import shutil
import zipfile
import subprocess
import sys
import re
from io import BytesIO
import warnings

try:
    import pdfplumber
    from docx import Document
    import textract
    import requests
    import pyautogui
    import pyphen
except ImportError as e:
    os.system("pip3 install -r requirements.txt")
    import pdfplumber
    from docx import Document
    import textract
    import requests
    import pyautogui
    import pyphen

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

try: 
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


RULES = { ## WILL ADD NEW RULES AS ISSUES ARISE
    "ea": {"not_start": True, "no_bridge": True, "no_end": True, "not_solo": True},
    "be": {"only_first_syllable": True},
    "dis": {"only_first_syllable": True, "not_solo": True},
    "con": {"only_first_syllable": True, "not_solo": True},
    "ing": {"not_start": True, "not_solo": True},
    "bb": {"not_start": True, "no_end": True},
    "cc": {"not_start": True, "no_end": True},
    "ff": {"not_start": True, "no_end": True},
    "gg": {"not_start": True, "no_end": True},
    "en": {"not_solo": True},
    "ful": {"not_start": True},
    "ound": {"not_start": True},
    "ance": {"not_start": True},
    "sion": {"not_start": True},
    "less": {"not_start": True},
    "ount": {"not_start": True},
    "ence": {"not_start": True},
    "ong": {"not_start": True},
    "tion": {"not_start": True},
    "ness": {"not_start": True},
    "ment": {"not_start": True},
    "ity": {"not_start": True},
    
}

default_delay = 45    
app.cpm = (app.stepsPerSecond*60/default_delay) 
app.selected_delay = (app.stepsPerSecond*60)/app.cpm
app.cellsSinceLastNewLine = 0
app.time_delay = 45
app.wideIndex = -1
app.pageWidth = 42
size = pyautogui.size()
width = size[0]
height = size[1]
app.width = width
app.height = height
app.storedCellsSince = []
app.reasons = []
app.indexSaverL = []
app.indexSaverR = []
app.specialFinalIndex = 0

filepath = os.path.abspath(__file__)
directory_path = os.path.dirname(filepath)
os.chdir(directory_path)
currentFile =  os.path.basename(__file__)
filename = currentFile[:-3]

def check_existence(path):
    '''
    Takes 1 arg, path which is the relative bath to the file
    If it exitsts, then do nothing, else run the braille generator file to create it
    '''
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.close()
            subprocess.run([sys.executable, "braille_generator.py"])

check_existence("brailledict.json")

with open("brailledict.json", "r") as f:
    raw = json.load(f)

legal_tokens = list(raw.keys())

def extract_text(path):
    '''
    Takes 1 arg, path which is the relative path to the document
    Tries to extraxt the text from the doc
    Returns the text from the document as a string
    '''
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


def tokenize(txt):
    '''
    Takes 1 arg: text, which is the extracted text
    Returns a list of all tokens based on the split rules
    '''
    tokens = re.findall(r"[A-Za-z0-9]+|[^\w\s]| |\n", txt)
    return tokens

_pyphen_dic = pyphen.Pyphen(lang="en")

def is_valid_contraction(key, word, pos):
    '''
    Takes 3 args: key, word, pos
    key: the key representing a contraction from the braille dictionary json file
    word: the word trying to be shortened
    pos: where in the word that the key begins
    Returns true if the key would be valid given the word, false otherwise, only false if a UEB rule would be broken given the key and word.
    '''
    broken = _pyphen_dic.inserted(word).split("-")
    rules = RULES.get(key)
    if not rules:
        return True
    if rules.get("not_solo") and key == word:
        return False
    if rules.get("not_start") and pos == 0:
        return False
    if rules.get("only_first_syllable") and key != broken[0]:
        return False
    if rules.get("no_bridge"):
        count = 0
        for i in range(len(broken)):
            if key in broken[i]:
                count += 1
        if count == 0:
            return False 
    if rules.get("no_end") and key == broken[len(broken)-1][-(len(key)):]:
        return False

    return True


def match_case(key, token):
    '''
    Takes 2 args, key and token
    key: the key from the braille dictionary
    token: the token being checked for capitalization
    Returns the lowercase key if it's place in the original text was lowercase, capitalized key otherwise
    '''
    if token.isupper():
        return key.upper()
    elif token[0].isupper():
        return key.capitalize()
    else:
        return key

def match_keys(text, keys):
    '''
    Takes 2 args, text and keys
    text: a list of tokenized text
    keys: a list of valid keys from the opened braile_dict json file.
    No returns, but causes mutation of certain app variables
    Makes the best available matches from the text to braille representation
    '''
    alpha_wordsigns = [k for k in keys if raw[k]["type"] == "alpha_wordsigns"]
    punctuation = [k for k in keys if raw[k]["type"] == "punctuation"]
    non_alpha_wordsigns = [
        k for k in keys
        if raw[k]["type"] in ("lower_wordsigns", "strong_wordsigns")
    ]
    groupsigns = [
        k for k in keys
        if raw[k]["type"] in (
            "strong_contraction",
            "strong_groupsigns",
            "initial_letter_contractions",
            "lower_groupsigns",
            "final_letter_groupsigns",
            "shortform_words",
        )
    ]
    leftover_letters = [k for k in keys if raw[k]["type"] == "lowercase"]
    digits = [k for k in keys if raw[k]["type"] == "digits"]

    app.sequence = [None] * len(text)
    app.matches = [None] * len(text)

    for i, token in enumerate(text):
        if token is None:
            continue
        for key in punctuation:
            if token == key:
                app.sequence[i] = raw[key]["value"]
                app.matches[i] = key
                text[i] = None
                break
            
    for i, token in enumerate(text):
        if token is None:
            continue
        for key in alpha_wordsigns:
            if token.lower() == key:
                val = raw[key]["value"]
                if token[0].isupper():
                    val = [[6]] + val
                app.sequence[i] = val
                app.matches[i] = match_case(key, token)
                text[i] = None
                break

    for i, token in enumerate(text):
        if token is None:
            continue
        for key in non_alpha_wordsigns:
            if token.lower() == key:
                val = raw[key]["value"]
                if token[0].isupper():
                    val = [[6]] + val
                app.sequence[i] = val
                app.matches[i] = match_case(key, token)
                text[i] = None
                break

    i = 0
    while i < len(text):
        token = text[i]

        if token is None or not token.strip():
            i += 1
            continue

        lower = token.lower()
        n = len(token)

        dp = [None] * (n + 1)
        dp[n] = (0, 0, [], [], [])

        for pos in range(n - 1, -1, -1):
            best_cells = float("inf")
            best_pri = float("inf")
            best_seq = None
            best_split = None
            best_keys = None

            next_cells, next_pri, next_seq, next_split, next_keys = dp[pos + 1]
            fallback_cells = next_cells + 1
            fallback_pri = next_pri + 2  
            fallback_seq = [None] + next_seq
            fallback_keys = [None] + next_keys
            fallback_split = [token[pos]] + next_split
            

            best_cells = fallback_cells
            best_pri = fallback_pri
            best_seq = fallback_seq
            best_split = fallback_split
            best_keys = fallback_keys

            for key in groupsigns:
                if lower.startswith(key, pos) and is_valid_contraction(key, token, pos):
                    end = pos + len(key)
                    next_cells, next_pri, next_seq, next_split, next_keys = dp[end]

                    val = raw[key]["value"]
                    cell_count = len(val)

                    pri = 0 if raw[key]['type'] in ("strong_groupsigns", "strong_contraction") else 1

                    total_cells = next_cells + cell_count
                    total_pri = next_pri + pri

                    if (best_seq is None or (total_cells, total_pri) < (best_cells, best_pri) or ((total_cells, total_pri) == (best_cells, best_pri) and len(key) > len(best_split[0]))):
                        best_cells = total_cells
                        best_pri = total_pri
                        best_seq = [val] + next_seq
                        best_split = [token[pos:end]] + next_split
                        segment = token[pos:end]
                        best_keys = [match_case(key, segment)] + next_keys
            dp[pos] = (best_cells, best_pri, best_seq, best_split, best_keys)

        _, _, seq_list, split_list, key_list = dp[0]


        text[i:i+1] = split_list
        app.sequence[i:i+1] = seq_list
        app.matches[i:i+1] = key_list

        i += len(split_list)
        
    i = 0
    in_number_mode = False

    while i < len(text):
        token = text[i]
        if token is None:
            i += 1
            continue

        if all(ch in digits for ch in token):
            digit_seq = []

            if not in_number_mode:
                digit_seq.append([3, 4, 5, 6])
                in_number_mode = True

            for ch in token:
                digit_seq.append(raw[ch]["value"])

            app.sequence[i] = digit_seq
            app.matches[i] = token
            text[i] = None

        else:
            if token not in punctuation:
                in_number_mode = False

        i += 1

    i = 0
    while i < len(text):
        token = text[i]
        seq = app.sequence[i]

        if token is None or seq is not None:
            i += 1
            continue

        new_tokens = []
        new_seq = []
        new_matches = []

        for ch in token:
            low = ch.lower()
            if low in leftover_letters:
                val = raw[low]["value"]
                new_tokens.append(ch)
                new_seq.append(val)
                new_matches.append(match_case(low, ch))
            else:
                new_tokens.append(ch)
                new_seq.append(None)
                new_matches.append(None)

        text[i:i+1] = new_tokens
        app.sequence[i:i+1] = new_seq
        app.matches[i:i+1] = new_matches

        i += len(new_tokens)

    for i, token in enumerate(text):
        seq = app.sequence[i]

        if token is None or seq is None:
            continue

        if token[0].isupper():
            app.sequence[i] = [[6]] + seq

def safe_to_proceed(dist):
    '''
    Takes 1 arg dist, which is the distance to the edge of the page
    Returns true if there is a space or newline in the text before the end of the page, false otherwise
    Used in this program to prevent cutting words off in the middle when possible
    '''
    for i in range(1, dist+1):
        if((app.wideIndex + i) < len(app.sequence)):
            if(app.sequence[app.wideIndex+i] == ['space'] or (app.sequence[app.wideIndex+i] == ['NewLine'])):
                return True 
        else:
            return True
    return False

def show_print(text, key):
    
    '''
    Takes 2 args: text and key
    text: the text to display relating to the braille dots presented, except in 2 newline cases, which will display some different text than given
    key: which key press was involved in this function call, to prevent a bug associated with this function in certain left key presses and space entries
    returns no values but does update app variables
    '''
    printed_version.value = text
    if(text == "\n"):
        app.cellsSinceLastNewLine = 0
        printed_version.value = "*Go to next line*"
        app.time_delay = (int)(app.stepsPerSecond * 3.5)
        if(app.sequence[app.wideIndex+1]) == ['space']:
            app.wideIndex+=1
    elif(text == "SpecialNL"):
        app.storedCellsSince.append(app.cellsSinceLastNewLine)
        app.cellsSinceLastNewLine = 0
        printed_version.value = "*Go to next line*"
        app.time_delay = (int)(app.stepsPerSecond * 3.5)
        app.reasons.append("End")
    if(key!='left'):
        if(app.pageWidth!="Infinite"):
            if(text ==" "):
                if(not(safe_to_proceed((app.pageWidth - app.cellsSinceLastNewLine)+1))):
                    if(app.wideIndex<(len(app.sequence)-1)):
                        show_print("SpecialNL", key)
                        display([])

def show_braille(tuple_val):
    '''
    Takes 1 arg: tuple_val which is a list or tuple of numbers. 
    Update fill of braille dots to be black if their id is in the tuple_val, empty/None otherwise
    Return no vals
    '''
    for dot in dots:
        if dot.id in tuple_val:
            dot.fill='black'
        else:
            dot.fill = None

def display(tuple_val):
    '''
    Takes 1 arg: tuple_val which is a list or tuple of numbers. 
    Update fill of buttons to be green if their id is in the tuple_val, grey otherwise
    Return no vals
    '''
    for thing in tuple_val:
        if(type(thing) == list): ##Only happens with numbers as a quirk of how match_keys handles digits
            display(thing)
            return
    show_braille(tuple_val)
    for button in buttons:
        if button.id in tuple_val:
            button.fill = 'lime'
        else:
            button.fill = 'grey'
            
app.tokens = []
app.matches = []
app.sequence = []

def from_device():
    '''
    Takes no args and returns no values
    Runs a helper file to help bring in a file to extract text from
    Update app variables
    '''
    app.tokens.clear()
    app.matches.clear()
    app.sequence.clear()
    result = subprocess.run(
        [sys.executable, "file_helper.py"],
        capture_output=True,
        text=True
    )
    output = json.loads(result.stdout)
    text_file_path = output['path']
    if text_file_path:
        text = extract_text(text_file_path)
        app.tokens = tokenize(text)
        match_keys(app.tokens,legal_tokens)

def onStep():
    '''
    Built in CMU function
    Called once each frane
    Used in this function to handle display in auto mode
    '''
    if(app.playing == True):
        if(app.time_delay>0):
            app.time_delay-=1
        if(app.time_delay == (int)(app.selected_delay/3)):
            display([])
            if(app.wideIndex<(len(app.sequence)-1)):
                if(((app.sequence[app.wideIndex] == app.sequence[app.wideIndex+1]) and len(app.matches[app.wideIndex]) == 1) or (not(app.matches[app.wideIndex] == app.matches[app.wideIndex+1]))):
                    show_print("", 'right')
            else:
                show_print("", 'right')
        if(app.time_delay == 0):
            if(app.mode == 'auto' and app.playing == True):
                app.time_delay = app.selected_delay
                if(len(app.sequence) == 0):
                    app.mode = 'selecting'
                if(app.wideIndex>= -1):
                    if(app.wideIndex<len(app.sequence)):
                        app.specialFinalIndex = app.cellsSinceLastNewLine
                        if(app.pageWidth!= "Infinite" and app.cellsSinceLastNewLine>=app.pageWidth and app.cellsSinceLastNewLine!=0 and app.wideIndex<len(app.sequence)-1):
                            display([])
                            show_print("\n", 'right')
                            app.cellsSinceLastNewLine = 0
                            if(app.currSpec != 'hyphen'):
                                app.reasons.append("End")
                                app.storedCellsSince.append(app.pageWidth)
                            else: 
                                app.reasons.append("Hyphen")
                                app.storedCellsSince.append(app.pageWidth)
                                app.wideIndex = app.indexSaverR.pop()-1
                        elif(app.pageWidth!= "Infinite" and app.cellsSinceLastNewLine == app.pageWidth-1 and app.wideIndex<len(app.sequence)-2 and app.cellsSinceLastNewLine!=0 and not(app.sequence[app.wideIndex+1] == ['space'] or app.sequence[app.wideIndex+1] ==["NewLine"] or app.sequence[app.wideIndex] == ["space"] or app.sequence[app.wideIndex] == ['NewLine'])):
                            display([3,6])
                            show_print("-", 'right')
                            app.currSpec = 'hyphen'
                            app.cellsSinceLastNewLine+=1
                            app.indexSaverL.append(app.wideIndex)
                            app.indexSaverR.append(app.wideIndex+1)
                        else:
                            app.currSpec = 'letter'
                            app.wideIndex+=1
                            app.cellsSinceLastNewLine += 1
                            app.storedCellsSince.append(app.cellsSinceLastNewLine)
                            if(app.wideIndex<len(app.sequence)):
                                display(app.sequence[app.wideIndex])
                                show_print(app.matches[app.wideIndex], 'right')
                            else:
                                display([])
                                show_print("", 'right')
                                app.currSpec = None
                    else:
                        play_pause_label.value = "Paused (P)"
                        play_pause_button.border = 'black'
                        app.cellsSinceLastNewLine = app.specialFinalIndex
                        app.playing = False
                        display([])
                        show_print("", 'right')
                        app.currSpec = None

app.mode = 'selecting'

buttons = Group()
dots = Group()
updateGUI = Group()

def create_button(locX, id):
    '''
    Takes 2 args, locX for horizontal position, and id which represents the dot number associated with the button
    Returns the shape created
    '''
    if(id == 'space'):
        new = Oval(locX, 3*app.height/4, app.width/4, app.height/10, fill='grey', border = 'black')
    else:
        new = Oval(locX, app.height/2, app.width/10, app.height/5, fill='grey', border = 'black')
    new.id = id
    new.label = (Label(id, locX, new.centerY, size = (app.width+app.height)/40))
    return new

def start():
    '''
    Takes no args, returns no values, but adds shape to appropraite shape group
    Create the buttons matching the buttons on a 6 dot brailler
    '''
    buttons.add(create_button(app.width/9, 3))
    buttons.add(create_button(2*app.width/9, 2))
    buttons.add(create_button(3*app.width/9, 1))
    buttons.add(create_button(6*app.width/9, 4))
    buttons.add(create_button(7*app.width/9, 5))
    buttons.add(create_button(8*app.width/9, 6))
    buttons.add(create_button(app.width/2, 'space'))

start()

typing_input_button = Rect(0,0,app.width/10, 79*app.height/1080, fill='white', border = 'black')
typing_input_label = Label("Type Your Input (T)", typing_input_button.centerX, typing_input_button.centerY)
file_input_button = Rect(app.width,0,app.width/10, 79*app.height/1080, fill='white', border = 'black', align = 'top-right')
file_input_label = Label("Insert File (F)", file_input_button.centerX, file_input_button.centerY)
play_pause_button = Circle(7 * app.width/16, app.width/35, app.width/35, fill='white', border = 'black')
play_pause_label = Label("Paused (P)", play_pause_button.centerX, play_pause_button.centerY)
app.playing = False
auto_manual_button = Circle(3*app.width/8, app.width/35, app.width/35, fill='white', border = 'black')
auto_manual_label = Label("Manual Mode (M)", auto_manual_button.centerX, auto_manual_button.centerY)
app.displayMode = "Manual"
linesPerPageLabel = Label("Characters per line: %d" %app.pageWidth, 9*app.width/40, app.height/40, size = app.width/50)
linesIncreaseButton = Rect(linesPerPageLabel.centerX+1, linesPerPageLabel.bottom, linesPerPageLabel.width/6, linesPerPageLabel.height, fill="white", border = 'black')
linesIncrease10Button = Rect(linesIncreaseButton.right+1, linesPerPageLabel.bottom, linesPerPageLabel.width/6, linesPerPageLabel.height, fill="white", border = 'black')
linesIncreaseMaxButton = Rect(linesIncrease10Button.right+1, linesPerPageLabel.bottom, linesPerPageLabel.width/6, linesPerPageLabel.height, fill="white", border = 'black')
linesDecreaseButton = Rect(linesPerPageLabel.centerX-1, linesPerPageLabel.bottom, linesPerPageLabel.width/6, linesPerPageLabel.height, fill="white", border = 'black', align = 'top-right')
linesDecrease10Button = Rect(linesDecreaseButton.left-1, linesPerPageLabel.bottom, linesPerPageLabel.width/6, linesPerPageLabel.height, fill="white", border = 'black', align = 'top-right')
linesDecreaseMaxButton = Rect(linesDecrease10Button.left-1, linesPerPageLabel.bottom, linesPerPageLabel.width/6, linesPerPageLabel.height, fill="white", border = 'black', align = 'top-right')
inc1Label = Label("+1",linesIncreaseButton.centerX, linesIncreaseButton.centerY)
inc2Label = Label("+10",linesIncrease10Button.centerX, linesIncreaseButton.centerY)
inc3Label = Label("Max",linesIncreaseMaxButton.centerX, linesIncreaseButton.centerY)
inc4Label = Label("-1",linesDecreaseButton.centerX, linesIncreaseButton.centerY)
inc5Label = Label("-10",linesDecrease10Button.centerX, linesIncreaseButton.centerY)
inc6Label = Label("Min",linesDecreaseMaxButton.centerX, linesIncreaseButton.centerY)
printed_version = Label("", buttons.centerX, app.height/4,size = app.width/40)
cpm_label = Label("%d cells per minute (Auto Mode)" %app.cpm, file_input_button.left - (3*app.width/16), play_pause_button.centerY, size = app.width/60)
increase_cpm_button = Rect(cpm_label.right+10, cpm_label.centerY, app.width/25, app.width/40, fill="white", border = 'black', align = 'left')
decrease_cpm_button = Rect(cpm_label.left-10, cpm_label.centerY, app.width/25, app.width/40, fill='white', border = 'black', align = 'right')
increase_cpm_label = Label("Increase (+)", increase_cpm_button.centerX, increase_cpm_button.centerY)
decrease_cpm_label = Label("Decrease (-)", decrease_cpm_button.centerX, decrease_cpm_button.centerY)
escape_button = Circle(app.width/2, auto_manual_button.centerY, auto_manual_button.radius, fill='white', border = 'red', borderWidth = 5)
escape_label = Label("Exit (X)", escape_button.centerX, escape_button.centerY, fill='red', size = inc1Label.size * 2, bold = True)


for i in range(1,7,1):
    '''
    Create the Braille Display Dots
    '''
    offsetX = -15 if i<4 else 15
    offsetY = 0 if i%3 == 1 else 30 if i%3 == 2 else 60
    new = Circle((app.width/2 + offsetX), (app.height/3 + offsetY), 10, fill = None, border = 'grey', borderWidth = 0.5)
    new.id = i
    dots.add(new)


def paired_expansion(lst1, lst2):
    '''
    Takes 2 lists as argument
    lst1 should be a list containing lists of lists of numbers (and some special strings)
    lst2 should be a list of strings
    Nothing is returned but the original lists are mutated such that 
    lst1 will be a list of lists of numbers with each list of numbers representing a single braille cell
    lst2 will be a list of strings but expanded put to match the updated lst 1 such that the indexes line up where each cell is related to the string found at the same index in lst2
    '''
    duplicate1 = []
    duplicate2 = []
    idx = 0
    for item in lst1:
        if(item!=None): ## item = None in the case of unmatched chars like \t or some weird punctuation which I don't have rules for
            for thing in item:
                duplicate1.append(thing)
                duplicate2.append(lst2[idx])
        idx+=1
    lst1.clear()
    lst2.clear()
    for i in range(len(duplicate1)):
        lst1.append(duplicate1[i])
        lst2.append(duplicate2[i])


def increase_width_max():
    '''
    Takes no args and returns no values
    If the game is in screensaver mode, then this will set screensaver autoclicks to max speed
    '''
    app.pageWidth = "Infinite"
    linesPerPageLabel.value = "Characters per line: %s" %app.pageWidth 

def decrease_width_max():
    '''
    Takes no args and returns no values
    If the game is in screensaver mode, then this will set screensaver autoclicks to minimum speed
    '''
    app.pageWidth = 10
    linesPerPageLabel.value = "Characters per line: %d" %app.pageWidth

def increase_width_10():
    '''
    Takes no args and returns no values
    If the game is in screensaver mode, then this will increase the speed of autoclicks by 10 per minute
    Will set to max speed if an increase of 10 would put the speed too high
    '''
    if ((app.pageWidth != "Infinite") and (app.pageWidth <51)):
        app.pageWidth+=10
        linesPerPageLabel.value = "Characters per line: %d" %app.pageWidth
    else:
        increase_width_max()

def decrease_width_10():
    '''
    Takes no args and returns no values
    If the game is in screensaver mode, then this will decrease the speed of autoclicks by 10 per minute
    Will set to minumum speed if a decrease of 10 would put the speed too low
    '''
    if (app.pageWidth != "Infinite") and (app.pageWidth >= 20):
        app.pageWidth -= 10
        linesPerPageLabel.value = "Characters per line: %d" %app.pageWidth
    else:
        if(app.pageWidth == "Infinite"):
            app.pageWidth = 50
            linesPerPageLabel.value = "Characters per line: %d" %app.pageWidth
        else: 
            decrease_width_max()

def increase_width():
    '''
    Takes no args and returns no values
    If the game is in screensaver mode, then this will increase the speed of autoclicks by 1 per minute
    Only take action if speed is not already max
    '''
    if app.pageWidth != "Infinite":
        app.pageWidth+=1
        linesPerPageLabel.value = "Characters per line: %d" %app.pageWidth
        if(app.pageWidth >60):
            app.pageWidth = "Infinite"
            linesPerPageLabel.value = "Characters per line: %s" %app.pageWidth

def decrease_width():
    '''
    Takes no args and returns no values
    If the game is in screensaver mode, then this will decrease the speed of autoclicks by 1 per minute
    Only take action is speed is not already minimum
    '''
    if(app.pageWidth == "Infinite"):
        app.pageWidth = 60
        linesPerPageLabel.value = "Characters per line %d" % app.pageWidth
    else:
        if app.pageWidth>10:
            app.pageWidth-=1
            linesPerPageLabel.value = "Characters per line %d" % app.pageWidth
          
            
def check_width(x,y):
    '''
    Takes 2 positional arguments, x and y
    Returns no values
    Checks if any speed related button contains those coordinates
    Calls speed alteration functions as needed
    '''
    if(linesDecreaseButton.contains(x, y)):
        decrease_width()
    if(linesIncreaseButton.contains(x, y)):
        increase_width()
    if(linesDecrease10Button.contains(x, y)):
        decrease_width_10()
    if(linesIncrease10Button.contains(x, y)):
        increase_width_10()
    if(linesDecreaseMaxButton.contains(x, y)):
        decrease_width_max()
    if(linesIncreaseMaxButton.contains(x, y)):
        increase_width_max()

def onKeyPress(key):
    '''
    Built in CMU function taking the label of the key pressed as argument
    Used to play/pause while in auto mode or move forward and backwards through the braille cells manually
    '''
    if(app.mode!='typing'):
        if(key=="space" or key =="p" or key == "P"):
            onMousePress(play_pause_button.centerX, play_pause_button.centerY)
        if(key == "m" or key == "M"):
            onMousePress(auto_manual_button.centerX, auto_manual_button.centerY)
        if(key == "+"):
            onMousePress(increase_cpm_button.centerX, increase_cpm_button.centerY)
        if(key == "-" or key == "_"):
            onMousePress(decrease_cpm_button.centerX, decrease_cpm_button.centerY)
        if(key == "1"):
            onMousePress(linesDecreaseMaxButton.centerX, linesDecreaseMaxButton.centerY)
        if(key == "2"):
            onMousePress(linesDecrease10Button.centerX, linesDecrease10Button.centerY)
        if(key == "3"):
            onMousePress(linesDecreaseButton.centerX, linesDecreaseButton.centerY)
        if(key == "4"):
            onMousePress(linesIncreaseButton.centerX, linesIncreaseButton.centerY)
        if(key == "5"):
            onMousePress(linesIncrease10Button.centerX, linesIncrease10Button.centerY)
        if(key == "6"):
            onMousePress(linesIncreaseMaxButton.centerX, linesIncreaseMaxButton.centerY)
        if(key == "f" or key == 'F'):
            onMousePress(file_input_button.centerX, file_input_button.centerY)
        if(key == "t" or key == "T"):
            onMousePress(typing_input_button.centerX, typing_input_button.centerY)
        if(key == "x" or key == "X"):
            onMousePress(escape_button.centerX, escape_button.centerY)
    if(len(app.sequence)>0):
        if(key == 'left'):
            app.time_delay = app.selected_delay
            if(app.wideIndex>0):
                if(app.pageWidth!="Infinite"):
                    if(app.cellsSinceLastNewLine == 0):
                        a = None
                        try:
                            a = app.reasons.pop()
                        except IndexError as e:
                            a = None
                        if(a != "Hyphen"):
                            if(app.wideIndex<len(app.sequence)):  
                                app.specialFinalIndex = app.cellsSinceLastNewLine                          
                                display(app.sequence[app.wideIndex])
                                show_print(app.matches[app.wideIndex], key)
                                app.currSpec = 'letter'
                            else:
                                display([])
                                show_print("", key)
                            try:
                                app.cellsSinceLastNewLine = app.storedCellsSince.pop()
                            except:
                                app.cellsSinceLastNewLine = app.pageWidth
                        else:
                            if(app.wideIndex<len(app.sequence)): 
                                app.specialFinalIndex = app.cellsSinceLastNewLine                           
                                display([3,6])
                                show_print("-", key)
                                app.currSpec = 'hyphen'
                                app.cellsSinceLastNewLine = app.pageWidth
                                app.indexSaverL.append(app.wideIndex)
                                app.indexSaverR.append(app.wideIndex+1)
                            else:
                                display([])
                                show_print("", key)
                                app.currSpec = None
                            try: 
                                app.storedCellsSince.pop()
                            except:
                                None
                    else:
                        if(app.wideIndex<len(app.sequence)):
                            app.specialFinalIndex = app.cellsSinceLastNewLine
                            if(app.cellsSinceLastNewLine>1):
                                app.wideIndex-=1
                                app.cellsSinceLastNewLine -=1
                                display(app.sequence[app.wideIndex])
                                show_print(app.matches[app.wideIndex], key)
                                app.currSpec = 'letter'
                            else:
                                a = None
                                try:
                                   a = app.reasons.pop()
                                except IndexError as e:
                                    a = None 
                                if(a == "Hyphen"):
                                    display([3,6])
                                    show_print("-", key)
                                    app.currSpec = 'hyphen'
                                    app.cellsSinceLastNewLine = app.pageWidth
                                    app.indexSaverL.append(app.wideIndex-1)
                                    app.indexSaverR.append(app.wideIndex)
                                else:
                                    app.wideIndex -=1
                                    display(app.sequence[app.wideIndex])
                                    show_print(app.matches[app.wideIndex], key)
                                    try:
                                        app.cellsSinceLastNewLine = app.storedCellsSince.pop()
                                    except:
                                        app.cellsSinceLastNewLine = app.pageWidth
                                    app.currSpec = 'letter'
                        else:
                            app.wideIndex-=1
                            display(app.sequence[app.wideIndex])
                            show_print(app.matches[app.wideIndex], key)
                            app.currSpec = 'letter'
                else:
                    app.wideIndex -=1
                    display(app.sequence[app.wideIndex])
                    show_print(app.matches[app.wideIndex], key)
                    app.currSpec = 'letter'
            else:
                app.wideIndex = -1
                app.cellsSinceLastNewLine = 0
                display([])
                show_print("", key)
                app.currSpec = None
        if(key =='right'):
            if(app.pageWidth!= "Infinite"):
                if(app.cellsSinceLastNewLine>=app.pageWidth and app.cellsSinceLastNewLine != 0 and app.wideIndex<len(app.sequence)-1):
                    app.specialFinalIndex = app.cellsSinceLastNewLine
                    display([])
                    show_print("\n", key)
                    app.cellsSinceLastNewLine = 0
                    if(app.currSpec != "hyphen"):
                        app.reasons.append("End")
                        app.storedCellsSince.append(app.cellsSinceLastNewLine)
                    else:
                        app.reasons.append("Hyphen")
                        app.storedCellsSince.append(app.cellsSinceLastNewLine)
                        app.wideIndex = app.indexSaverR.pop()-1 
                elif(app.pageWidth!= "Infinite" and app.cellsSinceLastNewLine == app.pageWidth-1 and app.wideIndex<len(app.sequence)-2 and app.cellsSinceLastNewLine!=0 and not(app.sequence[app.wideIndex+1] == ['space'] or app.sequence[app.wideIndex+1] ==["NewLine"])):
                    app.specialFinalIndex = app.cellsSinceLastNewLine
                    display([3,6])
                    show_print("-", 'right')
                    app.currSpec = 'hyphen'
                    app.cellsSinceLastNewLine+=1
                    app.indexSaverL.append(app.wideIndex)
                    app.indexSaverR.append(app.wideIndex+1)
                else:
                    app.currSpec = 'letter'
                    app.time_delay = app.selected_delay
                    if(app.wideIndex<len(app.sequence)-1):
                        app.wideIndex +=1
                        app.cellsSinceLastNewLine +=1
                        display(app.sequence[app.wideIndex])
                        show_print(app.matches[app.wideIndex], key)
                    else:
                        app.wideIndex = len(app.sequence)
                        display([])
                        show_print("", key)
            else:
                app.time_delay = app.selected_delay
                if(app.wideIndex<len(app.sequence)-1):
                    app.specialFinalIndex = app.cellsSinceLastNewLine
                    app.wideIndex +=1
                    app.cellsSinceLastNewLine +=1
                    display(app.sequence[app.wideIndex])
                    show_print(app.matches[app.wideIndex], key)
                else:
                    app.wideIndex = len(app.sequence)
                    display([])
                    show_print("", key)
    else:
        display([])
        show_print("", key)

def onMousePress(x,y):
    '''
    Built in CMU function
    Takes the coordinates of the mouse press as argument
    Used in this program to select settings, and choose text input methods
    '''
    if(app.mode!="checking"):
        check_width(x,y)
        if(typing_input_button.contains(x,y)):
            display([])
            show_print("", None)
            app.mode = 'typing'
            app.tokens.clear()
            app.matches.clear()
            app.sequence.clear()
            app.wideIndex = -1
            text = app.getTextInput("Enter your text for braille conversion")
            app.tokens+=tokenize(text)
            match_keys(app.tokens, legal_tokens)
            paired_expansion(app.sequence, app.matches)
            app.mode = 'auto' if auto_manual_label.value == "Auto Mode (M)" else "manual"
            app.tokens.clear()    
        if(file_input_button.contains(x,y)):
            display([])
            show_print("", None)
            from_device()
            paired_expansion(app.sequence, app.matches)
            app.mode = 'auto' if app.displayMode == "Auto" else "manual"
            app.wideIndex = -1
            app.tokens.clear()
        if(play_pause_button.contains(x,y)):
            if(play_pause_label.value == "Running (P)"):
                play_pause_label.value = "Paused (P)"
                play_pause_button.border = 'black'
                app.playing = False
            else:
                if(app.mode == "auto"):
                    play_pause_label.value = "Running (P)"
                    play_pause_button.border = 'lime'
                    app.playing = True
        if(auto_manual_button.contains(x,y)):
            if(auto_manual_label.value == "Manual Mode (M)"):
                auto_manual_label.value = "Auto Mode (M)"
                auto_manual_button.border = 'lime'
                app.displayMode = "Auto"
                if(app.mode == 'manual'):
                    app.mode = 'auto'
            else:
                auto_manual_label.value = "Manual Mode (M)"
                auto_manual_button.border = 'black'
                app.displayMode = "Manual"
                app.playing = False
                play_pause_label.value = "Paused (P)"
                if(app.mode == "auto"):
                    app.mode = 'manual'
        if(increase_cpm_button.contains(x,y)):
            if(app.cpm<120):
                app.cpm+=1
                app.selected_delay = (int)(app.stepsPerSecond*60/app.cpm)
                cpm_label.value = ("%d cells per minute (Auto Mode)") %app.cpm
        if(decrease_cpm_button.contains(x,y)):
            if(app.cpm>10):
                app.cpm-=1
                app.selected_delay = (int)(app.stepsPerSecond*60/app.cpm)
                cpm_label.value = ("%d cells per minute (Auto Mode)") %app.cpm
    else:
        if(app.updateButton.contains(x,y)):
            download_and_update()
        if(app.noUpdateButton.contains(x,y)):
            updateGUI.clear()
            app.mode = 'selecting'
    if(escape_button.contains(x,y)):
        sys.exit(0)


github_version_file = "https://raw.githubusercontent.com/Jtrout5/Braille-Guide-Project/main/version.txt"
repo_zip = "https://github.com/Jtrout5/Braille-Guide-Project/archive/refs/heads/main.zip"
local_version_file = "version.txt"
temp_dir = "_temp_update_dir"

def get_local_version():
    '''
    Takes no args, will return the current program version, 0.0.0 if not found
    '''
    if not os.path.exists(local_version_file):
        return "0.0.0"
    with open(local_version_file, "r") as f:
        return f.read().strip()

def get_remote_version():
    '''
    Takes no args, returns remote version, None if not found
    '''
    try:
        r = requests.get(github_version_file, timeout=5)
        return r.text.strip()
    except:
        return None

def is_newer(remote, local):
    '''
    Takes 2 args, remote and local which are both version labels
    Return True if the remote repo has a newer version
    False otherwise
    '''
    def parse(v):
        return tuple(map(int, v.split(".")))
    return parse(remote) > parse(local)

def download_and_update():
    '''
    Takes no args and returns no values
    Creates updater script, runs it, and sets everything up for deletion and replacement.
    '''
    r = requests.get(repo_zip)
    if r.status_code != 200:
        raise Exception("Failed to download update")

    z = zipfile.ZipFile(BytesIO(r.content))

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    z.extractall(temp_dir)

    extracted_root = None
    for name in os.listdir(temp_dir):
        path = os.path.join(temp_dir, name)
        if os.path.isdir(path):
            extracted_root = path
            break

    if not extracted_root or not os.listdir(extracted_root):
        raise Exception("Extraction failed or empty update")

    updater_script = "run_update.py"

    with open(updater_script, "w") as f:
        f.write(f"""
import os
import shutil
import time
import subprocess
import sys

file_path = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(file_path)
os.chdir(PROJECT_ROOT)

TEMP_DIR = "_temp_update_dir"
EXTRACTED = "_temp_update_dir/Braille-Guide-Project-main"
DISPLAYER = "displayer.py"
BACKUP_DIR = PROJECT_ROOT + "_backup"

if not os.path.exists(os.path.join(PROJECT_ROOT, DISPLAYER)):
    print("Safety check failed: displayer.py not found")
    sys.exit(1)

if len(PROJECT_ROOT) < 10 or PROJECT_ROOT in [os.path.expanduser("~"), "C:\\\\", "C:\\\\Users"]:
    print("Refusing to operate on unsafe directory:", PROJECT_ROOT)
    sys.exit(1)

if not os.path.exists(EXTRACTED) or not os.listdir(EXTRACTED):
    print("Extracted update is invalid")
    sys.exit(1)

time.sleep(1)

try:
    if os.path.exists(BACKUP_DIR):
        shutil.rmtree(BACKUP_DIR)
    shutil.copytree(PROJECT_ROOT, BACKUP_DIR, dirs_exist_ok=True)
    
    for item in os.listdir(EXTRACTED):
        src = os.path.join(EXTRACTED, item)
        dst = os.path.join(PROJECT_ROOT, item)

        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    shutil.rmtree(TEMP_DIR)
    
    subprocess.Popen([sys.executable, os.path.join(PROJECT_ROOT, DISPLAYER)])

    shutil.rmtree(BACKUP_DIR)

except Exception as e:
    print("Update failed, restoring backup:", e)

    if os.path.exists(BACKUP_DIR):
        for item in os.listdir(PROJECT_ROOT):
            if item in[ "run_update.py", "_temp_update_dir"]:
                continue
            path = os.path.join(PROJECT_ROOT, item)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

        for item in os.listdir(BACKUP_DIR):
            src = os.path.join(BACKUP_DIR, item)
            dst = os.path.join(PROJECT_ROOT, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

        shutil.rmtree(BACKUP_DIR)

    sys.exit(1)

os.remove("run_update.py")
""")

    subprocess.Popen([sys.executable, updater_script])
    exit()

def check_for_updates():
    '''
    Takes no args and returns no values
    Should run at each launcher to check if there is a new release or patch
    '''
    app.mode = 'checking'
    local = get_local_version()
    remote = get_remote_version()


    if remote is None:
        app.mode = 'selecting'

    if is_newer(remote, local):
        box = Rect(width/4, height/3, width/2, height/3, fill='white', border = 'cyan')
        question = Label("A newer version is available, do you wish to update?", box.centerX, box.top + box.height/3, align = 'top', size = width/60)
        app.updateButton = Rect(box.left, box.bottom, box.width/2, box.height/2, fill='green', align = 'bottom-left')
        app.noUpdateButton = Rect(box.right, box.bottom, box.width/2, box.height/2, fill='red', align = 'bottom-right')
        ans1 = Label("Yes", app.updateButton.centerX, app.updateButton.centerY, fill = 'white')
        ans2 = Label("No", app.noUpdateButton.centerX, app.noUpdateButton.centerY, fill='white')
        updateGUI.add(box, question, app.updateButton, app.noUpdateButton, ans1, ans2)
        return 
    else:
        app.mode = 'selecting'
        return

check_for_updates()
updateGUI.toFront()
warnings.filterwarnings("ignore", category=RuntimeWarning)
app.run()
