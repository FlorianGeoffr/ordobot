from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from assets.config import Config


class ThemeManager:
    def __init__(self):
        self.config = Config()
        self.current_theme = self.config.get("theme", "dark")

    def get_current_theme(self):
        """Retourne le thème actuel"""
        return self.current_theme

    def set_theme(self, theme_name):
        """Change le thème et l'applique"""
        if theme_name in ["dark", "light"]:
            self.current_theme = theme_name
            self.config.set("theme", theme_name)
            self.apply_theme()
            print(f" Thème changé vers: {theme_name}")

    def apply_theme(self):
        """Applique le thème à l'application"""
        app = QApplication.instance()
        if not app:
            return

        if self.current_theme == "dark":
            self._apply_dark_theme(app)
        else:
            self._apply_light_theme(app)

    def _apply_dark_theme(self, app):
        """Applique le thème sombre"""
        dark_palette = QPalette()

        # Couleurs sombres
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

        app.setPalette(dark_palette)
        print(" Thème sombre appliqué")

    def _apply_light_theme(self, app):
        """Applique le thème clair"""
        light_palette = QPalette()

        # Couleurs claires (palette par défaut)
        light_palette.setColor(QPalette.Window, QColor(240, 240, 240))
        light_palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.Base, QColor(255, 255, 255))
        light_palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
        light_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        light_palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.Text, QColor(0, 0, 0))
        light_palette.setColor(QPalette.Button, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        light_palette.setColor(QPalette.Link, QColor(0, 0, 255))
        light_palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        light_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

        app.setPalette(light_palette)
        print(" Thème clair appliqué")


# Instance globale
theme_manager = ThemeManager()
