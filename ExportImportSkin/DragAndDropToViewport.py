import maya.mel as mel    
import shutil
import os
import maya.cmds as cmds

def onMayaDroppedPythonFile(*args, **kwargs):
    """
    This function is only supported since Maya 2017 Update 3.
    Maya requires this in order to successfully execute.
    """
    pass

try:
    currentParent = os.path.abspath(os.path.dirname(__file__))
    scriptFile = os.path.join(currentParent, "ExportImportSkin.py")
    scriptFolder = cmds.internalVar(userScriptDir=True)
    shutil.copy(scriptFile, scriptFolder)
    
    nameExport = 'ExportSkin'
    tooltipExport = 'Export skinning of selected geo'
    commandExport = """import ExportImportSkin as eis
from importlib import reload
reload(eis)
eis.export_selected_skins()"""
    
    nameImport = 'ImportSkin'
    tooltipImport = 'Import skinning of selected files'
    commandImport = """import ExportImportSkin as eis
from importlib import reload
reload(eis)
eis.import_selected_skins()"""
    
    # Add to current shelf
    topShelf = mel.eval('$nul = $gShelfTopLevel')
    currentShelf = cmds.tabLayout(topShelf, q=1, st=1)
    cmds.shelfButton(parent=currentShelf, i="fileSave.png", c=commandExport, imageOverlayLabel=nameExport, annotation=tooltipExport)
    cmds.shelfButton(parent=currentShelf, i="fileOpen.png", c=commandImport, imageOverlayLabel=nameImport, annotation=tooltipImport)
    cmds.confirmDialog(message=f"Success ! \nYou can see two more buttons in the shelf: \n{currentShelf}", icon="information", title="Success")
except Exception as e:
    cmds.confirmDialog(message=f"Script failed to install: \n{e}", icon="warning", title="ERROR")
