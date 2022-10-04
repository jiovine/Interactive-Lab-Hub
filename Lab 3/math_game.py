import speech_recognition as sr
import os
import random 
import subprocess
import qwiic_i2c
import qwiic_button
import time
import sys

# defining the two buttons
my_button1 = qwiic_button.QwiicButton()
my_button2 = qwiic_button.QwiicButton(0x5B)

# checks which button was pressed first
def button_press():
    while True:
        if my_button1.is_button_pressed() == True:
            return 1
        if my_button2.is_button_pressed() == True:
            return 2

        time.sleep(0.1)
    
# takes in a string and plays through speaker
def speak(s):
    inputcommand = 'espeak -ven+f3 -k5 -s150 --punct="<characters>" "%s" 2>>/dev/null' % s
    p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return output

# asks a random math question
def ask_question(p1, p2, count):
    if count == 3:
        speak('Final score.. Player 1 {}... Player 2 {}... Thank you for playing... Press either button to play again.'.format(p1, p2))
        start()
    elif count == 2:
        speak('Final Question...')
    n, m = random.randrange(2, 10), random.randrange(2, 10)
    s = 'What is {} times {}'.format(n, m)
    speak(s)
    count+=1
    check_answer(n*m, p1, p2, count)

# gets the first number said by the user trying to answer the question, ignores any speech that isn't a number
def get_int_answer():
    # transforming speech into array
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    with mic as source:
        audio = r.listen(source, 10, 3)
    try:
        k = r.recognize_google(audio).split(' ')
    except sr.RequestError:
        # api is down
        raise RuntimeError("API unavailable")
    except sr.UnknownValueError:
        # speech was incoherent or nothing was said
        speak('I am sorry something went wrong, please press a button to play again.')
        start()
    
    # pulling the last integer said
    num = None
    for item in k:
        if item.isnumeric():
            num = int(item)
    # raising error if no integer was said
    if not num:
        speak('Please say an integer.')
        get_int_answer()

    return num

# checks who pressed button first and if they get it correct properly adjusts the score
def check_answer(ans, p1, p2, count):
    if button_press() == 1:
        speak('Player 1')
        if ans == get_int_answer():
            speak('Correct.')
            p1+=1
            ask_question(p1, p2, count)
        else:
            speak('I am sorry that is incorrect.')
            #speak('Final score.. Player 1 {}... Player 2 {}... Thank you for playing... Press either button to play again.'.format(p1, p2))
            #start()
            p1-=1
            ask_question(p1, p2, count)
    else:
        speak('Player 2')
        if ans == get_int_answer():
            speak('Correct.')
            p2+=1
            ask_question(p1, p2, count)
        else:
            speak('I am sorry that is incorrect.')
            #speak('Final score.. Player 1 {}... Player 2 {}... Thank you for playing... Press either button to play again.'.format(p1, p2))
            #start()
            p2-=1
            ask_question(p1, p2, count)


# idle/start state of the game
def start():
    t = button_press()
    if t >= 0:
        speak('Welcome, lets begin.')
        ask_question(p1=0, p2=0, count=0)

speak('Press any button to begin')
start()