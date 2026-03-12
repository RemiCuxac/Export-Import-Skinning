import json
import os

import maya.cmds as cmds

skel = cmds.ls(type="joint")
geos = cmds.ls(sl=1)

def get_skin_cluster(obj):
    return cmds.ls(cmds.findDeformers(obj), type="skinCluster")

def check_naming():
    skel = cmds.ls(type="joint")
    listErrors = [bone.split("|")[-1] for bone in skel if "|" in bone]
    listErrors = list(set(listErrors))
    if listErrors:
        message = "The followings bones has the same name than another bone :\n"
        for bone in listErrors:
            message += f"\n{bone}"
        cmds.confirmDialog(title="Problem", message=message, button="OK")
        return False
    return True

def get_skinned_joints_from_json(file):
    assert os.path.exists(file), f"Wrong path for {file}"
    jsonData = json.load(open(file))
    jointList = [weight["source"] for weight in jsonData["deformerWeight"]["weights"]]
    return jointList

def export_selected_skins(pGeoList):
    if not check_naming():
        return

    folder = cmds.fileDialog2(dialogStyle=1, fileMode=3)
    folder = folder[0] if folder else None
    for geo in pGeoList:
        skinDeformer = get_skin_cluster(geo)
        if skinDeformer:
            cmds.deformerWeights(geo + ".json", format="JSON", path=folder, export=True,
                                 deformer=str(skinDeformer[0]))
        else:
            cmds.confirmDialog(title="Problem", message=f"No skin cluster applied to {geo}. Export aborted.",
                               button="OK")
            return
    cmds.confirmDialog(title="Good", message="Done !", button="OK")


def import_selected_skins():
    files = cmds.fileDialog2(fileFilter="*.json", dialogStyle=1, fileMode=4)
    if files:
        listErrors = []
        for f in files:
            geoName = f.split(".")[-2].split("/")[-1]
            if geoName in cmds.ls(type="transform"):
                skinDeformer = get_skin_cluster(geoName)
                if not skinDeformer:
                    # shape = cmds.listRelatives(geoName, shapes=True)[0]
                    skel = get_skinned_joints_from_json(f)
                    cmds.skinCluster(skel, geoName, tsb=1)
                    skinDeformer = get_skin_cluster(geoName)
                    cmds.skinPercent(skinDeformer[0], geoName, normalize=True)
                cmds.deformerWeights(f.split("/")[-1], im=True, format="JSON", method="index", deformer=skinDeformer[0],
                                     path=f.rsplit("/", 1)[0])
                cmds.skinPercent(skinDeformer[0], geoName, normalize=True)
            else:
                listErrors.append(geoName)
        if listErrors:
            message = "The followings geos has not been found :\n"
            for geo in listErrors:
                message += f"\n{geo}"
            cmds.confirmDialog(title="Problem", message=message, button="OK")
        else:
            cmds.confirmDialog(title="Good", message="Done !", button="OK")


sel = cmds.ls(selection=True, type="transform")
#export_selected_skins(sel) if sel else cmds.error("Please select at least one geo", n=True)
#import_selected_skins()