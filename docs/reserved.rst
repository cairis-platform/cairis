Reserved characters in object names
===================================

When creating most new objects in CAIRIS, you need to provide a name.

The following characters are considered reserved and should be avoided when defining any object name: < > ' ` " \\ : % _ * / ? # £ $ &.   
You should also avoid using any non-ASCII characters.

The CAIRIS UI should warn you if you are about to create or update an object with a reserved character.  If your object includes these characters, it may be possible for you to add the object, but you may get problems update or deleting them, or exporting model files containing the objects

When using the `Persona Helper <https://chrome.google.com/webstore/detail/persona-helper/mhojpjjecjmdbbooonpglohcedhnjkho?hl=en-GB>`_, you may be diligently ensuring that spurious characters like ampersands don't creep into your factoid names.  However, you may not notice that the web page you work with may contain reserved characters like ampersands and, once you create a factoid from the page, an external document will be created in CAIRIS containing the reserved character/s.  This doesn't cause any problems while working with your model or even exporting it, but you will likely get errors about your model not being 'well-formed' when trying to import it back into CAIRIS.

There are no easy ways of getting around this problem in the Persona Helper extension, but there are two easy ways within CAIRIS itself to avoid or work-around this problem.

1.  Go to the UX/External Documents menu and, if you see any external documents with reserved characters in their names, simply remove them from CAIRIS.

2.  If you forget to do this and discover an error when importing the model file, you can easily remove the offending characters from the model file itself. If you have exported your model as 'Model (XML file)' then, you can use a tool like xmllint or one of the several free online XML validators available, such as FreeFormater to check your model.  This will flag invalid XML that you should remove or reword.  If you have exported your model as 'Model' then you need to (i) unzip the model file, (ii) repeat the above step for the model.xml file, (iii) re-zip the model file as a .cairis file.
