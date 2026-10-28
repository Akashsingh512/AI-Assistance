from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QProgressBar, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, QTimer
from app.system.system_monitor import SystemMonitor

class SystemPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(2000) # Update every 2 seconds

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("System Monitor")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Overview Metrics (CPU, RAM, Disk)
        metrics_layout = QHBoxLayout()
        
        # CPU
        cpu_group = QGroupBox("CPU Usage")
        cpu_group.setStyleSheet("color: white;")
        cpu_layout = QVBoxLayout(cpu_group)
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setStyleSheet("QProgressBar { border: 1px solid #3A3B3C; border-radius: 5px; text-align: center; } QProgressBar::chunk { background-color: #2D88FF; }")
        cpu_layout.addWidget(self.cpu_bar)
        self.cpu_label = QLabel("0%")
        cpu_layout.addWidget(self.cpu_label, alignment=Qt.AlignCenter)
        metrics_layout.addWidget(cpu_group)
        
        # RAM
        ram_group = QGroupBox("RAM Usage")
        ram_group.setStyleSheet("color: white;")
        ram_layout = QVBoxLayout(ram_group)
        self.ram_bar = QProgressBar()
        self.ram_bar.setStyleSheet("QProgressBar { border: 1px solid #3A3B3C; border-radius: 5px; text-align: center; } QProgressBar::chunk { background-color: #00A400; }")
        ram_layout.addWidget(self.ram_bar)
        self.ram_label = QLabel("0 GB / 0 GB")
        ram_layout.addWidget(self.ram_label, alignment=Qt.AlignCenter)
        metrics_layout.addWidget(ram_group)
        
        # Disk
        disk_group = QGroupBox("Disk Usage")
        disk_group.setStyleSheet("color: white;")
        disk_layout = QVBoxLayout(disk_group)
        self.disk_bar = QProgressBar()
        self.disk_bar.setStyleSheet("QProgressBar { border: 1px solid #3A3B3C; border-radius: 5px; text-align: center; } QProgressBar::chunk { background-color: #FFB900; }")
        disk_layout.addWidget(self.disk_bar)
        self.disk_label = QLabel("0 GB / 0 GB")
        disk_layout.addWidget(self.disk_label, alignment=Qt.AlignCenter)
        metrics_layout.addWidget(disk_group)
        
        layout.addLayout(metrics_layout)
        
        # Battery Status
        self.battery_label = QLabel("Battery: Checking...")
        self.battery_label.setStyleSheet("color: #B0B3B8; font-size: 14px;")
        layout.addWidget(self.battery_label)

        # Processes Table
        proc_group = QGroupBox("Top Processes (CPU)")
        proc_group.setStyleSheet("color: white;")
        proc_layout = QVBoxLayout(proc_group)
        
        self.proc_table = QTableWidget(0, 4)
        self.proc_table.setHorizontalHeaderLabels(["PID", "Name", "CPU %", "Mem %"])
        self.proc_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.proc_table.setStyleSheet("""
            QTableWidget { background-color: #242526; color: white; gridline-color: #3A3B3C; border: none; }
            QHeaderView::section { background-color: #3A3B3C; color: white; padding: 4px; border: 1px solid #18191A; }
        """)
        self.proc_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.proc_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        proc_layout.addWidget(self.proc_table)
        layout.addWidget(proc_group)

    def update_metrics(self):
        try:
            # CPU
            cpu_val = SystemMonitor.get_cpu_usage()
            self.cpu_bar.setValue(int(cpu_val))
            self.cpu_label.setText(f"{cpu_val:.1f}%")
            
            # RAM
            ram = SystemMonitor.get_ram_usage()
            self.ram_bar.setValue(int(ram['percent']))
            used_gb = ram['used'] / (1024**3)
            total_gb = ram['total'] / (1024**3)
            self.ram_label.setText(f"{used_gb:.1f} GB / {total_gb:.1f} GB")
            
            # Disk
            disk = SystemMonitor.get_disk_usage()
            self.disk_bar.setValue(int(disk['percent']))
            used_dgb = disk['used'] / (1024**3)
            total_dgb = disk['total'] / (1024**3)
            self.disk_label.setText(f"{used_dgb:.1f} GB / {total_dgb:.1f} GB")
            
            # Battery
            bat = SystemMonitor.get_battery_status()
            if bat["percent"] != "N/A":
                plugged = "Plugged In" if bat["power_plugged"] else "On Battery"
                self.battery_label.setText(f"Battery: {bat['percent']}% ({plugged})")
            else:
                self.battery_label.setText("Battery: N/A (Desktop or not supported)")
                
            # Processes
            procs = SystemMonitor.get_running_processes(10)
            self.proc_table.setRowCount(len(procs))
            for row, p in enumerate(procs):
                self.proc_table.setItem(row, 0, QTableWidgetItem(str(p.get('pid', ''))))
                self.proc_table.setItem(row, 1, QTableWidgetItem(str(p.get('name', ''))))
                
                cpu_p = p.get('cpu_percent', 0.0)
                cpu_str = f"{cpu_p:.1f}" if cpu_p is not None else "0.0"
                self.proc_table.setItem(row, 2, QTableWidgetItem(cpu_str))
                
                mem_p = p.get('memory_percent', 0.0)
                mem_str = f"{mem_p:.1f}" if mem_p is not None else "0.0"
                self.proc_table.setItem(row, 3, QTableWidgetItem(mem_str))
                
        except Exception as e:
            print(f"Error updating metrics: {e}")

    def hideEvent(self, event):
        self.timer.stop()
        super().hideEvent(event)
        
    def showEvent(self, event):
        self.timer.start(2000)
        super().showEvent(event)
