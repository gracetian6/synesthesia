// Javascript file for chordsheet.html

// Flag that indicates where audio file for chord sheet is up to date
let audio_updated = false;

// Posts to /midi2 route in application.py to create updated midi file for chord sheet
// if needed and then plays the music
$('#play').click(function(event) {
    // Play audio if it is up to date with current composition
    if (audio_updated) {
        MIDIjs.play('static/chords.midi');
        return;
    }

    // If audio file is not up to date, post request to /midi route in application.py
    $.post("/midi2", function(data) {
        if (data == true) {
            // When midi file is updated, play music
            MIDIjs.play('static/chords.midi');
            audio_updated = true
        }
    });
});

// Posts to /midi route in application.py to create updated midi file if needed
$('#download').click(function(event) {
    console.log("audio_updated:" + audio_updated);

    if (!audio_updated) {
        $.post("/midi2", function(data) {
            if (data == true) {
                audio_updated = true
            }
        });
    }
});
