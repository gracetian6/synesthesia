\version "2.18.2"
\header {
title = "Electro Folk"
composer = "malan"
}\score {
\midi {
}
<< 
\new Staff {
\clef treble
\key c \major
\time 3/4
\tempo "Lento" 4 = 54 
\relative 
e' 
{ 
e8 
} 
\bar "|." 
} 
<< 
\new Staff { 
 \clef bass 
\key c \major
\chordmode { c,8:5 } 
} 
\chords { c,8:5 } 
>> 
>> 
} 
