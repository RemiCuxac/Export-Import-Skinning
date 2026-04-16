"""
This script export the skin inside a json file, to be imported further.
Usage:
    Select one or more geos and execute the script.
"""
__author__ = "Rémi CUXAC"

import maya.cmds as cmds


def get_skin_cluster(obj):
    return cmds.ls(cmds.findDeformers(obj), type="skinCluster")


def check_naming():
    skel = cmds.ls(type="joint")
    list_errors = [bone.split("|")[-1] for bone in skel if "|" in bone]
    list_errors = list(set(list_errors))
    if list_errors:
        message = "The followings bones has the same name than another bone :\n"
        for bone in list_errors:
            message += f"\n{bone}"
        cmds.confirmDialog(title="Problem", message=message, button="OK")
        return False
    return True


def export_selected_skins(pGeoList):
    if not check_naming():
        return

    folder = cmds.fileDialog2(dialogStyle=1, fileMode=3)
    folder = folder[0] if folder else None
    for geo in pGeoList:
        skin_deformer = get_skin_cluster(geo)
        if skin_deformer:
            cmds.deformerWeights(geo + ".json", format="JSON", path=folder, export=True,
                                 deformer=str(skin_deformer[0]))
        else:
            cmds.confirmDialog(title="Problem", message=f"No skin cluster applied to {geo}. Export aborted.",
                               button="OK")
            return
    cmds.confirmDialog(title="Good", message="Done !", button="OK")


sel = cmds.ls(sl=1, type="transform")
export_selected_skins(sel) if sel else cmds.error("Please select at least one geo", n=True)
