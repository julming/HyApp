# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from osgeo import gdal
import numpy as np
from PyQt5.QtGui import QPixmap, QImage, QPainter, qRgba
from PyQt5.QtCore import Qt
from DialogML import *
from DiagDialog import *
from PlotDialog import *
class RasterViewer(QtWidgets.QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿
        self.setRenderHint(QPainter.SmoothPixmapTransform)  # 启用平滑变换
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)  # 启用拖动模式

        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)
        self.pixmap_item = None  # Initialize pixmap_item

    def load_raster(self, raster_path):
        dataset = gdal.Open(raster_path)  # 打开栅格文件
        if dataset is None:
            return
        band = dataset.GetRasterBand(1)  # 获取第一个波段
        raster_data = band.ReadAsArray()  # 读取栅格数据为数组
        nodata_value = band.GetNoDataValue()  # 获取无效值

        # 将栅格数据归一化为0-255，并处理无效值
        valid_mask = raster_data != nodata_value
        raster_data_normalized = np.zeros_like(raster_data, dtype=np.uint8)
        raster_data_normalized[valid_mask] = ((raster_data[valid_mask] - raster_data[valid_mask].min()) /
                                              (raster_data[valid_mask].max() - raster_data[
                                                  valid_mask].min()) * 255).astype(np.uint8)

        height, width = raster_data.shape
        bytes_per_line = width
        q_image = QImage(raster_data_normalized.data, width, height, bytes_per_line, QImage.Format_Indexed8)

        # 创建颜色表，将无效值设置为透明
        color_table = [qRgba(i, i, i, 255) for i in range(256)]
        if nodata_value is not None:
            color_table[0] = qRgba(0, 0, 0, 0)  # 将无效值设置为透明
        q_image.setColorTable(color_table)

        pixmap = QPixmap.fromImage(q_image)
        if self.pixmap_item:
            self.scene.removeItem(self.pixmap_item)  # 移除旧的 pixmap_item
        self.pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)

    def wheelEvent(self, event):
        zoom_factor = 1.25  # 缩放因子
        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)  # 放大
        else:
            self.scale(1 / zoom_factor, 1 / zoom_factor)  # 缩小


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1037, 762)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("图标/Soil.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        mainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 1011, 671))
        self.widget.setObjectName("widget")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1037, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(self.menubar)
        self.menu_5.setObjectName("menu_5")
        self.menu_6 = QtWidgets.QMenu(self.menubar)
        self.menu_6.setObjectName("menu_6")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(mainWindow)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        self.toolBar.setFont(font)
        self.toolBar.setObjectName("toolBar")
        mainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action = QtWidgets.QAction(mainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("图标/土壤含盐量.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action.setIcon(icon1)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(mainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("图标/资源 12.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_2.setIcon(icon2)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(mainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("图标/土壤含水量.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_3.setIcon(icon3)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(mainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("图标/盐类衍生物.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_4.setIcon(icon4)
        self.action_4.setObjectName("action_4")
        self.action_5 = QtWidgets.QAction(mainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("图标/土壤肥力.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_5.setIcon(icon5)
        self.action_5.setObjectName("action_5")
        self.action_6 = QtWidgets.QAction(mainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("图标/风险诊断.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_6.setIcon(icon6)
        self.action_6.setObjectName("action_6")
        self.action_7 = QtWidgets.QAction(mainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("图标/地图制图.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_7.setIcon(icon7)
        self.action_7.setObjectName("action_7")
        self.action_8 = QtWidgets.QAction(mainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("图标/分类图片大标题.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_8.setIcon(icon8)
        self.action_8.setObjectName("action_8")
        self.action_9 = QtWidgets.QAction(mainWindow)
        self.action_9.setCheckable(True)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("图标/24gf-folderOpen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_9.setIcon(icon9)
        self.action_9.setObjectName("action_9")
        self.action_10 = QtWidgets.QAction(mainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("图标/放大.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_10.setIcon(icon10)
        self.action_10.setObjectName("action_10")
        self.action_11 = QtWidgets.QAction(mainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("图标/缩小.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_11.setIcon(icon11)
        self.action_11.setObjectName("action_11")
        self.action_12 = QtWidgets.QAction(mainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("图标/保存.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_12.setIcon(icon12)
        self.action_12.setObjectName("action_12")
        self.action_13 = QtWidgets.QAction(mainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("图标/平移.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_13.setIcon(icon13)
        self.action_13.setObjectName("action_13")
        self.action_14 = QtWidgets.QAction(mainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("图标/功能介绍.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_14.setIcon(icon14)
        self.action_14.setObjectName("action_14")
        self.action_15 = QtWidgets.QAction(mainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("图标/帮助.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_15.setIcon(icon15)
        self.action_15.setObjectName("action_15")
        self.menu.addAction(self.action_9)
        self.menu.addAction(self.action_12)
        self.menu_2.addAction(self.action)
        self.menu_2.addAction(self.action_2)
        self.menu_2.addAction(self.action_3)
        self.menu_4.addAction(self.action_7)
        self.menu_4.addAction(self.action_8)
        self.menu_5.addAction(self.action_14)
        self.menu_5.addAction(self.action_15)
        self.menu_6.addAction(self.action_4)
        self.menu_6.addAction(self.action_5)
        self.menu_6.addAction(self.action_6)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_6.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_5.menuAction())
        self.toolBar.addAction(self.action_9)
        self.toolBar.addAction(self.action_10)
        self.toolBar.addAction(self.action_11)
        self.toolBar.addAction(self.action_13)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action)
        self.toolBar.addAction(self.action_2)
        self.toolBar.addAction(self.action_3)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_4)
        self.toolBar.addAction(self.action_5)
        self.toolBar.addAction(self.action_6)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_7)
        self.toolBar.addAction(self.action_8)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_14)
        self.toolBar.addAction(self.action_15)
        self.toolBar.addSeparator()

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

        # Connect the open file action
        self.action_9.triggered.connect(self.open_dialog)
        self.action.triggered.connect(self.open_dialogML)
        self.action_4.triggered.connect(self.open_diagdialog)
        # self.action_7.triggered.connect(self.open_dialogPlot)
        self.action_7.triggered.connect(self.open_raster_plot_dialog)


    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "土壤水肥盐诊断系统"))
        self.menu.setTitle(_translate("mainWindow", "文件"))
        self.menu_2.setTitle(_translate("mainWindow", "结果计算"))
        self.menu_4.setTitle(_translate("mainWindow", "结果制图"))
        self.menu_5.setTitle(_translate("mainWindow", "帮助"))
        self.menu_6.setTitle(_translate("mainWindow", "结果诊断"))
        self.toolBar.setWindowTitle(_translate("mainWindow", "toolBar"))
        self.action.setText(_translate("mainWindow", "土壤含盐量"))
        self.action_2.setText(_translate("mainWindow", "土壤肥力"))
        self.action_3.setText(_translate("mainWindow", "土壤水分含量"))
        self.action_4.setText(_translate("mainWindow", "土壤盐渍化程度诊断"))
        self.action_5.setText(_translate("mainWindow", "土壤肥力诊断"))
        self.action_6.setText(_translate("mainWindow", "水肥盐一体化诊断"))
        self.action_7.setText(_translate("mainWindow", "空间分布制图"))
        self.action_8.setText(_translate("mainWindow", "诊断结果制图"))
        self.action_9.setText(_translate("mainWindow", "打开文件"))
        self.action_10.setText(_translate("mainWindow", "放大"))
        self.action_11.setText(_translate("mainWindow", "缩小"))
        self.action_12.setText(_translate("mainWindow", "保存"))
        self.action_13.setText(_translate("mainWindow", "移动"))
        self.action_14.setText(_translate("mainWindow", "功能介绍"))
        self.action_15.setText(_translate("mainWindow", "关于水肥盐诊断系统"))

    def open_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(None, "打开文件", "", "All Files (*);;TIF Files (*.tif)", options=options)
        if file_name:
            self.raster_viewer.load_raster(file_name)

    def open_dialogML(self):
        dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(dialog)
        dialog.exec_()

    def open_diagdialog(self):
        dialog = QtWidgets.QDialog()
        ui = Ui_diagnosisDialog()
        ui.setupUi(dialog)
        dialog.exec_()

    def open_raster_plot_dialog(self):
        # 打开栅格数据绘图对话框
        self.raster_plot_dialog = RasterPlotDialog()
        self.raster_plot_dialog.exec_()  # 使用 exec_() 显示对话框，直到用户关闭

    def open_dialogPlot(self):
        dialog = QtWidgets.QDialog()
        ui = RasterPlotDialog()
        ui.setupUi(dialog)
        dialog.exec_()

class RasterViewerApp(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.raster_viewer = RasterViewer()
        layout = QtWidgets.QVBoxLayout(self.widget)
        layout.addWidget(self.raster_viewer)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = RasterViewerApp()
    window.show()
    sys.exit(app.exec_())
