import csv
import random
from tkinter import *
from datetime import datetime

#Main function that writes the csv
#Inputs
#spatialFreq: string value of spatial frequencies or single value
#name: string representing name of the csv file; will       automatically add .csv suffix
#flipFreq: string value of phase reversal frequency
#time1: string representation of initial gray screen time in seconds.
#time2: string representation of inter stimulus gray screen time in seconds
#angle: string of multiple or single orientation values
#contrast: string of multiple or single contrast values
#numblocks: string representation of number of blocks
#numFlips: string of number of phase reversals (1 reversal contains 2 stimulus)



def genCsv(spatialFreq, name, flipFreq, time1, time2, angle, contrast, numBlocks, numFlips):
  #If string contains a comma, split input into a list
  if ',' in spatialFreq:
    deck = spatialFreq.split(',')
  if ',' in angle:
    angles = angle.split(',')
  if ',' in contrast:
    contrasts = contrast.split(',')
  #If string does not contain a comma, it is a single value
  if ',' not in spatialFreq:
    deck = [spatialFreq]
  if ',' not in angle:
    angles = [angle]
  if ',' not in contrast:
    contrasts = [contrast]

#Convert string values to integers. This is important for contrast since bonsai takes in values between -1 and 1. Example a 50 percent contrast is .5.
  for i in range(len(contrasts)):
    contrasts[i] = (float(contrasts[i])) / 100

  flipFreq = int(flipFreq)
  time1 = int(time1)
  time2 = int(time2)
  numBlocks = int(numBlocks)
  numFlips = int(numFlips)

  numFlips = numFlips * 2

  #Convert hz to time. Example, 2 hz is .5 seconds per stimuli
  flipFreq = 1 / flipFreq

  #Creates a list of all possible stimulus parameters
  params = []
  for x in deck:
    for y in angles:
      for z in contrasts:
        list = [x, y, z]
        params.append(list)

  #Writing the CSV file
  header = ['Spatial', 'Orientation', 'Duration', 'contrast', 'Flip']
  with open(name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    #Write the gray screen
    writer.writerow(header)

    #Write the initial gray screen. Input for screen is in seconds so we need to convert seconds to number of stimuli by using hz.
    alt = 1
    grayFlip1 = int(time1 / flipFreq)
    for x in range(grayFlip1):
      initScreen = [100000, 0, flipFreq, 0, alt]
      writer.writerow(initScreen)
      alt = alt/(-1)

    #Write the Blocks
    
    grayFlip2 = int(time2 / flipFreq)

    for x in range(0, numBlocks):
      random.shuffle(params)
      for param in params:
        for i in range(numFlips):
          line = [param[0], param[1], flipFreq, param[2], alt]
          #This line generates the reversal of contrast. (Alternates between positive and negative value)
          param[2] = param[2] / -1
          writer.writerow(line)
          alt = alt/ (-1)
        for i in range(grayFlip2):
          betweenScreen = [100000, 0, flipFreq, 0, alt]
          writer.writerow(betweenScreen)
          alt = alt/ (-1)


#This function is run to check if the values entered into the gui are valid. For example, a contrast of over 100 results in a pop up error message.
def errorCheck(spatialFreq, name, flipFreq, time1, time2, angle, contrast,numBlocks, numFlips):
  if not numBlocks.isnumeric():
    top = Toplevel(master)
    txt = Label(top, text = "Please enter an integer value for number of blocks.").grid(row = 1)
    return False
  if not numFlips.isnumeric():
    top = Toplevel(master)
    txt = Label(top, text = "Please enter an integer value for number of phase reversals.").grid(row = 1)
    return False
  if not flipFreq.isnumeric():
    top = Toplevel(master)
    txt = Label(top, text = "Please enter an integer value for Phase Reversal Frequency.").grid(row = 1)
    return False
  if not time1.isnumeric():
    top = Toplevel(master)
    txt = Label(top, text = "Please enter an integer value for initial gray screen.").grid(row = 1)
    return False
  if not time2.isnumeric():
    top = Toplevel(master)
    txt = Label(top, text = "Please enter an integer value for interstimulus Gray Screen.").grid(row = 1)
    return False
  for x in spatialFreq:
    if x.isalpha():
      top = Toplevel(master)
      txt = Label(top, text = "Please enter a whole number or decimal for Spatial Freqency.").grid(row = 1)
      return False
  for x in angle:
    if x.isalpha():
      top = Toplevel(master)
      txt = Label(top, text = "Please enter a whole number or decimal for Orientation.").grid(row = 1)
      return False
  for x in contrast:
    if x.isalpha():
      top = Toplevel(master)
      txt = Label(top, text = "Please enter a whole number or decimal for Spatial Freqency.").grid(row = 1)
      return False
    if int(contrast) > 100:
      top = Toplevel(master)
      txt = Label(top, text = "Please enter a value for contrast between 0 and 100.").grid(row = 1)
      return False
  else:
    return True
  

  
#On button press, handles default values
#If blank, set the default value
def buttonPress(spatialFreq, name, flipFreq, time1, time2, angle, contrast,numBlocks, numFlips):
  now = datetime.now()
  dt_str = now.strftime("%d_%m_%Y_%H_%M_%S")  
  name = name + "_" + dt_str + ".csv"
  if spatialFreq == '':
    spatialFreq = ".05"
  if flipFreq == '':
    flipFreq = '2'
  if time1 == '':
    time1 = '120'
  if time2 == '':
    time2 = '30'
  if angle == '':
    angle = "45"
  if contrast == '':
    contrast = "100"
  if numBlocks == '':
    numBlocks = '3'
  if numFlips == '':
    numFlips = '30'

    #With blank inputs set to default values, call the genCsv function.
  if errorCheck(spatialFreq, name, flipFreq, time1, time2, angle, contrast,numBlocks, numFlips):
    genCsv(spatialFreq, name, flipFreq, time1, time2, angle, contrast, numBlocks,numFlips)
  

#GUI Code
master = Tk()
master.title("Stimulus Parameters")
Label(master, text='Spatial Frequency (cpd) [.05]').grid(row=0)
Label(master, text='Orientation(s) (deg) [45]').grid(row=1)
Label(master, text='Contrast(s) (%) [100]').grid(row=2)
Label(master,
      text="-------------------------------------------------").grid(row=3)
Label(master, text='Phase Reversal Frequency (Hz) [2]').grid(row=4)
Label(master, text='Num Phase Reversals [30]').grid(row=5)
Label(master, text='Num Blocks [3]').grid(row=6)
Label(master, text="Initial Gray Screen (sec) [120]").grid(row=7)
Label(master, text="Interstimulus Gray Screen (sec) [30]").grid(row=8)
Label(master, text='File Name').grid(row=9)

spatFreq1 = Entry(master)
Angle1 = Entry(master)
Cont1 = Entry(master)
flipFreq1 = Entry(master)
numFlips1 = Entry(master)
numBlocks1 = Entry(master)
timeG1 = Entry(master)
timeG2 = Entry(master)
fName = Entry(master)

spatFreq1.grid(row=0, column=1)
Angle1.grid(row=1, column=1)
Cont1.grid(row=2, column=1)
flipFreq1.grid(row=4, column=1)
numFlips1.grid(row=5, column=1)
numBlocks1.grid(row=6, column=1)
timeG1.grid(row=7, column=1)
timeG2.grid(row=8, column=1)
fName.grid(row=9, column=1)

button1 = Button(master,
                 text=' Generate ',
                 fg='black',
                 bg='green',
                 command=lambda: buttonPress(spatFreq1.get(), fName.get(
                 ), flipFreq1.get(), timeG1.get(), timeG2.get(), Angle1.get(
                 ), Cont1.get(), numBlocks1.get(), numFlips1.get()),
                 height=1,
                 width=7)
button1.grid(row=10, column=1)
