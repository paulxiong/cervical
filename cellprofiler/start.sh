#!/bin/bash
Xvfb :5 -screen 0 1920x1080x24 &
x11vnc -display :5 -once -loop -noxdamage -repeat -rfbauth ~/.vnc/passwd -rfbport 5905 -shared  -scale 1920x1080 &
export DISPLAY=:5
openbox &
/init cellprofiler
