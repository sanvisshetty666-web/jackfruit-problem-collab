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
        self.root.geometry("660x600")
        self.root.configure(bg="#f5f5dc")
        self.root.resizable(False,False)

        self.is_dark=False
        self.file_loaded=False
        self.loaded_text=""

        self.input_text=tk.StringVar()
        self.output_text=tk.StringVar()
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

        tk.Label(self.inner,text="🌼 Enter Your Secret Message",
                 bg="#faedcd",fg="#3f2e2e",
                 font=("Comic Sans MS",11,"bold")).grid(row=0,column=0,sticky="w")

        self.entry=ttk.Entry(self.inner,textvariable=self.input_text,width=38)
        self.entry.grid(row=1,column=0,columnspan=2,pady=8,sticky="w")
        self.entry.bind("<Key>",self.disable_file_mode)

        tk.Button(self.inner,text="📂 Open File",
                  font=("Comic Sans MS",9),
                  command=self.open_file)\
            .grid(row=1,column=2,padx=10)

        tk.Label(self.inner,text="🔑 Shift Key (1–25)",
                 bg="#faedcd",fg="#3f2e2e",
                 font=("Comic Sans MS",11,"bold")).grid(row=2,column=0,sticky="w")

        ttk.Entry(self.inner,textvariable=self.key_var,width=10)\
            .grid(row=3,column=0,sticky="w",pady=6)
        
        self.encrypt_btn = tk.Button(self.inner,text="🌸 Encrypt",bg="#e9edc9",
                  font=("Comic Sans MS",10,"bold"),width=12,
                  command=self.encrypt)
        self.encrypt_btn.grid(row=3,column=1,padx=10,sticky="w")

        self.decrypt_btn = tk.Button(self.inner,text="🌿 Decrypt",bg="#e9edc9",
                  font=("Comic Sans MS",10,"bold"),width=12,
                  command=self.decrypt)
        self.decrypt_btn.grid(row=3,column=2,sticky="w")
        
        self.bf_btn = tk.Button(self.inner,text="🔨 Brute Force Decrypt",bg="#e9edc9",
                  font=("Comic Sans MS",10,"bold"),width=29,
                  command=self.brute_force_decrypt)
        self.bf_btn.grid(row=4,column=1,columnspan=3,pady=10,sticky="w") 

        tk.Label(self.inner,text="🌷 Enchanted Output",
                 bg="#faedcd",fg="#3f2e2e",
                 font=("Comic Sans MS",11,"bold")).grid(row=5,column=0,sticky="w",pady=(15,0))

        self.output_box=tk.Label(self.inner,textvariable=self.output_text,
                                       bg="#e9edc9",fg="#344e41",
                                       width=52,height=3,
                                       font=("Consolas",11),
                                       anchor="w",justify="left")
        self.output_box.grid(row=6,column=0,columnspan=3,pady=10)

        self.status_label=tk.Label(self.inner,textvariable=self.status_var,
                                          bg="#e9edc9",fg="#6a994e",
                                          font=("Comic Sans MS",10,"bold"),
                                          width=52,height=2,anchor="w")
        self.status_label.grid(row=7,column=0,columnspan=3)

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

    def open_file(self):
        self.input_text.set("")
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
        text=self.output_text.get()
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
            self.output_box.configure(bg="#5E1735",fg="#d4a373")
            self.header.configure(bg="#5E1735")
            self.title_label.configure(bg="#111111",fg="#faedcd")
            
            self.toggle_btn.config(text="☀ Dark Mode: ON",bg="#d4a373",fg="#111111") 
            self.is_dark=True
        else:
            self.root.configure(bg="#f5f5dc")
            self.card.configure(bg="#faedcd",highlightbackground="#a3b18a")
            self.inner.configure(bg="#faedcd")
            self.status_label.configure(bg="#e9edc9",fg="#6a994e")
            self.output_box.configure(bg="#e9edc9",fg="#344e41")
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
        return self.input_text.get().strip()

    def encrypt(self):
        key=self.get_valid_key()
        text=self.get_input_text()

        if not text:
            self.status_var.set("❌ Please type a message OR load a file!")
            return

        if key:
            self.ciphertext=caesar_cipher(text,key,"encrypt")
            output_display=f"Key Used: {key}\nCiphertext: {self.ciphertext}"
            
            self.output_text.set(output_display)
            self.status_var.set(f"🌸 Encryption Successful! Key {key} noted.")

    def decrypt(self):
        key=self.get_valid_key()
        text=self.get_input_text()

        if not text:
            self.status_var.set("❌ Please type a message OR load a file!")
            return

        if key:
            self.plaintext=caesar_cipher(text,key,"decrypt")
            self.output_text.set(self.plaintext)
            self.status_var.set("🌿 Decryption Successful!")

    def brute_force_decrypt(self):
        text=self.get_input_text()

        if not text:
            self.status_var.set("❌ Please type a message OR load a file for cracking!")
            return
        
        results="--- CAESAR CIPHER BRUTE FORCE RESULTS ---\n\n"
        
        for key in range(1,26):
            decrypted_text=caesar_cipher(text,key,"decrypt")
            results+=f"KEY {key:02}:\n{decrypted_text}\n\n---\n\n"
            
        self.status_var.set("🔨 Brute Force analysis complete! Check the new window.")
        
        bf_window=tk.Toplevel(self.root)
        bf_window.title("🔨 Brute Force Decryption")
        bf_window.geometry("700x500")
        bf_window.configure(bg="#faedcd")
        
        tk.Label(bf_window,text="All Possible Plaintexts (Shift Key 1 to 25)",
                 font=("Comic Sans MS",14,"bold"),bg="#faedcd",fg="#3f2e2e").pack(pady=10)
        
        result_box=scrolledtext.ScrolledText(bf_window,wrap=tk.WORD, 
                                               width=80,height=25, 
                                               font=("Consolas",10), 
                                               bg="#e9edc9",fg="#344e41")
        result_box.pack(padx=10,pady=10)
        
        result_box.insert(tk.END,results)
        result_box.configure(state=tk.DISABLED)

    def copy_result(self):
        output_data=self.output_text.get()

        if not output_data:
            self.status_var.set("❌ Nothing to copy!")
            return
        
        if output_data.startswith("Key Used:"):
            lines=output_data.split('\n')
            if len(lines)>1:
                text_to_copy=lines[1].replace("Ciphertext: ","")
            else:
                text_to_copy=output_data
        else:
            text_to_copy=output_data

        if text_to_copy:
            self.root.clipboard_clear()
            self.root.clipboard_append(text_to_copy)
            self.status_var.set("📋 Encrypted/Decrypted Text Copied!")

    def clear_fields(self):
        self.input_text.set("")
        self.output_text.set("")
        self.key_var.set("")
        self.file_loaded=False
        self.loaded_text=""
        self.status_var.set("🧹 All Clean!")

if __name__=="__main__":
    root=tk.Tk()
    app=CaesarCipherModern(root)
    root.mainloop()
