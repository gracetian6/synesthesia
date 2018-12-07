# Documentation for Synesthesia

## A User's Manual

### for CS50 final project, fall 2018

#### by Christine Cai, Sílvia Casacuberta and Grace Tian

***

#### Start creating the file (index page)
When the web app is first launched, the user will be directed to the index page, in which the user will provide the
basic information for his or her musical composition: title, composer, time signature, key signature, tonality, and
tempo. All these items are required in order to start creating the pdf that will later display the music that the
user composes. The user must fill out the title and the name of the composer, whereas the time signature,
the key signature, the tonality and the tempo are selected from the options of a dropdown menu. Once all this
information has been provided, the user will click "Start creating music!" and he or she will be redirected to the
home page, which is the main page from which the user is able to compose music.

#### Composing the music (home page)
When the home page is first launched, the user will see three main features: a tab with all the musical elements
that can be included in the composition, a virtual keyboard with three octaves (starting at C3), and a pdf file that
for now only contains the information that was provided in the index page. At the top of the page the user can also
find buttons that will redirect him or her to the other pages of the web app: "compose" (which is the home page),
"chord sheet" (a page that will provide chord suggestions for the music that the user has written), "restart" (which
allows the user to start the composition from scratch), and "credits" (which contains information about the creators
of the web app as well as information about the packages that have been used for the code).

Below these buttons the user will find a box with all the features that can be used in the composition. The bar is
divided into an upper part and a lower part. The upper part contains three features that can be found to the left:
a play button which will play the music composed by the user so far (which is written in the pdf below), a stop
button which will stop the music while it is being played, a delete button which allows the user to delete
the last note that he or she has pressed in the keyboard in case the user has made a mistake, and a download button
that will allow the user download the MIDI file to his or her computer. The play button will play the music with the
sound of a piano and at the tempo that the user has indicated in the index page. The MIDI file that contains the
music is updated everytime the user writes a new note, and so it will always play the music that is displayed in the
pdf.

The lower part of the box contains all the musical features besides the note in the keyboard that the user may or not
use during his or her composition process: the duration of the note, a rest, a dotted note, dynamic markings, and
articulation marks. The only feature that is required is the duration of the note. By default, if the user does not
press any button regarding the duration of the note, the program will assume that it is a quarter note. The possible
rhythms that the user can use are: whole note, half note, quarter note, eighth note, sixteenth note and thirty-second
note. If the user wishes to use a dotted rythm, he or she will have to press the dotted note in the box. The program
will then dot the rythm that has been provided. For example, if the user presses the half note and the dotted rythm,
the pdf will display a dotted half note.

The user can also add complementary features to the note: dynamics and articulation. Dynamic marks include pianissimo,
piano, mezzo piano, mezzo forte, forte, and fortissimo. Articulation marks include: staccatto, accent, marcato, and
tenuto. Note that only one dynamic marking and one articulation marking are allowed. Also note that all the features
in the box that the user wishes to use must be pressed before the user presses a note in the keyboard. Pressing
the keyboard is the last action that the user should perform, because when any key is used the note will appear in the
pdf file with all the information that has been requested. For example, if the user wishes to write a G3 half dotted
note with a forte, he or she will press the half note rhythm button, the dotted note button, the forte button (
in any order), and then the G3 note in the keyboard.

Finally, the user can also write rests. The duration of the rest is indicated by using the rhythm buttons that are
also used for the notes. When the user wishes to use the rest, he or she should not press the keyboard. When the rest
button is pressed, the form is sent to the server and so the rest will be displayed in the pdf file. This means that
the duration of the rest must be selected before pressing the rest button. So for example, if the user wishes to
write a rest with the duration of an eight note, he or she will first press the eight note rhythm symbol and then the
rest. In relation to the bars, the PDF will automatically write a bar symbol according to the time signature that
has been provided. However, note that if the user writes a rhythm that is too long for the bar, the rhythm will be
written in the same bar. This does not raise problems in the pdf file or in the MIDI file but is musically incorrect,
so the user should be cautious when writing the rhythms.

The keyboard in the home page is interactive and is what the user will employ to indicate which note he or she wishes
to use. Once clicked, the note will be included in the pdf below. The third main feature in the page is, as indicated,
the pdf that contains the music that the user is writing. The PDF is automatically updated (along with the MIDI file)
every time the user clicks a note in the keyboard. As previously indicated, the pdf also includes bars and bar numbers.
The PDF file will be named with the title of the piece, and the user can download or print the file whenever he or she
wishes to do so.

#### Obtaining a chord sheet suggestion for the music that has been composed (chord sheet page)
Every time the user accesses the chord sheet page while composing, the chord sheet page will display a box similar
to the home page containing the features related to the MIDI file (play, stop, and download the MIDI file) and a PDF.
The PDF will contain a first part that is already familiar to the user because it is similar to the PDF from the
home page: title, composer, time signature, key signature, tonality, tempo (as provided in the index page) and the
notes (or octaves of the notes) that the user has written so far with the keyboard. But the user will find a new stave
containing chords (written both in the stave and labeled with chord names below the stave) that harmonize the melody the user
has written. With the chord sheet page, the site automatically generates a harmonic chord progression that fits the user's melody
and automatically enriches the piece. Our method of harmonization follows the main rules
of music theory chord harmonization patterns. The user is also able to play, stop, and download a MIDI file that plays
both his or her original music together with the chord harmonization that Synesthesia provides. Also, similar to the home
page, the user can download or print the PDF file with the harmonization that we provide. The user can go
back and forth between the home page and the chord sheet page.

Note: because the harmonies are built off of the standard I-IV-V-I progression, it is dependent on the key signature the user
selects and does yet not take into account melodies that are chromatic, atonal, or based in non-standard-scales. Also, the
automatically-generated chord progression is only one harmonization out of many. It is not intended to be a polished final
product, but a jumping-off point that can be helpful for those learning composition or music theory.

#### Start again a new file (restart button)
If the user presses the "restart" button at the navigation bar of the webpage, he or she will be prompted the index
page again, from which he or she will be able to start another composition from scratch. Be aware that all previous
information will be lost.

#### Access information about the developers of the web app and about the packages that this web app uses (credits button)
If the user presses the "credits" button at the navigation bar of the webpage, he or she will be prompted another
html page that contains basic information about the creators of this web app (brief biography and pictures) and
links to the packages that have been used to code the web app (Lilypond, Python, Flask, JQuery).
