import wave
from flask.helpers import send_file
import numpy
import pygame
import random
from flask import Flask, render_template, request, send_file, redirect

LICK_GEN_MAX = 10

app = Flask(__name__)

def lick_maths(start_freq, tempo, ornament, swing):
    calc_tempo = tempo / 30
    swings = [4/3, 2/3] if swing else [1, 1] 

    notes =  [
        (start_freq, (1.0/calc_tempo)*swings[0]),
        (start_freq*1.125, (1.0/calc_tempo)*swings[1]),
        (start_freq*1.2, (1.0/calc_tempo)*swings[0]),
        (start_freq*(4/3), (1.0/calc_tempo)*swings[1]),

        (start_freq*(16/15), 0.5/calc_tempo) if ornament == "ACC" else None,

        (start_freq*(16/15), (1/3)/calc_tempo) if ornament == "TURN" else None,
        (start_freq, (1/3)/calc_tempo) if ornament == "TURN" else None,
        (start_freq*1.2, (1/3)/calc_tempo) if ornament == "TURN" else None,

        (start_freq*1.125, 2.0/calc_tempo - (0.5/calc_tempo if ornament == "ACC" else 0)),

        (start_freq*(8/9), (1.0/calc_tempo)*swings[0]),
        (start_freq, (1.0/calc_tempo)*swings[1] + 5.0/calc_tempo)
    ]

    return [note for note in notes if note]

@app.route("/")
def index_handler():
    # This shows the fun of naming notes!
    data = {
        "notes": [
            (f"{letter[0]}{number}",
            440 * (2 ** ((number-5) if letter[1]>=3 else (number-4))) * ((2 ** (letter[1]/12)) if letter[1] != 0 else 1)
            ) 
        for number in range(9) 
        for letter in [
            ("C", 3),
            ("C#/D♭", 4),
            ("D", 5),
            ("D#/E♭", 6),
            ("E", 7),
            ("F", 8),
            ("F#/G♭", 9),
            ("G", 10),
            ("G#/A♭", 11),
            ("A", 0),
            ("A#/B♭", 1),
            ("B", 2)
            ]
        ]
    }
    return render_template("index.html", data=data)

@app.route("/audio/<lick_no>")
def serve_audio(lick_no):
    return send_file(f"audio/lick_{lick_no}.wav", cache_timeout=-1)

@app.route("/generate", methods=["POST"])
def generate_handler():

    lick_no = random.randint(0, LICK_GEN_MAX)

    sfile = wave.open(f"audio/lick_{lick_no}.wav", "w")
    sfile.setframerate(48000)
    sfile.setnchannels(2)
    sfile.setsampwidth(2)
    pygame.init()
    pygame.mixer.init(frequency=48000, channels=2)

    for note in lick_maths(
        float(request.form["note"]),
        float(request.form["tempo"]),
        request.form["ornament"] if request.form["ornament"] != "None" else None,
        True if request.form["rhythm"] == "swung" else False
        ):
        ncycles = note[1] * note[0]
        spc = int((48000 * note[1]) / ncycles)

        sine = numpy.arange(0, 2*numpy.pi, (2*numpy.pi)/spc)
        sine = numpy.sin(sine)
        sine *= 8000
        sine = numpy.hstack(int(ncycles)*list(sine))
        sine = numpy.repeat(sine, 2, axis=0)
        sine.reshape(len(sine)//2,2)

        snd = pygame.mixer.Sound(sine.astype('int16'))
        sfile.writeframesraw(snd.get_raw())

    sfile.close()

    return redirect(f"/audio/{lick_no}", code=303)

if __name__ == "__main__":
    app.run()