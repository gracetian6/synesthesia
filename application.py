# CS50 Final Project / Main functions of the web page

from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from helpers import update, front_required, insert_after, extract_notes
from chordsheet import notestrings, chordsheet, scale, convert, chordname, replace_after

# Configure application
app = Flask(__name__)

# Smallest size of valid lilypond file
MIN_LY_SIZE = 12


# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET"])
def get_index():
    """Return index.html template"""

    session.clear()
    return render_template("index.html")


@app.route("/", methods=["POST"])
def post_index():
    """Set up initial values of the sheet music (title, composer, clef, key, time, tempo)"""

    # Check all the fields in the form have been filled
    if not request.form.get("title"):
            return render_template("error.html", message="Missing title")

    if not request.form.get("composer"):
            return render_template("error.html", message="Missing composer")

    if not request.form.get("time"):
            return render_template("error.html", message="Missing time signature")

    if not request.form.get("notekey"):
            return render_template("error.html", message="Missing key signature")

    if not request.form.get("tonkey"):
            return render_template("error.html", message="Missing tonality")

    if not request.form.get("tempo"):
            return render_template("error.html", message="Missing tempo")

    # Write the form's values to trying.ly (Lilypond file)
    with open("trying.ly", "w") as file:
        file.write('\\version "2.18.2"' + '\n')
        file.write('\header {\n')
        file.write('title = "' + request.form.get("title") + '"\n')
        file.write('composer = "' + request.form.get("composer") + '"\n')
        file.write('}')
        file.write('\score {\n')
        file.write('\\new Staff {\n')
        file.write('\clef ' + "treble" + '\n')
        file.write('\key ' + request.form.get("notekey") + request.form.get("tonkey") + '\n')
        file.write('\\time ' + request.form.get("time") + '\n')
        file.write('\\tempo "' + request.form.get("tempo") + '" ')
        if request.form.get("time")=="2/4" or request.form.get("time")=="3/4" or request.form.get("time")=="4/4":
            file.write('4 = ')
            # Conversion: tempo for dotted is 2/3 times tempo for not dotted
            if request.form.get("tempo")=="Lento":
                file.write('54 \n')
            if request.form.get("tempo")=="Andante":
                file.write('60 \n')
            if request.form.get("tempo")=="Moderato":
                file.write('80 \n')
            if request.form.get("tempo")=="Allegro":
                file.write('116 \n')
            if request.form.get("tempo")=="Presto":
                file.write('160 \n')
        if request.form.get("time")=="6/8" or request.form.get("time")=="9/8" or request.form.get("time")=="12/8":
            file.write('4. =')
            if request.form.get("tempo")=="Lento":
                file.write('36 \n')
            if request.form.get("tempo")=="Andante":
                file.write('40 \n')
            if request.form.get("tempo")=="Moderato":
                file.write('54 \n')
            if request.form.get("tempo")=="Allegro":
                file.write('76 \n')
            if request.form.get("tempo")=="Presto":
                file.write('108 \n')

        file.write('\\bar "' + '|."\n')
        file.write('}}\n')

    # Create PDF by compiling trying.ly
    update("trying", "static/piano_score.pdf", "pdf")

    session['front_submitted'] = True

    # Direct user to the keyboard page to start composing
    return redirect("/home")


@app.route("/home", methods=["GET"])
@front_required
def get_home():
    """Return home.html template"""

    return render_template("home.html")


@app.route("/home", methods=["POST"])
def post_home():
    """Write notes and other musical aspects (duration, dynamics, articulation, rest) to the lilypond file"""

    # Successfully retrieves all the musical information from keyboard and radio buttons in home.html
    note = request.form.get("note")
    octave = request.form.get("octave")
    alternation = request.form.get("alternation")
    duration = request.form.get("duration")
    rest = request.form.get("rest")
    dot = request.form.get("dot")
    dyn = request.form.get("dyn")
    articulation = request.form.get("articulation")

    # Copy notes to trying.ly (Lilypond file)
    file_ly = open("trying.ly", "r")
    contents = file_ly.readlines()
    file_ly.close()

    # Deleting the last two brackets so that the file compiles
    contents.pop(len(contents)-1)
    contents.pop(len(contents)-1)
    contents = "".join(contents)

    if not rest:
        # Converting note from abc notation to Lilypond format
        octave = "'" * (int(octave) - 2)
        if alternation == "#":
            alternation = "is"
        elif alternation == "b":
            alternation = "es"

    # Write the note information in the Lilypond file
    with open("trying.ly","w") as file:
        file.write(contents)
        if not rest:
            if note:
                file.write(note)
            if alternation:
                file.write(alternation)
            if octave:
                file.write(octave)
            if duration:
                file.write(duration)
            if dot:
                file.write(dot)
            if dyn:
                file.write(dyn)
            if articulation:
                file.write(articulation)
        else:
            file.write(rest)
            file.write(duration)

        file.write("\n")
        file.write('\\bar "' + '|."\n')
        file.write("}}")

    # Update the music sheet PDF
    update("trying", "static/piano_score.pdf", "pdf")

    return jsonify(True)


@app.route("/undo", methods=["POST"])
def undo():
    """Delete's the last note of the .ly file"""

    # Copy notes of file
    f_ly = open("trying.ly", "r")
    contents_ly = f_ly.readlines()
    f_ly.close()

    if len(contents_ly) <= MIN_LY_SIZE:
        return jsonify(False)

    # Remove last note in the second to last line
    contents_ly.pop(len(contents_ly)-3)
    contents_ly = "".join(contents_ly)

    with open("trying.ly","w") as file:
        file.write(contents_ly)

    # Update sheet music PDF
    update("trying", "static/piano_score.pdf", "pdf")

    return jsonify(True)


@app.route("/midi", methods=["POST"])
def midi():
    """Create MIDI from Lilypond file so that it can be played in home.html"""

    # Insert the necessary feature for the Lilypond to create a MIDI file
    resp = insert_after('\\midi {\n}\n', '}\\score {\n', "trying.ly", "midi.ly")
    if resp == 0:
        return jsonify(False)

    # Update audio
    update("midi", "static/music.midi", "midi")

    return jsonify(True)


@app.route("/midi2", methods=["POST"])
def midi2():
    """Create MIDI from Lilypond file so that it can be played in chordsheet.html"""

    # Insert the necessary feature for the Lilypond to create a MIDI file
    resp = insert_after('\\midi {\n}\n', '}\\score {\n', "chords.ly", "midi2.ly")
    if resp == 0:
        return jsonify(False)

    # Create MIDI file
    update("midi2", "static/chords.midi", "midi")


    return jsonify(True)


@app.route("/credits", methods=["GET"])
def credits():
    """Return credits.html template"""

    return render_template("credits.html")


@app.route("/chords", methods=["GET"])
@front_required
def get_chords():

    """Write our harmonization for the melody"""

    # Ensures that user has added one note
    f = open("trying.ly", "r")
    contents = f.readlines()
    f.close()

    if len(contents) <= MIN_LY_SIZE:
        return redirect("/home")

    # Extract key signature, notes
    tried = extract_notes("trying.ly")
    key = tried[0]
    tried.pop(0)
    notes = tried

    # Save melody in harmony-friendly format
    notestr = notestrings(notes)

    # Find chords
    prog = chordsheet(notes, key)

    # Insert into new Lilypond file
    replacement = ["\\relative \n", notestr[0] + " \n", "{ \n", notestr[1],
                   '} \n\\bar "|." \n} \n<< \n\\new Staff { \n \clef bass \n', "\key " + key + "\n", prog[0], "} \n", prog[1],
                   '>> \n>> \n} \n']
    replace_after(10, replacement, "chords.ly")
    insert_after("<< \n", "}\\score {\n", "chords.ly", "chords.ly")

    # Render PDF
    update("chords", "static/piano_chords.pdf", "pdf")
    return render_template("chordsheet.html")

