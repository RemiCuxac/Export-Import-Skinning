import maya.cmds as cmds


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


sel = cmds.ls(sl=1, type="transform")
export_selected_skins(sel) if sel else cmds.error("Please select at least one geo", n=True)
