import sys
import os
import re
import random  # 添加random模块用于随机初始化数组
import datetime  # 添加datetime模块用于记录时间
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QFileDialog, QMessageBox, QGridLayout, QCheckBox,
                           QTextEdit, QSplitter)  # 添加QSplitter用于分割窗口
from PyQt5.QtCore import Qt
import sys  # 添加sys模块，用于程序退出

class KukaProgramEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口标题和大小
        self.setWindowTitle("库卡程序参数编辑器")
        self.resize(1200, 800)  # 增大窗口尺寸以容纳代码显示区域
        
        # 原始文件路径
        self.src_file_path = r"your_file_path\PB3.src"
        self.dat_file_path = r"your_file_path\PB3.dat"
        self.output_dir = r"your_file_path\generated_code"
        self.parameter_log_file = os.path.join(self.output_dir, "parameter.txt")  # 参数记录文件路径
        
        # 创建UI
        self.init_ui()
        
        # 加载默认值
        self.load_default_values()
        
    def init_ui(self):
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建顶部的参数输入区域
        params_widget = QWidget()
        params_layout = QVBoxLayout(params_widget)
        
        # 创建参数输入网格布局
        grid_layout = QGridLayout()
        
        # 参数标签和输入框
        self.normala_edit = QLineEdit()
        self.gapa_edit = QLineEdit()
        self.overlapa_edit = QLineEdit()
        self.cnt_edit = QLineEdit()
        self.cnt1a_edit = QLineEdit()
        self.cnt2a_edit = QLineEdit()
        self.layer_edit = QLineEdit()
        self.vel_edit = QLineEdit()
        self.acc_edit = QLineEdit()
        
        # 添加原点定位输入框
        self.position_x_edit = QLineEdit()
        self.position_y_edit = QLineEdit()
        
        # 添加到网格布局
        grid_layout.addWidget(QLabel("正常偏移 (NORMALA):"), 0, 0)
        grid_layout.addWidget(self.normala_edit, 0, 1)
        
        grid_layout.addWidget(QLabel("间隙偏移 (GAPA):"), 1, 0)
        grid_layout.addWidget(self.gapa_edit, 1, 1)
        
        grid_layout.addWidget(QLabel("重叠偏移 (OVERLAPA):"), 2, 0)
        grid_layout.addWidget(self.overlapa_edit, 2, 1)
        
        grid_layout.addWidget(QLabel("丝束数量 (CNT):"), 3, 0)
        grid_layout.addWidget(self.cnt_edit, 3, 1)
        
        grid_layout.addWidget(QLabel("间隙数量 (CNT1A):"), 4, 0)
        grid_layout.addWidget(self.cnt1a_edit, 4, 1)
        
        grid_layout.addWidget(QLabel("重叠数量 (CNT2A):"), 5, 0)
        grid_layout.addWidget(self.cnt2a_edit, 5, 1)
        
        grid_layout.addWidget(QLabel("铺放层数 (Layer):"), 6, 0)
        grid_layout.addWidget(self.layer_edit, 6, 1)
        
        grid_layout.addWidget(QLabel("铺放速度 (VEL):"), 7, 0)
        grid_layout.addWidget(self.vel_edit, 7, 1)
        
        grid_layout.addWidget(QLabel("铺放加速度 (ACC):"), 8, 0)
        grid_layout.addWidget(self.acc_edit, 8, 1)
        
        # 添加原点定位输入框到布局
        grid_layout.addWidget(QLabel("原点定位X (position_x):"), 9, 0)
        grid_layout.addWidget(self.position_x_edit, 9, 1)
        
        grid_layout.addWidget(QLabel("原点定位Y (position_y):"), 10, 0)
        grid_layout.addWidget(self.position_y_edit, 10, 1)
        
        # 添加"是否取消扫描"复选框
        self.disable_scan_checkbox = QCheckBox("取消扫描功能")
        grid_layout.addWidget(self.disable_scan_checkbox, 11, 0, 1, 2)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 创建生成按钮
        self.generate_button = QPushButton("生成新代码")
        self.generate_button.clicked.connect(self.generate_new_code)
        
        # 添加按钮到布局
        button_layout.addWidget(self.generate_button)
        
        # 添加到参数布局
        params_layout.addLayout(grid_layout)
        params_layout.addLayout(button_layout)
        
        # 创建底部的代码显示区域，使用分割器
        splitter = QSplitter(Qt.Vertical)
        
        # 创建代码显示窗口容器
        src_code_container = QWidget()
        src_code_layout = QVBoxLayout(src_code_container)
        src_code_layout.addWidget(QLabel("生成的SRC代码"))
        
        # 创建src文件文本编辑器
        self.src_text_edit = QTextEdit()
        self.src_text_edit.setReadOnly(True)  # 设置为只读
        self.src_text_edit.setLineWrapMode(QTextEdit.NoWrap)  # 不自动换行
        src_code_layout.addWidget(self.src_text_edit)
        
        # 添加到分割器
        splitter.addWidget(src_code_container)
        
        # 创建dat代码显示窗口容器
        dat_code_container = QWidget()
        dat_code_layout = QVBoxLayout(dat_code_container)
        dat_code_layout.addWidget(QLabel("生成的DAT代码"))
        
        # 创建dat文件文本编辑器
        self.dat_text_edit = QTextEdit()
        self.dat_text_edit.setReadOnly(True)  # 设置为只读
        self.dat_text_edit.setLineWrapMode(QTextEdit.NoWrap)  # 不自动换行
        dat_code_layout.addWidget(self.dat_text_edit)
        
        # 添加到分割器
        splitter.addWidget(dat_code_container)
        
        # 设置分割器初始比例
        splitter.setSizes([400, 400])
        
        # 创建顶部参数区和底部代码区的水平分割器
        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.addWidget(params_widget)
        main_splitter.addWidget(splitter)
        
        # 设置主分割器初始比例
        main_splitter.setSizes([400, 600])
        
        # 添加到主布局
        main_layout.addWidget(main_splitter)
        
    def load_default_values(self):
        """从原始文件加载默认参数值"""
        try:
            # 读取src文件
            with open(self.src_file_path, 'r', encoding='utf-8') as f:
                src_content = f.read()
                
                # 提取参数值
                normala_match = re.search(r'NORMALA\s*=\s*([\d.]+)', src_content)
                if normala_match:
                    self.normala_edit.setText(normala_match.group(1))
                    
                gapa_match = re.search(r'GAPA\s*=\s*([\d.]+)', src_content)
                if gapa_match:
                    self.gapa_edit.setText(gapa_match.group(1))
                    
                overlapa_match = re.search(r'OVERLAPA\s*=\s*([\d.]+)', src_content)
                if overlapa_match:
                    self.overlapa_edit.setText(overlapa_match.group(1))
                    
                cnt_match = re.search(r'CNT\s*=\s*(\d+)', src_content)
                if cnt_match:
                    self.cnt_edit.setText(cnt_match.group(1))
                    
                cnt1a_match = re.search(r'CNT1A\s*=\s*(\d+)', src_content)
                if cnt1a_match:
                    self.cnt1a_edit.setText(cnt1a_match.group(1))
                    
                cnt2a_match = re.search(r'CNT2A\s*=\s*(\d+)', src_content)
                if cnt2a_match:
                    self.cnt2a_edit.setText(cnt2a_match.group(1))
                    
                layer_match = re.search(r'Layer\s*=\s*(\d+)', src_content)
                if layer_match:
                    self.layer_edit.setText(layer_match.group(1))
                    
                # 提取速度值
                vel_match = re.search(r'SVEL_CP\(([\d.]+),', src_content)
                if vel_match:
                    self.vel_edit.setText(vel_match.group(1))
                    
            # 读取dat文件获取加速度默认值
            with open(self.dat_file_path, 'r', encoding='utf-8') as f:
                dat_content = f.read()
                
                # 提取加速度值，如果没有找到则使用默认值100
                acc_match = re.search(r'ACC\s*=\s*([\d.]+)', dat_content)
                if acc_match:
                    self.acc_edit.setText(acc_match.group(1))
                else:
                    self.acc_edit.setText("100")  # 默认设置为100
                    
            # 设置原点定位默认值
            self.position_x_edit.setText("100")  # 原点定位X默认设置为100
            self.position_y_edit.setText("20")   # 原点定位Y默认设置为20
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载默认值失败: {str(e)}")
            
    def show_generated_code(self, src_path, dat_path):
        """显示生成的代码"""
        try:
            # 读取并显示src文件内容
            with open(src_path, 'r', encoding='utf-8') as f:
                self.src_text_edit.setPlainText(f.read())
                
            # 读取并显示dat文件内容
            with open(dat_path, 'r', encoding='utf-8') as f:
                self.dat_text_edit.setPlainText(f.read())
                
        except Exception as e:
            QMessageBox.warning(self, "警告", f"无法显示生成的代码: {str(e)}")
            
    def generate_new_code(self):
        """生成新的代码文件"""
        try:
            # 验证输入
            if not self.validate_input():
                return
                
            # 读取原始文件
            with open(self.src_file_path, 'r', encoding='utf-8') as f:
                src_content = f.read()
                
            with open(self.dat_file_path, 'r', encoding='utf-8') as f:
                dat_content = f.read()
                
            # 获取用户输入的参数
            normala = self.normala_edit.text()
            gapa = self.gapa_edit.text()
            overlapa = self.overlapa_edit.text()
            cnt = int(self.cnt_edit.text())  # 转换为整数
            cnt1a = int(self.cnt1a_edit.text())  # 转换为整数
            cnt2a = int(self.cnt2a_edit.text())  # 转换为整数
            layer = self.layer_edit.text()
            vel = self.vel_edit.text()
            acc = self.acc_edit.text()
            
            # 获取原点定位参数
            position_x = self.position_x_edit.text()
            position_y = self.position_y_edit.text()
            
            # 计算normala的数量 (cnt3a = cnt - cnt1a - cnt2a)
            cnt3a = cnt - cnt1a - cnt2a
            
            # 确保数量合理
            if cnt3a < 0:
                QMessageBox.warning(self, "输入错误", "丝束数量必须大于等于间隙数量与重叠数量之和")
                return
                
            # 创建num数组的初始化字符串
            # 先创建包含指定数量的gapa、overlapa和normala的列表
            num_values = []
            num_values.extend([gapa] * cnt1a)  # 添加cnt1a个gapa值
            num_values.extend([overlapa] * cnt2a)  # 添加cnt2a个overlapa值
            num_values.extend([normala] * cnt3a)  # 添加cnt3a个normala值
            
            # 打乱列表顺序
            random.shuffle(num_values)
            
            # 修改src文件内容
            # 1. 修改DECL REAL NUM[CNT]中的CNT值
            src_content = re.sub(r'DECL REAL NUM\[\w+\]', f'DECL REAL NUM[{cnt}]', src_content)
            
            # 2. 修改CNT值
            src_content = re.sub(r'NORMALA\s*=\s*[\d.]+', f'NORMALA={normala}', src_content)
            src_content = re.sub(r'GAPA\s*=\s*[\d.]+', f'GAPA={gapa}', src_content)
            src_content = re.sub(r'OVERLAPA\s*=\s*[\d.]+', f'OVERLAPA={overlapa}', src_content)
            src_content = re.sub(r'CNT\s*=\s*\d+', f'CNT={cnt}', src_content)
            src_content = re.sub(r'CNT1A\s*=\s*\d+', f'CNT1A={cnt1a}', src_content)
            src_content = re.sub(r'CNT2A\s*=\s*\d+', f'CNT2A={cnt2a}', src_content)
            src_content = re.sub(r'Layer\s*=\s*\d+', f'Layer={layer}', src_content)
            src_content = re.sub(r'SVEL_CP\(([\d.]+),', f'SVEL_CP({vel},', src_content)
            src_content = re.sub(r'Vel=([\d.]+)\s*m/s', f'Vel={vel} m/s', src_content)
            
            # 3. 将NUM[cnt]={0,0,0}改为单独为每个元素赋值的形式
            # 查找NUM[cnt]={...}行并删除
            src_content = re.sub(r'NUM\s*\[\s*cnt\s*\]\s*=\s*\{[^}]*\}\s*', '', src_content)
            
            # 找到INI语句的位置
            ini_pattern = re.compile(r';FOLD INI;%\{PE\}')
            ini_match = ini_pattern.search(src_content)
            
            if ini_match:
                # 生成每个元素的赋值语句
                num_assignments = []
                for i in range(cnt):
                    num_assignments.append(f'NUM[{i+1}]={num_values[i]}')
                
                # 合并为字符串
                num_assignments_str = '\n'.join(num_assignments)
                
                # 在INI语句前插入NUM数组初始化语句
                src_content = src_content[:ini_match.start()] + num_assignments_str + '\n' + src_content[ini_match.start():]
            
            # 检查是否需要删除扫描相关代码
            if self.disable_scan_checkbox.isChecked():
                # 删除与EKI和DTM相关的所有代码段
                # 1. 删除EKI初始化和配置代码
                src_content = re.sub(r';FOLD INI EKI-RELATED PARAMS[\s\S]*?;ENDFOLD\s*', '', src_content)
                src_content = re.sub(r';FOLD Close EKI[\s\S]*?;ENDFOLD\s*', '', src_content)
                src_content = re.sub(r'RET = EKI_Init\("ClientXML"\)\s+RET = EKI_Open\("ClientXML"\)\s+ISOPEN = TRUE\s*', '', src_content)
                
                # 2. 删除所有测量相关的代码块，不管DTM值是什么
                src_content = re.sub(r';FOLD Start Measurement Before Reach Touch Point[\s\S]*?;ENDFOLD\s*', '', src_content)
                src_content = re.sub(r';FOLD End Measurement Before Lifting Robot Head[\s\S]*?;ENDFOLD\s*', '', src_content)
                src_content = re.sub(r';FOLD Start Acquisition After Roll Lift[\s\S]*?;ENDFOLD\s*', '', src_content)
                src_content = re.sub(r';FOLD End Acquisition Before Lifting Robot Head[\s\S]*?;ENDFOLD\s*', '', src_content)
                
                # 3. 删除没有正确ENDFOLD的代码段（针对当前发现的问题）
                # 匹配Start Acquisition After Roll Lift后直到下一个;FOLD或文件结束的内容
                src_content = re.sub(r';FOLD Start Acquisition After Roll Lift\s+WAIT SEC 0\.5\s+DTM = \d+\s+RET = EKI_SetInt\("ClientXML", "Sensor/DTMODE", DTM\)\s+RET = EKI_Send\("ClientXML", "Sensor"\)\s*', '', src_content)
                
                # 4. 删除任何残留的EKI和DTM相关单行代码
                src_content = re.sub(r'\s*RET = EKI_SetInt\("ClientXML", "Sensor/DTMODE", \d+\)\s*', '', src_content)
                src_content = re.sub(r'\s*RET = EKI_Send\("ClientXML", "Sensor"\)\s*', '', src_content)
                src_content = re.sub(r'\s*DTM = \d+\s*', '', src_content)
                src_content = re.sub(r'\s*WAIT SEC 0\.5\s*', '', src_content)
                
                # 5. 删除单独的 ;ENDFOLD 行（可能存在）
                # 修改正则表达式，只删除单独的;ENDFOLD行，不删除带注释的;ENDFOLD (XXX)
                src_content = re.sub(r';ENDFOLD\s*$', '', src_content)
            
            # 修改dat文件内容
            dat_content = re.sub(r'VEL\s*=\s*[\d.]+', f'VEL={vel}', dat_content)
            dat_content = re.sub(r'ACC\s*=\s*[\d.]+', f'ACC={acc}', dat_content)
            
            # 获取下一个可用的序号
            next_index = self.get_next_index()
            
            # 保存新文件到生成代码文件夹（使用序号作为后缀）
            new_src_path = os.path.join(self.output_dir, f"PB3_{next_index}.src")
            new_dat_path = os.path.join(self.output_dir, f"PB3_{next_index}.dat")
            
            with open(new_src_path, 'w', encoding='utf-8') as f:
                f.write(src_content)
                
            with open(new_dat_path, 'w', encoding='utf-8') as f:
                f.write(dat_content)
                
            # 生成参数记录并写入parameter.txt文件
            self.log_parameters(normala, gapa, overlapa, cnt, cnt1a, cnt2a, layer, vel, acc, next_index, new_src_path, position_x, position_y)
                
            # 显示生成的代码
            self.show_generated_code(new_src_path, new_dat_path)
            
            QMessageBox.information(self, "成功", f"新代码已生成并保存到:\n{new_src_path}\n{new_dat_path}\n\n参数记录已保存到parameter.txt")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成新代码失败: {str(e)}")
            
    def get_next_index(self):
        """获取下一个可用的序号"""
        try:
            # 检查输出目录是否存在
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
                return 1
            
            # 获取目录中的所有文件
            files = os.listdir(self.output_dir)
            
            # 查找所有PB3_数字.src或PB3_数字.dat的文件
            pattern = re.compile(r'PB3_([0-9]+)\.(src|dat)')
            indexes = []
            
            for file in files:
                match = pattern.match(file)
                if match:
                    index = int(match.group(1))
                    indexes.append(index)
            
            # 如果没有找到匹配的文件，返回1
            if not indexes:
                return 1
            
            # 返回最大序号加1
            return max(indexes) + 1
            
        except Exception as e:
            # 发生错误时默认返回1
            print(f"获取序号时出错: {str(e)}")
            return 1
            
    def log_parameters(self, normala, gapa, overlapa, cnt, cnt1a, cnt2a, layer, vel, acc, index, file_path, position_x="0", position_y="0"):
        """记录修改的参数到parameter.txt文件"""
        try:
            # 获取当前时间
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 准备参数记录内容
            log_content = """===========================================
生成时间: {}
生成文件: {}
序号: {}
参数修改记录:
- 正常偏移 (NORMALA): {}
- 间隙偏移 (GAPA): {}
- 重叠偏移 (OVERLAPA): {}
- 丝束数量 (CNT): {}
- 间隙数量 (CNT1A): {}
- 重叠数量 (CNT2A): {}
- 铺放层数 (Layer): {}
- 铺放速度 (VEL): {}
- 铺放加速度 (ACC): {}
- 原点定位X (position_x): {}
- 原点定位Y (position_y): {}
- 是否取消扫描: {}
===========================================
"""
            
            # 格式化参数记录
            formatted_log = log_content.format(
                current_time,
                os.path.basename(file_path),
                index,
                normala,
                gapa,
                overlapa,
                cnt,
                cnt1a,
                cnt2a,
                layer,
                vel,
                acc,
                position_x,
                position_y,
                "是" if self.disable_scan_checkbox.isChecked() else "否"
            )
            
            # 写入文件（追加模式）
            with open(self.parameter_log_file, 'a', encoding='utf-8') as f:
                f.write(formatted_log)
                
        except Exception as e:
            # 如果记录失败，显示警告但不中断主流程
            QMessageBox.warning(self, "警告", f"参数记录保存失败: {str(e)}")
            
    def validate_input(self):
        """验证用户输入"""
        # 验证数字输入
        try:
            float(self.normala_edit.text())
            float(self.gapa_edit.text())
            float(self.overlapa_edit.text())
            int(self.cnt_edit.text())
            int(self.cnt1a_edit.text())
            int(self.cnt2a_edit.text())
            int(self.layer_edit.text())
            float(self.vel_edit.text())
            float(self.acc_edit.text())
            
            # 验证原点定位值
            float(self.position_x_edit.text())
            float(self.position_y_edit.text())
            
            # 额外验证：丝束数量必须大于等于间隙数量与重叠数量之和
            cnt = int(self.cnt_edit.text())
            cnt1a = int(self.cnt1a_edit.text())
            cnt2a = int(self.cnt2a_edit.text())
            
            if cnt < cnt1a + cnt2a:
                QMessageBox.warning(self, "输入错误", "丝束数量必须大于等于间隙数量与重叠数量之和")
                return False
                
            return True
        except ValueError:
            QMessageBox.warning(self, "输入错误", "请确保所有参数都输入了有效的数字值")
            return False

if __name__ == "__main__":
    # 确保中文显示正常
    import matplotlib
    matplotlib.use('Agg')
    
    app = QApplication(sys.argv)
    window = KukaProgramEditor()
    window.show()
    sys.exit(app.exec_())