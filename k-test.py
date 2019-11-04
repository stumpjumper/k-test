#!/usr/bin/env python3

import sys
import os

from getchLib import _Getch

getch = _Getch()

testLines = [
  ["Daugher",
   "Marlene"],
  ["Wing Commander",
   "Cadet Colonel Bryant K. Ashe"],
  ["10x2",
   "20"],
  ]

startSep = "======================="
endSep   = "-----------------------"

print ("Welcome to k-test. Type ctrl-c to exit, ctrl-a for answer.")

for question, answer in testLines:

  correct = False
  while not correct:
    correct = True
    print("Question:")
    print(question)
    #print(answer)
    for ansChar in answer:
      inChar = getch()
      print(inChar, end='', flush=True)
      if inChar in chr(12): # Found ctrl-l
        if os.name == 'nt':
          os.system('cls')
        else:
          os.system('clear') 
        correct = False
        break
      if inChar in [chr(3),chr(4),chr(7)]:
        print("Recieved ctrl-c, ctrl-d, or ctrl-g. Exiting...")
        sys.exit(0)
      if inChar == chr(1): # Found ctrl-a
        print()
        print(startSep)
        print("Answer:")
        print(answer)
        print(endSep)
        correct = False
        break
      if ansChar != inChar:
        print()
        print(startSep)
        print("Expecting: %s" % ansChar)
        print("Recieved : %s" % inChar)
        print(endSep)
        correct = False
        break
    if correct:
      print()
      print("Correct!!")
    

