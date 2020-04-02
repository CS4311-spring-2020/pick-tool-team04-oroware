import os
import pickle

from pathlib import Path

import pymongo

from Icon import Icon


class IconManager:
    def __init__(self):
        self.icons = dict()
        self.filename = "icons.pkl"
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client["database"]
        self.col = self.db["icons"]

    def addIcon(self, icon):
        if icon.name in self.icons:
            return False
        self.icons[icon.name] = icon
        icon.getPixmapFromSource()
        icon.getGraphImageFromSource()
        return True

    def deleteIcon(self, iconName):
        if iconName in self.icons:
            del self.icons[iconName]
            self.deleteIconDb(iconName)
            return True
        else:
            return False

    def storeIcons(self):
        with open(self.filename, 'wb') as pkl_file:
            pickle.dump(self.icons, pkl_file)

    def storeIconDb(self, icon):
        iconEntry = {"_id": icon.name, "icon": pickle.dumps(icon)}
        self.col.insert_one(iconEntry)

    def deleteStoredIconsDb(self):
        self.col.delete_many({})

    def deleteIconDb(self, iconName):
        self.col.delete_one({"_id": iconName})

    def retrieveIconsDb(self):
        self.icons.clear()
        for iconEntry in self.col.find():
            icon = pickle.loads(iconEntry["icon"])
            self.icons[icon.name] = icon

    def updateIcon(self, icon):
        query = {"_id": icon.name}
        values = {"$set": {"_id": icon.name, "icon": pickle.dumps(icon)}}
        self.col.update_one(query, values)

    def storeIconsDb(self):
        for iconName, icon in self.icons.items():
            self.storeIconDb(icon)

    def retrieveIcons(self):
        filename_path = Path(self.filename)
        if filename_path.exists():
            with open(self.filename, 'rb') as pkl_file:
                self.icons = pickle.load(pkl_file)

    def deleteStoredIcons(self):
        filename_path = Path(self.filename)
        if filename_path.exists():
            os.remove(filename_path)
