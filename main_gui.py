import sys
from database import DataBase
import keyboard
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QTableWidget, QTableWidgetItem, QTabWidget,
                             QComboBox, QDateEdit, QMessageBox, QFormLayout,
                             QGroupBox, QFrame, QStackedWidget)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor
from PyQt5.QtCore import Qt, QDate
class SchoolManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DataBase()
        self.setWindowTitle("دارالفنون - سیستم مدیریت مدرسه")
        self.setGeometry(100, 100, 1200, 700)
        self.setWindowIcon(QIcon("school_icon.png"))
        
        # رنگ‌های اصلی برنامه
        self.primary_color = QColor(52, 152, 219)
        self.secondary_color = QColor(236, 240, 241)
        self.accent_color = QColor(231, 76, 60)
        
        self.initUI()
        
    def initUI(self):
        # نوار وضعیت اصلی
        self.statusBar().showMessage("آماده")
        
        # نوار منوی اصلی
        menubar = self.menuBar()
        
        # منوی فایل
        file_menu = menubar.addMenu("فایل")
        exit_action = file_menu.addAction("خروج")
        exit_action.triggered.connect(self.close)
        
        # منوی کمک
        help_menu = menubar.addMenu("کمک")
        about_action = help_menu.addAction("درباره")
        about_action.triggered.connect(self.show_about)
        
        # ویجت مرکزی
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # لایه‌بندی اصلی
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # نوار کناری
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet(f"background-color: {self.primary_color.name()};")
        
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar.setLayout(sidebar_layout)
        
        # لوگو
        logo = QLabel("SchoolVision")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("color: white; font-size: 18px; font-weight: bold; padding: 20px;")
        sidebar_layout.addWidget(logo)
        
        # دکمه‌های نوار کناری
        buttons = [
            ("داشبورد", "static/icon/dashboard.png"),
            ("دانش‌آموزان", "static/icon/students.png"),
            ("معلمان", "static/icon/teachers.png"),
            ("کلاس‌ها", "static/icon/classes.png"),
            ("مالی", "static/icon/finance.png"),
            ("گزارشات", "static/icon/reports.png"),
            ("تنظیمات", "static/icon/settings.png")
        ]
        
        for text, icon in buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon))
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    text-align: left;
                    padding: 10px;
                    border: none;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            btn.setCursor(Qt.PointingHandCursor)
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()
        
        # بخش محتویات اصلی
        content_area = QWidget()
        content_layout = QVBoxLayout()
        content_area.setLayout(content_layout)
        
        # نوار عنوان
        title_bar = QWidget()
        title_bar.setStyleSheet(f"background-color: {self.secondary_color.name()}; padding: 10px;")
        title_layout = QHBoxLayout()
        title_bar.setLayout(title_layout)
        
        self.title_label = QLabel("داشبورد")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        title_layout.addWidget(self.title_label)
        
        user_info = QLabel("مدیر | خروج")
        user_info.setStyleSheet("color: #7f8c8d;")
        title_layout.addWidget(user_info, alignment=Qt.AlignRight)
        
        content_layout.addWidget(title_bar)
        
        # تب‌های محتوا
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
        
        # تب داشبورد
        dashboard_tab = QWidget()
        self.init_dashboard_tab(dashboard_tab)
        self.tabs.addTab(dashboard_tab, "داشبورد")
        
        # تب دانش‌آموزان
        students_tab = QWidget()
        self.init_students_tab(students_tab)
        self.tabs.addTab(students_tab, "دانش‌آموزان")
        
        content_layout.addWidget(self.tabs)
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area)
        
    def init_dashboard_tab(self, tab):
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # کارت‌های آماری
        stats_layout = QHBoxLayout()
        
        stats = [
            ("تعداد دانش‌آموزان", "350", self.primary_color),
            ("تعداد معلمان", "28", QColor(155, 89, 182)),
            ("کلاس‌های فعال", "15", QColor(26, 188, 156)),
            ("پرداخت‌های امروز", "12", QColor(241, 196, 15))
        ]
        
        for title, value, color in stats:
            card = QGroupBox(title)
            card.setStyleSheet(f"""
                QGroupBox {{
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 15px;
                    background: white;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    color: #7f8c8d;
                }}
            """)
            
            card_layout = QVBoxLayout()
            
            value_label = QLabel(value)
            value_label.setStyleSheet(f"""
                font-size: 28px;
                font-weight: bold;
                color: {color.name()};
            """)
            value_label.setAlignment(Qt.AlignCenter)
            
            card_layout.addWidget(value_label)
            card.setLayout(card_layout)
            stats_layout.addWidget(card)
        
        layout.addLayout(stats_layout)
        
        # نمودارها و اطلاعات اضافی
        charts_group = QGroupBox("وضعیت کلی")
        charts_layout = QHBoxLayout()
        charts_group.setLayout(charts_layout)
        
        # نمودار نمونه (در عمل می‌توان از matplotlib یا دیگر کتابخانه‌ها استفاده کرد)
        chart1 = QLabel("نمودار حضور و غیاب ماهانه")
        chart1.setStyleSheet("""
            background: white;
            border: 1px solid #ddd;
            padding: 50px;
            qproperty-alignment: AlignCenter;
        """)
        
        chart2 = QLabel("نمودار وضعیت مالی")
        chart2.setStyleSheet("""
            background: white;
            border: 1px solid #ddd;
            padding: 50px;
            qproperty-alignment: AlignCenter;
        """)
        
        charts_layout.addWidget(chart1)
        charts_layout.addWidget(chart2)
        
        layout.addWidget(charts_group)
        
    def init_students_tab(self, tab):
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # نوار ابزار
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout()
        toolbar.setLayout(toolbar_layout)
        
        search_box = QLineEdit()
        search_box.setPlaceholderText("جستجوی دانش‌آموز...")
        search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 300px;
            }
        """)
        
        add_btn = QPushButton("دانش‌آموز جدید")
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.primary_color.name()};
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
        """)
        
        toolbar_layout.addWidget(search_box)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(add_btn)
        
        layout.addWidget(toolbar)
        
        # جدول دانش‌آموزان
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(5)
        self.students_table.setHorizontalHeaderLabels(["شناسه", "نام کامل", "کلاس", "تاریخ ثبت‌نام", "وضعیت"])
        self.students_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                background: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
            }
        """)
        
        # پر کردن جدول با داده‌های نمونه
        self.populate_students_table()
        
        layout.addWidget(self.students_table)
        
    def populate_students_table(self):
        # داده‌های نمونه
        students = self.db.read_students()
        
        self.students_table.setRowCount(len(students))
        
        for row, student in enumerate(students):
            for col, data in enumerate(student):
                item = QTableWidgetItem(data)
                
                # رنگ‌آمیزی وضعیت
                if col == 4:
                    if data == "فعال":
                        item.setForeground(QColor(39, 174, 96))
                    elif data == "غیر فعال":
                        item.setForeground(QColor(192, 57, 43))
                
                self.students_table.setItem(row, col, item)
        
        self.students_table.resizeColumnsToContents()
        
    def show_about(self):
        about_box = QMessageBox()
        about_box.setWindowTitle("درباره SchoolVision")
        about_box.setText("""
            <h3>SchoolVision</h3>
            <p>سیستم مدیریت مدرسه مدرن و هوشمند</p>
            <p>نسخه 1.0.0</p>
            <p>© 2023 تمام حقوق محفوظ است</p>
        """)
        about_box.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # تنظیم استایل کلی برنامه
    app.setStyle("Fusion")
    
    window = SchoolManagementApp()
    window.show()
    sys.exit(app.exec_())