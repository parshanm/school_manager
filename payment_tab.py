from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QComboBox,
)
from persiantools import digits
from jalalli_date import JalaliDateEdit
from PyQt5.QtGui import QColor
from jdatetime import date as jdate

class PaymentsTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
        self.filter_date_from = JalaliDateEdit()
        self.filter_date_to = JalaliDateEdit()
        self.load_payments()

    def init_ui(self):
        # لایه اصلی
        layout = QVBoxLayout()

        # نوار ابزار
        toolbar = QHBoxLayout()

        # دکمه‌های عملیاتی
        self.add_btn = QPushButton("ثبت پرداخت جدید")
        self.add_btn.setStyleSheet(
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

        self.refresh_btn = QPushButton("بروزرسانی لیست")
        self.refresh_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """
        )

        # فیلترها
        self.filter_student = QComboBox()
        self.filter_student.addItem("همه دانش‌آموزان")
        self.filter_student.setStyleSheet(
            """
            QComboBox {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                min-width: 150px;
            }
        """
        )

        self.filter_date_from = JalaliDateEdit()
        self.filter_date_from.setJalaliDate(1402, 1, 1)
        self.filter_date_from.setDisplayFormat("yyyy/MM/dd")


        self.filter_date_to = JalaliDateEdit()
        self.filter_date_to.setJalaliDate(jdate.today().year, jdate.today().month, jdate.today().day)
        self.filter_date_to.setDisplayFormat("yyyy/MM/dd")

        # اضافه کردن به نوار ابزار
        toolbar.addWidget(QLabel("فیلتر:"))
        toolbar.addWidget(self.filter_student)
        toolbar.addWidget(QLabel("از:"))
        toolbar.addWidget(self.filter_date_from)
        toolbar.addWidget(QLabel("تا:"))
        toolbar.addWidget(self.filter_date_to)
        toolbar.addStretch()
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.refresh_btn)

        # جدول پرداخت‌ها
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(6)
        self.payments_table.setHorizontalHeaderLabels(
            ["دانش‌آموز", "مبلغ", "تاریخ", "روش پرداخت", "شماره رسید", "توضیحات"]
        )
        self.payments_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.payments_table.setStyleSheet(
            """
            QTableWidget {
                border: 1px solid #ddd;
                background: white;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """
        )

        # اضافه کردن به لایه اصلی
        layout.addLayout(toolbar)
        layout.addWidget(self.payments_table)

        self.setLayout(layout)

        # اتصال سیگنال‌ها
        self.add_btn.clicked.connect(self.show_add_payment_dialog)
        self.refresh_btn.clicked.connect(self.load_payments)

    def load_payments(self):
        try:
            payments = self.db_manager.get_payments()
            self.payments_table.setRowCount(len(payments))
            
            for row, payment in enumerate(payments):
                # تبدیل تاریخ میلادی به شمسی
                jd = jdate.fromgregorian(date=payment['date'])
                jalali_date = f"{jd.year}/{jd.month:02d}/{jd.day:02d}"
                
                # نمایش مبلغ با اعداد فارسی
                amount_fa = digits.en_to_fa(f"{payment['amount']:,}")
            for row, payment in enumerate(payments):
                self.payments_table.setItem(
                    row, 0, QTableWidgetItem(payment["student"])
                )
                self.payments_table.setItem(
                    row, 1, QTableWidgetItem(f"{payment['amount']:,} تومان")
                )
                self.payments_table.setItem(row, 2, QTableWidgetItem(payment["date"]))
                self.payments_table.setItem(row, 3, QTableWidgetItem(payment["method"]))
                self.payments_table.setItem(
                    row, 4, QTableWidgetItem(payment["receipt"])
                )
                self.payments_table.setItem(
                    row, 5, QTableWidgetItem(payment.get("description", ""))
                )

                # رنگ‌آمیزی سطرها به صورت یک در میان
                if row % 2 == 0:
                    for col in range(6):
                        self.payments_table.item(row, col).setBackground(
                            QColor(240, 248, 255)
                        )

        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بارگذاری پرداخت‌ها: {str(e)}")

    def show_add_payment_dialog(self):
        from add_payment_dialog import AddPaymentDialog  # import دیالوگ ثبت پرداخت

        students = self.db_manager.read_students()  # دریافت لیست دانش‌آموزان
        dialog = AddPaymentDialog(students, self)
        dialog.payment_added.connect(self.handle_new_payment)
        dialog.exec_()

    def handle_new_payment(self, payment_data):
        try:
            # ذخیره پرداخت جدید در دیتابیس
            self.db_manager.add_payment(payment_data)
            self.load_payments()  # بروزرسانی جدول
            QMessageBox.information(self, "موفق", "پرداخت با موفقیت ثبت شد")
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ثبت پرداخت: {str(e)}")
