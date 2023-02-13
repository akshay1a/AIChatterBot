import tkinter as tk
import webbrowser
import openai
import sys
import os

# Command to make an executable file in cmd
# pyinstaller --name ChatterBot --onefile --windowed --icon=chat.ico ChatterBot.py


# from openai import whisper
openai.api_key = ""


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def resp(pro):
    # Generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=pro,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Print the response
    return response["choices"][0]["text"]


## Define the prompt
# while True:
#     prompt = input("Enter your question!\n")
#
#     if prompt == "stop":
#         break
#     else:
#         print(resp(prompt))

input_text = ''
output_text = ''


def handle_input(event):
    global input_text
    global output_text
    input_text = text_widget.get("1.0", "end-1c")
    input_text = input_text.replace(output_text, "")
    output_text = f"{resp(input_text)} \n\n"


def display_text():
    text_widget.delete("1.0", "end")
    text_widget.insert("end", output_text)


def on_submit():
    global text_widget
    value = entry.get()
    popup.title("API Query!")
    label = tk.Label(popup, text="Enter your API Key to use ")
    label.pack(padx=10, pady=10)
    # Do something with the value
    popup.destroy()
    if value != '':
        openai.api_key = value
    text_widget.focus_set()


def open_link(event):
    link = "https://platform.openai.com/account/api-keys"
    webbrowser.open_new_tab(link)


root = tk.Tk()
root.title("CHATTER-BOT")
root.geometry("1200x700+{}+{}".format(
    int((root.winfo_screenwidth() - 200) / 8),
    int((root.winfo_screenheight() - 200) / 18)
))
root.wm_iconbitmap(resource_path("C://Users//Dell//PycharmProjects//app//chat.ico"))
root.configure(background="#2E67F8")

## Pop-Up window for getting another api Key
popup = tk.Toplevel(root)
popup.title("Get Your API Key!")
popup.geometry("400x200+500+200")
label = tk.Label(popup, text="Please provide us your API Key to get started with the Chatter-Bot!", pady=20)
label.pack()
entry = tk.Entry(popup)
entry.pack(pady=10)
submit_button = tk.Button(popup, text="Submit", command=on_submit)
submit_button.pack()
link = tk.Label(popup, text="Click here to login to OpenAI to access your own API Key!", foreground="blue",
                cursor="hand2")
link.pack(padx=10, pady=10)
link.bind("<Button-1>", open_link)
popup.focus_set()

frame = tk.Frame(root, bd=5, bg='#2E67F8')
frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=(40, 0))
text_widget = tk.Text(frame, wrap=tk.WORD, relief=tk.FLAT, padx=20, pady=20)
# text_widget.focus_set()
text_widget.pack(fill=tk.BOTH, expand=True)
text_widget.configure(font=("Verdana", 14, 'bold'), height=10)

text_widget.bind("<Return>", handle_input)

# button = tk.Button(root, text="Send Message!", font=("Verdana", 16, 'bold'), command=display_text, width=15, height=3,
#                    background='#2B2B2B', foreground='white')
button = tk.Button(root, bd=0, bg='#2E67F8', command=display_text)
img = tk.PhotoImage(file=resource_path("C://Users//Dell//PycharmProjects//app//send.png"))
button.config(image=img)
button.pack(pady=(20, 40))

copyrgt = tk.Label(root, text='Powered by ChatGPT! Developed By @ Akshay Arora!', font=("Verdana", 8, 'bold'), pady='6'
                   , anchor='center', background='#0B1838', foreground='white')
copyrgt.pack(side=tk.BOTTOM, fill=tk.X)
frame1 = tk.Frame(root, height=1, width=90, relief=tk.SUNKEN, background='white')
frame1.pack(side=tk.BOTTOM)
status_bar = tk.Label(root, text='Status Bar', font=("Verdana", 10, 'bold'), pady=8, anchor='center',
                      background='#0B1838', foreground='white')
status_bar.pack(side=tk.BOTTOM, fill=tk.BOTH, pady=0, padx=0)

text_changed = False


def changed(event):
    global text_changed
    if text_widget.edit_modified():
        text_changed = True
        words = len(text_widget.get(1.0, 'end-1c').split())
        characters = len(text_widget.get(1.0, 'end-1c'))
        status_bar.config(text=f'Status:\tCharacters : {characters} Words : {words}')
        frame1.config(width=300)
    text_widget.edit_modified(False)


text_widget.bind('<<Modified>>', changed)
root.bind("<Return>", lambda event: button.invoke())

root.mainloop()
