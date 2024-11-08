import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QComboBox, QPushButton, QCheckBox,
                            QSystemTrayIcon, QMenu, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
import json
import os
import requests
from login_handler import LoginHandler

def resource_path(relative_path):
    """获取资源的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 创建临时文件夹，将路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JXNU校园网自动登录")
        self.setFixedSize(400, 350)
        
        # 初始化登录处理器
        self.login_handler = LoginHandler()
        
        # 设置窗口图标
        icon_path = resource_path(os.path.join("assets", "icon.ico"))
        self.setWindowIcon(QIcon(icon_path))
        
        # 初始化系统托盘
        self.setup_tray()
        
        # 主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 账号输入
        account_layout = QHBoxLayout()
        account_label = QLabel("账号:")
        self.account_input = QLineEdit()
        account_layout.addWidget(account_label)
        account_layout.addWidget(self.account_input)
        
        # 密码输入
        password_layout = QHBoxLayout()
        password_label = QLabel("密码:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # 运营商选择
        operator_layout = QHBoxLayout()
        operator_label = QLabel("运营商:")
        self.operator_combo = QComboBox()
        self.operator_combo.addItems([
            "移动校园宽带",
            "联通校园宽带",
            "电信校园宽带"
        ])
        operator_layout.addWidget(operator_label)
        operator_layout.addWidget(self.operator_combo)
        
        # 自动登录选项
        self.auto_login_checkbox = QCheckBox("开机自动登录")
        self.wifi_monitor_checkbox = QCheckBox("连接校园网时自动登录")
        
        # 记住密码选项
        self.remember_checkbox = QCheckBox("记住密码")
        
        # 状态标签
        self.status_label = QLabel("就绪")
        
        # 按钮
        button_layout = QHBoxLayout()
        self.login_button = QPushButton("登录")
        self.save_button = QPushButton("保存配置")
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.save_button)
        
        # 添加所有组件到主布局
        layout.addLayout(account_layout)
        layout.addLayout(password_layout)
        layout.addLayout(operator_layout)
        layout.addWidget(self.remember_checkbox)
        layout.addWidget(self.auto_login_checkbox)
        layout.addWidget(self.wifi_monitor_checkbox)
        layout.addLayout(button_layout)
        layout.addWidget(self.status_label)
        
        # 初始化WiFi监控器
        self.wifi_monitor = WifiMonitor(self)
        
        # 绑定事件
        self.login_button.clicked.connect(self.login)
        self.save_button.clicked.connect(self.save_config)
        
        # 加载配置
        self.load_config()
        
        # 根据配置启动监控
        if self.wifi_monitor_checkbox.isChecked():
            self.wifi_monitor.start()

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = resource_path(os.path.join("assets", "icon.ico"))
        self.tray_icon.setIcon(QIcon(icon_path))
        
        # 创建托盘菜单
        tray_menu = QMenu()
        show_action = tray_menu.addAction("显示")
        show_action.triggered.connect(self.show)
        
        login_action = tray_menu.addAction("重新登录")
        login_action.triggered.connect(self.login)
        
        quit_action = tray_menu.addAction("退出")
        quit_action.triggered.connect(self.quit_app)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # 双击托盘图标显示主窗口
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()

    def quit_app(self):
        QApplication.quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "JXNU校园网登录器",
            "程序已最小化到系统托盘",
            QSystemTrayIcon.Icon.Information,
            2000
        )

    def login(self):
        username = self.account_input.text()
        password = self.password_input.text()
        operator = self.operator_combo.currentText()
        
        if not username or not password:
            self.show_message("错误", "请输入账号和密码", QMessageBox.Icon.Warning)
            return
            
        try:
            self.status_label.setText("正在登录...")
            success, message = self.login_handler.login(username, password, operator)
            
            if success:
                self.status_label.setText("登录成功")
                self.tray_icon.showMessage("登录成功", "校园网已连接", QSystemTrayIcon.Icon.Information)
            else:
                self.status_label.setText(f"登录失败: {message}")
                self.show_message("登录失败", message, QMessageBox.Icon.Warning)
                
        except requests.exceptions.RequestException as e:
            self.status_label.setText("网络错误")
            self.show_message("网络错误", str(e), QMessageBox.Icon.Critical)
        except Exception as e:
            self.status_label.setText("系统错误")
            self.show_message("系统错误", str(e), QMessageBox.Icon.Critical)

    def check_connection(self):
        try:
            response = requests.get("http://www.baidu.com", timeout=5)
            if response.status_code != 200:
                self.login()
        except:
            self.login()

    def show_message(self, title, message, icon=QMessageBox.Icon.Information):
        QMessageBox.information(self, title, message, icon)

    def save_config(self):
        config = {
            'account': self.account_input.text(),
            'password': self.password_input.text() if self.remember_checkbox.isChecked() else '',
            'operator': self.operator_combo.currentText(),
            'remember': self.remember_checkbox.isChecked(),
            'auto_login': self.auto_login_checkbox.isChecked(),
            'wifi_monitor': self.wifi_monitor_checkbox.isChecked()
        }
        with open('config.json', 'w') as f:
            json.dump(config, f)
            
        # 设置开机自启动
        self.set_autostart(self.auto_login_checkbox.isChecked())
        
        # 启动或停止WiFi监控
        if self.wifi_monitor_checkbox.isChecked():
            self.wifi_monitor.start()
        else:
            self.wifi_monitor.stop()

    def load_config(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.account_input.setText(config.get('account', ''))
                if config.get('remember'):
                    self.password_input.setText(config.get('password', ''))
                self.operator_combo.setCurrentText(config.get('operator', '移动'))
                self.remember_checkbox.setChecked(config.get('remember', False))
                self.auto_login_checkbox.setChecked(config.get('auto_login', False))
                self.wifi_monitor_checkbox.setChecked(config.get('wifi_monitor', False))

    def set_autostart(self, enable):
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "JXNU校园网登录器"
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            if enable:
                app_path = os.path.abspath(sys.argv[0])
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'"{app_path}"')
            else:
                try:
                    winreg.DeleteValue(key, app_name)
                except WindowsError:
                    pass
            winreg.CloseKey(key)
        except WindowsError as e:
            self.show_message("错误", f"设置开机自启动失败: {str(e)}", QMessageBox.Icon.Warning)

# 添加WiFi监控类
class WifiMonitor:
    def __init__(self, main_window):
        self.main_window = main_window
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_wifi)
        
    def start(self):
        self.timer.start(5000)  # 每5秒检查一次
        
    def stop(self):
        self.timer.stop()
        
    def check_wifi(self):
        try:
            import subprocess
            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                                 capture_output=True, text=True)
            if "jxnu_stu" in result.stdout:
                # 检查是否已经可以访问互联网
                try:
                    response = requests.get("http://www.baidu.com", timeout=5)
                    if response.status_code != 200:
                        self.main_window.login()
                except:
                    self.main_window.login()
        except Exception as e:
            print(f"WiFi检查错误: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())