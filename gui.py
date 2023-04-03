# 机 构：中国科学院大学
# 程序员：李浩东
# 时 间：2023/3/24 11:54

import Hexadecimal
import Resolution
import pcap
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from scapy.all import *

# 列出当前操作系统的所有网络接口
devs = pcap.findalldevs()

# print(*devs, sep='\n')
# # 定义了一个pcap对象，首个参数devs[3]对应接口名，promisc为真代表打开混杂模式，immediate代表立即模式，启用将不缓存数据包,timeout_ms代表接收数据包的超时时间
# pc = pcap.pcap(devs[4], promisc=True, immediate=True, timeout_ms=50)
# # setfilter用来设置数据包过滤器，比如只想抓http的包，那就通过setfilter(tcp port 80)实现
# pc.setfilter('tcp port 80')

# 把所有网卡都设置成混杂模式
for idx,item in enumerate(devs):
    pc = pcap.pcap(devs[idx], promisc=True, immediate=True, timeout_ms=50)
    pc.setfilter('tcp port 80')

class Sniffer(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(900, 600)
        self.setWindowTitle("My Sniffer")
        self.setUpUI()

    # 定义嗅探器的主界面
    def setUpUI(self):
        global net_card_input
        global quantity_input
        global data_area
        global index_input
        # 总布局
        self.layout1 = QVBoxLayout(self)
        self.layout2 = QHBoxLayout(self)
        # 定义主界面最上面的三个功能
        grid = QGridLayout()
        grid.setSpacing(10)
        net_card = QLabel('网卡名称:')
        quantity = QLabel('抓包数量:')
        index = QLabel('查看/解析序号:')
        net_card_input = QComboBox(self)
        net_card_input.addItem('--请选择--')
        for item in devs:  # 用循环将本地所有的网卡插入网卡名称对应的下拉框内
            net_card_input.addItem(item)
        # net_card_input.addItem('--请选择--')
        # net_card_input.addItem('\\Device\\NPF_{236B1A5F-ECAC-4783-B406-9091AA0AAE13}')
        # net_card_input.addItem('\\Device\\NPF_{96EB3B71-360C-43AE-AAD2-37D7A081888B}')
        # net_card_input.addItem('\\Device\\NPF_{3E25CA9D-0535-4FA8-9BDE-508A137AB467}')
        # net_card_input.addItem('\\Device\\NPF_{7E967EA7-F121-4F8F-ACF1-AA1F62C55359}')
        # net_card_input.addItem('\\Device\\NPF_{881E2E13-C0E8-4AAD-9B34-D31E296281EF}')
        # net_card_input.addItem('\\Device\\NPF_{4D7CF169-344D-43A4-B365-D79E7BAC3A6E}')
        # net_card_input.addItem('\\Device\\NPF_{CFEFF375-63DE-4764-980F-FE9B0D5A31D0}')
        # net_card_input.addItem('\\Device\\NPF_{E2A690B2-7688-42B4-846D-B3BA3E98D582}')
        # net_card_input.addItem('\\Device\\NPF_{AEFCE49D-C8C4-4053-84F3-FB4F3B511972}')
        # net_card_input.addItem('\\Device\\NPF_Loopback}')
        # net_card_input.addItem('\\Device\\NPF_{E50CEC2C-E0B8-447A-9833-12706299D389}')
        # net_card_input.addItem('\\Device\\NPF_{C7C536D6-0E7D-4F72-B386-ED2A01546228}')
        quantity_input = QLineEdit()
        index_input = QLineEdit()

        grid.addWidget(net_card, 0, 0)
        grid.addWidget(net_card_input, 0, 1)
        grid.addWidget(quantity, 0, 2)
        grid.addWidget(quantity_input, 0, 3)
        grid.addWidget(index, 0, 4)
        grid.addWidget(index_input, 0, 5)

        net_card_input.setFixedWidth(350)
        # net_card_input.setFixedHeight(500)

        self.setLayout(grid)
        self.layout1.addLayout(grid)
        self.layout1.addLayout(self.layout2)
        # self.layout1.addStretch(1)

        # 按钮布局
        self.buttonLayout = QVBoxLayout()
        # 按钮
        self.start_capture = QPushButton("开始抓包")
        self.clear_data = QPushButton("清空数据")
        self.binary_information = QPushButton("十六进制信息")
        self.parse_data = QPushButton("解析数据")
        self.exit_sys = QPushButton("退出系统")
        self.buttonLayout.addWidget(self.start_capture)
        self.buttonLayout.addWidget(self.clear_data)
        self.buttonLayout.addWidget(self.binary_information)
        self.buttonLayout.addWidget(self.parse_data)
        self.buttonLayout.addWidget(self.exit_sys)
        self.start_capture.setFixedWidth(100)
        self.start_capture.setFixedHeight(42)
        self.clear_data.setFixedWidth(100)
        self.clear_data.setFixedHeight(42)
        self.binary_information.setFixedWidth(100)
        self.binary_information.setFixedHeight(42)
        self.parse_data.setFixedWidth(100)
        self.parse_data.setFixedHeight(42)
        self.exit_sys.setFixedWidth(100)
        self.exit_sys.setFixedHeight(42)
        font = QFont()
        font.setPixelSize(16)
        self.start_capture.setFont(font)
        self.clear_data.setFont(font)
        self.binary_information.setFont(font)
        self.parse_data.setFont(font)
        self.exit_sys.setFont(font)
        net_card.setFont(font)
        quantity.setFont(font)
        index.setFont(font)

        self.layout2.addLayout(self.buttonLayout)
        # 定义显示抓包数据区域
        self.grid_data = QGridLayout()
        self.data_area = QTextBrowser()
        self.grid_data.addWidget(self.data_area)
        self.layout2.addLayout(self.grid_data)
        # self.layout2.addStretch(1)

        self.setLayout(self.layout2)
        # self.show()

        self.start_capture.clicked.connect(self.start_captureClicked)
        self.clear_data.clicked.connect(self.clear_dataClicked)
        self.binary_information.clicked.connect(self.binary_informationClicked)
        self.parse_data.clicked.connect(self.parse_dataClicked)
        self.exit_sys.clicked.connect(self.exit_sysClicked)

    def start_captureClicked(self):
        # 第一种实现方式：
        # file_path = 'pkts'
        # lists = os.listdir(file_path)  # 获取所有的文件
        # # print(lists)
        # lists_new = []  # 用于提取所有文件里的数字
        # for item in lists:
        #     lists_new.append(int(item[5:13]+item[14:20]))  # 获取所有文件里的数字，转换成int类型
        # # file_new = os.path.join(file_path, lists[-1])
        # file = str(max(lists_new))  # 选取数字最大的文件，也即最新的文件
        # # print(file)
        # for item in lists:  # 找出包含该数字序列的文件名
        #     if item.find(file[:7]) != -1 & item.find(file[8:]) != -1:
        #         file = file_path + '\\' +item  # 找出最新文件的完整路径
        #         print(file)
        #         with open(file, encoding='utf-8') as file_obj:
        #             line = file_obj.readline()
        #             while line != '':
        #                 print(line)
        #                 self.data_area.append(line)
        #                 line = file_obj.readline()
        #         break

        # 第二种实现方式：
        # global hex_data
        # global pdata
        # for item in devs:
        #     if net_card_input.currentText() == item:
        #         # 定义了一个pcap对象，首个参数devs[3]对应接口名，promisc为真代表打开混杂模式，immediate代表立即模式，启用将不缓存数据包,timeout_ms代表接收数据包的超时时间
        #         pc = pcap.pcap(item, promisc=True, immediate=True, timeout_ms=50)
        #         # setfilter用来设置数据包过滤器，比如只想抓http的包，那就通过setfilter(tcp port 80)实现
        #         pc.setfilter('tcp port 80')
        #         filepath = 'pkts/pkts_{}.pcap'.format(time.strftime("%Y%m%d-%H%M%S", time.localtime()))
        #         sys.dataout = open(filepath, mode='w', encoding='utf-8')
        #         count = 0
        #         for ptime, pdata in pc:
        #             count += 1
        #             if count > int(quantity_input.text()):
        #                 break
        #             # 抓包信息读入文件
        #             # print('---------------------------第' + str(count) + '条数据-----------------------------')
        #             # print('序号' + str(count) + ':', ptime, pdata)
        #             print(pdata)
        #             hex_data = hexdump.hexdump(pdata, result='return')
        #             # print(hex_data)
        #             # 界面显示抓包信息
        #             self.data_area.append('---------------------------第' + str(count) + '条数据-----------------------------')
        #             self.data_area.append(hex_data)
        #         sys.dataout.close()
        #         break

        # 第三种实现方式：
        if net_card_input.currentText() == '--请选择--':
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请选择网卡名称！')
            msg_box.exec_()
        elif quantity_input.text() == '':  # 没有输入抓包数量
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入抓包数量！')
            msg_box.exec_()
        else:
            idx = int(quantity_input.text())  # 抓包数量
            if idx > 0:
                global packets
                self.data_area.clear()  # 清空抓包数据
                packets = sniff(iface=net_card_input.currentText(), count=int(quantity_input.text()))  # 抓包
                # print(packets)
                # 显示抓包数据f
                count = 1
                for p in packets:
                    # print(p)
                    self.data_area.append('序号'+str(count)+'：'+str(p))
                    count += 1
            else:
                msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入一个正整数！')
                msg_box.exec_()


    def clear_dataClicked(self):
        self.data_area.clear()  # 清空抓包数据


    def binary_informationClicked(self):
        if index_input.text() == '':  # 没有输入查看序号
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入查看序号！')
            msg_box.exec_()
        else:
            # if quantity_input.text() == '':
            if self.data_area.toPlainText() == '':  # 如果抓包显示区域已被清空，即没有包
                msg_box = QMessageBox(QMessageBox.Warning, '警告', '请先抓包！')
                msg_box.exec_()
            else:
                idx = int(index_input.text())  # 查看序号
                if idx > 0 and idx <= int(quantity_input.text()):
                    # print(idx)
                    # savedDataOut = sys.stdout  # 保存标准输出流
                    # 创建文件out_hex.txt
                    with open('out_hex.txt', 'w+', encoding='UTF-8') as file:
                        sys.stdout = file  # 标准输出重定向至文件
                        for k, p in enumerate(packets):  # 遍历抓包数据
                            if k + 1 == idx:  # 找到要查看的那条数据
                                print(hexdump(p))
                                break
                    # sys.stdout = savedDataOut  # 恢复标准输出流

                    self.hexadecimal = Hexadecimal.Hexadecimal()  # 创建查看窗口对象
                    self.hexadecimal.show()
                    # sys.exit(app.exec_())
                else:
                    msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入正确的查看序号！')
                    msg_box.exec_()


    def parse_dataClicked(self):
        if index_input.text() == '':  # 没有输入解析序号
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入解析序号！')
            msg_box.exec_()
        else:
            # if quantity_input.text() == '':
            if self.data_area.toPlainText() == '':  # 如果抓包显示区域已被清空，即没有包
                msg_box = QMessageBox(QMessageBox.Warning, '警告', '请先抓包！')
                msg_box.exec_()
            else:
                idx = int(index_input.text())  # 解析序号
                if idx > 0 and idx <= int(quantity_input.text()):
                    # print(idx)
                    # savedDataOut = sys.stdout  # 保存标准输出流
                    # 创建文件out.txt
                    with open('out_res.txt', 'w+', encoding='UTF-8') as file:
                        sys.stdout = file  # 标准输出重定向至文件
                        for k, p in enumerate(packets):  # 遍历抓包数据
                            if k + 1 == idx:  # 找到要解析的那条数据
                                print(p.show())
                                break
                    # sys.stdout = savedDataOut  # 恢复标准输出流

                    # savedDataOut = sys.stdout  # 保存标准输出流
                    # count = 1
                    # print(packets)
                    # with open('out.txt', 'w+', encoding='UTF-8') as file:
                    #     sys.dataout = file  # 标准输出重定向至文件
                    #     for p in packets:
                    #         print('-----------------------------第' + str(count) + '条解析数据---------------------------')
                    #         print(p.show())
                    #         count += 1
                    # self.data_area.append(file.read())
                    # sys.stdout = savedDataOut  # 恢复标准输出流
                    # p.show()
                    self.resolution = Resolution.Resolution()  # 创建解析窗口对象
                    self.resolution.show()
                    # sys.exit(app.exec_())
                else:
                    msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入正确的解析序号！')
                    msg_box.exec_()


    def exit_sysClicked(self):
        app = QApplication.instance()
        # print("退出程序")
        # 退出应用程序
        app.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("images/sniffer.jpg"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    main_window = Sniffer()  # 创建主窗口界面对象
    main_window.show()
    sys.exit(app.exec_())