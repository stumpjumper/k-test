#!/usr/bin/env python3

import sys

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

print ("Welcome to k-test. Type ctrl-c to exit")

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
      if inChar in  [chr(3),chr(4),chr(7)]:
        print("Recieved ctrl-c, ctrl-d, or ctrl-g. Exiting...")
        sys.exit(0)
      if ansChar != inChar:
        print()
        print("----------------------------------")
        print("Expecting: %s" % ansChar)
        print("Recieved : %s" % inChar)
        print("----------------------------------")
        correct = False
        break
    if correct:
      print()
      print("Correct!!")
    

