# CS50 Final Project / Create harmonization for the melody of the user

import sys


# Functions for making Lilypond chord sheet file


# Generates list: [first note, notestring], where notestring = melody notes for ly file
def notestrings(notes):
    # Find first non-rest note
    n = 0
    while notes[n][0] == "r":
        n += 1
    firstnote = notes[n][:notes[n].rfind("'")+1]
    firstnote = firstnote[:len(firstnote)-1]
    notestring = ""

    # Iterates over notes, makes higher octave ("'") into lower octave (",")
    for i in range(len(notes)):
        editnote = notes[i].replace("'", "")
        notestring += (editnote + " \n")

    return [firstnote, notestring]


# Generates lines to insert for chordsheet
def chordsheet(notes, keysig):
    # Key signature information
    keysig = keysig
    tonality = keysig.find("major")
    key = keysig[0]
    keyscale = scale(key, tonality)

    # Notes extracted from file, cleaned
    notes = notes

    # Flags indicate distance along standard I-IV-V-I chord progression
    flag_I = False
    flag_IV = False

    # Beginning for chord text
    prog1 = "\chordmode { "

    # Beginning for bass chords
    prog2 = "\chords { "

    # Iterates over notes
    for note in notes:
        # Gets scale degree and sharp
        converted = convert(note, keyscale)
        sdeg = converted[0]
        sharp = converted[1]
        rhythm = note[note.rfind("'")+1:]

        # Rests
        if sdeg == -1:
            label = "r" + note[len(note)-1]
        else:
            # Major
            if tonality > 0:
                # Before I chord
                if flag_I == False and flag_IV == False:
                    if sharp == False:
                        # Places I chord, turns on I chord flag
                        if sdeg == 1 or sdeg == 3 or sdeg == 5:
                            chord = [1, False, "5"]
                            flag_I = True
                        elif sdeg == 2 or sdeg == 4:
                            chord = [2, False, "m"]
                        elif sdeg == 6:
                            chord = [6, False, "m"]
                        elif sdeg == 7:
                            chord = [5, False, "5"]
                    else:
                        if sdeg == 1:
                            chord = [6, False, "5"]
                        if sdeg == 2 or sdeg == 6:
                            chord = [6, True, "5"]
                        if sdeg == 4:
                            chord = [2, False, "5"]
                        if sdeg == 5:
                            chord = [3, False, "5"]

                # After IV chord, before V
                elif flag_IV == True:
                    if sharp == False:
                        # Places V chord, turns off flags
                        if sdeg == 5 or sdeg == 7 or sdeg == 2 or sdeg == 4:
                            chord = [5, False, "7"]
                            flag_I = False
                            flag_IV = False
                        elif sdeg == 6:
                            chord = [2, False, "m"]
                        elif sdeg == 1:
                            chord = [6, False, "m"]
                        elif sdeg == 3:
                            chord = [3, False, "m"]
                    else:
                        if sdeg == 1:
                            chord = [6, False, "5"]
                        if sdeg == 2 or sdeg == 6:
                            chord = [6, True, "5"]
                        if sdeg == 4:
                            chord = [2, False, "5"]
                        if sdeg == 5:
                            chord = [3, False, "5"]

                # After I chord, before IV
                elif flag_I == True:
                    if sharp == False:
                        # Places IV chord, turns on IV flag
                        if sdeg == 4 or sdeg == 6 or sdeg == 1:
                            chord = [4, False, "5"]
                            flag_IV = True
                        elif sdeg == 2:
                            chord = [2, False, "m"]
                        elif sdeg == 5 or sdeg == 7:
                            chord = [3, False, "m"]
                        elif sdeg == 3:
                            chord = [6, False, "m"]
                    else:
                        if sdeg == 1:
                            chord = [6, False, "5"]
                        if sdeg == 2 or sdeg == 6:
                            chord = [6, True, "5"]
                        if sdeg == 4:
                            chord = [2, False, "5"]
                        if sdeg == 5:
                            chord = [3, False, "5"]

            # Minor
            else:
                # Before i chord
                if flag_I == False and flag_IV == False:
                    if sharp == False:
                        # Places i chord, turns on i flag
                        if sdeg == 1 or sdeg == 3 or sdeg == 5:
                            chord = [1, False, "m"]
                            flag_I = True
                        elif sdeg == 2 or sdeg == 4:
                            chord = [5, False, "7"]
                        elif sdeg == 6:
                            chord = [6, False, "5"]
                        elif sdeg == 7:
                            chord = [3, False, "5"]
                    else:
                        if sdeg == 1:
                            chord = [1, True, "5"]
                        elif sdeg == 3:
                            chord = [1, False, "5"]
                        elif sdeg == 4:
                            chord = [5, False, "maj7"]
                        elif sdeg == 6:
                            chord = [4, False, "5"]
                        elif sdeg == 7:
                            chord = [7, False, "dim"]

                # After IV chord, before V
                elif flag_IV == True:
                    if sharp == False:
                        # Places v chord, turns off flags
                        if sdeg == 5 or sdeg == 2:
                            chord = [5, False, ""]
                            flag_I = False
                            flag_IV = False
                        elif sdeg == 4:
                            chord = [5, False, "7"]
                        elif sdeg == 7:
                            chord = [7, False, ""]
                        elif sdeg == 6 or sdeg == 1:
                            chord = [6, False, ""]
                        elif sdeg == 3:
                            chord = [3, False, ""]
                    else:
                        if sdeg == 7:
                            chord = [5, False, ""]
                            flag_I = False
                            flag_IV = False
                        elif sdeg == 4:
                            chord = [5, False, "maj7"]
                            flag_I = False
                            flag_IV = False
                        elif sdeg == 1:
                            chord = [1, True, ""]
                        elif sdeg == 3:
                            chord = [1, False, ""]
                        elif sdeg == 6:
                            chord = [4, False, ""]

                # After I chord, before IV
                elif flag_I == True:
                    if sharp == False:
                        # Places iv chord, turns on iv flag
                        if sdeg == 4 or sdeg == 6 or sdeg == 1:
                            chord = [4, False, "m"]
                            flag_IV = True
                        elif sdeg == 2:
                            chord = [2, False, "dim"]
                        elif sdeg == 5 or sdeg == 7:
                            chord = [3, False, ""]
                        elif sdeg == 3:
                            chord = [6, False, ""]
                    else:
                        if sdeg == 1:
                            chord = [1, True, ""]
                        elif sdeg == 3:
                            chord = [1, False, ""]
                        elif sdeg == 4:
                            chord = [4, True, ""]
                        elif sdeg == 6:
                            chord = [4, False, ""]
                        elif sdeg == 7:
                            chord = [7, True, "dim"]

            # Name of the chord is added to strings
            label = chordname(chord[0], chord[1], chord[2], key, tonality)
            label = label[:label.find(":")] + "," + rhythm + label[label.find(":"):]

        prog1 += (label + " ")
        prog2 += (label + " ")

    prog1 += "} \n"
    prog2 += "} \n"
    return [prog1, prog2]


# Returns scale in a certain key
def scale(key, tonality):
    chrom = ["a", "ais", "b", "c", "cis", "d", "dis", "e", "f", "fis", "g", "gis"]
    scale = []

    # Finds number of half-steps each scale degree is from tonic
    for i in range(1, 8):
        # Major
        if tonality > 0:
            if i >= 1 and i <= 3:
                hfsteps = (i - 1) * 2
            elif i >= 4 and i <= 7:
                hfsteps = (i - 2) * 2 + 1
        # Minor
        else:
            if i >= 1 and i <= 2:
                hfsteps = (i - 1) * 2
            elif i >= 3 and i <= 5:
                hfsteps = (i - 2) * 2 + 1
            elif i >= 6 and i <= 7:
                hfsteps = (i - 2) * 2

        # Finds note in terms of half-steps from tonic
        note = (hfsteps + chrom.index(key)) % 12

        # Adds scale degree to scale
        scale.append(chrom[note])

    # Returns scale in list form
    return scale


# Converts note to format [scale degree, sharp]
def convert(note, scale):
    # Sets rests to -1
    if note[0] == "r":
        return [-1, False]

    # Finds scale degree
    deg = (ord(note[0]) - ord(scale[0]) + 1) % 7
    sdeg = [deg]

    # If note has accidental
    if note.find("is") > 0 or note.find("es") > 0:
        # Cut off the string after "is" or "es"
        note = note[:4]

        # If flat, convert to sharp
        if note.find("es") > 0:
            note = chr(((ord(note[0]) - ord("a") - 1) % 7) + ord("a")) + "is"

    # If note does not have accidental, cut off after first letter
    else:
        note = note[0]

    # If the note doesn't occur in scale (needs sharps)
    if note not in scale:
        # Add sharp
        sdeg.append(True)

        # Adjusting for ones where already sharped in scale
        if scale[deg - 1].find("is") > 0 and scale[deg - 1][0] == note[0]:
            sdeg[0] = (deg - 1) % 7

    # If no accidentals
    else:
        sdeg.append(False)
    return sdeg


# Names chords in Lilypond-friendly format
def chordname(sdeg, sharp, chordtype, key, tonality):
    chrom = ["a", "ais", "b", "c", "cis", "d", "dis", "e", "f", "fis", "g", "gis"]

    # Puts into half-steps (without accidentals)
    # Major
    if tonality > 0:
        if sdeg >= 1 and sdeg <= 3:
            hfsteps = (sdeg - 1) * 2
        elif sdeg >= 4 and sdeg <= 7:
            hfsteps = (sdeg - 2) * 2 + 1

    # Minor
    else:
        if sdeg >= 1 and sdeg <= 2:
            hfsteps = (sdeg - 1) * 2
        elif sdeg >= 3 and sdeg <= 5:
            hfsteps = (sdeg - 2) * 2 + 1
        elif sdeg >= 6 and sdeg <= 7:
            hfsteps = (sdeg - 2) * 2

    # Adds half-steps for sharps
    if sharp:
        hfsteps += 1

    # Full chord name
    chord = (hfsteps + chrom.index(key)) % 12
    label = chrom[chord] + ":" + chordtype
    return label


# Replaces code after a line with new code
def replace_after(ind, replacement, output_file):
    f = open("trying.ly", "r")
    contents = f.readlines()
    f.close()

    if len(contents) <= 12:
        return 0

    # Deletes all the contents after row of ind
    while len(contents) >= ind + 1:
        contents.pop(ind)

    contents.extend(replacement)
    contents = "".join(contents)

    with open(output_file, "w") as file:
        file.write(contents)

    return 1