#!/usr/bin/env python3

import sys
import os

from getchLib import _Getch

getch = _Getch()

if len(sys.argv) > 1 and sys.argv[1].lower() in ["-h","--help"]:
  print("Usage: ktest.py <input_file_name>")
  sys.exit(0)
if len(sys.argv) != 2:
  print("k-test.py: Missing a single input file name on commnd line",file=sys.stderr)
  print("Expecting: ktest.py <input_file_name>",file=sys.stderr)
  sys.exit(1)

inputFilename = sys.argv[1]
print("inputFilename =", inputFilename)
with open(inputFilename, 'r') as inputFile:
    testLinesText = inputFile.read()

testLines = eval(testLinesText)

startSep = "======================="
endSep   = "-----------------------"

print ("Welcome to k-test.")
print ("Type: ctrl-c to exit.")
print ("      ctrl-a for answer.")
print ("      ctrl-l to clear screen and restart answer.")

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
      elif inChar in [chr(3),chr(4),chr(7)]:
        print("Recieved ctrl-c, ctrl-d, or ctrl-g. Exiting...")
        sys.exit(0)
      elif inChar == chr(1): # Found ctrl-a
        print()
        print(startSep)
        print("Answer:")
        print(answer)
        print(endSep)
        correct = False
      elif ansChar != inChar:
        print()
        print(startSep)
        print("Expecting: %s" % ansChar)
        print("Recieved : %s" % inChar)
        print(endSep)
        correct = False
      if not correct:
        break
    if correct:
      print()
      print(startSep)
      print("Correct!!")
      print(endSep)
      print()
    

