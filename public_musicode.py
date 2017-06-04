#!/usr/bin/env python
import cv2
import random
import numpy as np
from midiutil import MIDIFile

filename = raw_input("Filename (Ex.: image.png) or path (Ex.: C:/image.png): ")
im = cv2.imread(filename) 
im = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)
w, h, _ = im.shape
iterator = 0 #determines the pixel distance travelled for each iteration
             #iterator = 0 sets it to a variable called 'lastval'
drums = 1 #set to 0 to turn off drums

maxtempo = 240 
mintempo = 70
tempo = int(((h*w)%(maxtempo-mintempo))+mintempo) #In beats per minute

track    = 0
channel  = 0
time     = 0 #Start time, in beats
MyMIDI = MIDIFile(1)
MyMIDI.addTempo(track, time, tempo)

avghue = np.median(im[:][:][0])
sharps = int((avghue/255)*20)

#Realised I should have called sharps something else a few minutes in
#but instead I doubled down and now the variable name makes no sense
#Generated sharps value ranges from 0 to 5
#Only the major scale tones are available unless sharps > 0
#when sharps = 1, 7 -> b7
#when sharps = 2, 7 -> b7, 3 -> b3
#and so on, in the order 7,3,6,2,5
#
#
transpose = 3 #set to a value between 0 and 11 to change the starting scale note
changekeys = 1 #set to 0 to disallow key changes in the song, or 1 to allow
#sharps = 20
#override sharps variable to
#6 for no accidentals (major)
#7 for b3+b5+bb7 (diminished seventh)
#8 for b3+b5+b7 (half-diminished seventh)
#9 for b3+b7 (minor seventh)
#10 for b3 (minor major seventh)
#11 for b7 (dominant seventh)
#12 for #5+b7 (augmented seventh)
#13 for #5 (augmented major seventh)
#14 for b3+b5+b7 without 2+6 (blues minor hexatonic)
#15 for b6 (harmonic major)
#16 for b6+b7 (melodic major)
#17 for b2+b6 (double harmonic major)
#18 for b2+b3+b6+b7 (phrygian)
#19 for b5 (lydian)
#20 for b2+b3+b5+b6+b7 (locrian)

###Alter instrument
##track   = 0
##channel = 0
##time    = 0
##program = 0 #MIDI instrument value range is 0-127
##MyMIDI.addProgramChange(track, channel, time, program)
autoalter = 0 #percentage chance of changing the current instrument
              #set to 0 to keep the instrument constant
program = 0 #starting instrument

print ("sharps " + str(sharps))
print ("change keys " + str(changekeys))
print ("iterator " + str(iterator))
transpose = transpose % 12
print ("transpose " + str(transpose))
lastval = random.randint(0,24)
shift = random.randint(0,24)
print ("shift " + str(shift))
print ("lastval " + str(lastval))
print ("auto-alter " + str(autoalter))
print ("program " + str(program))



def fixkey(pitch, sharps):
    note = ""
    #Snapping pitches to major scale
    if pitch % 12 == 0:   
        note = "C"        
    elif pitch % 12 == 1:
        note = "C#"
        if (sharps < 4) or (sharps > 5):
            pitch -= 1
            note = "C"
    elif pitch % 12 == 2: 
        note = "D"
    elif pitch % 12 == 3:
        note = "D#"
        if (sharps < 2) or (sharps > 5):
            pitch -= 1
            note = "D"
    elif pitch % 12 == 4: 
        note = "E"
    elif pitch % 12 == 5: 
        note = "F"
    elif pitch % 12 == 6:
        note = "F#"
        if (sharps < 5) or (sharps > 5):
            pitch -= 1
            note = "F"
    elif pitch % 12 == 7: 
        note = "G"
    elif pitch % 12 == 8:
        note = "G#"
        if (sharps < 3) or (sharps > 5):
            pitch -= 1
            note = "G"
    elif pitch % 12 == 9: 
        note = "A"
    elif pitch % 12 == 10:
        note = "A#"
        if (sharps < 1) or (sharps > 5):
            pitch -= 1
            note = "A"
    elif pitch % 12 == 11: 
        note = "B"

    #Handling override/key change values of sharps variable
    if sharps > 5:
        if sharps == 20:
            if note == "D":
                pitch -= 1
                note = "C#"
            elif note == "E":
                pitch -=1
                note = "D#"
            elif note == "G":
                pitch -= 1
                note = "F#"
            elif note == "A":
                pitch -= 1
                note = "G#"
            elif note == "B":
                pitch -= 1
                note = "A#"
        elif sharps == 19 and note == "G":
            pitch -= 1
            note = "F#"
        elif sharps == 18:
            if note == "D":
                pitch -= 1
                note = "C#"
            elif note == "E":
                pitch -=1
                note = "D#"
            elif note == "A":
                pitch -= 1
                note = "G#"
            elif note == "B":
                pitch -= 1
                note = "A#"
        elif (sharps == 17):
            if note == "A":
                pitch -= 1
                note = "G#"
            elif note == "D":
                pitch -= 1
                note = "C#"
        elif (sharps == 16):
            if note == "A":
                pitch -= 1
                note = "G#"
            elif note == "B":
                pitch -= 1
                note = "A#"
        elif (sharps == 15) and note == "A":
            pitch -= 1
            note = "G#"
        elif (sharps == 14):
            if note == "E":
                pitch -= 1
                note = "D#"
            elif note == "G":
                pitch -= 1
                note = "F#"
            elif note == "B":
                pitch -= 1
                note = "A#"
            elif note == "D":
                pitch -= 2
                note = "C"
            elif note == "A":
                pitch -= 2
                note = "G"
        elif (sharps == 13) and (note == "G"):
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
    return pitch

def addnote(pitch,sharps,chordrange):
    pitch = pitch + random.randint(-chordrange,chordrange)
    pitch = fixkey(pitch, sharps)
    return pitch

def keychange(avgsofar,sharps):
        #key change dependent on variation from average hue encountered so far
        chance = (int((float(n[0])/255)*10) + int((float(avgsofar)/255)*10)) % 10
        if chance == 3 or (random.randint(0,100) > 97):
            sharps += 1
            if sharps > 20:
                sharps = 19
            elif sharps == 6:
                sharps = 4
        elif chance == 4 or (random.randint(0,100) > 96):
            sharps -= 1
            if sharps < 0:
                sharps = 2
            elif sharps == 6:
                sharps = 8
        elif (chance == 5) or (random.randint(0,100) > 95):
            if sharps < 6:
                sharps = 7
            elif sharps > 6:
                sharps = 5
        return sharps

#PIANO
curw = 0 #current width, height value (to iterate over image)
curh = 0
enum = 1
avgsofar = 0
chordduration = 0
while time < h*w:
    n = im[curw][curh]

    volrange = 40 #Full MIDI volume range is 0-127
    minvol = 70
    volume = int((float(n[1])/255)*volrange)+minvol
    if volume > 126:
        volume = 126

    duration = float((int((float(n[1])/255)*63) + 1)) / 16
    #Note durations from sixteenth notes to whole notes
    if duration < 0.6:
        if random.randint(1,10) > 7:
            duration = duration*2

    #Alter instrument
    if random.randint(0,100) < autoalter:
        program = (program + random.randint(10,40)) % 127
        MyMIDI.addProgramChange(track, channel, time, program)
        
    
    pitchrange = 60 #Full MIDI pitch range is 0 - 127
    minpitch = 36
    pitch = (int((float(n[0])/255) * shift)
             - lastval) % pitchrange + minpitch
    lastval = pitch

    pitch = fixkey(pitch,sharps)
    MyMIDI.addNote(track, channel, pitch+transpose, time, duration, volume)

    #determining chance of adding chord tones
    chord = random.randint(0,100) 
    chordtime = time + chordduration
    if (time - chordtime) >= 0:
        chordduration = duration + float(random.randint(4,8)/2)
        if chord > 80:
            chordpitch = addnote(pitch,sharps,5)
            MyMIDI.addNote(track, channel, chordpitch+transpose, time, chordduration, volume)
        if chord > 85:
            chordpitch2 = addnote(pitch,sharps,8)
            if chordpitch > pitch and chordpitch2 > chordpitch:
                MyMIDI.addNote(track, channel, chordpitch2+transpose, time, chordduration, volume)
            elif chordpitch < pitch and chordpitch2 < chordpitch:
                MyMIDI.addNote(track, channel, chordpitch2+transpose, time, chordduration, volume)
        if chord > 95:
            chordpitch3 = addnote(pitch,sharps,12)
            if chordpitch > pitch and chordpitch2 > chordpitch and chordpitch3 > chordpitch2:
                MyMIDI.addNote(track, channel, chordpitch3+transpose, time, chordduration, volume)
            elif chordpitch < pitch and chordpitch2 < chordpitch and chordpitch3 < chordpitch2:
                MyMIDI.addNote(track, channel, chordpitch3+transpose, time, chordduration, volume)

    if changekeys != 0:
        avgsofar = (avgsofar + n[0])/enum
        sharps = keychange(avgsofar,sharps)
    
    enum += 1       
    time += duration
    if iterator < 1:
        iterator = lastval

    curw += iterator
    if curw > (w-1):
        curw = (curw % w)
        curh += 1
        if curh > (h-1):
            break
        
##DRUMS
drumtime = 0
curw = 0
curh = 0
while drumtime < h*w and drums == 1:
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

    if drumtime <= time:
        drumduration = float((int((float(n[2])/255)*64) + 1)) / 32
        if drumduration < 0.2:
            if random.randint(1,10) > 8:
                drumduration = drumduration*2
        drumpitchrange = 16 #Full MIDI "drum sounds" range is 34-80
        drumminpitch = 34
        drumpitch = ((int((float(n[2])/255) * shift)
                 - lastval) % drumpitchrange) + drumminpitch
        lastval = pitch
        drumtime += drumduration
        MyMIDI.addNote(track, 9, drumpitch, drumtime, drumduration, volume)
    else:
        break
        
    curw += iterator
    if curw > (w-1):
        curw = (curw % w)
        curh += 1
        if curh > (h-1):
            break

with open("musicode" + str(shift) + ".mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
    print("Complete")
    print("Filename: musicode" + str(shift) + ".mid")
