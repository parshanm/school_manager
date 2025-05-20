from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QFormLayout, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal
import jdatetime
from database import DataBase 

class AddStudentDialog(QDialog):
    student_added = pyqtSignal(dict)  # سیگنال برای ارسال داده دانش‌آموز
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DataBase()
        self.setWindowTitle("ثبت دانش‌آموز جدید")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(400, 300)
        
        # دیکشنری برای ذخیره اطلاعات
        self.student_data = {}
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # فرم ثبت اطلاعات
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        
        # فیلدهای ورودی
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("نام")
        
        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("نام خانوادگی")
        
        self.national_id = QLineEdit()
        self.national_id.setPlaceholderText("کد ملی")
        self.national_id.setMaxLength(10)
        
        self.grade = QLineEdit()
        self.grade.setPlaceholderText("پایه تحصیلی")
        
        self.parent_phone = QLineEdit()
        self.parent_phone.setPlaceholderText("تلفن ولی")
        
        # اضافه کردن فیلدها به فرم
        form.addRow(self.first_name)
        form.addRow(self.last_name)
        form.addRow(self.national_id)
        form.addRow(self.grade)
        form.addRow(self.parent_phone)
        
        # دکمه‌ها
        btn_layout = QHBoxLayout()
        self.submit_btn = QPushButton("ثبت اطلاعات")
        self.submit_btn.clicked.connect(self.submit_data)
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        self.cancel_btn = QPushButton("انصراف")
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        
        btn_layout.addWidget(self.submit_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        # اضافه کردن به لایه اصلی
        layout.addLayout(form)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def submit_data(self):
        # اعتبارسنجی داده‌ها
        if not all([
            self.first_name.text(),
            self.last_name.text(),
            self.national_id.text(),
            self.grade.text(),
            self.parent_phone.text()
        ]):
            QMessageBox.warning(self, "خطا", "لطفاً تمام فیلدها را پر کنید!")
            return
        
        if len(self.national_id.text()) != 10:
            QMessageBox.warning(self, "خطا", "کد ملی باید 10 رقمی باشد!")
            return
        
        # ذخیره اطلاعات در دیکشنری
        self.student_data = {
            'first_name': self.first_name.text(),
            'last_name': self.last_name.text(),
            'full_name': f"{self.first_name.text()} {self.last_name.text()}",
            'national_id': self.national_id.text(),
            'grade': self.grade.text(),
            'parent_phone': self.parent_phone.text(),
            'status': 'فعال',
            'registration_date': jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        }

        self.db.write_students(
            id= self.student_data['national_id'],
            name= f"{self.student_data['first_name']} {self.student_data['last_name']}",
            grade= self.student_data['grade'],
            checkin_date= self.student_data['registration_date'],
            status= self.student_data['status'],
            parent_phone= self.student_data['parent_phone']

        )

        # بستن پنجره
        self.accept()

if __name__ == "__main__":
    import sys   
    from PyQt5.QtWidgets import QApplication  
    app = QApplication(sys.argv)
    dialog = AddStudentDialog()
    dialog.exec_()