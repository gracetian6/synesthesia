# CS50 Final Project / Repetitive functions

import requests
import subprocess

from flask import redirect, render_template, session
from functools import wraps

# Defines constant values
# Index where key signature appears in lilypond files
KEY_SIG_INDEX = 7
# Smallest size of valid lilypond file
MIN_LY_SIZE = 12
# Index where notes appear
FIRST_NOTE_INDEX = 10

def update(lilypond_name, output_file, file_type):
    """Updates the sheet music pdf and audio file in the server"""

    try:
        # Update sheet music pdf
        subprocess.check_output('lilypond '+lilypond_name+'.ly', shell=True)
        subprocess.check_output('mv '+lilypond_name+'.' + file_type + " " + output_file, shell=True)
    # Restarts if there is an error
    except subprocess.CalledProcessError as e:
        print(e)
        return redirect("/")


def front_required(f):
    """
    Decorate routes to require front page is submitted.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("front_submitted") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


def insert_after(txt, line, input_file, output_file):
    """ Inserts txt after line in input_file and outputs as output_file """
    # Read all text in input file as a list where each line is an entry
    with open(input_file, "r") as file:
        contents = file.readlines()

    # Find index of <line> inside the list
    try:
        ind = contents.index(line)
    # If line cannot be found in list, exit out
    except:
        return 0

    # Inserts text after <line>
    contents.insert(ind + 1, txt)

    # Combines everything in the list and writes everything to output_file
    contents = "".join(contents)
    with open(output_file, "w") as file:
        file.write(contents)

    return 1


def extract_notes(input_file):
    """Extract notes from a lilypond input_file"""

    # List that contains key signature and
    notes = []

    # Read through input_file and copy all the contents as a list
    f = open(input_file, "r")
    contents = f.readlines()
    f.close()

    # Ensure that there are notes to extract
    if len(contents) < MIN_LY_SIZE:
        return 0

    # Gets the key signature
    key = contents[KEY_SIG_INDEX]
    key = key[len("\\key "):len(key)]
    notes.append(key.strip("\n"))

    # Gets the notes in the list
    for i in range(FIRST_NOTE_INDEX, len(contents)-2):
        notes.append(contents[i].strip("\n"))

    # Sort out dynamics, adlibs
    for i in range(1, len(notes)):
        note = notes[i]
        while note.find("\\") > 0:
            note = note[:note.find("\\")]
        notes[i] = note

    return(notes)