import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QFileDialog, QMessageBox

class FolderTreeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folder Tree Generator")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Folder Structure"])
        self.tree_widget.setColumnWidth(0, 400)

        main_layout.addWidget(self.tree_widget)

        self.create_root_folder()

        self.tree_widget.doubleClicked.connect(self.rename_node)
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.open_context_menu)

    def create_root_folder(self):
        root_item = QTreeWidgetItem(self.tree_widget, ["Root"])
        self.tree_widget.addTopLevelItem(root_item)

    def rename_node(self, index):
        item = self.tree_widget.currentItem()
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.tree_widget.editItem(item)

    def open_context_menu(self, position):
        menu = QMenu()
        add_folder_action = menu.addAction("Add Subfolder")
        remove_action = menu.addAction("Remove Folder")
        selected_action = menu.exec_(self.tree_widget.mapToGlobal(position))

        if selected_action == add_folder_action:
            self.add_subfolder()
        elif selected_action == remove_action:
            self.remove_folder()

    def add_subfolder(self):
        current_item = self.tree_widget.currentItem()
        new_folder = QTreeWidgetItem(current_item, ["New Folder"])
        current_item.addChild(new_folder)

    def remove_folder(self):
        current_item = self.tree_widget.currentItem()
        parent = current_item.parent()
        if parent:
            parent.removeChild(current_item)
        else:
            self.tree_widget.takeTopLevelItem(self.tree_widget.indexOfTopLevelItem(current_item))

    def generate_folder_structure(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder_path:
            self.create_folders(self.tree_widget.invisibleRootItem(), folder_path)
            QMessageBox.information(self, "Success", "Folder structure created successfully.")

    def create_folders(self, item, parent_path):
        for i in range(item.childCount()):
            child_item = item.child(i)
            folder_name = child_item.text(0)
            folder_path = os.path.join(parent_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            self.create_folders(child_item, folder_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderTreeApp()
    window.show()
    sys.exit(app.exec_())
