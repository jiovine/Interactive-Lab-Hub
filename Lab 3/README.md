# Chatterboxes
**NAMES OF COLLABORATORS HERE**
[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1).  First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond.  We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 

### Pick up Web Camera If You Don't Have One

Students who have not already received a web camera will receive their [IMISES web cameras](https://www.amazon.com/Microphone-Speaker-Balance-Conference-Streaming/dp/B0B7B7SYSY/ref=sr_1_3?keywords=webcam%2Bwith%2Bmicrophone%2Band%2Bspeaker&qid=1663090960&s=electronics&sprefix=webcam%2Bwith%2Bmicrophone%2Band%2Bsp%2Celectronics%2C123&sr=1-3&th=1) on Thursday at the beginning of lab. If you cannot make it to class on Thursday, please contact the TAs to ensure you get your web camera. 

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. There are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2022
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2022Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

## Part 1.

### Text to Speech 

In this part of lab, we are going to start peeking into the world of audio on your Pi! 

We will be using the microphone and speaker on your webcamera. In the home directory of your Pi, there is a folder called `text2speech` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file? Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*

In text2speech/greeting.sh

(This shell file should be saved to your own repo for this lab.)

Bonus: If this topic is very exciting to you, you can try out this new TTS system we recently learned about: https://github.com/rhasspy/larynx

### Speech to Text

Now examine the `speech2text` folder. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi. 

In particular, look at `test_words.py` and make sure you understand how the vocab is defined. 
Now, we need to find out where your webcam's audio device is connected to the Pi. Use `arecord -l` to get the card and device number:
```
pi@ixe00:~/speech2text $ arecord -l
**** List of CAPTURE Hardware Devices ****
card 1: Device [Usb Audio Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```
The example above shows a scenario where the audio device is at card 1, device 0. Now, use `nano vosk_demo_mic.sh` and change the `hw` parameter. In the case as shown above, change it to `hw:1,0`, which stands for card 1, device 0.  

Now, look at which camera you have. Do you have the cylinder camera (likely the case if you received it when we first handed out kits), change the `-r 16000` parameter to `-r 44100`. If you have the IMISES camera, check if your rate parameter says `-r 16000`. Save the file using Write Out and press enter.

Then try `./vosk_demo_mic.sh`

\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*

In speech2text/zipcode.sh

### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

### Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.) 

\*\***Post your storyboard and diagram here.**\*\*

My speech-enabled device is a simple mental math game. The device is started with the click of a button and prompts the user with an arithmetic question, if the user gets it right their score goes up and they get to answer another question. If they get it wrong the round ends and the device lets the user know their score.
![Lab3 Idea](lab3storyboard.jpeg)

Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses. 

\*\***Please describe and document your process.**\*\*

I imagine the dialogue to be very transactional. The device prompts the user with a math question and if the user gives the correct answer, the device gives a few words of encouragement and then goes straight into the next question. This cycle continues until the user gets a question wrong and the device will let the user know that it was wrong and how many they have answered correctly in that round.

### Acting out the dialogue

Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing.  Please record this interaction (for example, using Zoom's record feature).

\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*

[Video of Interaction.](https://drive.google.com/file/d/1kIuYyaoNEdOTw8ed-PBSLnhpHlMjkB-j/view?usp=sharing)

### Wizarding with the Pi (optional)
In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser.  You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*


# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...

There are a couple of things that I definitely think I could improve upon for the design of my device. First of all, the scenario in which the interaction occurs was very vague in the original video and storyboarding. I would like the interaction with the device to occur spontaneously (like the 1D joystick game outside of the Tata collaboratory space). The user sees something intriguing set up with an inviting phrase on it that makes them want to interact. I would like the interaction to be as simple as possible, the user should be able to go up to the device, press one button and begin to play the game. So to summarize the user interaction with my device:
* Set up as an interactive game  

* Occur spontaneously in an environment with lots of foot traffic (eg Tata space or Master's Studio)  

* Simple and transactional: press a button to play, don't need any instructions

2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?

An idea that I would like to implement would be a player vs player mode. This will involve two buttons and a _Family Feud_ styled gameplay where a math question is prompted and the first person to press their respective button gets to answer it. The score would be kept and a winner would be declared to encourage competition and therefore interaction.

3. Make a new storyboard, diagram and/or script based on these reflections.
![Lab3 Idea Updated](lab3part2storyboard.jpeg)

## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*

The system has two ways that the users interact with the device: the microphone and the buttons. On startup, the device prompts the user to press either button to start, and then the game begins. The device asks a random multiplication question and whoever presses their respective button first gets to answer the question. If the user gets it correct, their respective score is incremented by one, but if they get it wrong their score is decreased by one. There are a total of 10 (or 3 for the purpose of the video) questions and after the tenth question the device will tell the users the game is over and tell them the final score, it then prompts them to press either button to play again.

All of the code is included in _math_game.py_

*Include videos or screencaptures of both the system and the controller.*

My device worked on its own, so I did not opt to use the controller/wizarding.

[Video of a game between two users.](https://drive.google.com/file/d/1YK69hE4jI7ZQmN57-owkZDVUpz9nLWn0/view?usp=sharing)

## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?

What worked well was that the users were very into the game. The competition aspect made the users want to play and we even continued to play after filming. Although the slow response time to button presses and voice commands were very evident (especially in testing) it added another aspect to the game because the users found it funny when the device would mess up or hear them incorrectly.

### What worked well about the controller and what didn't?

The slow response times and subpar voice recognition of the device made playing a good game a little difficult. The users were a little _too_ into it and therefore they would press the button way too early for the device to recognize it. Same thing for the speech recognition. They would shout the number too fast and the device wouldn't be able to pick up on it. Other then that the device did work as intended.

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

I think in the design I could have made the device listen more actively so that I didn't have to create a microphone object every iteration. This would involve some multithreading, but I do believe it is achievable. The same goes for the buttons. It was single threaded so player 1 did have a slight advantage in response time.

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

I can use the voice interaction to create a dataset for the users. Besides that I can also add a motion detector to prompt users to use the device when they walk by.

