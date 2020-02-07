from Icon import Icon

class IconManager:
    def __init__(self):
        self.icons = dict()
        icon = Icon()
        icon.name = "Blue Shield"
        icon.source = "C:/Users/marka/Desktop/software/pick-tool-team04-oroware/icons/blueshield.png"
        icon.getPixmapFromSource()
        self.icons[icon.name] = icon

    def addIcon(self, icon):
        if icon.name in self.icons:
            return False
        self.icons[icon.name] = icon
        icon.getPixmapFromSource()
        return True
