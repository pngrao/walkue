import getpass
import datetime
import time
import winsound
import os

preferences = {'interval' : 30, #in minutes test=0.25
              'auto_off' : True,
              'auto_off_time' : 8} #in hours test=0.0166

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
    print(f"{datetime.datetime.now():%I:%M:%S %p} : Starting Walkue.",
          f"Expect walk cues every {preferences['interval']} mins.")
    if preferences['auto_off']:
        print(" "*13, f"Walkue automatic turn off ON.",
              f"Stopping in {preferences['auto_off_time']} hrs.")
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
    if preferences['auto_off']:
        auto_off_time = preferences['auto_off_time'] * 3600
    interval = preferences['interval']*60
    cue_counter = 0

    while True:
        curr_time = int(time.time())
        try:
            if curr_time - start_time >= interval:
                print(f"{datetime.datetime.now():%I:%M:%S %p} : Walkue says, \'WALK!\'")
                sound_filename = 'media/sound/bugle.wav'
                winsound.PlaySound(sound_filename, winsound.SND_FILENAME)
                cue_counter += 1
                start_time = curr_time
            time.sleep(1)
        except RuntimeError:
            time_str = f"{datetime.datetime.now():%I:%M:%S %p} :"
            space_str = " "
            print(f"{time_str} Error: Failed to play sound.")
            print(f"{space_str * len(time_str)} Stopping Walkue. Take care!")
            continue
        except KeyboardInterrupt:
            print(f"{datetime.datetime.now():%I:%M:%S %p} : Ok {getpass.getuser()}.",
                  f"You\'ve stopped Walkue. Take care!")
            break

        try:
            if preferences['auto_off'] and \
                curr_time - primo_start_time >= auto_off_time:
                time_str = f"{datetime.datetime.now():%I:%M:%S %p} :"
                space_str = " "
                print(f"{time_str} Ok {getpass.getuser()}.",
                      f"Walkue's automatic turn off activated.")

                #write to final report file
                file_prefix_str = "walkue_summary_"
                date_time_str = f"{datetime.datetime.now():%h%d_%Y_%I-%M-%S%p}"
                directory_str = "report"
                if not os.path.exists(directory_str):
                    os.makedirs(directory_str)
                report_file = directory_str + "/" + file_prefix_str + date_time_str + ".log"
                with open(report_file, 'w') as f:
                    f.write(f"{date_time_str} : Run Done! Total Walkues sent in this session : {cue_counter}")
                if os.path.exists(report_file):
                    print(f"{space_str * len(time_str)} Log file : {report_file}")

                print(f"{space_str * len(time_str)} Stopping Walkue. Take care!")
                break
        except FileNotFoundError:
            time_str = f"{datetime.datetime.now():%I:%M:%S %p} :"
            space_str = " "
            print(f"{space_str * len(time_str)} FileNotFoundError: Failed to create final report.")
            print(f"{space_str * len(time_str)} Stopping Walkue. Take care!")
            break
        except OSError:
            time_str = f"{datetime.datetime.now():%I:%M:%S %p} :"
            space_str = " "
            print(f"{space_str * len(time_str)} OSError: Failed to create final report.")
            print(f"{space_str * len(time_str)} Stopping Walkue. Take care!")
            break

if __name__ == "__main__":
    main()
