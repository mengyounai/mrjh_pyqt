import json
import os
from tkinter import messagebox

import requests as requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import  QFileDialog



# command = 'where python'
# process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
# output, _ = process.communicate()
#
# # 解码输出结果
# output = output.decode('gbk')
# # 去除换行符
# output = output.strip()
#
# # 使用正则表达式匹配路径中的 python.exe
# pattern = r".*\\Python\\([^\\]+\\python\.exe)"
# match = re.search(pattern, output)
#
# path_to_python = '"' + match.group(0) + '"'
# airtest_address = r"F:\study\软件\AirtestIDE"
#
# print(path_to_python)
data = {
    "code": "qaq",
    "version": 1,
    "is_gather": 0,
    "type": 0,
    "level": 1,
    "time": "100",
    "is_protect": 0,
    "is_train": 0,
    "is_shuaye": 0,
    "is_switch": 0,
    "is_search": 0,
    "is_sea_monster": 0,
    "is_gift": 0,
    "gift_time": "18",
    "protect_level": 0,
    "main_task": "1"
}

code = ''

multi_number = 1


def readConfig(code2):
    global data
    if code2 == '':
        return
    data2 = {'code': code2}

    response = requests.get('http://gasaiyuno.top:8080/readConfig', params=data2)
    # 处理响应
    if response.text != '':
        # 请求成功
        # data = response.text
        print(response.text)
        data = json.loads(response.text)



def saveConfig(code2, config):
    data = {'code': code2, 'config': config}

    response = requests.get('http://gasaiyuno.top:8080/saveConfig', params=data)
    return response.text


class WriteThread(QThread):
    finished = pyqtSignal(str)
    code_signal = pyqtSignal(str)

    def __init__(self):
        self.value = ''
        super().__init__()

    def work(self):
        # 在后台线程中执行写入操作
        data_json = json.dumps(data)
        res = saveConfig(self.value, data_json)
        with open("code.txt", "w", encoding="utf-8") as f:
            self.value = self.value.strip('"')
            f.write(self.value)
        self.finished.emit(res)

    def receive(self, value):
        self.value = value

    def run(self):
        self.work()


class GetConfigThread(QThread):
    finished = pyqtSignal(str)
    code_signal = pyqtSignal(str)

    def __init__(self):
        self.value = ''
        super().__init__()

    def work(self):
        with open("code.txt", "w", encoding="utf-8") as f:
            self.value = self.value.strip('"')
            f.write(self.value)
        readConfig(self.value)
        data_json = json.dumps(data)
        self.finished.emit(data_json)

    def receive(self, value):
        self.value = value

    def run(self):
        # 在后台线程中执行写入操作
        self.work()


def getConfig():
    global data
    try:
        with open("config.txt", "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {
            "version": 1,
            "is_gather": "开启",
            "type": 4,
            "level": 3,
            "time": "120",
            "is_protect": "开启1",
            "is_train": "开启",
            "is_shuaye": "开启1",
            "is_switch": "开启",
            "is_search": "开启1",
            "is_sea_monster": "开启1",
            "is_gift": "18",
            "gift_time": "18",
            "protect_level": "8",
            "main_task": "2",
        }


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print("文件夹创建成功")
        except OSError as e:
            print(f"创建文件夹失败：{e}")
    else:
        print("文件夹已存在")


def init_file():
    # 检查文件是否存在
    if not os.path.exists("code.txt"):
        # 使用 "w" 模式打开文件，如果文件不存在则自动创建
        with open("code.txt", "w") as file:
            # 可以在此处进行文件的写入操作
            file.write('')
    if not os.path.exists("address.txt"):
        # 使用 "w" 模式打开文件，如果文件不存在则自动创建
        with open("address.txt", "w") as file:
            # 可以在此处进行文件的写入操作
            file.write('')
    # files_to_check = ['mrjh1.bat', 'mrjh2.bat', 'mrjh3.bat', 'mrjh4.bat', 'mrjh5.bat', 'mrjh6.bat', 'mrjh7.bat',
    #                   'mrjh8.bat', 'mrjh9.bat']
    #
    # file_path = os.getcwd() + "/" + "多开"
    # create_folder(file_path)
    # file_path = os.getcwd() + "/" + "log" + "/" + "result"
    # create_folder(file_path)
    # i = 1
    # while i <= 9:
    #     file_path = os.getcwd() + "/" + "多开" + "/" + str(i) + "/" + "mrjh.air"
    #     create_folder(file_path)
    #     i += 1
    # i = 1
    # for file_name in files_to_check:
    #     if not os.path.exists(file_name):
    #         file_name = os.getcwd() + "/" + "多开" + "/" + str(i) + "/" + "mrjh.air" + "/" + "mrjh.bat"
    #         with open(file_name, 'w') as file:
    #             # 可以在此处进行文件的写入操作
    #             file.write('')
    #             i += 1
    #             print(f'{file_name} 文件已创建')
    #     else:
    #         print(f'{file_name} 文件已存在')

def getCode():
    global code
    try:
        with open("code.txt", "r", encoding="utf-8") as f:
            code = f.readline()
    except (FileNotFoundError, json.JSONDecodeError):
        return


def getAddress():
    global airtest_address
    try:
        with open("address.txt", "r", encoding="utf-8") as f:
            airtest_address = f.readline()
    except (FileNotFoundError, json.JSONDecodeError):
        return


init_file()
getCode()
getAddress()
readConfig(code)


class Ui_MainWindow(object):

    def __init__(self):
        self.data = data
        self.thread_2 = GetConfigThread()
        self.thread_2.code_signal.connect(self.handle_value_changed)
        self.thread_2.finished.connect(self.on_code_finished)

        self.file_dialog = QFileDialog()

    def data_in_ui(self):
        self.checkBox.setChecked(self.data['is_gather'])
        self.comboBox.setCurrentIndex(self.data['type'])
        self.comboBox_2.setCurrentIndex(self.data['level'] - 1)
        self.checkBox_2.setChecked(self.data['is_protect'])
        self.comboBox_3.setCurrentIndex(self.data['protect_level'])
        self.checkBox_3.setChecked(self.data['is_train'])
        self.checkBox_4.setChecked(self.data['is_shuaye'])
        self.checkBox_5.setChecked(self.data['is_switch'])
        self.checkBox_6.setChecked(self.data['is_sea_monster'])
        self.checkBox_7.setChecked(self.data['is_search'])
        self.checkBox_8.setChecked(self.data['is_gift'])
        self.comboBox_4.setCurrentIndex(self.data['version'])
        self.comboBox_5.setCurrentIndex(int(self.data['main_task']))
        self.lineEdit.setText(self.data['time'])

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 10, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 150, 41, 16))
        self.label_2.setObjectName("label_2")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(50, 150, 31, 19))
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(110, 150, 87, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(210, 150, 81, 16))
        self.label_3.setObjectName("label_3")

        # 采集等级
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(280, 150, 87, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")

        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(50, 190, 31, 19))
        self.checkBox_2.setText("")
        self.checkBox_2.setObjectName("checkBox_2")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(70, 190, 71, 16))
        self.label_4.setObjectName("label_4")
        # 开罩时间
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(140, 190, 87, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(240, 190, 261, 16))
        self.label_5.setObjectName("label_5")

        # 造兵
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(50, 220, 31, 19))
        self.checkBox_3.setText("")
        self.checkBox_3.setObjectName("checkBox_3")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(70, 220, 41, 16))
        self.label_6.setObjectName("label_6")

        # 刷野
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setGeometry(QtCore.QRect(110, 220, 31, 19))
        self.checkBox_4.setText("")
        self.checkBox_4.setObjectName("checkBox_4")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(130, 220, 41, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(70, 260, 101, 16))
        self.label_8.setObjectName("label_8")

        # 切号
        self.checkBox_5 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_5.setGeometry(QtCore.QRect(50, 260, 31, 19))
        self.checkBox_5.setText("")
        self.checkBox_5.setObjectName("checkBox_5")

        # 保存按钮
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(340, 450, 120, 40))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.button_clicked)

        # # 配置生成按钮
        # self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton_3.setGeometry(QtCore.QRect(340, 420, 120, 40))
        # self.pushButton_3.setObjectName("pushButton_3")
        # self.pushButton_3.clicked.connect(self.generate_startup_file)

        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(200, 220, 41, 16))
        self.label_12.setObjectName("label_12")

        # 海怪
        self.checkBox_6 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_6.setGeometry(QtCore.QRect(240, 220, 31, 19))
        self.checkBox_6.setText("")
        self.checkBox_6.setObjectName("checkBox_6")

        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(260, 220, 41, 16))
        self.label_13.setObjectName("label_13")

        # 寻宝
        self.checkBox_7 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_7.setGeometry(QtCore.QRect(180, 220, 31, 19))
        self.checkBox_7.setText("")
        self.checkBox_7.setObjectName("checkBox_7")

        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(320, 220, 71, 16))
        self.label_15.setObjectName("label_15")

        # 活跃奖励
        self.checkBox_8 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_8.setGeometry(QtCore.QRect(300, 220, 31, 19))
        self.checkBox_8.setText("")
        self.checkBox_8.setObjectName("checkBox_8")

        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(50, 120, 71, 16))
        self.label_14.setObjectName("label_14")

        # 版本
        self.comboBox_4 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_4.setGeometry(QtCore.QRect(120, 120, 87, 22))
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(50, 300, 72, 15))
        self.label_9.setObjectName("label_9")

        # 间隔
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(120, 300, 51, 21))
        self.lineEdit.setObjectName("lineEdit")

        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(50, 80, 72, 15))
        self.label_10.setObjectName("label_10")

        # 多开数
        self.comboBox_5 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_5.setGeometry(QtCore.QRect(120, 330, 80, 21))
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")

        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(50, 330, 72, 15))
        self.label_16.setObjectName("label_16")

        # airtest地址
        # self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        # self.lineEdit_4.setGeometry(QtCore.QRect(200, 330, 300, 21))
        # self.lineEdit_4.setObjectName("lineEdit_4")
        # self.lineEdit_4.setText(airtest_address)
        #
        # self.button_airtest = QtWidgets.QPushButton(self.centralwidget)
        # self.button_airtest.setGeometry(QtCore.QRect(500, 325, 80, 30))
        # self.button_airtest.setObjectName("button_airtest")
        # self.button_airtest.clicked.connect(self.open_file_dialog)

        # 激活码
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(120, 80, 250, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setText(code)

        # 激活码按钮
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(400, 80, 71, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.button_getConfig)

        # 创建一个整数验证器
        self.int_validator = QIntValidator(self.centralwidget)
        self.lineEdit.setValidator(self.int_validator)

        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

        self.data_in_ui()

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "末日进化脚本"))
        self.label.setText(_translate("mainWindow", "自动辅助系统设置"))
        self.label_2.setText(_translate("mainWindow", "采集"))
        self.comboBox.setItemText(0, _translate("mainWindow", "水"))
        self.comboBox.setItemText(1, _translate("mainWindow", "罐头"))
        self.comboBox.setItemText(2, _translate("mainWindow", "石油"))
        self.comboBox.setItemText(3, _translate("mainWindow", "矿石"))
        self.comboBox.setItemText(4, _translate("mainWindow", "水罐混采"))
        self.comboBox.setItemText(5, _translate("mainWindow", "油矿混采"))

        self.label_3.setText(_translate("mainWindow", "采集级别"))
        self.comboBox_2.setItemText(0, _translate("mainWindow", "1级"))
        self.comboBox_2.setItemText(1, _translate("mainWindow", "2级"))
        self.comboBox_2.setItemText(2, _translate("mainWindow", "3级"))
        self.comboBox_2.setItemText(3, _translate("mainWindow", "4级"))
        self.comboBox_2.setItemText(4, _translate("mainWindow", "5级"))
        self.comboBox_2.setItemText(5, _translate("mainWindow", "6级"))
        self.comboBox_2.setItemText(6, _translate("mainWindow", "7级"))
        self.comboBox_2.setItemText(7, _translate("mainWindow", "8级"))
        self.comboBox_2.setItemText(8, _translate("mainWindow", "9级"))
        self.label_4.setText(_translate("mainWindow", "自动开罩"))
        self.comboBox_3.setItemText(0, _translate("mainWindow", "8小时"))
        self.comboBox_3.setItemText(1, _translate("mainWindow", "1天"))
        self.comboBox_3.setItemText(2, _translate("mainWindow", "3天"))
        self.comboBox_3.setItemText(3, _translate("mainWindow", "7天"))
        self.label_5.setText(_translate("mainWindow", "优先使用背包道具，没有则用钻石购买"))
        self.label_6.setText(_translate("mainWindow", "造兵"))
        self.label_7.setText(_translate("mainWindow", "打野"))
        self.label_8.setText(_translate("mainWindow", "切号"))
        self.pushButton.setText(_translate("mainWindow", "保存"))
        # self.pushButton_3.setText(_translate("mainWindow", "生成配置文件"))
        self.pushButton_2.setText(_translate("mainWindow", "读取"))
        # self.button_airtest.setText(_translate("mainWindow", "启动路径"))
        self.label_12.setText(_translate("mainWindow", "寻宝"))
        self.label_13.setText(_translate("mainWindow", "海怪"))
        self.label_15.setText(_translate("mainWindow", "活跃领取"))
        self.label_14.setText(_translate("mainWindow", "游戏版本"))
        self.label_10.setText(_translate("mainWindow", "激活码"))
        self.comboBox_4.setItemText(0, _translate("mainWindow", "官网"))
        self.comboBox_4.setItemText(1, _translate("mainWindow", "华为"))
        self.comboBox_4.setItemText(2, _translate("mainWindow", "vivo"))

        self.comboBox_5.setItemText(0, _translate("mainWindow", "采集"))
        self.comboBox_5.setItemText(1, _translate("mainWindow", "主线"))

        self.label_9.setText(_translate("mainWindow", "循环时间"))
        self.label_16.setText(_translate("mainWindow", "模式选择"))
        # self.checkBox.setText(_translate("MainWindow", "采集"))
        # self.checkBox_2.setText(_translate("MainWindow", "自动开罩"))
        # self.checkBox_3.setText(_translate("MainWindow", "造兵"))
        # self.checkBox_4.setText(_translate("MainWindow", "打野"))
        # self.checkBox_5.setText(_translate("MainWindow", "切号"))
        # self.checkBox_6.setText(_translate("MainWindow", "海怪"))
        # self.checkBox_7.setText(_translate("MainWindow", "寻宝"))
        # self.checkBox_8.setText(_translate("MainWindow", "活跃领取"))

    # def generate_startup_file(self):
    #     multi_number = int(self.lineEdit_3.text())
    #     i = 1
    #     start_config = ''
    #     folder_list = []
    #     while i <= multi_number:
    #         multi_config = []
    #         # file_name = "mrjh" + str(i) + ".bat"
    #         file_name = os.getcwd() + "/" + "多开" + "/" + str(i) + "/" + "mrjh.air" + "/" + "mrjh.bat"
    #         port = 5554 + 2 * (i - 1)
    #         j = 1  # 重置 j 的值)
    #         folder_list.append(fr"{file_name}")
    #
    #         while j <= multi_number:
    #             config_line = path_to_python + " " + "-u" + " " + '"' + airtest_address \
    #                           + '/sample/custom_launcher.py' + '"' + " " \
    #                           + '"' + os.getcwd() + "/" + "多开" + "/" + str(j) + "/mrjh.air" + '"' \
    #                           + " " + "--device" + " " + 'android://127.0.0.1:5037/emulator-' \
    #                           + str(port) + "?" + " " + "--log" \
    #                           + " " + '"' + os.getcwd() + "/" + "log" + "/result" + '"' + "\n"
    #
    #             multi_config.append(config_line)
    #             j += 1
    #
    #
    #         with open(file_name, "w", encoding="gbk") as f:
    #             f.write("\n".join(multi_config))
    #
    #         i += 1
    #     # messagebox.showinfo("生成完毕", "启动文件配置成功！")
    #     for folder_path in folder_list:
    #         folder_directory = os.path.dirname(os.path.abspath(folder_path))
    #         start_config += f'cd /d "{folder_directory}"\n'
    #         start_config += f'start "" "{folder_path}"\n'
    #     with open("start.bat", "w", encoding="gbk") as f:
    #         f.write(start_config)
    #         # f.write("\n".join(start_config))


    def button_clicked(self):
        global data

        data['version'] = self.comboBox_4.currentIndex()
        data['main_task'] = self.comboBox_5.currentIndex()
        data['is_gather'] = self.checkBox.checkState()
        data['type'] = self.comboBox.currentIndex()
        data['level'] = self.comboBox_2.currentIndex() + 1
        data['time'] = "0" if self.lineEdit.text() == '' else self.lineEdit.text()
        data['is_protect'] = self.checkBox_2.checkState()
        data['is_train'] = self.checkBox_3.checkState()
        data['is_shuaye'] = self.checkBox_4.checkState()
        data['is_switch'] = self.checkBox_5.checkState()
        data['is_search'] = self.checkBox_7.checkState()
        data['is_sea_monster'] = self.checkBox_6.checkState()
        data['is_gift'] = self.checkBox_8.checkState()
        data['protect_level'] = self.comboBox_3.currentIndex()

        self.thread = WriteThread()
        self.thread.receive(self.lineEdit_2.text())
        self.thread.finished.connect(self.on_write_finished)
        self.thread.start()

        # self.generate_startup_file()

    def button_getConfig(self):
        self.thread_2.receive(self.lineEdit_2.text())
        self.thread_2.start()

    def handle_value_changed(self, value):
        global data
        self.data = value

    def on_write_finished(self, value):
        self.pushButton.setEnabled(True)
        if value == '读取成功':
            messagebox.showinfo("保存成功", "配置文件保存成功！")
        else:
            messagebox.showinfo("保存失败", value)

    def on_code_finished(self, value):
        global data
        self.data = json.loads(value)
        self.pushButton_2.setEnabled(True)
        messagebox.showinfo("读取成功", "配置文件读取成功！")
        self.data_in_ui()

    def open_file_dialog(self):
        global airtest_address
        try:
            file_path = self.file_dialog.getExistingDirectory(None, "选择文件")
        except Exception as e:
            print("发生错误:", str(e))
        if file_path:
            self.lineEdit_4.setText(file_path)
            airtest_address = file_path
        with open("address.txt", "w", encoding="utf-8") as f:
            f.write(file_path)

