import sys
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTableWidget, QTableWidgetItem, QPushButton, QLabel, QLineEdit, 
                             QHeaderView, QMessageBox, QDialog, QTextEdit)
from PyQt5.QtCore import Qt

# Import data and logic
try:
    import devices
    from devices import authorization_list, park_authorization_list
    import utils
    import importlib
except ImportError:
    # Fallback for testing execution path if modules aren't found directly (e.g. running from root)
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import devices
    from devices import authorization_list, park_authorization_list
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
        
        # Adjust column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # ID
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.setColumnWidth(1, 100) # VIP Info
        header.setSectionResizeMode(2, QHeaderView.Stretch) # Actions
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # Query
        header.setSectionResizeMode(4, QHeaderView.Stretch) # Records
        
        layout.addWidget(self.table)
        
        self.load_devices()
        
    def load_devices(self):
        try:
            importlib.reload(devices)
            from devices import authorization_list, park_authorization_list
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to reload devices: {e}")
            return

        self.table.setRowCount(0) # Clear existing
        self.table.setRowCount(len(authorization_list))
        
        # Store text widgets to update them later
        self.record_displays = {}

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
            record_layout = QHBoxLayout(record_widget) # Changed to HBox for compactness
            record_layout.setContentsMargins(0, 0, 0, 0)
            record_layout.setSpacing(2)
            
            # Parking Row
            park_layout = QVBoxLayout()
            park_layout.setContentsMargins(0, 0, 0, 0)
            park_layout.setSpacing(1)
            btn_park_rec = QPushButton("Parking")
            btn_park_rec.setFixedHeight(20) # Smaller button
            btn_park_rec.clicked.connect(lambda checked, idx=i: self.show_park_records(idx))
            park_layout.addWidget(btn_park_rec)
            
            park_text = QTextEdit()
            park_text.setReadOnly(True)
            park_text.setMaximumHeight(25) # Reduced height
            park_layout.addWidget(park_text)
            record_layout.addLayout(park_layout)

            # Coupon Row
            coupon_layout = QVBoxLayout()
            coupon_layout.setContentsMargins(0, 0, 0, 0)
            coupon_layout.setSpacing(1)
            btn_coupon_rec = QPushButton("Coupons")
            btn_coupon_rec.setFixedHeight(20) # Smaller button
            btn_coupon_rec.clicked.connect(lambda checked, idx=i: self.show_coupons(idx))
            coupon_layout.addWidget(btn_coupon_rec)
            
            coupon_text = QTextEdit()
            coupon_text.setReadOnly(True)
            coupon_text.setMaximumHeight(25) # Reduced height
            coupon_layout.addWidget(coupon_text)
            record_layout.addLayout(coupon_layout)

            self.record_displays[i] = {'parking': park_text, 'coupon': coupon_text}
            
            self.table.setCellWidget(i, 4, record_widget)
            self.table.setRowHeight(i, 60) # Compact row height
            
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

    def get_park_token(self, index):
        from devices import park_authorization_list
        raw = park_authorization_list[index]
        if raw.startswith("Bearer "):
            return raw.split("Bearer ")[1].strip()
        return raw

    def refresh_info(self, index):
        try:
            token = self.get_token(index)
            data = utils.query_vip_info(token)
            # Simplify display
            info_text = "Data Loaded"
            if 'data' in data and data['data'] and 'current_bonus' in data['data']:
                info_text = f"Points: {data['data']['current_bonus']}"
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
            token = self.get_park_token(index)
            data = utils.query_park_fee(token, plate)
            ResultDialog("Parking Fee", data, self).exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_park_records(self, index):
        try:
            from datetime import datetime
            token = self.get_park_token(index)
            data = utils.get_park_records(token)
            
            summary_info = "No Data"
            discountfee = 0
            
            if 'data' in data and isinstance(data['data'], list):
                today_str = datetime.now().strftime('%Y-%m-%d')
                keep_fields = ['carno', 'totalfee', 'modifytime', 'discountfee']
                filtered_data = []
                for item in data['data']:
                    if isinstance(item, dict) and item.get('modifytime', '').startswith(today_str):
                        filtered_item = {k: item.get(k) for k in keep_fields}
                        filtered_data.append(filtered_item)
                data['data'] = filtered_data
                
                # Update text display
                count = len(filtered_data)
                discountfee = sum(float(item.get('discountfee', 0) or 0) for item in filtered_data)
                summary_info = f"Discount: {discountfee}"

            if index in self.record_displays and 'parking' in self.record_displays[index]:
                widget = self.record_displays[index]['parking']
                widget.setText(summary_info)
                # Color logic: discountfee >= 80 -> Red, else Blue
                if discountfee >= 80:
                    widget.setStyleSheet("background-color: red; color: white;")
                else:
                    widget.setStyleSheet("background-color: blue; color: white;")

            ResultDialog("Parking Records (Today)", data, self).exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_coupons(self, index):
        try:
            token = self.get_token(index)
            data = utils.get_coupon_list(token)
            
            summary_info = "No Data"
            valid_count = 0

            if 'data' in data and isinstance(data['data'], list):
                # Filter fields
                keep_fields = ['giftcertlistno', 'giftcertno', 'effectivedate', 'expirydate', 'giftcert_name']
                filtered_data = []
                for item in data['data']:
                    if isinstance(item, dict):
                        filtered_item = {k: item.get(k) for k in keep_fields}
                        filtered_data.append(filtered_item)
                data['data'] = filtered_data
                
                # Update text display
                valid_count = len(filtered_data)
                names = [item.get('giftcert_name', 'Coupon') for item in filtered_data]
                counter = {}
                for name in names:
                    if name not in counter:
                        counter[name] = 0
                    counter[name] = counter[name] + 1
                names_str = ""
                for name in counter.keys():
                    names_str = names_str + name + ":" + str(counter[name]) + ","
                summary_info = f"{names_str}"

            if index in self.record_displays and 'coupon' in self.record_displays[index]:
                widget = self.record_displays[index]['coupon']
                widget.setText(summary_info)
                # Color logic: counter (valid_count) > 0 -> Blue, else Red
                if valid_count > 0:
                     widget.setStyleSheet("background-color: blue; color: white;")
                else:
                     widget.setStyleSheet("background-color: red; color: white;")

            ResultDialog("Coupon List", data, self).exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
