import pickle

from pathlib import Path

class IconManager:
    def __init__(self):
        self.icons = dict()
        self.filename = "icons.pkl"

    def addIcon(self, icon):
        if icon.name in self.icons:
            return False
        self.icons[icon.name] = icon
        icon.getPixmapFromSource()
        icon.getGraphImageFromSource()
        return True

    def storeIcons(self):
        with open(self.filename, 'wb') as pkl_file:
            pickle.dump(self.icons, pkl_file)

    def retrieveIcons(self):
        filename_path = Path(self.filename)
        if filename_path.exists():
            with open(self.filename, 'rb') as pkl_file:
                self.icons = pickle.load(pkl_file)
