import json
import os

import maya.cmds as cmds


def get_skin_cluster(obj):
    return cmds.ls(cmds.findDeformers(obj), type="skinCluster")


def get_skinned_joints_from_json(file):
    assert os.path.exists(file), f"Wrong path for {file}"
    jsonData = json.load(open(file))
    jointList = [weight["source"] for weight in jsonData["deformerWeight"]["weights"]]
    return jointList


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

import_selected_skins()
