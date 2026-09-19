import time
import os
import platform
import keyboard
text = input("waiting for input")
pupp = ""
pee_pee_poo_poo = 0
run = 0
scr = "###"
test = 0
rgb1 = 0,0,0
rgb2 = 0,0,0
rgb3 = 0,0,0
key = keyboard.read_key()
defn = ""

def rese():
    scr = " "


def cls():
    # Detect OS and run the appropriate clear command
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def rint(text, r, g, b):
     print(f"\033[38;2;{r};{g};{b}m{text}\033[0m")

def sint(text, r, g, b, txt, defn):
    print(f"\033[38;2;{r};{g};{b}m{text} {txt} {defn}\033[0m")

while True:
 
        pupp = input("commands")
        if pupp  == "com" :
            rint("convrt from short to invester", 255, 40, 0)
            pupp = input()

            if pupp in ("good", "keep", "going"):
                defn = "it migt kill us all or some thing bad. not marketing"

            if pupp in ("bad", "stop", "help"):
                defn = "it is getting better!"




        if pupp  == "decom" :
            rint("convrt from invester to short", 255, 40, 0)
            pupp = input()

            if pupp in ("kill", "something bad", "not marketing"):
                defn = "good, keep, help"

            if pupp in ("it is", "better", " getting"):
                defn = "bad, stop help"

        sint( "", 255, 50, 0, "", defn)
