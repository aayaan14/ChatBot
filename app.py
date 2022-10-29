from tkinter import *
from chat import get_response, bot_name
import pyaudio
import pyttsx3
from multiprocessing.connection import Listener
import speech_recognition as sr

listener = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

 
BG_GRAY = "#F9D342"
BG_COLOR = "#292826"
TEXT_COLOR = "#EAECEE"
BG_BLUE = "#cedada"
 
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"
 
class ChatApplication:
 
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
 
    def run(self):
        self.window.mainloop()
 
    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=800, height=650, bg=BG_COLOR)
 
        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
 
        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
 
        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
 
        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
 
        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
 
        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
 
        # send button
        send_button = Button(bottom_label, text="Record", font=FONT_BOLD, width=20, bg=BG_BLUE,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
 
    def _on_enter_pressed(self, event):
        # msg = self.msg_entry.get()
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            voice = listener.listen(source)
            msg = listener.recognize_google(voice)
        self._insert_message(msg, "You")
 
    def _insert_message(self, msg, sender):
        if not msg:
            return
 
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
 
        msg2 = f"{bot_name}: {get_response(msg)}\n\n"
        msg2_voice = msg2[5:]
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        engine.say(msg2_voice)
        self.text_widget.configure(state=DISABLED)
        engine.runAndWait()
        self.text_widget.see(END)
 
 
if __name__ == "__main__":
    app = ChatApplication()
    app.run()