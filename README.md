# Raspberry Pi Sensehat Snake game

This is a remake of the popular retro Nokia snake game on a Raspberry Pi 4 equipped with a SenseHat add-on board. The snake game is a common programming project
used to practice certain concepts such as object-oriented programming and array manipulation. There are a lot of SenseHat snake game
implementations online, this version attempts to program the game in an easier and well documented way, whilst leaving room for further amends/improvements.

## Hardware and software

### Hardware

The following hardware components are required for this project:

- Raspberry Pi 3/4
- SenseHat add-on board
- Monitor
- HDMI cable (depending on the version of RPi in use)
- Mouse and keyboard

### Software

**Raspberry Pi OS** is the operating system used on the Raspberry Pi 4. The download and installation procedure can be found [here](https://www.raspberrypi.org/software/). **Python 3** and the [SenseHat library](https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat/1) were employed in programming the game.

## SenseHat setup

The SenseHat is equipped with the following sensors and components:

- Accelerometer
- Magnetometer
- Gyroscope
- Humidity sensor
- Temperature sensor
- Pressure sensor
- 8x8 RGB LED matrix and
- Five-button joystick

However, only the joystick and 8x8 LED matrix will be used for the game.

---
<p align="center">
  <img src=images/sensehat_assembled.png>
</p>
assembling before and after pictures (including the hdmi, monitor, mouse and keyboard...talk briefly about them)

---
header, standoffs

## Snake game brief

The snake game starts out with a size of one pixel moving in a default position, to the right in this case. A few milliseconds later, food is spawned for the snake to consume. With each successive food ingestion, the snake's tail grows by one pixel and the snake's moves at a faster "rate/pace". Once the snake bites any part of its body, the game is over.

The diagram below (courtesy of [Raspberry Pi Projects](https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat/5)) shows the SenseHat LED matrix coordinates.

<p align="center">
  <img src=images/coordinates.png>
</p>

## "Game Pseudocode"

<p align="center">
    <img src=images/snake_game_flow_chart.png>
</p>

explain checking borders

Don't think this needs a separate section. 

Resize and position images well

## Video demonstration

link

## SenseHat Emulator

"If the SenseHat add-on is not available, the snake game can be tested online by pasting the code on a SenseHat an emulator at" [Trinket](https://trinket.io/sense-hat).
