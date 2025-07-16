import customtkinter as ctk
import datetime

ctk.set_appearance_mode("light")

class TrackmanStyleUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pitching Machine Control")
        self.geometry("1100x750")
        self.configure(bg="#F7F7F7")

        # Top bar (위치 조정: 타이틀과 Start 버튼이 겹치지 않게)
        self.topbar = ctk.CTkFrame(self, fg_color="#222222", height=60)
        self.topbar.pack(fill="x", side="top")
        ctk.CTkLabel(self.topbar, text="Pitching Machine", font=("Arial", 22, "bold"), text_color="#FF6600", bg_color="#222222").place(x=40, y=14)
        ctk.CTkButton(self.topbar, text="Start", fg_color="#FF6600", text_color="#FFFFFF", width=140, height=36, corner_radius=18).place(x=250, y=12)
        ctk.CTkButton(self.topbar, text="Settings", fg_color="#222222", text_color="#FF6600", border_width=2, border_color="#FF6600", width=80, height=36, corner_radius=18).place(relx=1.0, x=-120, y=12, anchor="ne")

        # Main area
        self.main = ctk.CTkFrame(self, fg_color="#F7F7F7")
        self.main.pack(fill="both", expand=True)

        # Left panel (Pitch history with details, 스크롤+디자인 개선)
        self.left_panel = ctk.CTkFrame(self.main, width=240, fg_color="#FFFFFF", border_width=1, border_color="#DDDDDD")
        self.left_panel.pack(side="left", fill="y", padx=(20,10), pady=20)
        ctk.CTkLabel(self.left_panel, text="History", font=("Arial", 17, "bold"), text_color="#222222").pack(pady=(18,8))
        # 스크롤 가능한 history 영역 (디자인 개선)
        self.history_canvas = ctk.CTkCanvas(self.left_panel, width=210, height=300, bg="#F7F7F7", highlightthickness=0, bd=0)
        self.history_scroll = ctk.CTkScrollbar(self.left_panel, orientation="vertical", command=self.history_canvas.yview, width=12, fg_color="#F7F7F7", button_color="#FF6600")
        self.history_frame = ctk.CTkFrame(self.history_canvas, fg_color="#F7F7F7")
        self.history_frame_id = self.history_canvas.create_window((0,0), window=self.history_frame, anchor="nw")
        self.history_canvas.configure(yscrollcommand=self.history_scroll.set)
        self.history_canvas.pack(padx=(12,0), pady=5, fill="x", expand=False, side="left")
        self.history_scroll.pack(padx=(0,8), pady=5, fill="y", side="left")
        self.history_frame.bind("<Configure>", lambda e: self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all")))
        self.history_rows = []
        self.history_data = []
        # 구종별 카운트/최고/최저 속도 (디자인 개선)
        self.summary_box = ctk.CTkFrame(self.left_panel, fg_color="#F7F7F7", border_width=0)
        self.summary_box.pack(padx=10, pady=(18,5), fill="x")
        self.count_label = ctk.CTkLabel(self.summary_box, text="Fastball: 0   Curve: 0   Slider: 0", font=("Arial", 12, "bold"), text_color="#222222")
        self.count_label.pack(anchor="w", pady=(0,2))
        self.maxmin_label = ctk.CTkLabel(self.summary_box, text="Max: -   Min: -", font=("Arial", 12), text_color="#222222")
        self.maxmin_label.pack(anchor="w")

        # Center panel (크기 및 배치 개선, 텍스트 겹침/삐져나옴 방지)
        self.center_panel = ctk.CTkFrame(self.main, fg_color="#FFFFFF", border_width=1, border_color="#DDDDDD")
        self.center_panel.pack(side="left", fill="both", expand=True, padx=10, pady=20)
        # 카메라 미리보기(더 크게)
        cam_frame = ctk.CTkFrame(self.center_panel, width=400, height=260, fg_color="#222222", border_width=2, border_color="#FF6600")
        cam_frame.place(x=40, y=40)
        ctk.CTkLabel(cam_frame, text="Camera", font=("Arial", 20, "bold"), text_color="#FFFFFF", bg_color="#222222").place(relx=0.5, rely=0.5, anchor="center")
        # Speed control (더 크게, 내부 요소 정렬 개선)
        speed_card = ctk.CTkFrame(self.center_panel, width=180, height=120, fg_color="#FFFFFF", border_width=2, border_color="#FF6600")
        speed_card.place(x=480, y=60)
        ctk.CTkLabel(speed_card, text="Speed", font=("Arial", 16, "bold"), text_color="#222222").place(x=20, y=15)
        self.speed_var = ctk.IntVar(value=80)
        self.speed_label = ctk.CTkLabel(speed_card, textvariable=self.speed_var, font=("Arial", 32, "bold"), text_color="#FF6600")
        self.speed_label.place(x=70, y=45)
        ctk.CTkButton(speed_card, text="-", width=40, height=40, fg_color="#222222", text_color="#FFFFFF", command=self.decrease_speed).place(x=20, y=70)
        ctk.CTkButton(speed_card, text="+", width=40, height=40, fg_color="#222222", text_color="#FFFFFF", command=self.increase_speed).place(x=120, y=70)
        # Pitch type (더 크게, 라디오버튼 세로 정렬, Type 라벨 위치 조정)
        pitch_card = ctk.CTkFrame(self.center_panel, width=180, height=120, fg_color="#FFFFFF", border_width=2, border_color="#FF6600")
        pitch_card.place(x=680, y=60)
        ctk.CTkLabel(pitch_card, text="Type", font=("Arial", 16, "bold"), text_color="#222222").place(x=60, y=10)
        self.pitch_type_var = ctk.StringVar(value="Fastball")
        for i, name in enumerate(["Fastball", "Curve", "Slider"]):
            ctk.CTkRadioButton(pitch_card, text=name, variable=self.pitch_type_var, value=name, fg_color="#FF6600", text_color="#222222", font=("Arial", 14)).place(x=30, y=40+i*25)
        # Graph/Sensor (더 크게)
        graph_frame = ctk.CTkFrame(self.center_panel, width=320, height=150, fg_color="#F7F7F7", border_width=1, border_color="#FF6600")
        graph_frame.place(x=40, y=340)
        ctk.CTkLabel(graph_frame, text="Graph", font=("Arial", 15), text_color="#222222").place(relx=0.5, rely=0.5, anchor="center")
        # Log/Status (더 크게)
        log_frame = ctk.CTkFrame(self.center_panel, width=400, height=150, fg_color="#F7F7F7", border_width=1, border_color="#FF6600")
        log_frame.place(x=400, y=340)
        ctk.CTkLabel(log_frame, text="Status / Log", font=("Arial", 15), text_color="#222222").place(relx=0.5, rely=0.5, anchor="center")
        # 하단 컨트롤(버튼 2개, 더 크게)
        self.pitch_btn = ctk.CTkButton(self.center_panel, text="Pitch", fg_color="#FF6600", text_color="#FFFFFF", width=200, height=60, corner_radius=30, font=("Arial", 18, "bold"), command=self.add_history)
        self.pitch_btn.place(x=220, y=540)
        ctk.CTkButton(self.center_panel, text="Stop", fg_color="#222222", text_color="#FFFFFF", width=200, height=60, corner_radius=30, font=("Arial", 18, "bold")).place(x=480, y=540)

    def add_history(self):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        pitch_type = self.pitch_type_var.get()
        speed = self.speed_var.get()
        ok = True  # 임시로 성공 처리
        # 데이터 추가
        self.history_data.insert(0, (now, pitch_type, speed, ok))
        # UI 갱신
        for row in self.history_rows:
            row.destroy()
        self.history_rows.clear()
        for idx, (t, typ, spd, ok) in enumerate(self.history_data):
            row = ctk.CTkFrame(self.history_frame, fg_color="#FFFFFF", border_width=0, corner_radius=10)
            row.pack(fill="x", pady=4, padx=4)
            ctk.CTkLabel(row, text=t, width=54, anchor="w", font=("Arial", 12)).pack(side="left", padx=(6,0))
            ctk.CTkLabel(row, text=typ, width=62, anchor="w", font=("Arial", 12, "bold"), text_color="#FF6600" if typ=="Fastball" else ("#0077CC" if typ=="Slider" else "#22AA22")).pack(side="left")
            ctk.CTkLabel(row, text=f"{spd}km/h", width=60, anchor="w", font=("Arial", 12)).pack(side="left")
            ctk.CTkLabel(row, text="✔" if ok else "✖", text_color="#FF6600" if ok else "#FF2222", width=20, font=("Arial", 15, "bold")).pack(side="left", padx=(0,6))
            if idx < len(self.history_data)-1:
                ctk.CTkFrame(self.history_frame, height=1, fg_color="#EEEEEE").pack(fill="x", padx=8)
            self.history_rows.append(row)
        # 통계 갱신
        counts = {"Fastball":0, "Curve":0, "Slider":0}
        speeds = []
        for _, typ, spd, _ in self.history_data:
            counts[typ] += 1
            speeds.append(spd)
        self.count_label.configure(text=f"Fastball: {counts['Fastball']}   Curve: {counts['Curve']}   Slider: {counts['Slider']}")
        if speeds:
            self.maxmin_label.configure(text=f"Max: {max(speeds)}km/h   Min: {min(speeds)}km/h")
        else:
            self.maxmin_label.configure(text="Max: -   Min: -")

    def increase_speed(self):
        v = self.speed_var.get()
        if v < 150:
            self.speed_var.set(v+10)
    def decrease_speed(self):
        v = self.speed_var.get()
        if v > 80:
            self.speed_var.set(v-10)

if __name__ == "__main__":
    app = TrackmanStyleUI()
    app.mainloop()