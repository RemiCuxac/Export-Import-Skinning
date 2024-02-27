import maya.cmds as cmds

skel = cmds.ls(type="joint")
geos = cmds.ls(sl=1)

def get_skin_cluster(pShape):
    if not cmds.objectType(pShape).lower() == "mesh":
        pShape = cmds.listRelatives(pShape, shapes=True, noIntermediate=True)
    skin = cmds.listConnections(pShape, exactType=True, type="skinCluster")
    return skin[0] if skin else None

def export_selected_skins():
    if not geos:
        cmds.confirmDialog(title="Problem", message="Please select at least one geo", button="OK")
    else:
        listErrors = [bone.split("|")[-1] for bone in skel if "|" in bone]
        listErrors = list(set(listErrors))
        if listErrors:
            message = "The followings bones has the same name than another bone :\n"
            for bone in listErrors:
                message += f"\n{bone}"
            cmds.confirmDialog(title="Problem", message=message, button="OK")
        else:
            folder = cmds.fileDialog2(dialogStyle=1,fileMode=3)
            folder = folder[0] if folder else None
            if folder:
                for geo in geos:
                    skinDeformer = get_skin_cluster(geo)
                    if cmds.objectType(geo).lower() == "mesh":
                        geoName = cmds.listRelatives(geo, parent=True)[0]
                    else:
                        geoName = geo
                    if skinDeformer:
                        cmds.deformerWeights(geoName+".json", format="JSON", path=folder, export=True, deformer=str(skinDeformer))
                    else:
                        cmds.confirmDialog(title="Problem", message=f"No skin cluster applied to {geoName}. Export aborted.", button="OK")
                        return False
                cmds.confirmDialog(title="Good", message="Done !", button="OK")

def import_selected_skins():
    files = cmds.fileDialog2(fileFilter="*.json", dialogStyle=1,fileMode=4)
    if files:
        listErrors = []
        for f in files:
            geoName = f.split(".")[-2].split("/")[-1]
            if geoName in cmds.ls(type="transform"):
                skinDeformer = get_skin_cluster(geoName)
                if not skinDeformer:
                    shape = cmds.listRelatives(geoName, shapes=True)[0]
                    #cmds.skinCluster(maximumInfluences=4, dropoffRate=4, tsb=True)
                    cmds.skinCluster(skel, geoName, tsb=1)
                    skinDeformer = get_skin_cluster(geoName)
                    cmds.skinPercent(skinDeformer, geoName, normalize=True)
                cmds.deformerWeights(f.split("/")[-1], im=True,format="JSON", method="index", deformer=skinDeformer, path=f.rsplit("/", 1)[0])
                cmds.skinPercent(skinDeformer, geoName, normalize=True)
            else:
                listErrors.append(geoName)
        if listErrors:
            message = "The followings geos has not been found :\n"
            for geo in listErrors:
                message += f"\n{geo}"
            cmds.confirmDialog(title="Problem", message=message, button="OK")
        else:
            cmds.confirmDialog(title="Good", message="Done !", button="OK")
                    
#export_selected_skins()
#import_selected_skins()