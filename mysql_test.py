## appMain.py
## 使用mianUI.py文件中的类 Ui_MianWindow创建app
#pragma execution_character_set("utf-8"
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import MySQLdb
from PyQt5.uic import loadUiType
import datetime
## add
import sys
from PyQt5 import QtWidgets 
from PyQt5.QtSql import * 

from mainUI import Ui_MainWindow

class QmyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btnLoadDb.clicked.connect(self.do_LoadDb)
        self.ui.btnQuery.clicked.connect(self.do_Query)
        self.ui.btnQueryModify.clicked.connect(self.do_QueryModify)
        self.ui.btnQueryDelete.clicked.connect(self.do_QueryDelete)

        self.ui.btnSelectFile.clicked.connect(self.do_Select)
        self.ui.btnAddtoDb.clicked.connect(self.do_Add)





    ###########自定义槽函数#################################################
    #---加载函数-------------------------------------------------------------------
    def do_LoadDb(self):
        #链接数据库
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='1234' , db='db_test',charset='utf8')
        self.cur = self.db.cursor()
        print('Good job!')
        #更新/加载条件选择的comBOX
        self.cur.execute("SELECT DISTINCT data_location FROM clutter_table;")
        name_location = self.cur.fetchall()
        self.ui.cmbDataLocation.clear()
        self.ui.cmbDataLocation.addItem('不限')
        for category in name_location:
            self.ui.cmbDataLocation.addItem(category[0])
        self.cur.execute("SELECT DISTINCT data_model FROM clutter_table;")
        name_model = self.cur.fetchall()
        self.ui.cmbDataModel.clear()
        self.ui.cmbDataModel.addItem('不限')
        for category in name_model:
            self.ui.cmbDataModel.addItem(category[0])
        self.cur.execute("SELECT DISTINCT data_mode FROM clutter_table;")
        name_mode = self.cur.fetchall()
        self.ui.cmbDataMode.clear()
        self.ui.cmbDataMode.addItem('不限')
        for category in name_mode:
            self.ui.cmbDataMode.addItem(category[0])
        self.cur.execute("SELECT DISTINCT data_env FROM clutter_table;")
        name_env = self.cur.fetchall()
        self.ui.cmbDataEnv.clear()
        self.ui.cmbDataEnv.addItem('不限')
        for category in name_env:
            self.ui.cmbDataEnv.addItem(category[0])
        #显示加载数据
        self.ui.tableView1.clearContents()
        self.cur.execute("SELECT * FROM clutter_table ORDER BY data_id DESC")
        data = self.cur.fetchall()
        print(data)
        self.ui.tableView1.setRowCount(0)
        self.ui.tableView1.insertRow(0)
        for row,form in enumerate(data):
            for column, item in enumerate(form):
                self.ui.tableView1.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.ui.tableView1.rowCount()
            self.ui.tableView1.insertRow(row_position)
        #打印操作记录
        item_num = len(data)
        print(str(item_num))
        text_history = "------------------------------------\n"
        text_history += "杂波数据库共保存" + str(item_num) + "条数据..."
        self.ui.textHistory.append(text_history)
        self.db.close()
    #---查询函数-------------------------------------------------------------------
    def do_Query(self):
        #链接数据库
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='1234' , db='db_test',charset='utf8')
        self.cur = self.db.cursor()
        condition_id = self.ui.textDataId.text()
        condition_name = self.ui.textDataFileName.text()
        condition_date1 = self.ui.dateDataDate1.text()
        #condition_date1.toString(dtStr, "MM-dd-yyyy")
        condition_date2 = self.ui.dateDataDate2.text()
       # condition_date2.toString(dtStr, "MM-dd-yyyy")
        condition_location = self.ui.cmbDataLocation.currentText()
        condition_model = self.ui.cmbDataModel.currentText()
        condition_mode = self.ui.cmbDataMode.currentText()
        condition_env = self.ui.cmbDataEnv.currentText()
        condition_remarks = self.ui.textDataRemarks.toPlainText()
        #开始查询
        query_sql = "SELECT * FROM clutter_table WHERE 1=1 "
        if condition_id != '':
           # query_sql += "AND data_id like \%%d\% " %int(condition_id)
           query_sql += "AND data_id like '%" + condition_id + "%' "
        if condition_name != '':
            query_sql += " AND data_filename LIKE '%" + condition_name + "%' "
        if condition_location != '不限':
            query_sql += " AND data_location ='" + condition_location + "' "
        if condition_model != '不限':
            query_sql += " AND data_model ='" + condition_model + "' "
        if condition_mode != '不限':
            query_sql += " AND data_mode ='" + condition_mode + "' "
        if condition_env != '不限':
            query_sql += " AND data_env ='" + condition_env + "' "
        if condition_remarks != '':
            query_sql += " AND data_remarks like '%" + condition_remarks + "%' "
        query_sql += ";"
        self.cur.execute(query_sql)
        data = self.cur.fetchall()
        #在tableView1中显示
        self.ui.tableView1.clearContents()
        self.ui.tableView1.setRowCount(0)
        self.ui.tableView1.insertRow(0)
        for row,form in enumerate(data):
            for column, item in enumerate(form):
                self.ui.tableView1.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.ui.tableView1.rowCount()
            self.ui.tableView1.insertRow(row_position)
        #打印操作记录
        item_num = len(data)
        print(str(item_num))
        text_history = "------------------------------------\n"
        text_history += "共检索到" + str(item_num) + "条数据..."
        self.ui.textHistory.append(text_history)
        self.db.close()
    #---批量更改-------------------------------------------------------------------
    def do_QueryModify(self):
        reply = QMessageBox.question(self, 'Message', '确认修改数据？',
                           QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("Good!")
            #链接数据库
            self.db = MySQLdb.connect(host='localhost' , user='root' , password ='1234' , db='db_test',charset='utf8')
            self.cur = self.db.cursor()
            rowCount = self.ui.tableView1.rowCount()
            columnCount = self.ui.tableView1.columnCount()
            for i in range(rowCount - 1):
                value_lst = []
                for j in range(columnCount):
                    #item_data = QTableWidgetItem(None)
                    #self.ui.tableView1.setItem(i,j,item_data)
                    tmp_data = self.ui.tableView1.item(i,j).text()
                    value_lst.append(tmp_data)
                sql = "UPDATE clutter_table SET data_filename = '" + value_lst[1] + "',data_date = '" + value_lst[2] + "',"
                sql += "data_location = '" + value_lst[3] + "',data_model ='" + value_lst[4] + "',"
                sql += "data_mode = '" + value_lst[5] + "',data_env = '" + value_lst[6] + "',data_remarks = '" + value_lst[7] + "',"
                sql += "data_path = '" + value_lst[8] + "'"
                sql += " WHERE data_id = " + value_lst[0] + ";"
                #sql =
                #sql%(value_lst[1],value_lst[2],value_lst[3],value_lst[4],value_lst[5],value_lst[6],value_lst[7],value_lst[8],int(value_lst[0]))
                self.cur.execute(sql)
                self.db.commit() #必须显示提交才行
            text_history = "------------------------------------\n"
            text_history += "数据库更新完毕..."
            self.ui.textHistory.append(text_history)
            self.db.close()  # 这里必须关掉，否则数据实际无更改
            self.ui.tableView1.clearContents()
            
    #---单个删除-------------------------------------------------------------------
    def do_QueryDelete(self):
        reply = QMessageBox.question(self, 'Message', '确认删除该条数据？',
                           QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("Delete it !")
            #链接数据库
            self.db = MySQLdb.connect(host='localhost' , user='root' , password ='1234' , db='db_test',charset='utf8')
            self.cur = self.db.cursor()
            #提取当前行
            row_del = self.ui.tableView1.currentRow()
            id_del = self.ui.tableView1.item(row_del,0).text()
            #从数据中删除该行数据
            sql = "DELETE FROM clutter_table WHERE data_id =" + id_del
            self.cur.execute(sql)
            self.db.commit()
            #删除表格中该行数据
            self.ui.tableView1.removeRow(row_del)
            text_history = "------------------------------------\n"
            text_history += "该数据已删除..."
            self.ui.textHistory.append(text_history)
            self.db.close()  # 这里必须关掉，否则数据实际无更改
    #---添加多个文件-------------------------------------------------------------------
    def do_Select(self):
        files, filetype = QFileDialog.getOpenFileNames(self,"请选择：","E:/my_python/gui/test_data",
                                                       "All Files(*);;Text Files(*.txt)")
        files_name = []
        files_date = []
        files_location = []
        files_model = []
        files_mode = []
        files_env = []
        files_path = []
        #遍历files,获取信息 格式：7s2020062501_上海_1x_SAR_湿地.txt
        for file in files:
            files_path.append(file)
            file = QFileInfo(file)
            name = file.fileName()
            p1 = name.find('_',0)
            p2 = name.find('_',p1 + 1)
            p3 = name.find('_',p2 + 1)
            p4 = name.find('_',p3 + 1)
            p5 = name.find('.',p4 + 1)
            files_name.append(name)
            date = name[2:p1 - 2]
            date = date[:4] + '-' + date[4:6] + '-' + date[6:]
            files_date.append(date)
            files_location.append(name[p1 + 1:p2])
            files_model.append(name[p2 + 1:p3])
            files_mode.append(name[p3 + 1:p4])
            files_env.append(name[p4 + 1:p5])
        num_files = len(files_name)
        self.ui.tableView2.clearContents()
        self.ui.tableView2.setRowCount(0)
        self.ui.tableView2.insertRow(0)
        for i in range(num_files):
            self.ui.tableView2.setItem(i,1,QTableWidgetItem(str(files_name[i])))
            self.ui.tableView2.setItem(i,2,QTableWidgetItem(str(files_date[i])))
            self.ui.tableView2.setItem(i,3,QTableWidgetItem(str(files_location[i])))
            self.ui.tableView2.setItem(i,4,QTableWidgetItem(str(files_model[i])))
            self.ui.tableView2.setItem(i,5,QTableWidgetItem(str(files_mode[i])))
            self.ui.tableView2.setItem(i,6,QTableWidgetItem(str(files_env[i])))
            self.ui.tableView2.setItem(i,8,QTableWidgetItem(str(files_path[i])))
            row_position = self.ui.tableView2.rowCount()
            self.ui.tableView2.insertRow(row_position)
        text_history = "------------------------------------\n"
        text_history += "打开" + str(num_files) + "条数据, 点击 添加至数据库 完成导入..."
        self.ui.textHistory.append(text_history)
    #---从表格导入数据库----------------------------------------------------------------
    def Add(self):
        reply = QMessageBox.question(self, 'Message', '确认导入数据？',
                           QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            #链接数据库
            self.db = MySQLdb.connect(host='localhost' , user='root' , password ='1234' , db='db_test',charset='utf8')
            self.cur = self.db.cursor()
            rowCount = self.ui.tableView2.rowCount()
            colCount = self.ui.tableView2.columnCount()
            for i in range(rowCount - 1):
                value_lst = []
                for j in range(colCount):
                    #item_data = QTableWidgetItem(None)
                    #self.ui.tableView1.setItem(i,j,item_data)
                    tmp_data = self.ui.tableView2.item(i,j).text()
                    value_lst.append(tmp_data)
                sql = "INSERT INTO clutter_table (data_filename, data_date, data_location, data_model,"
                sql += " data_mode, data_env, data_remarks, data_path)"
                sql += " VALUES('") data_id = " + value_lst[0] + ";"
                #sql =
                #sql%(value_lst[1],value_lst[2],value_lst[3],value_lst[4],value_lst[5],value_lst[6],value_lst[7],value_lst[8],int(value_lst[0]))
                self.cur.execute(sql)



        
            



        




if __name__ == '__main__':
    app =QApplication(sys.argv)
    form = QmyMainWindow()

    form.show()
    sys.exit(app.exec_())

