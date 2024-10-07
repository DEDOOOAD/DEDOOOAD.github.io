import tkinter as tk
from tkinter import messagebox
import csv
import os
import re

class AddressBook:
    def __init__(self, master):
        self.master = master
        self.master.title("주소록")
        self.master.geometry("600x400")
        self.master.configure(bg="#f7f7f7")

        self.contacts = {}
        self.load_contacts()

        # 제목 프레임
        self.title_frame = tk.Frame(master, bg="#007BFF", bd=0)
        self.title_frame.pack(fill=tk.X)

        self.title_label = tk.Label(self.title_frame, text="주소록", font=("Helvetica", 20, "bold"), bg="#007BFF", fg="white")
        self.title_label.pack(pady=10)

        # 입력 프레임
        self.input_frame = tk.Frame(master, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.input_frame.pack(pady=20, padx=20)

        self.name_label = tk.Label(self.input_frame, text="이름:", bg="#ffffff", font=("Helvetica", 12))
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.name_entry = tk.Entry(self.input_frame, width=30, font=("Helvetica", 12), bd=2, relief=tk.SUNKEN)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.phone_label = tk.Label(self.input_frame, text="전화번호:", bg="#ffffff", font=("Helvetica", 12))
        self.phone_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.phone_entry = tk.Entry(self.input_frame, width=30, font=("Helvetica", 12), bd=2, relief=tk.SUNKEN)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10)
        self.phone_entry.bind("<KeyRelease>", self.format_phone_entry)

        # 버튼 프레임
        self.button_frame = tk.Frame(master, bg="#ffffff")
        self.button_frame.pack(pady=20)

        button_styles = {
            'width': 10,
            'font': ("Helvetica", 12),
            'bg': "#007BFF",
            'fg': "white",
            'activebackground': "#0056b3",
            'bd': 0,
            'relief': tk.RAISED
        }

        self.add_button = tk.Button(self.button_frame, text="추가", command=self.add_contact, **button_styles)
        self.add_button.grid(row=0, column=0, padx=10, pady=5)

        self.find_button = tk.Button(self.button_frame, text="찾기", command=self.open_search_window, **button_styles)
        self.find_button.grid(row=0, column=1, padx=10, pady=5)

        self.update_button = tk.Button(self.button_frame, text="수정", command=self.update_contact, **button_styles)
        self.update_button.grid(row=0, column=2, padx=10, pady=5)

        # 수정 및 삭제 기능 버튼을 검색창에서 처리하도록 수정
        self.delete_button = tk.Button(self.button_frame, text="삭제", command=self.open_search_window, **button_styles)
        self.delete_button.grid(row=0, column=3, padx=10, pady=5)

    def load_contacts(self):
        if os.path.exists("contacts.csv"):
            with open("contacts.csv", mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:
                        name, phone = row
                        self.contacts[name] = phone

    def save_contacts(self):
        with open("contacts.csv", mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            for name, phone in self.contacts.items():
                writer.writerow([name, phone])

    def is_valid_phone(self, phone):
        pattern = r"^010-\d{4}-\d{4}$"
        return re.match(pattern, phone)

    def is_valid_name(self, name):
        pattern = r"^[가-힣]+$"
        return re.match(pattern, name)

    def format_phone(self, phone):
        phone = re.sub(r'\D', '', phone)  # 숫자 외 문자 제거
        if len(phone) == 11 and phone.startswith('010'):
            return f"{phone[:3]}-{phone[3:7]}-{phone[7:]}"
        return None

    def format_phone_entry(self, event):
        phone = self.phone_entry.get().replace("-", "")
        if len(phone) >= 11:
            phone = phone[:11]
        if len(phone) > 6:
            formatted = f"{phone[:3]}-{phone[3:7]}-{phone[7:]}"
        elif len(phone) > 3:
            formatted = f"{phone[:3]}-{phone[3:]}"
        else:
            formatted = phone
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, formatted)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        if name and phone:
            if not self.is_valid_name(name):
                messagebox.showwarning("경고", "이름은 한글만 입력 가능합니다.")
                return

            formatted_phone = self.format_phone(phone)
            if formatted_phone:
                self.contacts[name] = formatted_phone
                messagebox.showinfo("정보", "연락처가 추가되었습니다.")
                self.save_contacts()
                self.clear_entries()
            else:
                messagebox.showwarning("경고", "올바른 전화번호 형식이 아닙니다. (예: 010-xxxx-xxxx)")
        else:
            messagebox.showwarning("경고", "이름과 전화번호를 입력하세요.")

    def open_search_window(self):
        self.search_window = tk.Toplevel(self.master)
        self.search_window.title("검색 결과")
        self.search_window.geometry("400x300")

        search_label = tk.Label(self.search_window, text="이름 초성 입력:", font=("Helvetica", 12))
        search_label.pack(pady=10)

        search_entry = tk.Entry(self.search_window, font=("Helvetica", 12))
        search_entry.pack(pady=5)

        search_button = tk.Button(self.search_window, text="검색", command=lambda: self.find_contact(search_entry.get()), font=("Helvetica", 12))
        search_button.pack(pady=5)

        self.result_listbox = tk.Listbox(self.search_window, width=50, height=10, font=("Helvetica", 12))
        self.result_listbox.pack(pady=10)
        self.result_listbox.bind("<Double-Button-1>", self.select_contact)

        self.edit_button = tk.Button(self.search_window, text="수정", command=self.edit_selected_contact, font=("Helvetica", 12))
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(self.search_window, text="삭제", command=self.delete_selected_contact, font=("Helvetica", 12))
        self.delete_button.pack(pady=5)

    def find_contact(self, initial):
        self.result_listbox.delete(0, tk.END)  # 이전 검색 결과 삭제
        results = [name for name in self.contacts if self.get_initial(name) == self.get_initial(initial)]
        if results:
            for name in results:
                phone = self.contacts[name]
                self.result_listbox.insert(tk.END, f"{name}: {phone}")
        else:
            messagebox.showinfo("정보", "해당 초성으로 검색된 결과가 없습니다.")

    def get_initial(self, name):
        if not name:
            return ''
        initials = {
            '가': 'ㄱ', '나': 'ㄴ', '다': 'ㄷ', '라': 'ㄹ', '마': 'ㅁ', '바': 'ㅂ', '사': 'ㅅ',
            '아': 'ㅇ', '자': 'ㅈ', '차': 'ㅊ', '카': 'ㅋ', '타': 'ㅌ', '파': 'ㅍ', '하': 'ㅎ'
        }
        return initials.get(name[0], '')

    def select_contact(self, event):
        selected_index = self.result_listbox.curselection()
        if selected_index:
            selected_info = self.result_listbox.get(selected_index)
            name, phone = selected_info.split(": ")
            messagebox.showinfo("정보", f"{name}: {phone}")

    def edit_selected_contact(self):
        selected_index = self.result_listbox.curselection()
        if selected_index:
            selected_info = self.result_listbox.get(selected_index)
            name, phone = selected_info.split(": ")
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, name)
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, phone)

    def delete_selected_contact(self):
        selected_index = self.result_listbox.curselection()
        if selected_index:
            selected_info = self.result_listbox.get(selected_index)
            name, _ = selected_info.split(": ")
            del self.contacts[name]
            messagebox.showinfo("정보", "연락처가 삭제되었습니다.")
            self.save_contacts()
            self.result_listbox.delete(selected_index)
        else:
            messagebox.showwarning("경고", "삭제할 연락처를 선택하세요.")

    def update_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        if name in self.contacts:
            if not self.is_valid_name(name):
                messagebox.showwarning("경고", "이름은 한글만 입력 가능합니다.")
                return

            formatted_phone = self.format_phone(phone)
            if formatted_phone:
                self.contacts[name] = formatted_phone
                messagebox.showinfo("정보", "연락처가 수정되었습니다.")
                self.save_contacts()
                self.clear_entries()
            else:
                messagebox.showwarning("경고", "올바른 전화번호 형식이 아닙니다. (예: 010-xxxx-xxxx)")
        else:
            messagebox.showwarning("경고", "연락처를 찾을 수 없습니다.")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

    def on_closing(self):
        self.save_contacts()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    address_book = AddressBook(root)
    root.protocol("WM_DELETE_WINDOW", address_book.on_closing)
    root.mainloop()
