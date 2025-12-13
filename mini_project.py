import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext

def caesar_cipher(text, key, mode='encrypt'):
    result=""
    key=key%26
    if mode=='decrypt':
        key=-key

    for char in text:
        if char.isupper():
            result+=chr((ord(char)-65+key)%26+65)
        elif char.islower():
            result+=chr((ord(char)-97+key)%26+97)
        else:
            result+=char
    return result


class CaesarCipherModern:
    def __init__(self, root):
        self.root=root
        self.root.title("🌸 Caesar Cipher Garden 🌷")
        self.root.geometry("660x800") 
        self.root.configure(bg="#f5f5dc")
        self.root.resizable(True,True)

        self.is_dark=False
        self.file_loaded=False
        self.loaded_text=""

        self.key_var=tk.StringVar()
        self.status_var=tk.StringVar(value="Ready 🌼")

        self.header=tk.Frame(root,bg="#FFCFEF",height=80)
        self.header.pack(fill="x")

        self.title_label=tk.Label(
            self.header,
            text="🌸 Caesar Cipher Garden 🌷",
            font=("Segoe Script",22,"bold"),
            fg="#3f2e2e",bg="#FFCFEF"
        )
        self.title_label.pack(pady=18)

        self.card=tk.Frame(root,bg="#faedcd",
                              highlightbackground="#a3b18a",
                              highlightthickness=2)
        self.card.pack(pady=20,padx=20,fill="both",expand=True)

        self.inner=tk.Frame(self.card,bg="#faedcd",padx=25,pady=25)
        self.inner.pack(fill="both",expand=True)
        
        self.inner.grid_columnconfigure(1, weight=1) 
        self.inner.grid_rowconfigure(7, weight=1) 

        tk.Label(self.inner,text="🌼 Enter Your Secret Message",
                  bg="#faedcd",fg="#3f2e2e",
                  font=("Comic Sans MS",11,"bold")).grid(row=0,column=0,sticky="w")

        self.input_box = scrolledtext.ScrolledText(self.inner, wrap=tk.WORD, 
                                                   width=40, height=4, 
                                                   font=("Consolas", 10))
        self.input_box.grid(row=1,column=0,columnspan=2,pady=8,sticky="new")
        self.input_box.bind("<Key>",self.disable_file_mode)

        tk.Button(self.inner,text="📂 Open File",
                  font=("Comic Sans MS",9),
                  command=self.open_file)\
            .grid(row=1,column=2,padx=10,rowspan=2,sticky="nw")

        tk.Label(self.inner,text="🔑 Shift Key (1–25)",
                  bg="#faedcd",fg="#3f2e2e",
                  font=("Comic Sans MS",11,"bold")).grid(row=2,column=0,sticky="w",pady=(10,0))

        ttk.Entry(self.inner,textvariable=self.key_var,width=10)\
            .grid(row=3,column=0,sticky="w",pady=6)
        
        self.encrypt_btn = tk.Button(self.inner,text="🌸 Encrypt",bg="#e9edc9",
                  font=("Comic Sans MS",10,"bold"),width=12,
                  command=self.encrypt)
        self.encrypt_btn.grid(row=3,column=1,sticky="e") 

        self.decrypt_btn = tk.Button(self.inner,text="🌿 Decrypt",bg="#e9edc9",
                  font=("Comic Sans MS",10,"bold"),width=12,
                  command=self.decrypt)
        self.decrypt_btn.grid(row=3,column=2,padx=(5,0), sticky="e") 
        
        self.bf_btn = tk.Button(self.inner,text="🔨 Brute Force Decrypt",bg="#e9edc9",
                  font=("Comic Sans MS",10,"bold"),width=26,
                  command=self.brute_force_decrypt)
        self.bf_btn.grid(row=4,column=1,columnspan=2,pady=10,sticky="e") 


        tk.Label(self.inner,text="🌷 Enchanted Output",
                  bg="#faedcd",fg="#3f2e2e",
                  font=("Comic Sans MS",11,"bold")).grid(row=5,column=0,sticky="w",pady=(15,0))

        self.output_box=scrolledtext.ScrolledText(self.inner, wrap=tk.WORD,
                                                 width=50, 
                                                 height=10, 
                                                 bg="#e9edc9",fg="#344e41",
                                                 font=("Consolas",11))
        self.output_box.grid(row=6,column=0,columnspan=3,pady=10, sticky="nsew")
        self.output_box.configure(state=tk.DISABLED)


        self.status_label=tk.Label(self.inner,textvariable=self.status_var,
                                             bg="#e9edc9",fg="#6a994e",
                                             font=("Comic Sans MS",10,"bold"),
                                             width=52,height=2,anchor="w")
        self.status_label.grid(row=7,column=0,columnspan=3, sticky="ew")

        tk.Button(self.inner,text="💾 Download Output",
                  font=("Comic Sans MS",10,"bold"),
                  width=18,command=self.save_file)\
            .grid(row=8,column=0,pady=10)

        tk.Button(self.inner,text="📋 Copy Output",
                  font=("Comic Sans MS",10,"bold"),
                  width=14,command=self.copy_result)\
            .grid(row=8,column=2)


        self.toggle_btn=tk.Button(
            self.inner,text="🌙 Dark Mode: OFF",bg="#ffffff",fg="#3f2e2e",
            font=("Comic Sans MS",10,"bold"),
            width=18,command=self.toggle_theme
        )
        self.toggle_btn.grid(row=9,column=0,pady=10)

        tk.Button(self.inner,text="🧹 Clear",
                  font=("Comic Sans MS",10,"bold"),
                  width=14,command=self.clear_fields)\
            .grid(row=9,column=2)

        tk.Label(self.inner,text="🌸 🌼 🌷 🌿 🌸",
                  bg="#faedcd",font=("Comic Sans MS",11))\
            .grid(row=10,column=0,columnspan=3,pady=12)


    def _set_output(self, text):
        self.output_box.configure(state=tk.NORMAL)
        self.output_box.delete('1.0', tk.END)
        self.output_box.insert(tk.END, text)
        self.output_box.configure(state=tk.DISABLED)

    def _get_output(self):
        self.output_box.configure(state=tk.NORMAL)
        text = self.output_box.get('1.0', tk.END).strip()
        self.output_box.configure(state=tk.DISABLED)
        return text

    def _set_input(self, text):
        self.input_box.delete('1.0', tk.END)
        self.input_box.insert(tk.END, text)

    def _get_input(self):
        return self.input_box.get('1.0', tk.END).strip()
    
    def open_file(self):
        self._set_input("")
        file_path=filedialog.askopenfilename(filetypes=[("Text Files","*.txt")])
        if not file_path:
            return

        try:
            with open(file_path,"r",encoding="utf-8")as file:
                self.loaded_text=file.read()
            self.file_loaded=True
            self.status_var.set(f"📂 Text file loaded successfully from {file_path.split('/')[-1]}!")
        except Exception as e:
            self.status_var.set(f"❌ Error loading file: {e}")

    def disable_file_mode(self,event):
        self.file_loaded=False
        self.loaded_text=""

    def save_file(self):
        text=self._get_output()
        if not text:
            self.status_var.set("❌ Nothing to download!")
            return

        file_path=filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            try:
                with open(file_path,"w",encoding="utf-8")as file:
                    file.write(text)
                self.status_var.set("💾 File downloaded successfully!")
            except Exception as e:
                self.status_var.set(f"❌ Error saving file: {e}")

    def toggle_theme(self):
        if not self.is_dark:
            self.root.configure(bg="#333333")
            self.card.configure(bg="#1e1e1e",highlightbackground="#4a4e69")
            self.inner.configure(bg="#1e1e1e")
            self.status_label.configure(bg="#5E1735",fg="#cccccc")
            self.output_box.configure(bg="#5E1735",fg="#d4a373", insertbackground="#ffffff")
            self.input_box.configure(bg="#111111", fg="#cccccc", insertbackground="#ffffff")

            self.header.configure(bg="#5E1735")
            self.title_label.configure(bg="#111111",fg="#faedcd")
            
            self.toggle_btn.config(text="☀ Dark Mode: ON",bg="#d4a373",fg="#111111") 
            self.is_dark=True
        else:
            self.root.configure(bg="#f5f5dc")
            self.card.configure(bg="#faedcd",highlightbackground="#a3b18a")
            self.inner.configure(bg="#faedcd")
            self.status_label.configure(bg="#e9edc9",fg="#6a994e")
            self.output_box.configure(bg="#e9edc9",fg="#344e41", insertbackground="#000000")
            self.input_box.configure(bg="#ffffff", fg="#000000", insertbackground="#000000")

            self.header.configure(bg="#f2c6de")
            self.title_label.configure(bg="#f2c6de",fg="#3f2e2e")
            
            self.toggle_btn.config(text="🌙 Dark Mode: OFF",bg="#ffffff",fg="#3f2e2e")
            self.is_dark=False

    def get_valid_key(self):
        try:
            key=int(self.key_var.get())
            if not 1<=key<=25:
                raise ValueError
            return key
        except:
            self.status_var.set("❌ Key must be between 1 and 25")
            return None

    def get_input_text(self):
        if self.file_loaded:
            return self.loaded_text.strip()
        return self._get_input()

    def encrypt(self):
        key=self.get_valid_key()
        text=self.get_input_text()

        if not text:
            self.status_var.set("❌ Please type a message OR load a file!")
            return

        if key:
            self.ciphertext=caesar_cipher(text,key,"encrypt")
            
            output_display=self.ciphertext 
            
            self._set_output(output_display)
            self.status_var.set("🌸 Encryption Successful!")

    def decrypt(self):
        key=self.get_valid_key()
        text=self.get_input_text()

        if not text:
            self.status_var.set("❌ Please type a message OR load a file!")
            return

        if key:
            self.plaintext=caesar_cipher(text,key,"decrypt")
            self._set_output(self.plaintext)
            self.status_var.set("✅ Operation Successful!")

    def brute_force_decrypt(self):
        text=self.get_input_text()

        if not text:
            self.status_var.set("❌ Please type a message OR load a file for cracking!")
            return
        
        results="--- CAESAR CIPHER BRUTE FORCE RESULTS ---\n\n"
        
        for key in range(1,26):
            decrypted_text=caesar_cipher(text,key,"decrypt")
            
            results+=f"KEY {key:02}:\n{decrypted_text}\n\n---\n\n"
            
        self._set_output(results)

        self.status_var.set("🔨 Brute Force analysis complete! Results displayed in output box.")

    def copy_result(self):
        output_data=self._get_output()

        if not output_data:
            self.status_var.set("❌ Nothing to copy!")
            return
        
        text_to_copy = output_data

        if text_to_copy:
            self.root.clipboard_clear()
            self.root.clipboard_append(text_to_copy)
            self.status_var.set("📋 Text Copied!")

    def clear_fields(self):
        self._set_input("")
        self._set_output("")
        self.key_var.set("")
        self.file_loaded=False
        self.loaded_text=""
        self.status_var.set("🧹 All Clean!")


if __name__=="__main__":
    root=tk.Tk()
    app=CaesarCipherModern(root)
    root.mainloop()

