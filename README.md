# VSEPIA (Volumetric Statistical Estimate Preparation Instrumental Analysis)
This is a project based on Arduino and Python interfacing through Serial connection.
A GUI has been developed that helps vendors and farmers to keep track of their current sales, expenses and vegetable leftovers in a cost effective manner.
This is a single unit which has been implemented. However, this can easily and effectively be scaled to over multiple units which will be connected to a central server (wireless) that will show the summary of every crop, and cost estimate. etc.

## Screenshots of the GUI App:
![screenshot 65 635](https://user-images.githubusercontent.com/16799596/42185187-974661e8-7e65-11e8-8db7-1f41bbb1fd5d.png) ![screenshot 66 636](https://user-images.githubusercontent.com/16799596/42185188-97b20826-7e65-11e8-91fd-02b6f7270e4f.png)

## Dependencies:
  1. Python 3
  2. Arduino IDE
  3. BeautifulSoup
  4. PyQt5

## Hardware Requirements:
  1. Arduino UNO (or any other compatible Arduino board)
  2. HC-SR04 (Ultrasonic Ranging Module)
  3. Connecting Wires

## Hardware/Software Setup:
  1. Put the Vegetables in a bucket and and attach the Ultrasonic Sensor elevated, in the center of the bucket pointing down.
  2. Connect the Ultrasonic Sensor to the Arduino using Jumpers (wires)
  3. Connect the Arduino to the PC and Upload the Arduino Code.
  4. Open Up Python, enter the bucket diameter in the program and run the GUI and Interact with it.

## How does it work?
  1. The Ultrasonic Sensor is placed above the bucket which senses the distance from itself to the top of the vegetables.
  2. It is assumed that the distance from sensor to the bottom of empty bucket is known or hard coded from before.
  3. The Arduino stays in sleep mode by default in order to conserve power.
  4. When the "Refresh" button is pressed in the Python GUI App, it sends a wake signal to the Arduino from sleep mode.
  5. The Arduino takes 10 readings and sends them to the Laptop through Serial Port. Python Reads the same and averages out the values.
  6. The Average height of the vegetables is then taken along with known bucket diameter to calculate the volume.
  7. The Density of vegetable is known (pre-coded). Therefore, From Volume and Density, an Approximate Weight of the vegetable is determined.
  8. Another Script in the background runs to update the current vegetable prices from the web.
  9. The Vegetable weight and current market price is multiplied to display the total value of vegetable left in the bucket to the vendor.
  10. Along with this, the app also shows the previous week's leftover vegetables and the amount of vegetables added newly or sold.
  11. There is a shelf life calculator built in, which notifies the vendor when a vegetable is about to rot. (this feature is not implemented fully)
  12. Depending on the past and current week's sales, the app predicts the sales for the following week. (Not implemented yet)
