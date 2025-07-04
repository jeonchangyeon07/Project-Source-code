import customtkinter as ctk

# CustomTkinter 설정
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# 메인 윈도우 생성
root = ctk.CTk()
root.geometry("600x800")
root.title("CustomTkinter 위젯 예제")

# Switch 위젯 (모드 토글)
def toggle_mode():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")

    else:
        ctk.set_appearance_mode("Dark")

mode_toggle = ctk.CTkSwitch(root, text="모드 변경", command=toggle_mode)
mode_toggle.pack(pady=10, anchor="se", padx=10)

# Entry 위젯
entry = ctk.CTkEntry(root, placeholder_text="이름을 입력하세요")
entry.pack(pady=10)

# Slider 위젯 (라벨 위젯으로 슬라이더 값 표시)
label = ctk.CTkLabel(root, text="슬라이더 값: ")
label.pack(pady=10)

def slider_event(value):
    label.configure(text=f"슬라이더 값: {int(value)}")

slider = ctk.CTkSlider(root, from_=0, to=100, command=slider_event)
slider.pack(pady=10)

# CheckBox 위젯
checkbox = ctk.CTkCheckBox(root, text="동의합니다")
checkbox.pack(pady=10)

# RadioButton 위젯
radio_var = ctk.StringVar(value="옵션1")
radiobutton1 = ctk.CTkRadioButton(root, text="옵션 1", variable=radio_var, value="옵션1")
radiobutton2 = ctk.CTkRadioButton(root, text="옵션 2", variable=radio_var, value="옵션2")
radiobutton1.pack()
radiobutton2.pack()

# ComboBox 위젯
combobox = ctk.CTkComboBox(root, values=["선택 1", "선택 2", "선택 3"])
combobox.pack(pady=10)

# ProgressBar 위젯
progressbar = ctk.CTkProgressBar(root)
progressbar.pack(pady=10)
progressbar.set(0.5)  # 50% 진행 상태

# TabView 위젯
tabview = ctk.CTkTabview(root)
tabview.pack(pady=10)

# 탭 추가
tab1 = tabview.add("탭 1")
tab2 = tabview.add("탭 2")

# 각 탭에 내용 추가
ctk.CTkLabel(tab1, text="탭 1의 내용입니다").pack(pady=10)
ctk.CTkLabel(tab2, text="탭 2의 내용입니다").pack(pady=10) 

# ScrollableFrame 위젯
scrollable_frame = ctk.CTkScrollableFrame(root, width=300, height=150)
scrollable_frame.pack(pady=10)
for i in range(10):
    ctk.CTkLabel(scrollable_frame, text=f"항목 {i+1}").pack()

# 실행
root.mainloop()