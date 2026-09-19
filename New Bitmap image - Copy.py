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

def rint(text, r, g, b ,):
     print(f"\033[38;2;{r};{g};{b}m{text}\033[0m")

def sint(text, r, g, b ,u):
    print(f"\033[38;2;{r};{g};{b}m{text} m{u}\033[0m")


while pee_pee_poo_poo < 2:    
    rint("  ------------------------                                 -------------------             ", 255, 0 ,0,)
    rint("  :                      :                                 :                 :             ", 250, 10 ,0,)
    rint("  :                      :                                 :                 :             ", 240, 20 ,0,)
    rint("  :                      :                                 :                 :             ", 230, 30 ,0,)
    rint("  :                      :                                 :                 :             ", 220, 40, 0,)
    rint("  ------------------------                                 -------------------              ", 210, 50, 0,)
    rint("                                                                                           ", 200, 60, 0,)
    rint("           -----------------------------------------------------------                     ", 190, 70, 0,)
    
    time.sleep(1)
    cls()
    rint("                                                                                           ", 170, 60, 0, )
    rint("                                                                                           ", 160, 60, 0, )
    rint("  ------------------------                                  ---------------                ", 150, 80, 0, )
    print("                                                                                           ")
    print("                                                                                           ")
    print("                                                                                           ")
    print("                                                                                           ")
    rint("           -----------------------------------------------------------                     ", 120, 110, 0,)
    time.sleep(0.25)
    cls()
    pee_pee_poo_poo += 1


while True:

 pupp = text
if pupp  == "com" :
    rint("convrt from short to invester", 255, 40, 0)
    pupp = input()

    if pupp in ("good", "keep go"):
        defn == "it migt kill us all or some thing bad."

    sint( "", 255, 50, 0, defn)


