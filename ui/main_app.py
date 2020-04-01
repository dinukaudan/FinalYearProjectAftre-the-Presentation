import threading
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from analyzer.analyzer import Analyzer


########################################
# All the code for the UI & interactions
########################################
class MainApp(Tk):
    # analyzer is completely isolated from UI, check the '/analyzer' module
    analyzer = Analyzer()

    def __init__(self):
        super(MainApp, self).__init__()
        self.setup()
        self.top_frame = TopFrame(self)
        self.body_frame = BodyFrame(self)

    def setup(self):
        self.title('GitHub User Performance Analyzer')
        self.configure(bg='white')
        self.minsize(0, 500)
        self.resizable(0, 0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    @staticmethod
    def confirm(question, icon='question'):
        result = messagebox.askquestion("Confirmation", question, icon=icon)
        return result == 'yes'


class TopFrame(Frame):
    def __init__(self, parent):
        super(TopFrame, self).__init__(master=parent)
        self.setup()
        # banner
        self.banner_img = PhotoImage(file="./img/banner.png")
        self.banner = Label(self, image=self.banner_img, bg='white')
        self.banner.grid(row=0, column=0)

    def setup(self):
        self.configure(bg='white')
        self.grid(row=0, column=0, sticky='we')
        self.grid_columnconfigure(0, weight=1)


class BodyFrame(Frame):
    def __init__(self, parent):
        super(BodyFrame, self).__init__(master=parent)
        self.setup()
        self.list_frame = ListFrame(self)
        self.analyze_bar = AnalyzeBar(self, self.list_frame)
        self.list_frame.append('Analyzer initialized.')

    def setup(self):
        self.configure(bg='yellow')
        self.grid(row=1, column=0, sticky='news')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)


class AnalyzeBar(Frame):
    def __init__(self, parent, list_frame):
        super(AnalyzeBar, self).__init__(master=parent)
        self.list_frame = list_frame
        self.setup()
        self.analyze_label = Label(self, text="Enter GitHub username : ", bg=self['bg'])
        self.analyze_label.grid(row=0, column=0, sticky='e')
        self.username_ctrl = StringVar()
        self.username_entry = Entry(self, textvariable=self.username_ctrl)
        self.username_ctrl.set('githubanalyzeruser')
        self.username_entry.focus()
        self.username_entry.grid(row=0, column=1, sticky='we')
        self.clone_button = Button(self, text='Clone all', bg='white', padx=10, command=self.on_clone)
        self.clone_button.grid(row=0, column=2, sticky='we', padx=4)
        self.analyze_button = Button(self, text='Analyze', bg='white', padx=10, command=self.on_analyze)
        self.analyze_button.grid(row=0, column=3, sticky='w', padx=4)
        self.report_button = Button(self, text='Report', bg='white', padx=10, command=self.on_report)
        self.report_button.grid(row=0, column=4, sticky='w', padx=4)
        self.clear_button = Button(self, text='Clear', bg='red', fg='white', padx=10, command=self.on_clear)
        self.clear_button.grid(row=0, column=5, sticky='w', padx=4)

    def freeze(self):
        self.clone_button.configure(state=DISABLED)
        self.analyze_button.configure(state=DISABLED)
        self.report_button.configure(state=DISABLED)
        self.clear_button.configure(state=DISABLED)
        self.username_entry.configure(state=DISABLED)

    def unfreeze(self):
        self.clone_button.configure(state=NORMAL)
        self.analyze_button.configure(state=NORMAL)
        self.report_button.configure(state=NORMAL)
        self.clear_button.configure(state=NORMAL)
        self.username_entry.configure(state=NORMAL)

    def setup(self):
        self.configure(bg='white', padx=20, pady=20)
        self.grid(row=0, column=0, sticky='we')
        self.grid_columnconfigure(0, weight=100)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=100)

    def on_clone(self):
        username = self.username_ctrl.get()
        process_thread = threading.Thread(target=MainApp.analyzer.clone,
                                          args=(
                                              self.list_frame.append, self.list_frame.indicate, MainApp.confirm,
                                              username))
        process_thread.start()

    def on_analyze(self):
        process_thread = threading.Thread(target=MainApp.analyzer.analyze,
                                          args=(self.list_frame.append, self.list_frame.indicate))
        process_thread.start()

    def on_report(self):
        # Removed threading for report generation because threads caused prediction problems
        # process_thread = threading.Thread(target=MainApp.analyzer.report,
        #                                   args=(self.list_frame.append, self.list_frame.indicate,
        #                                         MainApp.analyzer.get_user_expertise))
        # process_thread.start()
        MainApp.analyzer.report(self.list_frame.append, self.list_frame.indicate,
                                MainApp.analyzer.get_user_expertise)

    def on_clear(self):
        self.list_frame.clear()


class ListFrame(Frame):

    def __init__(self, parent):
        super(ListFrame, self).__init__(master=parent)
        self.LEADING = ''
        self.setup()
        self.analyze_bar = AnalyzeBar(self, self)
        # report text
        self.report_text = ScrolledText(self, bg='white', relief=GROOVE, font='TkFixedFont')
        self.report_text.grid(row=0, column=0, sticky='news')
        # status bar
        self.status_bar = StatusBar(self)

    def setup(self):
        self.grid(row=1, column=0, sticky='wens')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def append(self, string):
        self.report_text.insert(END, self.LEADING + string + '\n')
        self.report_text.see(END)

    def indicate(self, string, freeze):
        self.status_bar.set_text(string)
        if freeze:
            self.master.analyze_bar.freeze()
        else:
            self.master.analyze_bar.unfreeze()

    def clear(self):
        self.status_bar.set_text('Ready')
        self.report_text.delete('1.0', END)


class StatusBar(Frame):
    def __init__(self, parent):
        super(StatusBar, self).__init__(master=parent)
        self.setup()
        # status text
        self.status_label = Label(self, text="Ready", bg=self['bg'], fg='white', font=('bold', 14))
        self.status_label.grid(row=0, column=0, sticky='news', pady=5)

    def setup(self):
        self.configure(bg='#4CAF50')
        self.grid(row=1, column=0, sticky='news')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def set_text(self, string):
        self.status_label.configure(text=string)
