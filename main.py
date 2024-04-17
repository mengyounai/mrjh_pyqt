
import sys
import mrjh
from PyQt5 import QtCore, QtGui, QtWidgets



if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        # 调自定义的界面（即刚转换的.py对象）
        Ui = mrjh.Ui_MainWindow()  # 这里也引用了一次helloworld.py文件的名字注意
        Ui.setupUi(MainWindow)
        # 显示窗口并释放资源
        MainWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        print("发生错误:", str(e))


