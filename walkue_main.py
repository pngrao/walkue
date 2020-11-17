import getpass
import datetime
import time
import winsound

preferences = {'interval' : 30, #in minutes test=0.25
              'auto_off' : True,
              'auto_off_time' : 8} #in hours test=0.01

def main():
    """
    Function prints welcome message.
    It starts the cue timer as per user preferences.
    TODO: get custom user preferences
    Input: None
    Return: None
    """
    print(f"Welcome {getpass.getuser()}, Walkue is here to help!")
    start_time = int(time.time())
    print(f"Your walk cue will appear every {preferences['interval']} mins.")
    start_cue_timer(start_time, preferences)

def start_cue_timer(primo_start_time, preferences):
    """
    Function sends user audio cue at set intervals.
    It also handles automatic turn off at specified time.
    KeyboardInterrupt exception is handled.
    Input:
    primo_start_time (int) : application start time in seconds
    preferences (dict) : user preferences
    Return:
    None
    """
    start_time = primo_start_time
    auto_off_time = preferences['auto_off_time'] * 3600
    interval = preferences['interval']*60
    while True:
        curr_time = int(time.time())
        try:
            if preferences['auto_off'] and \
                curr_time - primo_start_time >= auto_off_time:
                print(f"Ok {getpass.getuser()}. Walkue's automatic turn off activated.")
                print("Stopping Walkue. Take care!")
                break
        except KeyboardInterrupt:
            print(f"Ok {getpass.getuser()}. You\'ve stopped Walkue.")
            print("Take care!")
            break

        try:
            if curr_time - start_time >= interval:
                print(f"{datetime.datetime.now():%I:%M:%S %p} : Walkue says WALK!")
                beep_frequency = 3020
                beep_duration = 5000
                winsound.Beep(beep_frequency, beep_duration)
                start_time = curr_time
            time.sleep(1)
        except KeyboardInterrupt:
            print(f"Ok {getpass.getuser()}. You\'ve stopped Walkue.")
            print("Take care!")
            break

if __name__ == "__main__":
    main()
