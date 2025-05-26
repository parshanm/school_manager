from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QWidget, QLineEdit, 
                            QPushButton, QFormLayout, QMessageBox, QHBoxLayout, QTabWidget)
from PyQt5.QtCore import Qt, pyqtSignal
import jdatetime
from database import DataBase 
from PyQt5.QtGui import QColor

class DeleteStudentDialog(QDialog):
    student_deleted = pyqtSignal(dict)  # سیگنال برای ارسال داده دانش‌آموز
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DataBase()
        self.setWindowTitle("حذف دانش‌آموز ")
        self.setWindowModality(Qt.ApplicationModal)
        self.parent = parent
        self.setFixedSize(200, 100)
        
        # دیکشنری برای ذخیره اطلاعات
        self.student_data = {}
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # فرم ثبت اطلاعات
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        
        # فیلدهای ورودی
        self.national_id = QLineEdit()
        self.national_id.setPlaceholderText("کد ملی")
        self.national_id.setMaxLength(10)

        # اضافه کردن فیلدها به فرم
        form.addRow(self.national_id)
        form.setSpacing(10)
        
        # دکمه‌ها
        btn_layout = QHBoxLayout()
        self.submit_btn = QPushButton("حذف")
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
        if len(self.national_id.text()) != 10:
            QMessageBox.warning(self, "خطا", "کد ملی باید 10 رقمی باشد!")
            return

        self.db.delete_student(self.national_id.text())
        self.primary_color = QColor(52, 152, 219)
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 0; }
            QTabBar::tab { 
                padding: 8px 15px; 
                background: #ecf0f1; 
                border: 1px solid #ddd; 
                border-bottom: none; 
                border-top-left-radius: 4px; 
                border-top-right-radius: 4px; 
            }
            QTabBar::tab:selected { 
                background: white; 
                border-bottom: 2px solid %s; 
            }
        """ % self.primary_color.name())

        self.parent.statusBar().showMessage("دانش‌آموز با موفقیت حذف شد")
        self.parent.init_dashboard_tab(self=self.parent,tab=self.dashboard_tab)


        # بستن پنجره
        self.accept()
