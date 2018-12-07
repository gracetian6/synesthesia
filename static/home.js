// Javascript file for home.html

// global flag that indicates when piano key is done loading
let done = true;

// flag that indicates whether audio file is up to date
let audio_updated = false;

// Posts piano key info to home route in application.py when piano key pressed
// and dynamically updates pdf with changes
$('.white, .black').click(function(event){
    // Disables form submission until previous key is processed
    if (!done){
        $("p").show();
        return;
    }

    done = false;

    // Extract note and octave of the piano key
    let piano = this.id;
    let note = piano[0];
    let octave = piano[piano.length-1];

    // Instantiate dyn, articulation, alternation, and dot
    let dyn = "";
    let articulation = "";
    let alternation = "";
    let dot = "";

    // Extract alternation of the piano key
    if (piano.length == 3){
        console.log("alternation");
        alternation = piano[1];
    }

    // Update checked options from the form into variables
    let duration = "4";
    $('#form input').each(function() {
        if (this.checked) {
            if (this.name == 'length'){
            duration = this.value;
            }
            if (this.name == 'dyn'){
              dyn = this.value;
            }
            if (this.name == 'dot'){
              dot = this.value;
            }
            if (this.name == 'articulation'){
              articulation = this.value;
            }
        }
    });


    // Post form values to /home in application.py
    $.post( "/home", { note: note, octave: octave, alternation: alternation, duration: duration,
                    dyn: dyn, articulation: articulation, rest: "", dot: dot}, function(data){

                // Update flags
                done = true;
                audio_updated = false;

                if (data == true){
                    // Reloads pdf when piano note is updated
                    $("#pdf").attr("src","static/piano_score.pdf");

                    // Hides message for user to wait
                    $("p").hide();

                    // Clears form
                    clearForm()
                }

    });
});

// Posts rest info to home route in application.py when rest is pressed
// and dynamically updates pdf with changes
$('#rest').click(function(event){

    // Disables form submission until previous key is processed
    if (!done){
        $("p").show();
        return;
    }

    // Gets the duration value from the form
    let duration = "4";
    $('[name="length"]').each(function() {
        if (this.checked) {
          duration = this.value;
        }
    });

    // Post form values to /home in application.py
    $.post( "/home", { note: "", octave: "", alternation: "", duration: duration,
                        dyn: "", articulation: "", rest: "r"}, function( data ) {
            // Update flag variables
            done = true;
            audio_updated = false;

            if (data == true){
                // Reload pdf when rest is added to core
                $("#pdf").attr("src","static/piano_score.pdf");

                // Hides message for user to wait
                $("p").hide();

                // Clears form
                clearForm();
            }
    });

});

// Posts to undo route in application.py when undo button is pressed
// and dynamically updates pdf with the deleted note
$('#undo').click(function(event){

    // Disables form submission until previous key is processed
    if (!done){
        $("p").show();
        return;
    }

    done = false;

    // Post form values to /undo in application.py
    $.post( "/undo", function(data){
        // Update flag variables
        done = true;
        audio_updated = false;

        // Ensures that no notes are deleted if there are not notes
        if (data == false) {

            alert("Cannot delete last note!");
        }

        // When rest is added pdf in server
        else {
            // Reload pdf on page
            $("#pdf").attr("src","static/piano_score.pdf");

            // Hides message for user to wait
            $("p").hide();
        }
    });
});


// Posts to /midi route in application.py to create updated midi file if needed
// and then plays the music
$('#play').click(function(event){
    // Play audio if it is up to date with current composition
    if (audio_updated){
        MIDIjs.play('static/music.midi');
        return;
    }

    // If audio file is not up to date, post request to /midi route in application.py
    $.post("/midi", function(data){
        if (data==true) {
            // When midi file is updated, play music
            MIDIjs.play('static/music.midi');
            audio_updated = true
        }
    });
});

// Posts to /midi route in application.py to create updated midi file if needed
$('#download').click(function(event){
    if (!audio_updated){
        $.post("/midi", function(data){
            if (data==true) {
                audio_updated = true
            }
        });
    }
});

// Clears form for everything except length/duration
function clearForm(){
    $('#form input').each(function() {
        if (this.checked && this.name != 'length') {
            this.checked = false;
        }
    });
}