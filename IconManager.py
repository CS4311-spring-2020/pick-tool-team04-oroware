from Icon import Icon

class IconManager:
    def __init__(self):
        self.icons = dict()
        icon = Icon()
        icon.name = "Blue Shield"
        icon.source = "icons/blueshield.png"
        icon.preview = icon.getImageFromSource()
        self.icons[icon.name] = icon

    def addIcon(self, icon):
        if icon.name in self.icons:
            return False
        self.icons[icon.name] = icon
        return True
