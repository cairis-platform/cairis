

def threatColourCode(valueId):
  if (valueId == 9): return '359 1 .5'
  elif (valueId > 9): return '359 1 .5'
  elif (valueId == 8): return '359 1 .7'
  elif (valueId == 7): return '6 .86 .44'
  elif (valueId == 6): return '10 .7 .94'
  elif (valueId == 5): return '19 .65 .99'
  elif (valueId == 4): return '27 .48 .99'
  elif (valueId == 3): return '34 .38 .99'
  elif (valueId == 2): return '36 .21 1'
  elif (valueId == 1): return '37 .07 1'
  elif (valueId < 1): return '37 .07 1'

def responseColourCode(valueId):
  if (valueId == 1): return '359 1 .5'
  elif (valueId == 2): return '359 1 .7'
  elif (valueId == 3): return '6 .86 .44'
  elif (valueId == 4): return '10 .7 .94'
  elif (valueId == 5): return '19 .65 .99'
  elif (valueId == 6): return '27 .48 .99'
  elif (valueId == 7): return '34 .38 .99'
  elif (valueId == 8): return '36 .21 1'
  elif (valueId == 9): return '37 .07 1'
  elif (valueId > 9): return '37 .07 1'

def usabilityColourCode(valueId):
  if (valueId <= 1): return '#F7FBFF'
  elif (valueId == 2): return '#DEEBF7'
  elif (valueId == 3): return '#C6DBEF'
  elif (valueId == 4): return '#9ECAE1'
  elif (valueId == 5): return '#6BAED6'
  elif (valueId == 6): return '#4292C6'
  elif (valueId == 7): return '#2171B5'
  elif (valueId == 8): return '#08519C'
  elif (valueId == 9): return '#08306B'
  elif (valueId > 9): return '#08306B'
