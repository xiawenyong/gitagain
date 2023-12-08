class Window(QMainWindow, Ui_MainWindow):
    # ... (其他函数和初始化代码)

    def startThread_cmd(self):
        tabname = self.tabwidget.tabText(self.tabwidget.currentIndex())
        cmd_combobox = self.combox[tabname + '_aau']
        docker_names = self.docker_dict[tabname]

        threads = []
        for docker_name in docker_names:
            cmd = cmd_combobox.currentText()
            timeout = float(self.timeout_line.text())

            try:
                self.validateInput(timeout)
                paradict = {
                    'cmd': cmd,
                    'expected': f'end to excel fun: {cmd}',
                    'timeout': timeout
                }

                edit_name = self.textEdit[docker_name]
                edit_label_name = self.editlabel[docker_name]
                thread = self.createThread(paradict, docker_name, [edit_name, edit_label_name])
                thread.start()
                threads.append(thread)
            except ValueError:
                self.showErrorMessageBox('错误', '请确认超时时间输入无误')

        for thread in threads:
            thread.exec()

    def createThread(self, paradict, docker_name, edit_names):
        thread = exec_MGR(paradict, docker_name, edit_names, self.exec_time_line.text(),
                          self.intercal_time_line.text(), self.sshParaDict, self.vbpParaDict, self.aauParaDict)
        thread.docker_result_mgr.connect(self.dockerresult)
        thread.editlabel_mgr.connect(self.edit_processing)
        thread.docker_result_mgr_text.connect(self.write_text)
        return thread

    def validateInput(self, timeout):
        if not timeout > 0:
            raise ValueError('Invalid timeout value')

    def showErrorMessageBox(self, title, message):
        msg_box = QMessageBox(QMessageBox.Critical, title, message)
        msg_box.exec_()
