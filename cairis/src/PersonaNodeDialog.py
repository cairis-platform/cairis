#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonaNodeDialog.py $ $Id: PersonaNodeDialog.py 249 2010-05-30 17:07:31Z shaf $
import sys
import gtk
from NDImplementationDecorator import NDImplementationDecorator

class PersonaNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("PersonaNodeDialog")
    self.decorator = NDImplementationDecorator(builder) 
    self.decorator.updateTextCtrl("personaNameCtrl",objt.name())
    self.decorator.updateMLTextCtrl("personaActivitiesCtrl",objt.activities())
    self.decorator.updateMLTextCtrl("personaAttitudesCtrl",objt.attitudes())
    self.decorator.updateMLTextCtrl("personaAptitudesCtrl",objt.aptitudes())
    self.decorator.updateMLTextCtrl("personaMotivationsCtrl",objt.motivations())
    self.decorator.updateMLTextCtrl("personaSkillsCtrl",objt.skills())
    self.decorator.updateImageCtrl("personaImageCtrl",objt.image())

    self.decorator.updateTextCtrl("personaDirectCtrl",objt.directFlag(environmentName,dupProperty))
    roles = []
    for role in objt.roles(environmentName,dupProperty):
      roles.append([role])
    self.decorator.updateListCtrl("personaRolesCtrl",['Role'],gtk.ListStore(str),roles)
    self.decorator.updateMLTextCtrl("personaNarrativeCtrl",objt.narrative(environmentName,dupProperty))

    self.window.resize(400,400)

  def on_personaOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
