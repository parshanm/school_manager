from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QMessageBox,
    QComboBox,
    QDateEdit,
    QDoubleSpinBox,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from jdatetime import date as jdate
from jalalli_date import JalaliDateEdit
import jdatetime


class AddPaymentDialog(QDialog):
    payment_added = pyqtSignal(dict)  # سیگنال برای ارسال داده پرداخت

    def __init__(self, students_list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ثبت پرداخت جدید")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(450, 400)
        self.payment_date = JalaliDateEdit()
        self.payment_date.setJalaliDate(
            jdate.today().year, jdate.today().month, jdate.today().day
        )
        self.students = students_list
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # فرم ثبت اطلاعات
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)

        # فیلدهای ورودی
        self.student_combo = QComboBox()
        self.student_combo.addItems(self.students)
        self.student_combo.setStyleSheet(
            """
            QComboBox {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
        """
        )

        self.setStyleSheet(
            """
    QLabel {
        font-size: 14px;
        color: #2c3e50;
    }
    QLineEdit, QDateEdit, QDoubleSpinBox {
        padding: 6px;
        border: 1px solid #bdc3c7;
        border-radius: 4px;
        min-width: 200px;
    }
    QGroupBox {
        border: 1px solid #ddd;
        border-radius: 5px;
        margin-top: 10px;
        padding-top: 15px;
        font-size: 14px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        color: #7f8c8d;
    }
"""
        )

        self.amount = QDoubleSpinBox()
        self.amount.setRange(0, 10000000)
        self.amount.setValue(100000)
        self.amount.setPrefix("تومان ")
        self.amount.setSingleStep(10000)

        self.payment_date = QDateEdit(calendarPopup=True)
        self.payment_date.setDate(QDate.currentDate())
        self.payment_date.setDisplayFormat("yyyy/MM/dd")

        self.payment_method = QComboBox()
        self.payment_method.addItems(["نقدی", "کارت به کارت", "چک", "پوز"])

        self.receipt_number = QLineEdit()
        self.receipt_number.setPlaceholderText("شماره فیش/رسید")

        self.description = QLineEdit()
        self.description.setPlaceholderText("توضیحات (اختیاری)")

        # اضافه کردن فیلدها به فرم
        form.addRow(QLabel("دانش‌آموز:"), self.student_combo)
        form.addRow(QLabel("مبلغ:"), self.amount)
        form.addRow(QLabel("تاریخ پرداخت:"), self.payment_date)
        form.addRow(QLabel("روش پرداخت:"), self.payment_method)
        form.addRow(QLabel("شماره رسید:"), self.receipt_number)
        form.addRow(QLabel("توضیحات:"), self.description)

        # دکمه‌ها
        btn_layout = QHBoxLayout()
        self.submit_btn = QPushButton("ثبت پرداخت")
        self.submit_btn.clicked.connect(self.submit_payment)
        self.submit_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )

        self.cancel_btn = QPushButton("انصراف")
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        )

        btn_layout.addWidget(self.submit_btn)
        btn_layout.addWidget(self.cancel_btn)

        # اضافه کردن به لایه اصلی
        layout.addLayout(form)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def submit_payment(self):
        # اعتبارسنجی داده‌ها
        if not self.receipt_number.text():
            QMessageBox.warning(self, "خطا", "لطفاً شماره رسید را وارد کنید!")
            return

        # جمع‌آوری داده‌ها
        payment_data = {
            "student": self.student_combo.currentText(),
            "amount": self.amount.value(),
            "date": jdatetime.datetime.now(),
            "method": self.payment_method.currentText(),
        }

        # بستن پنجره
        self.accept()
