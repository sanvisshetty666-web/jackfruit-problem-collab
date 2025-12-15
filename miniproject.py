import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext

# --- Core Cipher Logic Function ---
def caesar_cipher(text, key, mode='encrypt'):
    """
    Applies the Caesar Cipher to the given text using the specified key and mode.
    (Encrypt: Shift letters forward; Decrypt: Shift letters backward).
    Non-alphabetic characters are left unchanged.
    """
    result=""
    
    # Decryption is essentially encryption with a negative key (shift backwards)
    if mode=='decrypt':
        key=-key

    for char in text:
        if char.isupper():
            # For uppercase letters:
            # 1. ord(char) - 65 gives 0-25 (A=0, B=1, ...)
            # 2. Add the shift key
            # 3. % 26 ensures wrap-around (e.g., 26 becomes 0)
            # 4. + 65 converts back to ASCII for the shifted uppercase letter
            result+=chr((ord(char)-65+key)%26+65)
        elif char.islower():
            # For lowercase letters:
            # Same logic as uppercase, but using 97 (ord('a'))
            result+=chr((ord(char)-97+key)%26+97)
        else:
            # Keep non-alphabetic characters (spaces, numbers, punctuation) as is
            result+=char
    return result


# --- Tkinter GUI Class ---
class CaesarCipherModern:
    def __init__(self, root):
        self.root=root
        self.root.title("🌸 Caesar Cipher Garden 🌷")
        self.root.geometry("660x880")
        self.root.configure(bg="#f5f5dc") # Light Mode Root Background
        self.root.resizable(True,True)

        # State Variables
        self.is_dark=False
        self.file_loaded=False
        self.loaded_text=""

        # Tkinter control variables
        self.key_var=tk.StringVar()
        self.status_var=tk.StringVar(value="Ready 🌼")

        # Header Frame (for title)
        self.header=tk.Frame(root,bg="#FFCFEF",height=80)
        self.header.pack(fill="x")

        self.title_label=tk.Label(
            self.header,
            text="🌸 Caesar Cipher Garden 🌷",
            font=("Segoe Script",22,"bold"),
            fg="#3f2e2e",bg="#FFCFEF"
        )
        self.title_label.pack(pady=18)

        # Main Card Frame (for content, with a border/highlight)
        self.card=tk.Frame(root,bg="#faedcd",
                             highlightbackground="#a3b18a",
                             highlightthickness=2)
        self.card.pack(pady=20,padx=20,fill="both",expand=True)

        # Inner Frame (for padding and grid layout)
        self.inner=tk.Frame(self.card,bg="#faedcd",padx=25,pady=25)
        self.inner.pack(fill="both",expand=True)
        
        # Grid Configuration for responsiveness
        self.inner.grid_columnconfigure(1, weight=1)
        self.inner.grid_rowconfigure(6, weight=1) # The row with the output box

        # Input Section
        tk.Label(self.inner,text="🌼 Enter Your Secret Message",
                  bg="#faedcd",fg="#3f2e2e",
                  font=("Comic Sans MS",11,"bold")).grid(row=0,column=0,sticky="w")

        self.input_box = scrolledtext.ScrolledText(self.inner, wrap=tk.WORD,
                                                     width=40, height=4,
                                                     font=("Consolas", 10))
        self.input_box.grid(row=1,column=0,columnspan=2,pady=8,sticky="new")
        # Bind event to detect manual typing and disable file mode
        self.input_box.bind("<Key>",self.disable_file_mode)

        tk.Button(self.inner,text="📂 Open File",
                  font=("Comic Sans MS",9),
                  command=self.open_file)\
            .grid(row=1,column=2,padx=10,rowspan=2,sticky="nw")

        # Key Input and Action Buttons
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

        # Output Section
        tk.Label(self.inner,text="🌷 Enchanted Output",
                  bg="#faedcd",fg="#3f2e2e",
                  font=("Comic Sans MS",11,"bold")).grid(row=5,column=0,sticky="w",pady=(15,0))

        self.output_box=scrolledtext.ScrolledText(self.inner, wrap=tk.WORD,
                                                     width=50,
                                                     height=10,
                                                     bg="#e9edc9",fg="#344e41",
                                                     font=("Consolas",11))
        self.output_box.grid(row=6,column=0,columnspan=3,pady=10, sticky="nsew")
        self.output_box.configure(state=tk.DISABLED) # Start in disabled state

        # Status Bar
        self.status_label=tk.Label(self.inner,textvariable=self.status_var,
                                          bg="#e9edc9",fg="#6a994e",
                                          font=("Comic Sans MS",10,"bold"),
                                          width=52,height=2,anchor="w")
        self.status_label.grid(row=7,column=0,columnspan=3, sticky="ew")

        # Utility Buttons
        tk.Button(self.inner,text="💾 Download Output",
                  font=("Comic Sans MS",10,"bold"),
                  width=18,command=self.save_file)\
            .grid(row=8,column=0,pady=10)

        tk.Button(self.inner,text="📋 Copy Output",
                  font=("Comic Sans MS",10,"bold"),
                  width=14,command=self.copy_result)\
            .grid(row=8,column=2)

        # Theme and Clear Buttons
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

        # Footer
        tk.Label(self.inner,text="🌸 🌼 🌷 🌿 🌸",
                  bg="#faedcd",font=("Comic Sans MS",11))\
            .grid(row=10,column=0,columnspan=3,pady=12)


    # --- Helper Methods for Text Boxes ---

    def _set_output(self, text):
        """Clears and sets text in the output box, temporarily enabling writing."""
        self.output_box.configure(state=tk.NORMAL)
        self.output_box.delete('1.0', tk.END)
        self.output_box.insert(tk.END, text)
        self.output_box.configure(state=tk.DISABLED)

    def _get_output(self):
        """Gets all text from the output box."""
        self.output_box.configure(state=tk.NORMAL) # Must enable to get text
        text = self.output_box.get('1.0', tk.END).strip()
        self.output_box.configure(state=tk.DISABLED)
        return text

    def _set_input(self, text):
        """Clears and sets text in the input box."""
        self.input_box.delete('1.0', tk.END)
        self.input_box.insert(tk.END, text)

    def _get_input(self):
        """Gets all text from the input box."""
        return self.input_box.get('1.0', tk.END).strip()
    
    def get_input_text(self):
        """Returns the text to be processed, prioritizing the loaded file content."""
        if self.file_loaded:
            return self.loaded_text.strip()
        return self._get_input()

    # --- File Handling ---

    def open_file(self):
        """Opens a text file and stores its content for processing."""
        self._set_input("") # Clear input box to visually indicate file mode
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
        """Called on keypress in input box; disables file mode."""
        self.file_loaded=False
        self.loaded_text=""
        # Update status if needed, but not strictly necessary on every keypress

    def save_file(self):
        """Saves the output box content to a selected file path."""
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

    # --- Theme Toggling ---

    def toggle_theme(self):
        """Switches the application between light and dark themes."""
        if not self.is_dark:
            # Dark Mode Settings
            dark_bg = "#1e1e1e"
            dark_fg = "#cccccc"
            dark_accent = "#5E1735" # Dark Header/Status
            dark_input_bg = "#111111"
            dark_output_bg = "#5E1735"
            dark_output_fg = "#d4a373"

            self.root.configure(bg="#333333")
            self.card.configure(bg=dark_bg,highlightbackground="#4a4e69")
            self.inner.configure(bg=dark_bg)
            self.status_label.configure(bg=dark_accent,fg=dark_fg)
            self.output_box.configure(bg=dark_output_bg,fg=dark_output_fg, insertbackground="#ffffff")
            self.input_box.configure(bg=dark_input_bg, fg=dark_fg, insertbackground="#ffffff")

            self.header.configure(bg=dark_accent)
            self.title_label.configure(bg=dark_accent,fg="#faedcd")
            
            self.toggle_btn.config(text="☀ Dark Mode: ON",bg="#d4a373",fg="#111111")
            
            # Change all labels in the inner frame
            for widget in self.inner.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=dark_bg, fg=dark_fg)
            
            # Re-configure specific labels that have unique backgrounds/colors
            self.status_label.configure(bg=dark_accent, fg=dark_fg)
            self.title_label.configure(bg=dark_accent,fg="#faedcd") 
            
            self.is_dark=True
        else:
            # Light Mode Settings
            light_bg = "#faedcd"
            light_fg = "#3f2e2e"
            light_accent = "#FFCFEF" # Light Header
            light_status_bg = "#e9edc9"
            light_status_fg = "#6a994e"
            light_output_bg = "#e9edc9"
            light_output_fg = "#344e41"

            self.root.configure(bg="#f5f5dc")
            self.card.configure(bg=light_bg,highlightbackground="#a3b18a")
            self.inner.configure(bg=light_bg)
            self.status_label.configure(bg=light_status_bg,fg=light_status_fg)
            self.output_box.configure(bg=light_output_bg,fg=light_output_fg, insertbackground="#000000")
            self.input_box.configure(bg="#ffffff", fg="#000000", insertbackground="#000000")

            self.header.configure(bg=light_accent)
            self.title_label.configure(bg=light_accent,fg=light_fg)
            
            self.toggle_btn.config(text="🌙 Dark Mode: OFF",bg="#ffffff",fg=light_fg)
            
            # Change all labels in the inner frame
            for widget in self.inner.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=light_bg, fg=light_fg)
            
            # Re-configure specific labels that have unique backgrounds/colors
            self.status_label.configure(bg=light_status_bg,fg=light_status_fg)
            self.title_label.configure(bg=light_accent,fg=light_fg) 
            
            self.is_dark=False

    # --- Cipher Operations ---

    def get_valid_key(self):
        """Validates the shift key input."""
        try:
            key=int(self.key_var.get())
            if not 1<=key<=25:
                raise ValueError
            return key
        except:
            self.status_var.set("❌ Shift value must be between 1 and 25")
            return None

    def encrypt(self):
        """Encrypts the input text using the Caesar cipher."""
        key=self.get_valid_key()
        text=self.get_input_text()

        if not text:
            self.status_var.set("❌ Please type a message OR load a file!")
            return

        if key:
            # Call the core cipher logic in 'encrypt' mode
            result=caesar_cipher(text,key,"encrypt")
            
            self._set_output(result)
          
            self.status_var.set("🌸 Encoding Successful!")

    def decrypt(self):
        """Decrypts the input text using the Caesar cipher."""
        key=self.get_valid_key()
        text=self.get_input_text()

        if not text:
            self.status_var.set("❌ Please type a message OR load a file!")
            return

        if key:
            # Call the core cipher logic in 'decrypt' mode
            result=caesar_cipher(text,key,"decrypt")
            self._set_output(result)
            
            self.status_var.set("✅ Decoding Successful!")

    def brute_force_decrypt(self):
        """Attempts decryption with all possible 25 shifts (keys 1-25)."""
        text=self.get_input_text()

        if not text:
            self.status_var.set("❌ Please type a message OR load a file for cracking!")
            return
        
        # Header for the brute force output
        results="--- BRUTE FORCE ANALYSIS ---\n\n"
        
        # Iterate through all possible keys (1 to 25)
        for key in range(1,26):
            decrypted_text=caesar_cipher(text,key,"decrypt")
            
            results+=f"Shift {key:02}:\n{decrypted_text}\n\n---\n\n"
            
        self._set_output(results)

        self.status_var.set("🔨 Brute Force analysis complete! Results displayed in output box.")

    def copy_result(self):
        """Copies the content of the output box to the system clipboard."""
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
        """Clears all input/output fields and resets state variables."""
        self._set_input("")
        self._set_output("")
        self.key_var.set("")
        self.file_loaded=False
        self.loaded_text=""
        self.status_var.set("🧹 All Clean!")


# --- Main Execution Block ---
if __name__=="__main__":
    root=tk.Tk()
    app=CaesarCipherModern(root)
    root.mainloop()