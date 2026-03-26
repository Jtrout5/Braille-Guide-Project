import json
import os
import shutil
import zipfile
import subprocess
import sys
import re
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
    
selected_delay = 45
app.time_delay = 45
app.index = -1
app.pageWidth = 42
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

def check_existence(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.close()
            subprocess.run([sys.executable, "braille_generator.py"])

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


def tokenize(txt):
    tokens = re.findall(r"[A-Za-z0-9]+|[^\w\s]| ", txt)
    return tokens


def match_keys(text, keys):
    # Precompute categories
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
    leftover_letters = [
        k for k in keys
        if raw[k]["type"] in ("lowercase", "uppercase")
    ]

    app.sequence = [None] * len(text)

    for i, token in enumerate(text):
        if token is None:
            continue
        for key in punctuation:
            if token == key:
                app.sequence[i] = raw[key]["value"]
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
        dp[n] = (0, [], [])

        for pos in range(n - 1, -1, -1):
            best_cells = float("inf")
            best_seq = None
            best_split = None

            next_cells, next_seq, next_split = dp[pos + 1]
            fallback_cells = next_cells + 1
            fallback_seq = [None] + next_seq
            fallback_split = [token[pos]] + next_split

            best_cells = fallback_cells
            best_seq = fallback_seq
            best_split = fallback_split

            for key in groupsigns:
                if lower.startswith(key, pos):
                    end = pos + len(key)
                    next_cells, next_seq, next_split = dp[end]

                    val = raw[key]["value"]
                    cell_count = len(val)

                    total = next_cells + cell_count
                    if total < best_cells:
                        best_cells = total
                        best_seq = [val] + next_seq
                        best_split = [token[pos:end]] + next_split

            dp[pos] = (best_cells, best_seq, best_split)

        _, seq_list, split_list = dp[0]

        if token[0].isupper():
            for idx, seq in enumerate(seq_list):
                if seq is not None:
                    seq_list[idx] = [[6]] + seq
                    break

        text[i:i+1] = split_list
        app.sequence[i:i+1] = seq_list

        i += len(split_list)

    i = 0
    while i < len(text):
        token = text[i]
        seq = app.sequence[i]

        if token is None or seq is not None:
            i += 1
            continue

        new_tokens = []
        new_seq = []

        for ch in token:
            low = ch.lower()
            if low in leftover_letters:
                val = raw[low]["value"]
                if ch.isupper():
                    val = [[6]] + val
                new_tokens.append(ch)
                new_seq.append(val)
            else:
                new_tokens.append(ch)
                new_seq.append(None)

        text[i:i+1] = new_tokens
        app.sequence[i:i+1] = new_seq

        i += len(new_tokens)


def display(tuple_val):
    for button in buttons:
        if button.id in tuple_val:
            button.fill = 'lime'
        else:
            button.fill = 'grey'
            
app.tokens = []
app.matches = []
app.sequence = []

def from_device():
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
        app.sequence = [[None]]*len(app.tokens)
        match_keys(app.tokens,legal_tokens)



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
                for j in range(len(app.tokens[app.index])):
                    display(app.tokens[app.index][j])

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
play_pause_button = Circle(app.width/2, app.width/40, app.width/40, fill='white', border = 'black')
play_pause_label = Label("Paused", play_pause_button.centerX, play_pause_button.centerY)
app.playing = False
auto_manual_button = Circle(app.width/4, app.width/40, app.width/40, fill='white', border = 'black')
auto_manual_label = Label("Manual Mode", auto_manual_button.centerX, auto_manual_button.centerY)
app.displayMode = "Manual"


def onMousePress(x,y):
    if(typing_input_button.contains(x,y)):
        app.mode = 'typing'
        app.tokens.clear()
        app.matches.clear()
        app.sequence.clear()
        text = app.getTextInput("Enter your text for braille conversion")
        app.mode = 'chooseSetting'
        app.tokens+=tokenize(text)
        app.sequence = [[None]]*len(app.tokens)
        match_keys(app.tokens, legal_tokens)
        print(text)
        print(app.sequence)
        app.tokens.clear()
        sys.exit(0) ## JUST DURING TESTING
    if(file_input_button.contains(x,y)):
        from_device()
        app.mode = 'chooseSetting'
        print(app.sequence)
        app.tokens.clear()
        sys.exit(0) ## JUST DURING TESTING
    if(play_pause_button.contains(x,y)):
        if(play_pause_label.value == "Running"):
            play_pause_label.value = "Paused"
            app.playing = False
        else:
            if(app.displayMode == "Auto"):
                play_pause_label.value = "Running"
                app.playing = False
    if(auto_manual_button.contains(x,y)):
        if(auto_manual_label.value == "Manual Mode"):
            auto_manual_label.value = "Auto Mode"
            app.displayMode = "Auto"
        else:
            auto_manual_label.value = "Manual Mode"
            app.displayMode = "Manual"
            app.playing = False
            play_pause_label.value = "Paused"



app.run()