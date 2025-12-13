import sys
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTableWidget, QTableWidgetItem, QPushButton, QLabel, QLineEdit, 
                             QHeaderView, QMessageBox, QDialog, QTextEdit)
from PyQt5.QtCore import Qt

# Import data and logic
try:
    import devices
    from devices import authorization_list
    import utils
    import importlib
except ImportError:
    # Fallback for testing execution path if modules aren't found directly (e.g. running from root)
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import devices
    from devices import authorization_list
    import utils
    import importlib

class ResultDialog(QDialog):
    def __init__(self, title, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(600, 400)
        layout = QVBoxLayout(self)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(json.dumps(data, indent=2, ensure_ascii=False))
        layout.addWidget(text_edit)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Citic Park Manager")
        self.resize(1000, 600)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "VIP Info", "Actions", "Parking Query", "Records"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        self.load_devices()
        
    def load_devices(self):
        try:
            importlib.reload(devices)
            from devices import authorization_list
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to reload devices: {e}")
            return

        self.table.setRowCount(0) # Clear existing
        self.table.setRowCount(len(authorization_list))
        for i, token in enumerate(authorization_list):
            # clean token for display logic if needed, but mainly for usage
            
            # ID
            self.table.setItem(i, 0, QTableWidgetItem(str(i)))
            
            # VIP Info Placeholder
            info_label = QLabel("Click Refresh")
            info_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(i, 1, info_label)
            
            # Actions
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(2, 2, 2, 2)
            
            btn_refresh = QPushButton("Refresh")
            btn_refresh.clicked.connect(lambda checked, idx=i: self.refresh_info(idx))
            action_layout.addWidget(btn_refresh)
            
            btn_signin = QPushButton("Sign In")
            btn_signin.clicked.connect(lambda checked, idx=i: self.sign_in(idx))
            action_layout.addWidget(btn_signin)
            
            btn_exchange = QPushButton("Exchange")
            btn_exchange.clicked.connect(lambda checked, idx=i: self.exchange(idx))
            action_layout.addWidget(btn_exchange)
            
            self.table.setCellWidget(i, 2, action_widget)
            
            # Parking Query
            query_widget = QWidget()
            query_layout = QHBoxLayout(query_widget)
            query_layout.setContentsMargins(2, 2, 2, 2)
            
            plate_input = QLineEdit()
            plate_input.setPlaceholderText("沪A12345")
            query_layout.addWidget(plate_input)
            
            btn_query = QPushButton("Query")
            btn_query.clicked.connect(lambda checked, idx=i, inp=plate_input: self.query_fee(idx, inp))
            query_layout.addWidget(btn_query)
            
            self.table.setCellWidget(i, 3, query_widget)
            
            # Records
            record_widget = QWidget()
            record_layout = QHBoxLayout(record_widget)
            record_layout.setContentsMargins(2, 2, 2, 2)
            
            btn_park_rec = QPushButton("Parking")
            btn_park_rec.clicked.connect(lambda checked, idx=i: self.show_park_records(idx))
            record_layout.addWidget(btn_park_rec)
            
            btn_coupon_rec = QPushButton("Coupons")
            btn_coupon_rec.clicked.connect(lambda checked, idx=i: self.show_coupons(idx))
            record_layout.addWidget(btn_coupon_rec)
            
            self.table.setCellWidget(i, 4, record_widget)
            
            # Auto-load basic info
            self.refresh_info(i)

    def get_token(self, index):
        # Reload list just in case needed but usually internal list is stale if not reloaded
        # We rely on load_devices to update the UI count, so we must access the module list
        from devices import authorization_list
        raw = authorization_list[index]
        if raw.startswith("Bearer "):
            return raw.split("Bearer ")[1].strip()
        return raw

    def refresh_info(self, index):
        try:
            token = self.get_token(index)
            data = utils.query_vip_info_office(token)
            # Simplify display
            info_text = "Data Loaded"
            if 'Data' in data and data['Data'] and 'Point' in data['Data']:
                info_text = f"Points: {data['Data']['Point']}"
            elif 'msg' in data:
                info_text = data['msg']
            else:
                 info_text = json.dumps(data)[:20] # Show partial result if unknown fmt
                
            label = self.table.cellWidget(index, 1)
            if label:
                label.setText(info_text)
            
        except Exception as e:
            label = self.table.cellWidget(index, 1)
            if label:
                label.setText("Error")
            # Show error in console or message box if manually clicked? 
            # It's auto called, so maybe just print. But user complained no reaction.
            print(f"Error fetching info for {index}: {e}")
            if self.sender(): # Only show popup if manually triggered
                 QMessageBox.warning(self, "Refresh Error", str(e))

    def sign_in(self, index):
        try:
            token = self.get_token(index)
            data = utils.sign_shangyuewan(token)
            QMessageBox.information(self, "Sign In Result", json.dumps(data, indent=2, ensure_ascii=False))
            self.refresh_info(index)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def exchange(self, index):
        try:
            token = self.get_token(index)
            data = utils.exchange_office_coupon(token)
            QMessageBox.information(self, "Exchange Result", json.dumps(data, indent=2, ensure_ascii=False))
            self.refresh_info(index)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def query_fee(self, index, input_field):
        plate = input_field.text().strip()
        if not plate:
            QMessageBox.warning(self, "Warning", "Please enter a plate number")
            return
        
        try:
            token = self.get_token(index)
            data = utils.query_park_fee(token, plate)
            ResultDialog("Parking Fee", data, self).exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_park_records(self, index):
        try:
            token = self.get_token(index)
            data = utils.get_park_records(token)
            ResultDialog("Parking Records", data, self).exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_coupons(self, index):
        try:
            token = self.get_token(index)
            data = utils.get_coupon_list(token)
            ResultDialog("Coupon List", data, self).exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
