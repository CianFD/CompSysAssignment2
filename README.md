# A dog barking alert/dissuasion prototype.
# A RaspberryPi is linked to a PiCamera V2 Camera Module, a Funduino Sound Detection Sensor, and a Keyestudio Passive Buzzer.
# The Sensor is listening continuously on a loop, written in a Python Script.
# Normal sounds are not reacted to but loud noises, e.g. a dog barking, will trigger a reaction.
# When a loud noise is received, the sensor sends a command to the RPi.
# The RPi sends a command to the Passive Buzzer to begin ringing at a particular tone for a short interval to distract the dog to stop barking.
# A simultaneous command is sent to trigger the Camera to take a photo.
# The Photo is sent to Firebase Storage and RealTime Database.
# A command is also sent to a ThingSpeak Channel triggering a ThingTweet React.
# The ThingTweet triggers a Tweet to be posted to a particular Twitter Page, which the dog's owner is subscribed to so they receive an alert when a new post appears.
# Inside the Tweet posted is a link.
# If the Owner clicks on the Link they are directed to a Glitch WebApp which displays the most recent image taken by the RPi Camera.
# This Image is pulled from the Firebase Realtime Database along with the timestamp to be displayed on the WebApp.
