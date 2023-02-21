import os
from appJar import gui
import webbrowser
def save(btn):
    print("Saved")
app=gui("OMB Setup")
app.addLabel("welcome")

app.startLabelFrame("Location")
app.addLabel("Choose a Place for the OMB media folder")
app.addButton("Save", save)
app.stopLabelFrame()

app.startLabelFrame("2")
app.addButton("Finish", save)
app.stopLabelFrame()
app.go()