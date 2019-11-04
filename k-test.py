#!/usr/bin/env python3

import sys
import os

from getchLib import _Getch

getch = _Getch()

wrongCountMax = 1

usageMsg = "Usage: ktest.py [<num_bad_chars] <input_file_name>"
if len(sys.argv) > 1 and sys.argv[1].lower() in ["-h","--help"]:
  print(usageMsg)
  sys.exit(0)
if len(sys.argv) < 2 or len(sys.argv) > 3:
  print("k-test.py: Expecting either one or two arguments. Got",
        len(sys.argv)-1,file=sys.stderr)
  print(usageMsg,file=sys.stderr)
  sys.exit(1)

if len(sys.argv) == 3:
  try:
    wrongCountMax = int(sys.argv[1])
  except ValueError:
    print("k-test.py: Found 2 arguments but could not convert",end="",
          file=sys.stderr)
    print("1st arg '%s' into an integer for number of bad characters" % sys.argv[1],
          file=sys.stderr)
    print(usageMsg,file=sys.stderr)
    sys.exit(0)
  inputFilename = sys.argv[2]
if len(sys.argv) == 2:
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
    answerSoFar = ""
    for ansChar in answer:
      tryAgain = True
      wrongCount = 0
      while tryAgain and correct:
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
          wrongCount += 1
          if wrongCount < wrongCountMax:
            print()
            print("Wrong char '%s', try again" % inChar)
            print(answerSoFar,end='',flush=True)
            continue
          else:
            print()
            print(startSep)
            print("Expecting: %s" % ansChar)
            print("Recieved : %s" % inChar)
            print(endSep)
            correct = False
        answerSoFar += inChar
        tryAgain = False
        wrongCount = 0
      if not correct:
        break
    if correct:
      print()
      print(startSep)
      print("Correct!!")
      print(endSep)
      print()
    

