import tkinter as tk
from tkinter import ttk
import json
import os
import random

# 저장할 파일 이름
FILE_NAME = "names.json"

# 12명의 플레이어 이름을 저장할 리스트
players = []

# 저장된 파일이 있으면 불러오기, 없으면 기본값 설정
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        players = json.load(f)
else:
    players = [f"플레이어{i+1}" for i in range(12)]  # 기본값

# 플레이어의 가능 여부 초기화 (True: 가능, False: 불가능)
availability = {name: False for name in players}  # 🔥 모든 플레이어를 기본적으로 "불가능(False)"로 설정

# Tkinter 윈도우 생성
root = tk.Tk()
root.title("🔵 리그 오브 레전드 5대5 랜덤 팀 생성기 🔴")
root.geometry("600x500")
root.configure(bg="#2c2f33")  # 짙은 회색 배경 (디스코드 스타일)

# 🔹 **스타일 적용 (어두운 테마)**
style = ttk.Style()
style.configure("Custom.TButton", font=("Arial", 12, "bold"), padding=10, borderwidth=0,
                background="#7289da", foreground="white")
style.map("Custom.TButton",
          background=[("active", "#5b6eae"), ("pressed", "#4a5b96")],
          foreground=[("active", "white")])

# **이름 저장 함수**
def save_names():
    global players
    new_names = [entry.get() for entry in name_entries]  # 사용자가 입력한 이름 가져오기
    players = new_names
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=4)
    update_ui()  # UI 업데이트

# **체크박스 상태 업데이트**
def toggle_availability(player):
    availability[player] = not availability[player]  # 선택 여부 반전

# **UI 업데이트 (체크박스 새로고침)**
def update_ui():
    for widget in frame.winfo_children():
        widget.destroy()

    for i, player in enumerate(players):
        var = tk.BooleanVar(value=availability[player])  # 체크 여부 반영
        chk = tk.Checkbutton(frame, text=player, variable=var, 
                             command=lambda p=player: toggle_availability(p),
                             font=("Arial", 12), bg="#2c2f33", fg="white", selectcolor="#7289da",
                             activebackground="#4b4f56", padx=15, pady=5, relief="flat")
        chk.grid(row=i//6, column=i%6, padx=10, pady=5, sticky="w")  # 가로 6개씩 정렬

# **✅ 체크된 사람만 팀을 랜덤으로 배정 (체크 안 된 사람 절대 포함 X)**
def create_teams():
    available_players = [p for p in players if availability.get(p, False)]  # ✅ 체크된 사람만 포함

    # ✅ 10명 이상 체크되지 않으면 오류 메시지 표시
    if len(available_players) < 10:
        result_label.config(text="❌ 최소 10명의 플레이어를 선택하세요!", fg="red")
        return

    # ✅ 체크된 사람 중에서 랜덤으로 10명을 선택
    selected_players = random.sample(available_players, 10)
    team1 = selected_players[:5]
    team2 = selected_players[5:]
    
    # ✅ 결과를 result_label에 표시 (체크 안 된 사람은 절대 포함되지 않음)
    result_label.config(text=f"🔵 팀 1: {', '.join(team1)}\n🔴 팀 2: {', '.join(team2)}", fg="white")

# **UI 구성**
frame = tk.Frame(root, bg="#2c2f33")
frame.pack(pady=10)

# **이름 입력 필드**
name_entries = []
entry_frame = tk.Frame(root, bg="#2c2f33")
entry_frame.pack(pady=10)

for i in range(12):
    entry = tk.Entry(entry_frame, width=15, font=("Arial", 12), bg="#40444b", fg="white", justify="center",
                     relief="solid", bd=1, insertbackground="white")  # 어두운 배경에 흰색 글씨
    entry.insert(0, players[i])  # 기존 저장된 이름 불러오기
    entry.grid(row=i//6, column=i%6, padx=5, pady=5)
    name_entries.append(entry)

# **이름 저장 버튼 (어두운 스타일)**
save_button = ttk.Button(root, text="💾 이름 저장", command=save_names, style="Custom.TButton")
save_button.pack(pady=5)

# **체크박스 UI 업데이트**
update_ui()

# **팀 생성 버튼 (어두운 스타일)**
team_button = ttk.Button(root, text="⚔ 랜덤 팀 생성", command=create_teams, style="Custom.TButton")
team_button.pack(pady=10)

# **결과 출력 라벨**
result_label = tk.Label(root, text="", fg="white", font=("Arial", 12, "bold"), bg="#2c2f33")
result_label.pack()

# Tkinter 실행
root.mainloop()