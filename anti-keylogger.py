import tkinter as tk
from cryptography.fernet import Fernet, InvalidToken

class EncryptedKeyboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encrypted Keyboard")
        self.root.geometry("600x300")  # Adjusted window size
        
        self.key_path = "encryption_key.key"
        self.load_or_generate_key()
        
        self.text_var = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.text_var, width=50)
        self.entry.pack(pady=10)
       
        self.buttons = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M'
        ]

        self.encrypted_history = []  # Maintain a list of encrypted characters
        self.create_keyboard()
        
        # Real-time Decrypted Text Display
        self.decrypted_text_var = tk.StringVar()
        self.decrypted_text_label = tk.Label(root, textvariable=self.decrypted_text_var, font=("Helvetica", 16), justify="right")
        self.decrypted_text_label.pack()
        
    def create_keyboard(self):
        button_frame = tk.Frame(self.root)
        
        for button_text in self.buttons:
            button = tk.Button(button_frame, text=button_text, command=lambda t=button_text: self.on_button_click(t))
            button.grid(row=self.buttons.index(button_text) // 10, column=self.buttons.index(button_text) % 10)
        
        # Create a new frame for the space bar and backspace buttons
        space_backspace_frame = tk.Frame(self.root)
        
        # Add Space Bar
        space_bar = tk.Button(space_backspace_frame, text="Space", command=lambda: self.on_button_click(' '))
        space_bar.grid(row=0, column=0, columnspan=5)
        
        # Add Backspace
        backspace = tk.Button(space_backspace_frame, text="Backspace", command=self.on_backspace_click)
        backspace.grid(row=0, column=5, columnspan=5)
        
        button_frame.pack()
        space_backspace_frame.pack()

    def on_button_click(self, char):
        encrypted_char = self.fernet.encrypt(char.encode()).decode()
        self.encrypted_history.append(encrypted_char)
        current_text = ''.join(self.encrypted_history)
        self.text_var.set(current_text)
        self.entry.icursor("end")
        
        # Decrypt and update the real-time display
        self.update_decrypted_text()

    def on_backspace_click(self):
        if self.encrypted_history:
            self.encrypted_history.pop()
            current_text = ''.join(self.encrypted_history)
            self.text_var.set(current_text)
            self.entry.icursor("end")
            
            # Decrypt and update the real-time display
            self.update_decrypted_text()

    def load_or_generate_key(self):
        try:
            with open(self.key_path, "rb") as key_file:
                key = key_file.read()
                self.fernet = Fernet(key)
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as key_file:
                key_file.write(key)
            self.fernet = Fernet(key)

    def update_decrypted_text(self):
        decrypted_text = "Real-time decrypting text (LIVE):  "
        for encrypted_char in self.encrypted_history:
            try:
                decrypted_char = self.fernet.decrypt(encrypted_char.encode()).decode()
                decrypted_text += decrypted_char
            except InvalidToken:
                self.text_var.set("ERROR")
                return
        self.decrypted_text_var.set(decrypted_text)

def main():
    root = tk.Tk()
    app = EncryptedKeyboardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
