"""
Create Space Switch SCRIPT
Created by Alva Stenhammar

Create a space switch with any amount of parents.

TO-DO:
- maybe add matching the pose when switching between spaces

"""

import maya.cmds as cmds
import functools



def _______________UI_______________(): pass


def toggleAttributeOptions(attributeObjectBox: str,
                           attributeObjectField: str,
                           *args):
    """ Toggle the attribute options. """

    if cmds.checkBox(attributeObjectBox, query=True, value=True) == True:
        cmds.textField(attributeObjectField, edit=True, enable=True)
    else:
        cmds.textField(attributeObjectField, edit=True, enable=False)



def insertSeparator(parent: str):
    """ Create custom separator. """

    cmds.separator(height=2,
                  style="none",
                  backgroundColor=(0.2, 0.2, 0.2),
                  parent=parent)



def createColumnLayout(parent: str) -> str:
    """
    Create row/column layout with custom settings.

    Return layout's full path name.
    """

    layout = cmds.rowColumnLayout(numberOfColumns=2,
                                  columnWidth=[(1, 130), (2, 130)],
                                  columnOffset=[(1, "right", 10), (2, "left", 10)],
                                  rowSpacing=(1, 5),
                                  parent=parent)
    
    return cmds.rowColumnLayout(layout, query=True, fullPathName=True)



def createFrameLayout(label: str, parent: str) -> str:
    """
    Create frame layout layout with custom settings.

    Return layout's full path name.
    """

    layout = cmds.frameLayout(label=label,
                              width=300,
                              marginWidth=20,
                              marginHeight=10,
                              backgroundShade=True,
                              font="boldLabelFont",
                              parent=parent)
    
    return cmds.frameLayout(layout, query=True, fullPathName=True)



def createButton(label: str, parent: str) -> str:
    """
    Create button with custom settings.
    
    Return button's full path name.
    """

    cmds.rowLayout(numberOfColumns=1,
                   columnWidth=(1, 260),
                   parent=parent)
    
    button = cmds.button(label=label,
                         width=260)
    
    return cmds.button(button, query=True, fullPathName=True)



def createUI(buildSpaceSwitch):
    """ Create and open the UI. """


    # WINDOW CREATION
    windowID = "createSpaceSwitchWindowID"
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
    cmds.window(windowID, title=f"Create Space Switch", sizeable=True)


    # LAYOUTS
    mainLayout = cmds.columnLayout(width=310, margins=5)

    cmds.columnLayout(margins=10,
                      parent=mainLayout)
    cmds.text(label="Create Space Switch Tool",
              width=280,
              font="boldLabelFont")
    cmds.separator(height=10, style="none")


    # LAYOUT SETUP
    layout = createFrameLayout("Options", mainLayout)
    cmds.separator(height=5, style="none", parent=mainLayout)
    
    cmds.text(label="First select object to apply space switch to,",
                width=260, height=10,
                font="smallPlainLabelFont")
    cmds.text(label="then select the parent objects.",
                    width=260, height=10,
                    font="smallPlainLabelFont")
    insertSeparator(layout)

    cmds.separator(height=5, style="none", parent=mainLayout)


    createColumnLayout(parent=layout)
    

    cmds.text(label="Use different object")
    cmds.text(label="")
    cmds.text(label="for switch attribute:")
    attributeObjectBox = cmds.checkBox(label="", value=False)

    cmds.text("Attribute object:")
    attributeObjectField = cmds.textField(text="", enable=False)


    # apply button
    cmds.separator(height=1, style="none", enableBackground=False, parent=layout)
    applyButton = createButton("Create Space Switch", layout)


    # CREDITS TEXT
    cmds.columnLayout(margins=10,
                        parent=mainLayout)
    
    cmds.separator(height=5,
                    style="none")
    
    cmds.text(label="Created by Alva Stenhammar", width=280,
                font="obliqueLabelFont")
    

    # ADD COMMANDS
    # control options
    cmds.checkBox(attributeObjectBox, edit=True,
                  onCommand=functools.partial(toggleAttributeOptions,
                                              attributeObjectBox,
                                              attributeObjectField),
                  offCommand=functools.partial(toggleAttributeOptions,
                                                  attributeObjectBox,
                                                  attributeObjectField))


    # apply button
    cmds.button(applyButton, edit=True,
                command=functools.partial(buildSpaceSwitch,
                                          attributeObjectBox,
                                          attributeObjectField))


    cmds.showWindow()



def _______________BUILD_______________(): pass


def buildSpaceSwitch(attributeObjectBox: str,
                     attributeObjectField: str,
                     *args):

    # BUILD NAMES FROM UI

    addAttributeObject = cmds.checkBox(attributeObjectBox, query=True, value=True)

    if addAttributeObject:
        attributeObjectName = cmds.textField(attributeObjectField, query=True, text=True)

    # get selection and create variables
    selection = cmds.ls(selection=True)

    object = selection[0]
    attributeObject = object
    parentList = []

    for i in range(len(selection) - 1):
        parentList.append(selection[i + 1])

    # add different attribute object if box is checked
    if addAttributeObject:
        attributeObject = attributeObjectName


    # parent constrain the object to the parents
    constraint = cmds.parentConstraint(parentList, object, maintainOffset=True)[0]

    # create string of parent names for the enum attribute options
    enumParentString = ""
    for i in range(len(parentList)):
        enumParentString = f"{enumParentString}:{parentList[i]}"

    # create space switch attributes
    cmds.select(attributeObject)
    cmds.addAttr(attributeType="enum",
                 longName="spaceSwitch",
                 niceName="Space Switch",
                 enumName=enumParentString)
    cmds.setAttr(f"{attributeObject}.spaceSwitch", channelBox=True)
    cmds.setAttr(f"{attributeObject}.spaceSwitch", keyable=True)
    cmds.select(clear=True)


    # SET DRIVEN KEYS TO CONNECT SWITCH TO PARENT CONSTRAINT

    # set all weights to 0
    for i in range(len(parentList)):
        cmds.setAttr(f"{constraint}.{parentList[i]}W{i}", 0)

    for i in range(len(parentList)):
        cmds.setAttr(f"{attributeObject}.spaceSwitch", i)
        cmds.setAttr(f"{constraint}.{parentList[i]}W{i}", 1)

        # reset prev weight to 0
        if i != 0:
            cmds.setAttr(f"{constraint}.{parentList[i - 1]}W{i - 1}", 0)

        # set driven key on all weights
        for i in range(len(parentList)):
            cmds.setDrivenKeyframe(f"{constraint}.{parentList[i]}W{i}",
                                    currentDriver=f"{attributeObject}.spaceSwitch")

    # set attr to first parent
    cmds.setAttr(f"{attributeObject}.spaceSwitch", 0)
    


createUI(buildSpaceSwitch)