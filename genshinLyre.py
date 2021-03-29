import midi
import keyboard
import time
import math
import win32api
import win32con
import PySimpleGUI as sg

VK_CODE = {
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A,
           }
#midi_to_vk = list('zxcvbnmasdfghjqwertyu')
white_key = {'48': 'z', '50': 'x', '52': 'c', '53': 'v', '55': 'b', '57': 'n', '59': 'm', '60': 'a', '62': 's', '64': 'd', '65': 'f', '67': 'g', '69': 'h', '71': 'j', '72': 'q', '74': 'w', '76': 'e', '77': 'r', '79': 't', '81': 'y', '83': 'u'}
black_key = {'49': 'x', '51': 'c', '54': 'b', '56':'n' , '58':'m', '61' : 'a', '63' : 's', '66' : 'g', '68':'h', '70' : 'j', '73': 'w', '75': 'e', '78' : 't' , '80' : 'y', '82':'u'}

def shift(semitone = 0):
    global white_key;
    new_map = {}
    for key,value in white_key.items():
    	new_map[str(int(key)+semitone)] = value;
    white_key = new_map

def read(file):
    global pattern
    global sleep
    pattern = midi.read_midifile(file)
    for x in pattern:
        for y in x:
            if type(y) == midi.SetTempoEvent:
                sleep = (60 * 1000000 / y.get_bpm() / 1000000.0 / 50)
                return

def find_scroll_time(channel = 0):
    global t
    global pattern
    local_t = 0
    for x in pattern[channel]:
        if type(x) == midi.NoteOnEvent or type(x) == midi.NoteOffEvent:
            local_t += x.tick
    t = max(t,local_t)

def add_pattern(channel = 0):
    global scroll
    global pattern
    Ttime = 0
    for x in pattern[channel]:
        if type(x) == midi.NoteOnEvent:
            scroll[Ttime] += [x.data[0]]
            Ttime += x.tick
        elif type(x) == midi.NoteOffEvent:
           Ttime += x.tick

#len(pattern)
def play():
    global scroll
    global sleep
    for x in scroll:
        for y in x:
            if str(y) in white_key:
                key = white_key[str(y)]
                if key != None:
                    win32api.keybd_event(VK_CODE[key],0,0,0)
                    win32api.keybd_event(VK_CODE[key],0 ,win32con.KEYEVENTF_KEYUP ,0)
        time.sleep(sleep)


# Create an event loop
scroll = []
t = 0
pattern = []
sleep = 100


layout =  [[sg.In() ,sg.FileBrowse(file_types=(("Midi", "*.mid"),))],
            [sg.Button("COMPUTE"),sg.Text('Semitone shift'),sg.InputText('0',size=(2, 1))],[sg.Button("PLAY")],
            [sg.Text('Made by: TENTEN youtube.com/c/TenTenGaming/')]
            #[sg.Text('BPM override'),sg.InputText('0',size=(3, 1)),sg.Button("OVERRIDE")]
            ]
# Create the window
window = sg.Window("Tenten Genshin Lyre player", layout)


while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if(values['Browse'] != ""):
        pattern = []
        read(values['Browse'])
    #if(event == "OVERRIDE"):
    #    sleep = (60 * 1000000 / values[2] / 1000000.0 / 200)
    if(event == "COMPUTE"):
        t = 0
        for i in range(len(pattern)):
            find_scroll_time(i)
        scroll = [[] for i in range(t+1)]
        for i in range(len(pattern)):
            add_pattern(i)
        print("done computing")
    if(event == "PLAY"):
        shift(int(values[1]))
        time.sleep(3)
        play()

    if event == sg.WIN_CLOSED:
        break

window.close()
