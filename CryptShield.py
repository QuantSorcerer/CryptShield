import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet
import os


file_extension=".txt"
def open_file():
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[ ("All files", "*.*")])
    if file_path:
        with open(file_path, 'rb') as file:
            content = file.read()
            text_widget.delete(1.0, tk.END)  # Clear previous content
            text_widget.insert(tk.END, content)
        file_extension = os.path.splitext(file_path)[1]
        print(file_extension)

def encrypt():
    content = text_widget.get(1.0, tk.END)
    '''
    num=content.count("\n")
    for i in range(num):
        content=content.replace('\n', '')
        '''
    n=2
    List_keys=[]
    for i in range(n):
        List_keys.append(Fernet.generate_key())


    step=content
    step=bytes(step, 'utf-8')
    for i in range(n):
        fernet=Fernet(List_keys[i])
        step=fernet.encrypt(step)
        step=step.decode('utf-8')
        step=step+List_keys[i].decode('utf-8')
            #Shuffle
        step=step[(n//2):]+step[0:(n//2)]
        step=step[::-1]
        step=step[(2*n)//3:]+step[:(2*n)//3]
        step=step[n//3:]+step[:n//3]
        step=step[(n//2):]+step[0:(n//2)]
        step=bytes(step, 'utf-8')
    save_path = filedialog.asksaveasfilename(defaultextension=file_extension, filetypes=[("All files", "*.*")])
    if save_path:
        with open(save_path, 'wb') as file:
            file.write(step)



def decrypt():
    content = text_widget.get(1.0, tk.END)
    print(content)
    num=content.count("\n")
    for i in range(num):
        content=content.replace('\n', '')
        
    n=2
    step=content 
    
    for i in range(n):
        #Unshuffle
        step=step[(n//2)+1:]+step[0:(n//2)+1]
        step=step[::-1]
        step=step[((2*n)//3):]+step[:((2*n)//3)]
        step=step[n//3:]+step[:n//3]
        step=step[(n//2)+1:]+step[0:(n//2)+1]
        
        thekey=step[-44:]
        step=step[:-44]
      
        
        
        fernet=Fernet(thekey)
        step=fernet.decrypt(step)
    

        
    save_path = filedialog.asksaveasfilename(defaultextension=file_extension, filetypes=[("All files", "*.*")])
    if save_path:
        with open(save_path, 'wb') as file:
            file.write(step)



# Create the main window
root = tk.Tk()
root.title("CryptShield")

# Create a Text widget to display the file contents
text_widget = tk.Text(root, wrap="word",width=200, height=40)
text_widget.pack(padx=5, pady=5)

# Create an "Open File" button
open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack(padx=5,pady=5)

# Create a "Encrypt" button
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt)
encrypt_button.pack(side=tk.LEFT,padx=400,pady=5)

# Create a "Decrypt" button
decrypt_button = tk.Button(root, text="Decrypt", command=decrypt)
decrypt_button.pack(side=tk.LEFT, padx=1,pady=5)

# Run the Tkinter event loop
root.mainloop()


