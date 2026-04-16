"""
This script import the skin from a json file. It will also create the skin cluster if the geo isn't skinned.
Usage:
    Select one or more geos and execute the script.
"""
__author__ = "Rémi CUXAC"

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
        list_errors = []
        for f in files:
            geo_name = f.split(".")[-2].split("/")[-1]
            if geo_name in cmds.ls(type="transform"):
                skin_deformer = get_skin_cluster(geo_name)
                if not skin_deformer:
                    # shape = cmds.listRelatives(geo_name, shapes=True)[0]
                    skel = get_skinned_joints_from_json(f)
                    cmds.skinCluster(skel, geo_name, tsb=1)
                    skin_deformer = get_skin_cluster(geo_name)
                    cmds.skinPercent(skin_deformer[0], geo_name, normalize=True)
                cmds.deformerWeights(f.split("/")[-1], im=True, format="JSON", method="index",
                                     deformer=skin_deformer[0],
                                     path=f.rsplit("/", 1)[0])
                cmds.skinPercent(skin_deformer[0], geo_name, normalize=True)
            else:
                list_errors.append(geo_name)
        if list_errors:
            message = "The followings geos has not been found :\n"
            for geo in list_errors:
                message += f"\n{geo}"
            cmds.confirmDialog(title="Problem", message=message, button="OK")
        else:
            cmds.confirmDialog(title="Good", message="Done !", button="OK")


import_selected_skins()
