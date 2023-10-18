## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from collections import Counter
from collections import defaultdict

from qtpy import QtCore, QtGui

from PyFlow.Core.Common import *


class InputActionType(Enum):
    Mouse = 1
    Keyboard = 2



class InputAction(object):
    def __init__(self, name="defaultName", actionType=InputActionType.Keyboard, group="default", mouse=QtCore.Qt.MouseButton.NoButton, key=None, modifiers=QtCore.Qt.KeyboardModifier.NoModifier):
        self.__actionType = actionType
        self._name = name
        self._group = group
        # if type(mouse)=='enum'
        # add_enum_members_to_class(modifiers,modifiers1)

        self._data={}
        self._data['mouse']=mouse
        self._data['modifiers']=modifiers
        self._data['key']=key
        # self._data = {"mouse": mouse, "key": key, "modifiers": modifiers}

    def __str__(self):
        return "{0} {1} {2}".format(QtGui.QKeySequence(self.getModifiers()).toString(),
                                    self.getMouseButton().name.decode('utf=8'),
                                    QtGui.QKeySequence(self.getKey()).toString())

    @property
    def group(self):
        return self._group

    @property
    def actionType(self):
        return self.__actionType

    def __eq__(self, other):
        sm = self._data["mouse"]
        sk = self._data["key"]
        smod = self._data["modifiers"]
        om = other.getData()["mouse"]
        ok = other.getData()["key"]
        omod = other.getData()["modifiers"]
        smod == omod
        return all([sm == om,
                    sk == ok,
                    smod == omod])

    def __ne__(self, other):
        sm = self._data["mouse"]
        sk = self._data["key"]
        smod = self._data["modifiers"]
        om = other.getData()["mouse"]
        ok = other.getData()["key"]
        omod = other.getData()["modifiers"]
        return not all([sm == om,
                        sk == ok,
                        smod == omod])

    def getName(self):
        return self._name

    def getData(self):
        return self._data

    def setMouseButton(self, btn):
        assert(isinstance(btn, QtCore.Qt.MouseButton))
        self._data["mouse"] = btn

    def getMouseButton(self):
        return self._data["mouse"]

    def setKey(self, key=[]):
        assert(isinstance(key, QtCore.Qt.Key))
        self._data["key"] = key

    def getKey(self):
        return self._data["key"]

    def setModifiers(self, modifiers=QtCore.Qt.NoModifier):
        self._data["modifiers"] = modifiers

    def getModifiers(self):
        return self._data["modifiers"]

    @staticmethod
    def _modifiersToList(mods):
        result = []
        if mods & QtCore.Qt.ShiftModifier:
            result.append(QtCore.Qt.ShiftModifier)
        if mods & QtCore.Qt.ControlModifier:
            result.append(QtCore.Qt.ControlModifier)
        if mods & QtCore.Qt.AltModifier:
            result.append(QtCore.Qt.AltModifier)
        if mods & QtCore.Qt.MetaModifier:
            result.append(QtCore.Qt.MetaModifier)
        if mods & QtCore.Qt.KeypadModifier:
            result.append(QtCore.Qt.KeypadModifier)
        if mods & QtCore.Qt.GroupSwitchModifier:
            result.append(QtCore.Qt.GroupSwitchModifier)
        return result

    def _listOfModifiersToEnum(self, modifiersList):
        result = QtCore.Qt.NoModifier
        for mod in modifiersList:
            result = result | mod
        return result

    def toJson(self):
        saveData = {}
        saveData["name"] = self._name
        saveData["group"] = self._group

        try:
            saveData["mouse"] = self._data["mouse"].value
            saveData["actionType"] = self.actionType.value
            key = self._data["key"]
            saveData["key"] = int(key) if key is not None else None
            modifiersList = self._modifiersToList(self._data["modifiers"])
            saveData["modifiers"] = [int(i) for i in modifiersList]
        except:
            print(self._data["mouse"])

        return saveData

    def fromJson(self, jsonData):
        try:
            self._name = jsonData["name"]
            self._group = jsonData["group"]
            self._data["mouse"] = QtCore.Qt.MouseButton(jsonData["mouse"])
            keyJson = jsonData["key"]
            self._data["key"] = QtCore.Qt.Key(keyJson) if isinstance(keyJson, int) else None
            self._data["modifiers"] = self._listOfModifiersToEnum([QtCore.Qt.KeyboardModifier(i) for i in jsonData["modifiers"]])
            self.__actionType = InputActionType(jsonData["actionType"])
            return self
        except:
            return None


@SingletonDecorator
class InputManager(object):
    """Holds all registered input actions."""

    def __init__(self, *args, **kwargs):
        self._actions = defaultdict(list)

    def __getitem__(self, key):
        # try find input action by name
        if key in self._actions:
            return self._actions[key]
        return []

    def __contains__(self, item):
        return item.getName() in self._actions

    def getData(self):
        return self._actions

    def registerAction(self, action):

        try:
            if action not in self._actions[action.getName()]:
                self._actions[action.getName()].append(action)
        except:
            print("Getting Error None Error")

    def loadFromData(self, data):
        for actionName, actionVariants in data.items():
            for variant in actionVariants:
                actionInstance = InputAction().fromJson(variant)
                self.registerAction(actionInstance)

    def serialize(self):
        result = defaultdict(list)
        for actionName in self._actions:
            for actionVariant in self._actions[actionName]:
                result[actionName].append(actionVariant.toJson())
        return result

