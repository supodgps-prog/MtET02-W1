import customtkinter as ctk

# ตั้งค่าธีมหน้าตาและสีสัน
ctk.set_appearance_mode("System")  # เลือกปรับตามระบบคอมพิวเตอร์ (Light/Dark)
ctk.set_default_color_theme("blue") # โทนสีหลักของปุ่ม

class ModernCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ตั้งค่าหน้าต่างโปรแกรม
        self.title("Modern Calculator")
        self.geometry("360x520")
        self.resizable(False, False)
        self.configure(fg_color=("#F2F4F7", "#1A1C1E")) # สีพื้นหลัง Light/Dark

        # ตัวแปรเก็บสมการคำนวณ
        self.expression = ""

        # --- ส่วนแสดงผลหน้าจอ (Display) ---
        self.display = ctk.CTkEntry(
            self, 
            width=330, 
            height=80, 
            font=("Segoe UI", 36, "bold"), 
            justify="right",
            border_width=0,
            fg_color=("#FFFFFF", "#282A2D"),
            text_color=("#1A1C1E", "#FFFFFF"),
            corner_radius=15
        )
        self.display.pack(pady=(20, 15), padx=15)
        self.display.insert(0, "0")

        # --- เฟรมสำหรับจัดวางปุ่ม (Buttons Grid) ---
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # กำหนดแถวและคอลัมน์ของ Grid
        for i in range(5):
            self.buttons_frame.rowconfigure(i, weight=1, pad=10)
        for i in range(4):
            self.buttons_frame.columnconfigure(i, weight=1, pad=10)

        # รายชื่อปุ่มและพิกัดการจัดวาง
        button_config = {
            'C': (0, 0, '#E57373', '#EF5350'),    '⌫': (0, 1, '#CFD8DC', '#37474F'),
            '%': (0, 2, '#CFD8DC', '#37474F'),    '÷': (0, 3, '#FFB74D', '#F57C00'),
            '7': (1, 0, '#FFFFFF', '#2C2E31'),    '8': (1, 1, '#FFFFFF', '#2C2E31'),
            '9': (1, 2, '#FFFFFF', '#2C2E31'),    '×': (1, 3, '#FFB74D', '#F57C00'),
            '4': (2, 0, '#FFFFFF', '#2C2E31'),    '5': (2, 1, '#FFFFFF', '#2C2E31'),
            '6': (2, 2, '#FFFFFF', '#2C2E31'),    '-': (2, 3, '#FFB74D', '#F57C00'),
            '1': (3, 0, '#FFFFFF', '#2C2E31'),    '2': (3, 1, '#FFFFFF', '#2C2E31'),
            '3': (3, 2, '#FFFFFF', '#2C2E31'),    '+': (3, 3, '#FFB74D', '#F57C00'),
            '0': (4, 0, '#FFFFFF', '#2C2E31'),    '.': (4, 2, '#FFFFFF', '#2C2E31'),
            '=': (4, 3, '#81C784', '#4CAF50')
        }

        # วาดปุ่มลงบนหน้าจอ
        for text, config in button_config.items():
            row, col, light_color, dark_color = config
            
            # ปรับปุ่ม '0' ให้กว้างเป็นพิเศษ
            colspan = 2 if text == '0' else 1

            btn = ctk.CTkButton(
                self.buttons_frame,
                text=text,
                font=("Segoe UI", 20, "bold"),
                fg_color=(light_color, dark_color),
                text_color=("#1A1C1E" if text not in ['÷', '×', '-', '+', '=', 'C'] else "#FFFFFF", "#FFFFFF"),
                hover_color=("#E0E0E0", "#424242"),
                corner_radius=15,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=4, pady=4)

    # ฟังก์ชันจัดการแรงกดปุ่มต่างๆ
    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.update_display("0")
        elif char == '⌫':
            self.expression = self.expression[:-1]
            self.update_display(self.expression if self.expression else "0")
        elif char == '=':
            try:
                # แปลงสัญลักษณ์ก่อนการคำนวณจริงใน Python
                formatted_expr = self.expression.replace('×', '*').replace('÷', '/')
                result = str(eval(formatted_expr))
                
                # หากเป็นเลขทศนิยม ให้ตัดตัวท้ายหากไม่มีค่า
                if '.' in result and result.split('.')[1] == '0':
                    result = result.split('.')[0]
                
                self.update_display(result)
                self.expression = result
            except:
                self.update_display("Error")
                self.expression = ""
        else:
            # ป้องกันไม่ให้กดเครื่องหมายซ้ำซ้อนกันหน้าสุด
            if self.expression == "" and char in ['+', '×', '÷', '%']:
                return
            
            self.expression += char
            self.update_display(self.expression)

    def update_display(self, text):
        self.display.configure(state="normal")
        self.display.delete(0, "end")
        self.display.insert(0, text)

# รันแอปพลิเคชัน
if __name__ == "__main__":
    app = ModernCalculator()
    app.mainloop()
