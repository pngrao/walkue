import argparse
import getpass
import datetime
import time
import winsound
import os

def main():
    """
    Function prints welcome message and starts the cue timer as per user's preferences.
    Input: None
    Return: None
    """
    preferences = get_user_preferences()

    print(f"Welcome {getpass.getuser()}, Walkue is here to help!")
    start_time = int(time.time())

    time_str = f"{datetime.datetime.now():%I:%M:%S %p} :"
    space_str = " "
    print(f"{time_str} Starting Walkue.",
          f"Expect walk cues every {preferences['interval']} mins.")

    if preferences['auto_off']:
        print(f"{space_str * len(time_str)} Walkue automatic turn off feature is ON.",
              f"Stopping in {preferences['auto_off_time']} hrs.")
    else:
        print(f"{space_str * len(time_str)} Walkue automatic turn off feature is OFF.",
              f"Use ctrl+c to quit.")

    start_cue_timer(start_time, preferences)

def get_user_preferences():
    """
    Function collects user preferences by parsing the command line arguments.
    Default preferences are set via add_argument method of ArgumentParser class.
    Currently supported arguments:
    usage: walkue_main.py [-h] [-i INTERVAL] [-o] [-ot AUTO_OFF_TIME]
                      [-s {beep,bugle,buzzer}]

    optional arguments:
    -h, --help              show this help message and exit
    -i INTERVAL, --interval INTERVAL
                            positive time interval in minutes eg: 30, 45 etc
    -o, --auto_off          flag to enable or disable automatic off feature
    -ot AUTO_OFF_TIME, --auto_off_time AUTO_OFF_TIME
                            automatic off time in hours eg: 8, 9.5 etc
    -s {beep,bugle,buzzer}, --sound {beep,bugle,buzzer}
                            choose a sound cue : beep | bugle | buzzer
    Input:
    None
    Return:
    preferences (dict) : user preferences
    """
    #Define all default preferences here
    default_interval = 30 #0.25
    default_auto_off_time = 8 #0.0166
    default_sound = 'beep'

    #Create a parser object and parse all command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interval',\
                        help = 'positive time interval in minutes eg: 30, 45 etc',\
                        type = float, default = default_interval)
    parser.add_argument('-o', '--auto_off',\
                        help = 'flag to enable or disable automatic off feature',\
                        action = 'store_true')
    parser.add_argument('-ot', '--auto_off_time',\
                        help = 'automatic off time in hours eg: 8, 9.5 etc',\
                        type = float, default = default_auto_off_time)
    parser.add_argument('-s', '--sound',\
                        help = 'choose a sound cue : beep | bugle | buzzer',\
                        choices = ['beep', 'bugle', 'buzzer'],\
                        default = default_sound)
    args = parser.parse_args()

    #Raise ValueError if negative time values are input
    if args.interval < 0:
        raise ValueError('Time interval cannot be a negative value! ***This is not a time machine!***')
    if args.auto_off_time < 0:
        raise ValueError('Automatic off time cannot be a negative value! ***This is not a time machine!***')

    #Populate preferences dictionary with parsed arguments
    preferences = {'interval' : args.interval,
                  'auto_off' : args.auto_off,
                  'auto_off_time' : args.auto_off_time,
                  'sound' : args.sound}
    return preferences

def start_cue_timer(primo_start_time, preferences):
    """
    Function sends user, audio cue at set intervals.
    It also handles automatic turn off at specified time.
    KeyboardInterrupt exception is handled when user wants to quit.
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
    if preferences['sound'] == 'beep':
        beep_frequency = 3020
        beep_duration = 5000
    else:
        sound_filedir = 'media/sound/'
        sound_filename = preferences['sound'] + '.wav'
        sound_filepath = sound_filedir + sound_filename
    cue_counter = 0

    while True:
        curr_time = int(time.time())
        try:
            if curr_time - start_time >= interval:
                print(f"{datetime.datetime.now():%I:%M:%S %p} : Walkue says, \'WALK!\'")
                if preferences['sound'] == 'beep':
                    winsound.Beep(beep_frequency, beep_duration)
                else:
                    winsound.PlaySound(sound_filepath, winsound.SND_FILENAME)
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
