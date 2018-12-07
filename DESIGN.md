# Design Document for Synesthesia

## A Technical Tour

### for CS50 final project, Fall 2018

#### by Christine Cai, Sílvia Casacuberta and Grace Tian

***

In our project we have used five types of documents: Python files (application.py, chordsheet.py and helpers.py),
HTML files (layout.html, layout2.html, index.html, home.html, chordsheet.html, error.html and credits.html),
JavaScript files (home.js chordsheet.js), CSS files (styles.css, styleform.css and stylegradient.cdd) and Lilypond files
(trying.ly, midi.ly, tryingchords.ly and midichords.ly). Inside our web app we create two more types of files:
PDF and MIDI files. For the Lilypond files we use the Lilypond package and documentation.

### Python files
#### application.py
This is the main document of the web app. After some declarations and importations, the first flask route of
application.py is "/", which is related to the index.html file.

##### "/" route
This route displays index.html if the GET method
is used and gets the form from the index.html if the POST method is used. This route first checks that all the fields
in the index.html form have been filled, prompting an error message if any of the items (title, composer, time
signature, key signature, tonality or tempo) is missing. Then we write all this information into the lilypond
file “trying.ly” in the format described in the Lilypond documentation. When writing the time, we convert every
tempo signature into a metronome mark that depends on the time signature. If the time signature is 2/4, 3/4 or 4/4,
then the tempo signature is computed in quarter notes per minute. Otherwise, it is computed in dotted quarter notes
per minute. Even though trying.ly is a Lilypond file, we use the same python I/O functions
(i.e. file.write). At the end we add a final bar symbol and two brackets. These two brackets are necessary
if we want the Lilypond to compile in order to produce the PDF with the music.

We then call the function update(), which is found in helpers.py (we decided to code it there because we use it
throughout the file and so we are avoiding copying and pasting the code in application.py). The update() function
compiles the current Lilypond file trying.ly and then produces a PDF file with all the music that has been
composed. The first time that the user accesses the home page (the page with the keyboard) the PDF will only display
the information that the user has provided in the form (the title and so on). Finally, the user is redirected to the
home page (the keyboard page) to start composing.

##### "/home" route
The following route deals with the keyboard page. The GET method takes the user to home.html. In home.js, we have click
event listeners for when the rest and keyboard buttons are clicked. In those event listeners, we post the form information
to the POST method in the home route. The POST method in home is what
converts the composed music selected on the form into a Lilypond file. In the home page there are many buttons that send information
to the home route, but only the keyboard buttons (each key in the keyboard is a button) and the rest button
will submit the POST form to the home route.  The other options add additional information to the fundamental information,
which is what note the user pressed in the keyboard or if the user has pressed the rest button (so the other buttons
do not submit the form). The way Lilypond files take in the notes is the following: if for example the user wants to
write a dotted C3 note with the value of a half note, with an accent and a piano dynamic, in the Lilypond file we
would write c'2.\piano\accent (one apostrophe indicates the notes from C3 to B flat 3, two apostrophes indicate the
following octave, and so on). So in the keyboard displayed in home.html, each key in the keyboard stores the value
in this format (i.e. c'). The flats are indicated with the ending "es" and the sharps are indicated with the ending
"is" (so for example, c sharp is “cis”). The rhythm is the only other feature besides the note that is not optional, and
so by default we set it to a quarter note (a whole note is a 1, a half note is a 2, and so on).

The home route therefore extracts all this information from all these buttons in the home.html page and concatenates
all the values that it has retrieved in order to create the note in Lilypond format. However, before writing the
we write a note in the Lilypond file, we have to delete the last two brackets and the bar using the pop function (file.write
does not allow us to write in a specific line of the file). We add the bar and the two brackets at the end so that we
can compile the lilypond file. After deleting the last two brackets, the route then opens the trying.ly Lilypond file and
writes the information that the user has provided. Recall that the form can be submitted either by pressing the
keyboard button or the rest button, and so we differentiate between these two cases in the home route. After writing
either the note or a rest in the Lilypond file, we write again the final bar and the two brackets so that the
Lilypond file can be compiled into a PDF. Finally, we call the function update() found in helpers.py so that the
PDF in the server is updated. We return jsonify(True) inside the POST method in home when we are done. The event listeners for
the keyboard button and rest in home.js will receive jsonify(True) once POST in home.js is done and then reupdate the new pdf
containing the very last note that the user has clicked on home.html page.  This way, the PDF file
is dynamically updated every time the user writes into the music sheet (either a note or a rest), and so the user is able to
visualize his or her changes almost instantly.

##### "/undo" route
This route deletes the last note or rest that the user has written into the music sheet. The delete button is found
in home.html as an undo arrow. It is intended to allow the user correct any mistakes that he or she makes. In home.js, we have
a click event listener that posts a request to the undo route on application.py and then waits for a response. The undo route
first reads and copies all text in the trying.ly Lilypond file as a list where each line is an element in the list. We then
determine if there is a note or rest that can be deleted by checking the size of the list. If the size of the list is smaller than
the minimum lilypond size, we return jsonify(False), which will then prompt a javascript error message in home.js
Otherwise, we delete the last entry in the Lilypond file using the pop function. Finally we call the update() function in
helpers.py so that the PDF in the server updates. Then we finally return jsonify(True), and then the undo event listener in
home.js will then update the new pdf on home.html that shows the last note or rest that has been deleted.

##### "/midi" route
This route is intended to produce the Lilypond file midi.ly in order the produce a MIDI file so that the user can listen
to his or her music that has been produced so far. In home.js, we have a click event listener for the play and download button
that posts a request to the midi route on application.py and then waits for a response if the midi file is up to date with
the user’s current music. The midi route is called when the user presses the play or download
button in home.html (and so we only create the MIDI file when the user wishes to do so; not every time he or she
updates the music sheet). Per the Lilypond package documentation, the only difference between a Lilypond file that
produces a PDF file when compiled and a Lilypond file that produces a MIDI file when compiled is the addition of
"\midi {}" in a specific part of the file (after "\score{"). By tracing where "\score{" is in the trying.ly file, we
create a new Lilypond file called midi.ly and we copy all the trying.ly file in it, adding the "\midi {}" so that
when compiled it produces a MIDI file instead of a PDF file. Again, in order to avoid code repetitions, we call the
update() function in helpers.py in order to compile the midi.ly file and obtain a MIDI file. Using a JavaScript
function in home.js, this MIDI file can then be played and stopped in home.html. The user is also able to download
the MIDI file into his or her computer (this is coded in home.js and home.html; not in application.py).

##### "/credits" route
This route renders the template credits.html.

##### "/chords" route
This route generates the chord sheet page. This page is similar to the keyboard page in that it renders a pdf of the
chord sheet (which is generated automatically whenever it redirects) and it has a play/stop/download bar on top, where
it generates and plays a midi file when users press play.
However, it does not have an option to edit the PDF or chord sheet-- it only has options to download the midi or pdf,
but they can be edited by switching back to home.
The way that the chordsheet lilypond file is generated is by using notestrings to convert the original notes into relative
key (see notestrings function for explanation of pros of this) and chordsheet to generate the chord progression and figured bass,
then inserting the outputs of both into a list. The list is then entered into replace_after(), which deletes everything
after the header information (title, composer, tempo) in the original file to input the harmonies while maintaining the header.
The PDF is compiled similarly to on the homepage by using subprocesses.

#### chordsheet.py
This document contains the following functions for creating the chordsheet: notestrings, chordsheet, scale, convert,
and chordname. It also contains the function replace_after for creating the lilypond sheet. The goal is to provide
functions to create a lilypond file with harmonies while maintaining the musical integrity of the original melody line.

##### notestrings function
The first function, notestrings, takes the original sequence of notes and returns a list containing the first note
(without rhythm) and a string of notes without octave notation, which makes it easy to convert into a relative key.
The pros of relative key are that it makes it easier to visually place the melody notes into their vertical/harmonic
context, and it is more compatible with Lilypond's chordmode/chordmode midi conversions.

##### chordsheet function
Chordsheet is the actual algorithm that takes the sequence of notes, converts them into scale degree, and finds an
appropriate and fairly musical chord progression. It tries to maintain harmonic musicality as well as horizontal (melodic)
integrity by making sure that the melody notes are a part of all the chords, then placing all chords into the context
of the basic I-IV-V-I (tonic-predominant-dominant-tonic) chord progression: it uses flags to indicate where along the chord
progression the melody is, and along each step of the chord progression, it will try to resolve dissonant chords by choosing
what chords to best accompany each note by scale degree so that it can sound good when resolving to the next step.

It maps scale degrees to chords individually depending on if it is minor (i-iv-v-i chord progression) or major (I-IV-V-I) and
determines tonality by searching for the substring "major". The quality of the chord (major, minor, diminished, dominant, etc.)
is manually determined for each scale degree both by what harmonically makes sense in a key or what sounds best due to general
music theory. Some scale degrees may map to different chords under different circumstances depending on whether the I and IV
flags are turned on -- for example, if both flags are on, it indicates that there was an I chord and a IV chord, so a V chord
would be appropriate for the 5th scale degree. On the other hand, if only the I chord is on, a V chord would not be appropriate
for the 5th scale degree because a IV chord needs to come first.

Chordsheet also accounts for chords that are not in the natural major/minor scales by making tonicizations (temporary key changes)
to keys that are close to the original key and tonality, although it does not generate permanent modulations.

Chordsheet first maps to chords in the format [scaledegree, scaledegree modification, chord quality], then uses this list to
generate a string for the chord name with the function chordname. It concatenates this string with longer strings to make
Lilypond code.

Chordsheet returns these two strings in a list: the first one is chordmode, which will actually implement the chords in the
bassline, and the second one is chords, which shows the figured bass (text) labels.


##### scale function
Scale takes the key signature and generates the scale in order to make it easier to find scale degree. By the format the key
signature is in ("note \majororminor"), we can find the tonic by finding the 1st character of the string and find the tonality
by searching for the substring "major" (because it is either major or minor).

We can then use the unique sequence of whole and half steps in major vs minor scales to iterate over a chromatic scale list
[a, a#, b, ...] to select the notes in this scale and insert them into a new list. We return this list as the scale.


##### convert function
Convert takes a note and calculates the scale degree in the given key in list form by finding the numerical degree by the note
and then stating if it is a half-step above that degree.

By doing this, it makes it easy to have a general chordsheet function that is
not key signature-dependent, since pitches and harmonies can be relatively determined via scale degrees and then rooted by setting
the tonic as the key. It is used in chordsheet to convert from note to scale degree.


##### chordname function
Chordname finds the name of the chord given the scale degree (number and accidental) and the key signature by referring to the
scale produced in the scale function. Sometimes, the note name may be incorrect because all information is stored as sharps
("is") or half-steps up for simplicity, so while the chordname "Eb" may be more appropriate, it may actually be "D#". To take
this into account, for notes that are a half-step below their analagous note of that scale degree, the function subtracts 1 from
the scale degree.

Chordname is used in chordsheet to convert back from scale degree to note name. It also adds on the quality (major, minor,
diminished, dominant seventh, etc.) of a chord in a form that lilypond can recognize.


##### replace_after function
Replace_after creates a copy of the main lilypond file (trying.ly), then replaces the contents after a certain line with a certain
input. It takes a list input: [index (of last line you want in the file), replacement text, name of output file].
It works similarly to insert_after, but first uses a while loop and the pop function to remove lines from the list
until only the last line desired remains. After that, it inserts the replacement lines similarly to insert_after.

Replace_after makes it possible to insert the outputs from notestrings() and chordsheet() into a lilypond file to render
into a pdf and midi.


#### helpers.py
This Python file is intended for functions that we use more than one time in application.py, and so it allows us to
avoid code repetitions and to save lines of code. It has several functions defined in it.

##### update function
This function updates a Lilypond file to create the subsequent files of type pdf or midi. It takes in the parameters
lilypond\_name, output\_file, and file\_type. It converts the lilypond file [lilypond\_name].ly into file location output_file of the
file type (pdf/midi) [file_type]. We take in these parameters so that the user can compile any lilypond files they wish.

If a user wanted to the lilypond file "trying.ly" to be compiled into a pdf in the location "static/piano_score.pdf" (i.e. a pdf
file called piano\_score.pdf inside the folder static), he/she would run "update" with the parameters lilypond_name = "trying",
output\_file = "static/piano_score.pdf" and file_type="pdf". The user can also compile a lilypond file "midi.ly" into a MIDI file
in the location "static/music.midi" with `update("midi", "static/music.midi", "midi")`.

In order to compile the Lilypond file inside a Python file we use the check_output function from the subprocess library. The
subprocess library allows us to run command line arguments inside the shell and the check_output function catches errors.
We use it because lilypond requires command line arguments to compile the lilypond files into pdf. We first compile the
lilypond file into a pdf/midi file, and then move that created file into into the static folder so that it can be displayed
in the respective HTML pages. We also check if there has been any error with the subprocess function and display an error
message and bring the user back to the index page if this is the case.


##### front_required function
Front_required function decorates routes to require that the front page is submitted. This is necessary since the home page and
chords page require information from the front page.

After the user submits the form in index, we add a flag variable called `front_required` inside session with the value `True`.
We set clear the session when we go back to the home page. We use session since it was the best way to ensure that front_required
only existed for the user's current session.

This function essentially checks whether the front page has been submitted by seeing whether `front_required` has any value
inside session. We use this decoration function when in the get routes of "/home" and "/chords" in application.py.


##### insert_after function
Since file I/O in Python does not allow us to write in a specific row of the file, we implement this
function that allows us to insert a string into after a specific text that we know is inside the Lilypond file.
This function only works if we know at which exact line of the Lilypond file we want to insert the string, and inserts the contents
after that line.

This allows us to make small changes inside our lilypond files to create music files.
For example, to convert a lilypond file into a midi file, the lilypond file must have the text `\\midi {\n}\n'` inserted
after `}\\score {\n`in the lilypond file, which is convenient to execute with `insert_after` function.

We first read and copy all the text in  "trying.ly", the lilypond file of the user's currently composed music, as a list where
each line is an element in the list. We do this with the readline() function. Next, we find the index of [line] in the list and
insert the desired text after the index. We finally combine the entire list into a string using join and write the entire string
into the output file.


##### extract_notes function
Similarly to the previous function, we also need to extract information from the Lilypond files (to pass information
from one file to another) for creating the chord sheet. Also similar to the previous function, we need to know the number
of the line from which we start copying to the number of the line in which we finish copying. This function creates a list in which
we append all the lines that we copy from the original file. It "cleans" the data by eliminating the "\n" with the split
function and also removes all of the additional note decorations (ex. accents, dynamics), which are not necessary for
the chord sheet. The list of the key signature and the notes is then returned at the end of the function.


### HTML files
#### layout.html
This is the HTML that all the other HTML files extend. The style of this page comes from two CSS files: one imported
from Bootstrap and one that we have created. We use AJAX to extend the blocks and so all the other HTML pages can
use the same stlye. In this HTML page we also set up the navigation bar, which contains buttons that redirect the
user to four possible HTML pages: the home page (compose), the chord sheet page, the index page (restart), and the
credits page.

#### layout2.html
We needed to have this secondary layout page because for some stylistic purposes regarding radio buttons the previous
layout.html did not allow us to have textboxes. This is because we wanted radiobuttons that displayed images instead
of text, and in order to have this feature we could not have text boxes in the same layout, so this is why we have
two layout html files. This second layout does allow textboxes and is therefore used in the form in the index.html
page.

#### index.html
This is the first HTML that is displayed when the user launches the web page. It contains a personal CSS file for
radiobuttons and also allows the background color to keep changing. The purpose of this HTML page is to have the
user complete a form in order to get the basic information to set up the Lilypond file: this includes two text boxes
(title and composer) and four dropdown menus (time signature, key signature, tonality and tempo). The value of each
of these items is written exactly as how we will later use it in the Lilypond file. Finally, there is a button that
sends the form to application.py. After the form we have also included some JavaScript that ensures that the user
is filling all the required fields before submitting. If any of the fields has not been filled, the user will be
prompted an alert and the form will not be sent. We have also included error checking for the form in application.py
just in case JavaScript has been disabled.

#### home.html
This is the main page in which the user is able to compose his or her music. The first feature that we include is a
box that contains the items related to the MIDI files: a play button, a stop button, and a download button. We have
also included the button that allows the user to delete the last note. The play button calls a JavaScript function
that can be found in home.js. This function in home.js compiles the midi.ly file so that it creates a MIDI file and
then the browser is able to play it. We can also stop the MIDI file through another JavaScript function that we have
included directly in the HTML file, and the download function is also embedded in the button. Finally, the delete
button calls a JavaScript function that in turn will call the "/undo" route in application.py that we have previously
described.

Below these features related to the MIDI file we find the features related that can be added to the music composed:
duration, rests, dots, dynamics and articulations. This form is sent to application.py and, as we have previously
explained, it can be sent either by pressing the rest button or by pressing any key in the keyboard. The other
buttons add complementary features to the note that is being written. Similarly to the form in index.html, the values
of all the buttons in home.html are exactly written as required by the Lilypond file documentation. We also
put images in the radio buttons instead of text, so that the information can be much more visual. The JavaScript
functions needed to send the form either through the rest button or through the keyboard can be found in home.js.

Below this we can find a virtual keyboard. This keyboard has been built by using the polygon feature of HTML and then
defining the points for each rectangle, as well as the color (either white or black). The value of each key in the
keyboard is the alphabetical representation of the notes as required by the Lilypond file documentation.

After the keyboard there is a text line displaying "Wait, PDF is still loading...". This line is initially hidden
and shows up when the user is pressing the keyboard too fast, thereby not allowing the PDF to update before another
note can be added. Since we update the PDF every time a key in the keyboard is pressed, the user has to wait until
he or she can add another note to the PDF file. If this is not the case, then this message becomes visible through
a JavaScript function that can be found in home.js. The message will disappear again when the PDF has been uploaded,
again through a JavaScript function that can be found in home.js.

Finally, the HTMl contains the PDF that displays the music that is being written by the user. The Lilypond file
is compiled into a PDF file in application.py, and so the HTML just needs to display the PDF. The PDF can be
downloaded and printed.

#### chordsheet.html
This HTML file is very similar to home.html. It again contains the same box regarding the MIDI features (play, stop
and download), although it does not contain the delete button. These buttons allow the user to interact with another
MIDI file which contains not only the melody that the user has created but also the harmonization that we provide.
The harmonization is created through an algorithm in chordsheet.py, whereas the MIDI JavaScript playing features can
be found in home.js.

After this box we display the PDF of the Lilypond file that contains both the melody of the user and the harmonization
that we have created. Similar to home.html, the PDF is already compiled in chordsheet.py, and so HTML just needs to
display it. The PDF can be downloaded and printed.

#### error.html
This HTML is very short and is only used to display errors in the Python file (therefore not related to JavaScript).
For example, we use the error.html page to display an error message if the user has not filled all the fields in
the form displayed in index.html. This HTML displays a message that is passed by the Python and can be included by
using AJAX.

#### credits.html
This HTML page does not include any forms, buttons, or JavaScript functions. It is an HTML page that just displays
information about us. We have included a short biography of the three of us as well as one picture of each. We have
also included links to the documentation of the packages and languages that we have used.


### JavaScript files
#### home.js
This JavaScript file is used in the other Python and HTML files that we have just described in order to implement
interactive functions.

##### '.white, .black' click event listener
This JavaScript function is related to the virtual keyboard that can be found in home.html, as well as all the
buttons that are related to musical features also in home.html (the rhythm, dot, res, dynamic and articulation
buttons). We use this function to submit the form in home.html to the "/home" page in application.py when any key in
the keyboard is pressed. Note that in JavaScript we have two functions that submit the form in home.html to the
"/home" page: this function ('.white, .black'), which submits the form if a key is pressed, and
the '#rest' function, which submits the form if the rest button is pressed. The function extracts the note and the
octave directly from the id of the key and other values (note, octave, alteration, duration, dynamics, articulation, and dot)
It modifies the values and posts the form value in the proper format to the "/home" route in application.py. Once the
"/home" route in application.py has successfully created the pdf with the added note, this function updates the pdf in home.html and
updates flag variables accordingly.

##### '#rest' click event listener
Similarly to the previous function, this one also submits the form from home.html to "/home" in application.py but
when the rest button is pressed. The duration of the rest is extracted from the length value in home.html.
Because we will just write the rest in the music sheet, all the other variables are left empty. We then
post information about the rest and its duration to /home in application.py. After the /home route in application.py
has succefully created the pdf with the added rest, this function updates the pdf in home.html and updates the flag variables
accordingly.

##### '#undo' click event listener

This function posts to the undo route in application.py when the undo button is pressed and error checks to make sure that there
are notes to be deleted. After the undo route has successfully created the pdf with the deleted note, this function updates the
pdf in home.html and updates the flag variables accordingly.


##### '#play' click event listener
This function is triggered when the user clicks the play button in home.html. It allows the user to play the MIDI file
of the music that he or she has written so far. If the audio is up to date with the user's current compsition, then the JavaScript
function will just play this file using a JavaScript library. Else, the audio needs to be updated, so this function posts a request
to the "/midi" route in application.py, which will then update the MIDI file. Once the MIDI file has been succesfully updated,
the audio is played in the browser.

##### '#download' click event listener
Like the play event listener, it allows the user to download the MIDI file of the music that he or she has written so far. If the
audio is not up to date, then the function posts a request to '/midi' route in application.py, which updates the MIDI file.



#### clearForm function
Clear form is a helper function for the rest button and piano button event listeners. After the piano button
is pressed, it clears the form for everything except length/duration option values. This allows user to conveniently add notes
without having to unselect form options.

### chordsheet.js
##### '#play' click event listener
This function is triggered when the user clicks the play button in chordsheet.html. It allows the user to play the MIDI file
of the music found in chordsheet.html (that is, the melody of the user plus the harmonization that we provide).
If the audio is up to date with the user's current chord sheet harmonization, then the JavaScript
function will just play this file using a JavaScript library. Else, the audio needs to be updated, so this function posts a request
to the "/midi2" route in application.py, which will then update the MIDI file for the chord sheet. Once the MIDI file has been
succesfully updated,the audio is played in the browser.

##### '#download' click event listener
Like the play event listener, it allows the user to download the MIDI file of the chord sheet music that the user has written so
far.If the audio is not up to date, then the function posts a request to '/midi2' route in application.py, which updates the MIDI
file.


### CSS files
#### styles.css
This is our general design for all of our HTML pages.

#### stylegradient.css
This CSS file allows the permanent change of the color of the background of index.html (the first page that is
prompet when the user launches the web app).

#### styleform.css
This CSS file customs radio buttons.


### Lilypond files
#### trying.ly
This is the main Lilypond file and it is where all the notes from the keyboards and rests are first inserted. All
the other three Lilypond files extract the information from this first file.

#### midi.ly
This is the Lilypond file that will produce a MIDI file when compiled. This file is created by copying all the
information in trying.ly and adding a MIDI feature as per the Lilypond documentation. This addition is possible
thanks to the update_after function that is found in helpers.py.

#### chords.ly
This is the Lilypond file that contains both the melody of the user and our harmonization of it (we include both
the chords displayed in the stave and the chords written in plain letters below the stave). The melody is copied
from trying.ly and then the harmonization is added following the algorithm explained in chordsheet.py. The Lilypond
library then allows us to display the chords both in the stave and below in English.

#### midichords.ly
This is the Lilypond file that will produce a MIDI file when compiled. This file is created by copying all the
information in chords.ly and then adding a MIDI feature as per the Lilypond documentation. This addition is possible
thanks to the update_after function that is found in helpers.py.

### Other Files

#### references.txt
Links that we visited/were helpful to us.