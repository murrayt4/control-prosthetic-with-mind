#Imports necessary libraries
from InsightCom import *#Imports InsightCom class
from ArmCom import *#Imports ArmCom class
from datetime import datetime
import time
import serial
import json
import urllib2

# -------------------------------------------------------------------------
# Make dictionary for logEmoState
header = ['Time', 'UserID', 'wirelessSigStatus', 'Blink', 'leftWink',
          'rightWink', 'Surprise', 'Frown',
          'Smile', 'Clench',
          'MentalCommand Action', 'MentalCommand Power']
emoStateDict = {}
for emoState in header:#Loops throguh each value in header
    emoStateDict.setdefault(emoState, None)#Sets default emoState values to None if no key is returned.

def send_emo_state_to_arduino(blink_count):
    #Sets value of all key pairs to values recieved from API in Insight class
    emoStateDict['Time'] = insight.get_time_from_start(insight.eState)
    emoStateDict['UserID'] = insight.get_userID(insight.eEvent, insight.user)
    emoStateDict['wirelessSigStatus'] = insight.get_wireless_signal_status(insight.eState)
    emoStateDict['Blink'] = insight.get_facial_expression_is_blink(insight.eState)
    emoStateDict['leftWink'] = insight.get_left_wink(insight.eState)
    emoStateDict['rightWink'] = insight.get_right_wink(insight.eState)

    emoStateDict['Surprise'] = insight.get_surprise(insight.eState)
    emoStateDict['Frown'] = insight.get_frown(insight.eState)
    emoStateDict['Clench'] = insight.get_clench(insight.eState)
    emoStateDict['Smile'] = insight.get_smile(insight.eState)

    emoStateDict['MentalCommand Action'] = insight.get_mental_command_current_action(insight.eState)
    emoStateDict['MentalCommand Power'] = insight.get_mental_command_current_action_power(insight.eState)
    #Creates tuple of these parameters
    #emoStateTuple = (emoStateDict['Time'], emoStateDict['UserID'],
    #                emoStateDict['wirelessSigStatus'], emoStateDict['Blink'],
    #                 emoStateDict['leftWink'], emoStateDict['rightWink'],
    #                 emoStateDict['Surprise'], emoStateDict['Frown'],
    #                 emoStateDict['Clench'], emoStateDict['Smile'],
    #                 emoStateDict['MentalCommand Action'],
    #                 emoStateDict['MentalCommand Power'])

    #valToArduino(emoStateTuple) Only need this to send emostates to arduino, dont need that
    #check_blink(emoStateTuple)
    #Formats data to be sent to cloud computer via HTTP
    data = "time=" + str(emoStateDict['Time']) + "&userid=" + str(emoStateDict['UserID']) + "&signal=" + str(emoStateDict['wirelessSigStatus']) + "&blink=" + str(emoStateDict['Blink'])+ "&leftwink=" + str(emoStateDict['leftWink']) + "&rightwink" + str(emoStateDict['rightWink']) + "&surprise" + str(emoStateDict['Surprise']) + "&frown=" + str(emoStateDict['Frown']) + "&clench=" + str(emoStateDict['Clench']) + "&smile=" + str(emoStateDict['Smile']) + "&mentalaction=" + str(emoStateDict['MentalCommand Action']) + "&mentalpower=" + str(emoStateDict['MentalCommand Power'])
    #data = "time=1&userid=2&signal=3&blink=4&leftwink=5&rightwink=6&surprise=7&frown=8&clench=9&smile=10&mentalaction=11&mentalpower=12"
    #print data
    #Dumps data to remote server
    req = urllib2.Request("http://18.223.15.149:8000/notes")
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib2.urlopen(req, data)
    #Checks if user blinks, if so sends command
    if insight.get_facial_expression_is_blink(insight.eState) == 1:
        blink_count = blink_count + 1
        if blink_count == 2:
            motor_on()
            print "motor on"
            blink_count = 0
            return blink_count
        else:
            return blink_count
    else:
        blink_count = 0
        return blink_count
#def check_blink(emoStateTuple):#Check the blink state of headset parameters, call motor on function if high, call motor off if low
#    if emoStateTuple[3] == 1:
#        blink_count = 1
#        print blink_count
#        if blink_count == 2:
#            motor_on()
#            blink_count = 0
#    return blink_count
    #elif emoStateTuple[3] == 0:
    #    motor_off()
    
# # -------------------------------------------------------------------------
#
# # connect to Arduino

print "==================================================================="
print "Please enter port for Arduino"
print "==================================================================="
print "Example:"
print "Mac -- \n /dev/tty.usbmodem1451 "
print "Windows -- \n COM6"
print ">>"
arduino_port = str(raw_input())#Recieves keyobard input from user
setupSerial(arduino_port)
# -------------------------------------------------------------------------
# start EmoEngine or EmoComposer

print "==================================================================="
print "Example to show how to log EmoState from EmoEngine/EmoComposer."
print "==================================================================="
print "Press '1' to start and connect to the EmoEngine                    "
print "Press '2' to connect to the EmoComposer                            "
print ">> "

log_from_emo = int(raw_input())
# -------------------------------------------------------------------------

# instantiate Insight class
if log_from_emo == 1:
    insight = Insight()
elif log_from_emo == 2:
    insight = Insight(composerConnect=True)
else:
    print "option = ?"

print "Start receiving Emostate! Press any key to stop logging...\n"

# connect insight instance to Xavier composer or EmoEngine
insight.connect()
last_command = None

# event loop to update Insight state
#need while loop to run every 7.8ms for 128 hz
blink_count = 0
while (1):#Determine if the event is a blink, if so call motor on function
    # set of operations to get state from Insight
    # returns 0 if successful
    #now = time.time()
    #print now
    #print blink_count
    state = insight.get_state(insight.eEvent)
    if state== 0:
        # event types IEE_Event_t returns 64 if EmoStateUpdated
        eventType = insight.get_event_type(insight.eEvent)
        user_ID = insight.get_userID(insight.eEvent, insight.user)
        if eventType == 64:
            insight.get_engine_event_emo_state(insight.eEvent, insight.eState)
            timestamp = insight.get_time_from_start(insight.eState)
            blink_count = send_emo_state_to_arduino(blink_count)#Keeps track of blink count
            #print "%10.3f New EmoState from user %d ...\r" % (timestamp,
                                                              #user_ID)
                
            #Limit the command rate so that we won't overflow the buffer
            #if not last_command:
            #    last_command = datetime.now()
            #    send_emo_state_to_arduino()
            #else:
            #    diff = datetime.now()-last_command
            #    if (diff.microseconds/1000.0 > 250.0):
            #        last_command = datetime.now()
            #        send_emo_state_to_arduino()
    elif state != 0x0600:
        print "Internal error in Emotiv Engine ! "
    #elapsed = time.time() - now
    #print elapsed


