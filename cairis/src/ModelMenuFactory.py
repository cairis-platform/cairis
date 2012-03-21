import gtk

def build(modelType):
  if (modelType == 'goal'):
    return ['And Goal','Or Goal','Goal','Sub Goal','And Requirement','Sub Requirement','Assign Responsibility']
  elif (modelType == 'obstacle'):
    return ['And Obstacle','Or Obstacle','','','','','']
  elif (modelType == 'class'):
    return ['Associate']
  else:
    return []
