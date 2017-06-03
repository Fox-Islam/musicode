#!/usr/bin/env python
import cv2
import random
import numpy as np
from midiutil import MIDIFile

filename = raw_input("Filename (Ex.: image.png) or path (Ex.: C:/image.png): ")
im = cv2.imread(filename) 
im = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)
w, h, _ = im.shape

maxtempo = 240 
mintempo = 70
tempo = int(((h*w)%(maxtempo-mintempo))+mintempo) #In beats per minute

track    = 0
channel  = 0
time     = 0 #Start time, in beats
MyMIDI = MIDIFile(1)
MyMIDI.addTempo(track, time, tempo)

avghue = np.median(im[:][:][0])
sharps = int((avghue/255)*5)

#Realised I should have called sharps something else a few minutes in
#but instead I doubled down and now the variable name makes no sense
#Generated sharps value ranges from 0 to 5
#Only the major scale tones are available unless sharps > 0
#when sharps = 1, 7 -> b7
#when sharps = 2, 7 -> b7, 3 -> b3
#and so on, in the order 7,3,6,2,5
#
#
#sharps = 0
#override sharps variable to
#0 for no accidentals
#7 for b3+b5+bb7 (diminished seventh)
#8 for b3+b5+b7 (half-diminished seventh)
#9 for b3+b7 (minor seventh)
#10 for b3 (minor major seventh)
#11 for b7 (dominant seventh)
#12 for #5+b7 (augmented seventh)
#13 for #5 (augmented major seventh)

print ("sharps " + str(sharps))

lastval = random.randint(0,24)
shift = random.randint(0,24)
print ("shift " + str(shift))
print ("lastval " + str(lastval))

#Alter instrument
track   = 0
channel = 0
time    = 0
program = 1 #MIDI instrument value range is 0-127
MyMIDI.addProgramChange(track, channel, time, program)

#PIANO
curw = 0 #current width, height value (to iterate over image)
curh = 0
while time < h*w:
    n = im[curw][curh]

    volrange = 20 #MIDI volume range is 0-127
    minvol = 70
    volume = int((float(n[1])/255)*volrange)+minvol
    if volume > 127:
        volume = 127
        
##    duration = 0.5
##    if n[2] % 3 == 0:
##        duration = 1
##    elif n[2] % 5 == 0:
##        duration = 2
##    elif n[2] % 7 == 0:
##        duration = 3
##    elif n[2] % 9 == 0:
##        duration = 0.125

    duration = float((int((float(n[1])/255)*63) + 1)) / 16
    #Note durations from eighth notes to whole notes
    

    pitchrange = 84 #MIDI pitch range is 0 - 127
    minpitch = 12
    pitch = (int((float(n[0])/255) * shift)
             - lastval) % pitchrange + minpitch
    lastval = pitch

    #Snapping pitches to major scale
    note = ""
    if pitch % 12 == 0:   
        note = "C"        
    elif pitch % 12 == 1:
        note = "C#"
        if (sharps < 4) or (sharps > 6):
            pitch -= 1
            note = "C"
    elif pitch % 12 == 2: 
        note = "D"
    elif pitch % 12 == 3:
        note = "D#"
        if (sharps < 2) or (sharps > 6):
            pitch -= 1
            note = "D"
    elif pitch % 12 == 4: 
        note = "E"
    elif pitch % 12 == 5: 
        note = "F"
    elif pitch % 12 == 6:
        note = "F#"
        if (sharps < 5) or (sharps > 6):
            pitch -= 1
            note = "F"
    elif pitch % 12 == 7: 
        note = "G"
    elif pitch % 12 == 8:
        note = "G#"
        if (sharps < 3) or (sharps > 6):
            pitch -= 1
            note = "G"
    elif pitch % 12 == 9: 
        note = "A"
    elif pitch % 12 == 10:
        note = "A#"
        if (sharps < 1) or (sharps > 6):
            pitch -= 1
            note = "A"
    elif pitch % 12 == 11: 
        note = "B"

    #Handling override/key change values of sharps variable
    if sharps > 6:
        if (sharps == 13) and (note == "G"):
            pitch += 1
            note = "G#"
        elif sharps == 12:
            if note == "G":
                pitch += 1
                note = "G#"
            elif note == "B":
                pitch -= 1
                note = "A#"
        elif (sharps == 11) and (note == "B"):
            pitch -= 1
            note = "A#"
        elif (sharps == 10) and (note == "E"):
            pitch -= 1
            note = "D#"
        elif sharps == 9:
            if note == "E":
                pitch -= 1
                note = "D#"
            elif note == "B":
                pitch -= 1
                note = "A#"
        elif sharps == 8:
            if note == "E":
                pitch -= 1
                note = "D#"
            elif note == "G":
                pitch -= 1
                note = "F#"
            elif note == "B":
                pitch -= 1
                note = "A#"
        elif sharps == 7:
            if note == "E":
                pitch -= 1
                note = "D#"
            elif note == "G":
                pitch -= 1
                note = "F#"
            elif note == "B":
                pitch -= 2
                note = "A"

         
    MyMIDI.addNote(track, channel, pitch, time, duration, volume)
    time += duration
    curw += lastval

    #50% chance of a key change in each loop
    change = random.randint(0,10)
    if change > 8:
        sharps += 1
        if sharps > 13:
            sharps = 12
        elif sharps == 6:
            sharps = 4
    elif change < 2:
        sharps -= 1
        if sharps < 0:
            sharps = 2
        elif sharps == 6:
            sharps = 8
    elif change == 5:
        if sharps < 6:
            sharps = 7
        elif sharps > 6:
            sharps = 5
        
    if curw > (w-1):
        curw = (curw % w)
        curh += 1
        if curh > (h-1):
            break
##DRUMS
time = 0
curw = 0
curh = 0
while time < h*w:
    n = im[curw][curh]

    volrange = 100
    minvol = 10
    volume = int((float(n[1])/255)*volrange)+minvol
    if volume > 127:
        volume = 127
        
##    duration = 0.5
##    if n[2] % 3 == 0:
##        duration = 1
##    elif n[2] % 5 == 0:
##        duration = 2
##    elif n[2] % 7 == 0:
##        duration = 3
##    elif n[2] % 9 == 0:
##        duration = 0.125
    
    drumduration = float((int((float(n[2])/255)*63) + 1)) / 64 
    drumpitchrange = 16 #MIDI "drum sounds" range is 34-80
    drumminpitch = 34
    drumpitch = ((int((float(n[2])/255) * shift)
             - lastval) % drumpitchrange) + drumminpitch
    lastval = pitch
    time += drumduration
    MyMIDI.addNote(track, 9, drumpitch, time, drumduration, (volume-10))
    
    time += duration
    curw += lastval
    
    if curw > (w-1):
        curw = (curw % w)
        curh += 1
        if curh > (h-1):
            break

with open("musicode" + str(shift) + ".mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
    print("Complete")
    print("Filename: musicode" + str(shift) + ".mid")
