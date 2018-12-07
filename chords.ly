\version "2.18.2"
\header {
title = "Electro Folk Music"
composer = "Malan"
}\score {
<< 
\new Staff {
\clef treble
\key c \major
\time 2/4
\tempo "Moderato" 4 = 80 
\relative 
f' 
{ 
f4 
r4 
c4 
c4 
} 
\bar "|." 
} 
<< 
\new Staff { 
 \clef bass 
\key c \major
\chordmode { d,4:m r4 c,4:5 f,4:5 } 
} 
\chords { d,4:m r4 c,4:5 f,4:5 } 
>> 
>> 
} 
