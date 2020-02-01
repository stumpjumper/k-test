#!/usr/bin/env python3

import sys
import os
import time
from optparse import OptionParser
from getchLib import _Getch

getch = _Getch()

wrongCountMaxDefault = 1

ctrlHelp = \
'''\
Type: ctrl-a to see the answer.
      ctrl-n for next question.
      ctrl-p for previous question.
      ctrl-l to clear screen and restart answer.
      ctrl-h to see this control character help.
      ctrl-c or ctrl-d to exit.\
'''


def setupCmdLineArgs(cmdLineArgs):
  usage =\
"""\
%prog [-h|--help] [options] input_file
"""
  usage += os.linesep + ctrlHelp
  parser = OptionParser(usage)
                       
  help="verbose mode."
  parser.add_option("-v", "--verbose",
                    action="store_true", default=False,
                    dest="verbose",
                    help=help)
  help="Number of tries per character. Default is %default"
  parser.add_option("-t", "--tries",
                    type=int,
                    dest="wrongCountMax",
                    metavar='num',
                    default=wrongCountMaxDefault,
                    action='store',
                    help=help)
  
  (cmdLineOptions, cmdLineArgs) = parser.parse_args(cmdLineArgs)

  numArgs = len(cmdLineArgs)

  if cmdLineOptions.verbose:
    print("cmdLineOptions:",cmdLineOptions)
    for index in range(0,numArgs):
      print( "cmdLineArgs[%s] = '%s'" % (index, cmdLineArgs[index]))

  if numArgs != 1:
    parser.error("Did not find an input file name on the command line")

  return (cmdLineOptions, cmdLineArgs)

def main(cmdLineArgs):
  (clo, cla) = setupCmdLineArgs(cmdLineArgs)

  inputFilename = cla[0]
  wrongCountMax = clo.wrongCountMax

  if clo.verbose:
    print("inputFilename = '%s'" % inputFilename)
    print("wrongCountMax = %s"   % wrongCountMax)

  startSep = "======================="
  endSep   = "-----------------------"

  print()
  print("Welcome to k-test.")
  print(ctrlHelp)
  print()
  print("You will have %s chance per character." % wrongCountMax,
        "Use -t option to change" )
  print()
  print("inputFilename =", inputFilename)
  with open(inputFilename, 'r') as inputFile:
      testLinesText = inputFile.read()

  testLines = eval(testLinesText)
  numTestLines = len(testLines)
  testLinesIndex = 0

  while testLinesIndex < numTestLines:
    (question, answer) = testLines[testLinesIndex]
    getNewQuestion = False

    correct = False
    while not correct:
      correct = True
      print(startSep)
      print("Question:")
      print(question)
      time.sleep(.5) # Get rid of any extra typing
      answerSoFar = ""
      for ansChar in answer:
        tryAgain = True
        wrongCount = 0
        while tryAgain and correct:
          inChar = getch()
          print(inChar, end='', flush=True)
          # Ctrl-h
          if inChar == chr(8):
            print()
            print("Help on control characters:")
            print(ctrlHelp)
            correct = False
          # Ctrl-n 
          elif inChar == chr(14):
            testLinesIndex += 1
            getNewQuestion = True
          # Ctrl-p
          elif inChar == chr(16):
            testLinesIndex = max(testLinesIndex-1,0)
            getNewQuestion = True
          # Ctrl-l 
          elif inChar == chr(12):
            if os.name == 'nt':
              os.system('cls')
            else:
              os.system('clear') 
            correct = False
          # Ctrl-c, Ctrl-d
          elif inChar in [chr(3),chr(4)]:
            print("Recieved ctrl-c or ctrl-d. Exiting...")
            sys.exit(0)
          # Ctrl-a
          elif inChar == chr(1):
            print()
            print(startSep)
            print("Answer:")
            print(answer)
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
              print("Recieved : %s" % str(inChar))
              correct = False
          # If made it here, character is not correct or ctrl char found
          # so set flags and move on to next character
          answerSoFar += str(inChar)
          tryAgain = False
          wrongCount = 0
          if getNewQuestion:
            correct = False
            break # while try again
        if getNewQuestion:
          break
        elif not correct:
          break # for next char
      if getNewQuestion:
        break # while not correct
      elif correct:
        testLinesIndex += 1
        print()
        print(startSep)
        print("Correct!!")
    
if (__name__ == '__main__'):
  main(sys.argv[1:])
