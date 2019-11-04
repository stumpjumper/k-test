#!/usr/bin/env python3

import sys
import os
from optparse import OptionParser
from getchLib import _Getch

getch = _Getch()

wrongCountMaxDefault = 1

def setupCmdLineArgs(cmdLineArgs):
  usage =\
"""\
%prog [-h|--help] [options] input_file\
"""
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
    parser.error("Did not fine an input file name on the command line")

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

  print("Welcome to k-test.")
  print("Type: ctrl-c to exit.")
  print("      ctrl-a for answer.")
  print("      ctrl-l to clear screen and restart answer.")
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
          # If made it here, character is correct, so reset flags
          # and move on to next character
          answerSoFar += inChar
          tryAgain = False
          wrongCount = 0
        if not correct:
          break
      if correct:
        testLinesIndex += 1
        print()
        print(startSep)
        print("Correct!!")
        print(endSep)
        print()
    
if (__name__ == '__main__'):
  main(sys.argv[1:])
