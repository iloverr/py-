import time
def logger(msg):
    def time_master(func):
        def call_func():
            start=time.time()
            func()
            stop=time.time()
            print(f"[{msg}]一共用了{(stop-start):.2f}")
        return call_func
    return time_master

@logger(msg='A')
def funA():
    import tkinter as tk
    import random
    import threading
    import time

    class WindowManager:
        def __init__(self, total_windows=300):
            self.total_windows = total_windows
            self.created_count = 0
            self.windows = []
            self.creation_complete = False
            self.lock = threading.Lock()
            self.root = None
            
        def create_window(self):
            """创建一个弹窗"""
            # 必须在主线程中创建Tkinter组件
            def _create():
                window = tk.Toplevel()
                
                # 设置窗口位置和大小
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                
                width = 250
                height = 60
                x = random.randint(0, max(1, screen_width - width))
                y = random.randint(0, max(1, screen_height - height))
                
                window.geometry(f"{width}x{height}+{x}+{y}")
                window.attributes('-topmost', True)
                
                # 内容
                tips = ['要多喝水', '今天开心嘛', '好好爱自己', '平平安安']
                colors = ['lightpink', 'skyblue', 'lightgreen', 'lightyellow']
                
                tk.Label(
                    window,
                    text=random.choice(tips),
                    bg=random.choice(colors),
                    font=('微软雅黑', 14)
                ).pack(expand=True, fill='both')
                
                self.windows.append(window)
                
                with self.lock:
                    self.created_count += 1
                    if self.created_count == self.total_windows:
                        self.creation_complete = True
                        print(f"✓ 所有 {self.total_windows} 个窗口创建完成")
                        # 2秒后关闭所有窗口
                        self.root.after(2000, self.close_all)
            
            self.root.after(0, _create)
        
        def close_all(self):
            """关闭所有窗口"""
            print("开始关闭所有窗口...")
            for window in self.windows:
                try:
                    window.destroy()
                except:
                    pass
            self.windows.clear()
            print("所有窗口已关闭")
            self.root.quit()
        
        def start_creation(self):
            """开始创建窗口"""
            print(f"开始创建 {self.total_windows} 个弹窗...")
            
            # 批量创建窗口
            for i in range(self.total_windows):
                self.root.after(i * 10, self.create_window)  # 间隔10ms创建一个
            
            # 监控进度
            self.monitor_progress()
        
        def monitor_progress(self):
            """监控创建进度"""
            if not self.creation_complete:
                with self.lock:
                    print(f"进度: {self.created_count}/{self.total_windows}")
                self.root.after(500, self.monitor_progress)
        
        def run(self):
            """运行主程序"""
            self.root = tk.Tk()
            self.root.withdraw()
            
            # 开始创建窗口
            self.root.after(100, self.start_creation)
            
            self.root.mainloop()

    def main():
        manager = WindowManager(total_windows=300)
        manager.run()

    if __name__ == "__main__":
        main()


@logger(msg="b")
def funB():
    aa=1
    for aa in range(10):
        print('李欣睿是猪')


funA()
funB()
