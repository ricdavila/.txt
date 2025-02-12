import os

from customtkinter import *

PREFERENCES = {
    "wrap text": True,
    "display actual font": True,
    "display actual file": True,
    "show word count": True,
    "show character count": True,
    "view font size": False,
    "view margin size": False
}

CONFIG = {
    "theme": "light",
    "font": "Consolas",
    "default_font": "Consolas",
    "font_size": 16,
    "margin": 10
}

COLOR_CONFIG = {
    "main_color": "white",
    "text_color": "black",
    "secondary_text_color": "gray",
    "button_color": "#d1d1d1",
    "button_hover": "#e3e2e1",
    "button_text": "#424242" 
}

class MainApp(CTk):
    """Main application class"""

    def __init__(self):
        super().__init__()

        # configure main window
        self.window_height = 450
        self.window_width = 800
        self.spawn_x = int((self.winfo_screenwidth() - self.window_width)/2)
        self.spawn_y = int((self.winfo_screenheight() - self.window_height)/2)
        self.title(".txt")
        #self.geometry("800x450")
        self.geometry(f"{self.window_width}x{self.window_height}+{self.spawn_x}+{self.spawn_y}")
        self.minsize(200, 80)
        self.configure(fg_color="white")
        set_appearance_mode(CONFIG["theme"])

        # bind "ESC" to quit 
        #self.bind("<Escape>", lambda event: self.quit())
        
        # FILE MANAGEMENT VARIABLES
        self.actual_file = None
        self.last_saved_text = ""

        # create the widgets and shortcuts
        self.create_text_editor()
        self.create_bottom_bar()
        self.bind_shortcuts()

        # active popup var
        self.active_popup = None

        # manage the preferences window
        self.preferences_window = None

    def create_text_editor(self):
        """Create the text editor"""

        # create the text editor frame
        self.text_frame = CTkFrame(self, corner_radius=0, fg_color="white")
        self.text_frame.pack(expand=True, fill="both")
        # create the text editor
        self.text_editor = CTkTextbox(
            self.text_frame, font=(CONFIG["font"], CONFIG["font_size"]), 
            corner_radius=0, fg_color="white", text_color="#4a4a4a", 
            undo=True, wrap="word", scrollbar_button_color=COLOR_CONFIG["button_color"],
        )

        self.text_editor.pack(expand=True, fill="both", padx=CONFIG["margin"], pady=25)

        # bind key pressing to verify text changes
        self.text_editor.bind("<KeyRelease>", self.text_changed)

    def create_bottom_bar(self, which_widgets="all"):
        """Create the bottom bar widgets"""
        
        if which_widgets == "all":
            self.bottom_frame = CTkFrame(self, height=40, corner_radius=0, bg_color=COLOR_CONFIG["main_color"], fg_color=COLOR_CONFIG["main_color"])
            self.bottom_frame.pack(fill="x", padx=20)

            self.bottom_frame.columnconfigure((1, 2, 3, 4, 5), weight=0)
            self.bottom_frame.columnconfigure(0, weight=13)

        ### REFACTOR THIS !!! ###

        if which_widgets == "title" or which_widgets == "all":

            if self.actual_file:
                text = self.text_editor.get("1.0", "end-1c")
                self.title_label = CTkLabel(self.bottom_frame, font=(CONFIG["default_font"], 13), text_color=COLOR_CONFIG["secondary_text_color"], text=os.path.basename(self.actual_file) + (" *" if text != self.last_saved_text else "") if self.actual_file else "Untitled")
                #self.title_label.configure(text=os.path.basename(self.actual_file) + (" *" if text != self.last_saved_text else ""))
            else:
                self.title_label = CTkLabel(self.bottom_frame, font=(CONFIG["default_font"], 13), text_color=COLOR_CONFIG["secondary_text_color"], text="Untitled")
            self.title_label.grid(row=0, column=0, sticky="w")
        if which_widgets == "chars" or which_widgets == "all":
            self.chars_label = CTkLabel(self.bottom_frame, font=(CONFIG["default_font"], 13), text_color=COLOR_CONFIG["secondary_text_color"], text=f"C: {len(self.text_editor.get("1.0", "end-1c"))}")
            self.chars_label.grid(row=0, column=5, sticky="e", ipadx=20)
        if which_widgets == "word_count" or which_widgets == "all":
            self.word_count_label = CTkLabel(self.bottom_frame, font=(CONFIG["default_font"], 13), text_color=COLOR_CONFIG["secondary_text_color"], text=f"W: {len(self.text_editor.get("1.0", "end-1c").split())}")
            self.word_count_label.grid(row=0, column=4, sticky="e", ipadx=20)
        if which_widgets == "margin":
            self.margin_label = CTkLabel(self.bottom_frame, font=(CONFIG["default_font"], 13), text_color=COLOR_CONFIG["secondary_text_color"], text=f"M: {CONFIG["margin"]}")
            self.margin_label.grid(row=0, column=1, sticky="e", ipadx=20)
        if which_widgets == "font_size":
            self.font_size_label = CTkLabel(self.bottom_frame, font=(CONFIG["default_font"], 13), text_color=COLOR_CONFIG["secondary_text_color"], text=f"FS: {CONFIG["font_size"]}")
            self.font_size_label.grid(row=0, column=2, sticky="e", ipadx=20)
        if which_widgets == "actual_font" or which_widgets == "all":
            self.actual_font_label = CTkLabel(self.bottom_frame, font=(CONFIG["default_font"], 13), text_color=COLOR_CONFIG["secondary_text_color"], text=CONFIG["font"])
            self.actual_font_label.grid(row=0, column=3, sticky="e", ipadx=20)
        
    def bind_shortcuts(self):
        """Bind keyboard shortcuts to corresponding functions"""

        shortcuts = {
            "<Control-n>": self.new_file,
            "<Control-o>": self.open_file,
            "<Control-s>": self.save_file,
            "<Control-Shift-S>": self.save_as_file,
            "<Control-.>": self.increase_font,
            "<Control-,>": self.decrease_font,
            "<Control-=>": self.increase_margin,
            "<Control-minus>": self.decrease_margin,
            "<Control-d>": self.toggle_theme,
            "<Control-f>": self.next_font,
            "<F1>": self.show_preferences
        }

        # bind each key and fucntion in the dictionary
        for key, func in shortcuts.items():
            self.text_editor.bind(key, func)

    def text_changed(self, event=None):
        """Updates the character count"""

        # grab the actual text
        text = self.text_editor.get("1.0", "end-1c")
        # get the chars and word count and updates the labels
        if self.chars_label:
            self.chars_label.configure(text=f"C: {len(text)}")
        if self.word_count_label:
            self.word_count_label.configure(text=f"W: {len(text.split())}")

        # if the text is NOT equal to the last saved one, adds the * in the file name
        if self.title_label:
            if self.actual_file:
                self.title_label.configure(text=os.path.basename(self.actual_file) + (" *" if text != self.last_saved_text else ""))
            else:
                self.title_label.configure(text="Untitled")

    # FILE MANAGEMENT

    def new_file(self, event=None):
        """Clear the editor to create a new file"""

        self.actual_file = None
        self.text_editor.delete("1.0", END)
        self.last_saved_text = ""
        self.title_label.configure(text="Untitled")
    
    def open_file(self, event=None):
        """Open a file"""

        # show open file dialog
        file_path = filedialog.askopenfilename(title="Open File", filetypes=(("All Files", "*.*"), ("Text Files", "*.txt")))
        # if a file was selected, sets it as the actual
        if file_path:
            try:
                # open the selected file, read the content and paste it on the editor
                with open(file_path, "r") as file:
                    content = file.read()
                    # erase previous text
                    self.text_editor.delete("1.0", END)
                    # inserts the opened file's text
                    self.text_editor.insert(END, content)
                    # set the opened text as saved
                    self.last_saved_text = content
                # set the file path as the actual file
                self.actual_file = file_path
                # update labels
                self.text_changed()
            # if not able to open the file, shows a popup
            except Exception as e:
                 self.create_popup("Error: Unable to open the file.", True)

        # prevents other default methods bound to the ctrl+o shortcut from being executed
        return "break"

    def save_file(self, event=None):
        """Save the file in the stored path"""

        # if there's a path for the file, saves in it
        if self.actual_file:
            with open(self.actual_file, "w") as file:
                file.write(self.text_editor.get("1.0", "end-1c"))
            # set as saved this new text
            self.last_saved_text = self.text_editor.get("1.0", "end-1c")
            self.text_changed()
        # if there's no path, grabs it in the save as file function
        else:
            self.save_as_file()

    def save_as_file(self, event=None):
        """Opens a file dialog to grab a path to save the file"""

        # grab file name and path to save
        file_path = filedialog.asksaveasfilename(title="Save File", defaultextension=".*", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))

        if file_path:
            # stores the new path
            self.actual_file = file_path
            self.save_file()

    # PREFERENCES
    
    def increase_font(self, event=None):
        """Increase font size"""

        CONFIG["font_size"] += 2
        self.text_editor.configure(font=(CONFIG["font"], CONFIG["font_size"]))

        try:
            if self.font_size_label:
                self.font_size_label.configure(text=f"FS: {CONFIG["font_size"]}")
        except:
            pass
    
    def decrease_font(self, event=None):
        """Decrease font size"""

        if CONFIG["font_size"] > 10:
            CONFIG["font_size"] -= 2
            self.text_editor.configure(font=(CONFIG["font"], CONFIG["font_size"]))
            try:
                if self.font_size_label:
                    self.font_size_label.configure(text=f"FS: {CONFIG["font_size"]}")
            except:
                pass
        
    def next_font(self, event=None):
        """Switch to next font"""
        
        # fonts avaible
        fonts = ["Consolas", "Inconsolata", "Garamond", "Arial", "Times"]
        # gets the ACTUAL font index and adds 1 to ti (and, if the new index is BIGGER than the actual number of fonts, sets it to 0)
        index = (fonts.index(CONFIG["font"]) + 1) % len(fonts)
        # set the font with the new index as the actual font
        CONFIG["font"] = fonts[index]
        # update the text editor
        self.text_editor.configure(font=(CONFIG["font"], CONFIG["font_size"]))
        # update the label 
        try:
            if self.actual_font_label:
                self.actual_font_label.configure(text=CONFIG["font"])
        except:
            pass
        
    def toggle_theme(self, event=None):
        """Toggle the actual app theme"""

        global COLOR_CONFIG

        CONFIG["theme"] = "dark" if CONFIG["theme"] == "light" else "light"
        
        if CONFIG["theme"] == "light":
            COLOR_CONFIG = {
            "main_color": "white",
            "text_color": "black",
            "secondary_text_color": "gray",
            "button_color": "#d1d1d1",
            "button_hover": "#e3e2e1",
            "button_text": "#424242" 
            }
        else:
            COLOR_CONFIG = {
            "main_color": "black",
            "text_color": "#bdbdbd",
            "secondary_text_color": "gray",
            "button_color": "gray",
            "button_hover": "light gray",
            "button_text": "black" 
            }   

        set_appearance_mode(CONFIG["theme"])
        self.update_widgets_color()

        # prevents other default methods bound to the ctrl+d shortcut from being executed
        return "break"
    
    def update_widgets_color(self):
        """Update the colors of the displayed widgets"""

        self.configure(fg_color=COLOR_CONFIG["main_color"])
        self.text_frame.configure(fg_color=COLOR_CONFIG["main_color"])

        self.text_editor.configure(fg_color=COLOR_CONFIG["main_color"], text_color=COLOR_CONFIG["text_color"], scrollbar_button_color=COLOR_CONFIG["button_color"])

        self.bottom_frame.configure(fg_color=COLOR_CONFIG["main_color"])

        # if there's an active popup, update its colors too
        if self.active_popup:
            # update the main frame of the popup
            self.active_popup.configure(fg_color=COLOR_CONFIG["main_color"])
            # update the colors of the label
            self.active_popup.label.configure(bg_color=COLOR_CONFIG["main_color"], text_color=COLOR_CONFIG["text_color"])
            # update the button colors
            self.active_popup.button.configure(
                bg_color=COLOR_CONFIG["main_color"], 
                fg_color=COLOR_CONFIG["button_color"], 
                hover_color=COLOR_CONFIG["button_hover"], 
                text_color=COLOR_CONFIG["button_text"]
                )
        
        if self.preferences_window:
            
            self.preferences_window.configure(fg_color=COLOR_CONFIG["main_color"])

            self.preferences_window.main_frame.configure(fg_color=COLOR_CONFIG["main_color"])
            self.preferences_window.side_frame.configure(fg_color=COLOR_CONFIG["main_color"])

            self.preferences_window.page_selector.configure(fg_color=COLOR_CONFIG["main_color"])
            self.preferences_window.page_selector.tab_title.configure(fg_color=COLOR_CONFIG["main_color"], bg_color=COLOR_CONFIG["main_color"], text_color=COLOR_CONFIG["secondary_text_color"])
            self.preferences_window.page_selector.settings_button.configure(fg_color=COLOR_CONFIG["main_color"], bg_color=COLOR_CONFIG["main_color"], text_color=COLOR_CONFIG["secondary_text_color"], text_color_disabled=COLOR_CONFIG["text_color"])
            self.preferences_window.page_selector.shortcuts_button.configure(fg_color=COLOR_CONFIG["main_color"], bg_color=COLOR_CONFIG["main_color"], text_color=COLOR_CONFIG["secondary_text_color"], text_color_disabled=COLOR_CONFIG["text_color"])
            
            if self.preferences_window.actual_page.__class__ == self.preferences_window.SettingsPage:
                
                self.preferences_window.actual_page.configure(fg_color=COLOR_CONFIG["main_color"])

                self.preferences_window.actual_page.title_label.configure(fg_color=COLOR_CONFIG["main_color"], text_color=COLOR_CONFIG["text_color"], bg_color=COLOR_CONFIG["main_color"])
                self.preferences_window.actual_page.separator.configure(fg_color=COLOR_CONFIG["main_color"], text_color=COLOR_CONFIG["secondary_text_color"], bg_color=COLOR_CONFIG["main_color"])
                self.preferences_window.actual_page.options_frame.configure(bg_color=COLOR_CONFIG["main_color"], fg_color=COLOR_CONFIG["main_color"])

                for button in self.preferences_window.actual_page.buttons_dictionary:
                    button.configure(fg_color=COLOR_CONFIG["text_color"], text_color=COLOR_CONFIG["text_color"], bg_color=COLOR_CONFIG["main_color"], checkmark_color=COLOR_CONFIG["main_color"], hover_color=COLOR_CONFIG["secondary_text_color"], border_color=COLOR_CONFIG["secondary_text_color"])
                
                self.preferences_window.actual_page.close_button.configure(fg_color=COLOR_CONFIG["button_color"], bg_color=COLOR_CONFIG["main_color"], hover_color=COLOR_CONFIG["button_hover"], text_color=COLOR_CONFIG["button_text"])

            if self.preferences_window.actual_page.__class__ == self.preferences_window.ShortcutsPage:
                
                self.preferences_window.actual_page.configure(fg_color=COLOR_CONFIG["main_color"])

                self.preferences_window.actual_page.title_label.configure(fg_color=COLOR_CONFIG["main_color"], text_color=COLOR_CONFIG["text_color"], bg_color=COLOR_CONFIG["main_color"])
                self.preferences_window.actual_page.separator.configure(fg_color=COLOR_CONFIG["main_color"], text_color=COLOR_CONFIG["secondary_text_color"], bg_color=COLOR_CONFIG["main_color"])

                self.preferences_window.actual_page.shortcuts_frame.configure(fg_color=COLOR_CONFIG["main_color"])

                for (key, desc) in self.preferences_window.actual_page.labels_dictionary:
                    key.configure(bg_color=COLOR_CONFIG["main_color"], fg_color=COLOR_CONFIG["main_color"], text_color=COLOR_CONFIG["text_color"])
                    desc.configure(bg_color=COLOR_CONFIG["main_color"], fg_color=COLOR_CONFIG["main_color"], text_color=COLOR_CONFIG["secondary_text_color"])

                self.preferences_window.actual_page.close_button.configure(fg_color=COLOR_CONFIG["button_color"], bg_color=COLOR_CONFIG["main_color"], hover_color=COLOR_CONFIG["button_hover"], text_color=COLOR_CONFIG["button_text"])

    def increase_margin(self, event=None):
        """Increase the lateral margin"""

        CONFIG["margin"] += 10
        self.text_editor.configure(padx=CONFIG["margin"])
        try:
            if self.margin_label:
                self.margin_label.configure(text=f"M: {CONFIG["margin"]}")
        except:
            pass
    
    def decrease_margin(self, event=None):
        """Decrease the lateral margin"""

        if CONFIG["margin"] > 10:
            CONFIG["margin"] -= 10
            self.text_editor.configure(padx=CONFIG["margin"])
        try:
            if self.margin_label:
                self.margin_label.configure(text=f"M: {CONFIG["margin"]}")
        except:
            pass
    
    def update_preferences(self):
        
        ### REFACTOR THIS (URGENT!!!) ###

        # wrap text
        if PREFERENCES["wrap text"]:
            self.text_editor.configure(wrap="word")    
        else:
            self.text_editor.configure(wrap="none")
        
        # actual font
        if self.actual_font_label and not PREFERENCES["display actual font"]:
            self.actual_font_label.destroy()
            self.actual_font_label = None
        elif not self.actual_font_label and PREFERENCES["display actual font"]:
            self.create_bottom_bar("actual_font")
        
        # actual file
        if self.title_label and not PREFERENCES["display actual file"]:
            self.title_label.destroy()
            self.title_label = None
        elif not self.title_label and PREFERENCES["display actual file"]:
            self.create_bottom_bar("title")
        
        # char count
        if self.chars_label and not PREFERENCES["show character count"]:
            self.chars_label.destroy()
            self.chars_label = None
        elif not self.chars_label and PREFERENCES["show character count"]:
            self.create_bottom_bar("chars")
        
        # word count
        if self.word_count_label and not PREFERENCES["show word count"]:
            self.word_count_label.destroy()
            self.word_count_label = None
            self.bottom_frame.columnconfigure(4, weight=0)
        elif not self.word_count_label and PREFERENCES["show word count"]:
            self.create_bottom_bar("word_count")
        
        # font size
        try:
            if self.font_size_label and not PREFERENCES["view font size"]:
                self.font_size_label.destroy()
                self.font_size_label = None
            elif not self.font_size_label and PREFERENCES["view font size"]:
                self.create_bottom_bar("font_size")
        except:
            self.create_bottom_bar("font_size")
            
        # margin size
        try:
            if self.margin_label and not PREFERENCES["view margin size"]:
                self.margin_label.destroy()
                self.margin_label = None
            elif not self.margin_label and PREFERENCES["view margin size"]:
                self.create_bottom_bar("margin")
        except:
            self.create_bottom_bar("margin")

    # POPUPS AND WINDOWS MANAGEMENT

    def show_preferences(self, event=None):

        if not self.preferences_window:
            self.preferences_window = Preferences()

    def create_popup(self, message, only_ok_button):
        """Create popups"""

        if self.active_popup:
            self.destroy_popup()
        
        self.active_popup = Popup(message, only_ok_button)

    def destroy_popup(self):
        """Destroy popups when its exit buttons are pressed"""
        
        self.active_popup.destroy()
        self.active_popup = None

# SECUNDARY WIDGET CLASSES

class Preferences(CTkToplevel):
    """Preferences and setttings window"""

    def __init__(self):
        super().__init__(master=app)

        # initial attributes
        self.title(" ")
        self.configure(fg_color=COLOR_CONFIG["main_color"])
        self.resizable(width=False, height=FALSE)
        self.attributes("-topmost", True)
        #self.geometry("600x450")
        self.spawn_x = int((self.winfo_screenwidth() - 600)/2)
        self.spawn_y = int((self.winfo_screenheight() - 500)/2)
        self.geometry(f"600x500+{self.spawn_x}+{self.spawn_y}")
        
        self.actual_page = None
    
        self.create_widgets()

        # handler exit button 
        self.protocol("WM_DELETE_WINDOW", self.close_preferences)
        self.bind("<Escape>", lambda event: self.close_preferences())
        self.bind("<Control-d>", lambda event: self.master.toggle_theme())
    def create_widgets(self):
        """Create the window's widgets"""

        # configure the main grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=8)
        self.grid_rowconfigure(0, weight=1)

        # setup the main (right) frame
        self.main_frame = CTkFrame(self, fg_color=COLOR_CONFIG["main_color"], corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="NWES")
        # setup the side (left) frame
        self.side_frame = CTkFrame(self, fg_color=COLOR_CONFIG["main_color"], width=0, corner_radius=0)
        self.side_frame.grid(row=0, column=0, sticky="NWES")

        self.page_selector = self.PageSelector(self.side_frame)
        
    def toggle_page(self, page):

        if page == "settings":
            if self.actual_page:
                self.actual_page.destroy()
            self.actual_page = self.SettingsPage(self.main_frame)
            self.actual_page.pack(fill="both", expand=True, pady=5, padx=20)
    
        elif page == "shortcuts":
            if self.actual_page:
                self.actual_page.destroy()
            self.actual_page = self.ShortcutsPage(self.main_frame)
            self.actual_page.pack(fill="both", expand=True, pady=5, padx=20)
    
    def close_preferences(self):
        self.destroy()
        self.master.preferences_window = None

    class PageSelector(CTkFrame):
        """Create the buttons for selecting the pages"""

        def __init__(self, parent):
            super().__init__(master=parent)

            # initial configuration
            self.configure(fg_color=COLOR_CONFIG["main_color"])
            self.pack(fill="both", padx=20, expand=True)
            # the Preferences class window
            self.prefs_window = self.master.master
            # create the tab title
            self.tab_title = CTkLabel(
                self,
                text="Preferences",
                font=(CONFIG["default_font"], 14, "bold"),
                fg_color=COLOR_CONFIG["main_color"],
                bg_color=COLOR_CONFIG["main_color"],
                text_color=COLOR_CONFIG["secondary_text_color"],
                anchor="w"
            )
            self.tab_title.pack(fill="x", ipady=20)

            # create settings page button
            self.settings_button = CTkButton(self, text="> Settings", command=self.settings_page_pressed)
            # create the shortcuts page button
            self.shortcuts_button = CTkButton(self,text="> Shortcuts", command=self.shortcut_page_pressed)
            
            # configure the buttons styles
            buttons = [self.settings_button, self.shortcuts_button]

            for button in buttons:
                button.configure(
                corner_radius=0,
                font=(CONFIG["default_font"], 14),
                fg_color=COLOR_CONFIG["main_color"],
                bg_color=COLOR_CONFIG["main_color"],
                text_color=COLOR_CONFIG["secondary_text_color"],
                hover=False,
                text_color_disabled=COLOR_CONFIG["text_color"],
                anchor="w"
            )
                # pack every button
                button.pack(fill="x", pady=2)

            # bind the buttons to make the hover effect
            self.bind_hover()
            self.settings_page_pressed()
            
        def bind_hover(self, bind_settings=True, bind_shortcuts=True):
            """Manages the bindings for showing (or not) the hover effect"""

            # bind settings button
            if bind_settings:
                self.settings_button.bind("<Enter>", lambda e: self.settings_button.configure(
                    text=" > Settings"
                ))
                self.settings_button.bind("<Leave>", lambda e: self.settings_button.configure(
                    text="> Settings"
                ))
            # if the caller especify, unbinds the settings button (when the button is already selected)
            else:
                self.settings_button.unbind("<Enter>")
                self.settings_button.unbind("<Leave>")
            
            # bind shortcuts button
            if bind_shortcuts:
                self.shortcuts_button.bind("<Enter>", lambda e: self.shortcuts_button.configure(
                    text=" > Shortcuts"
                ))
                self.shortcuts_button.bind("<Leave>", lambda e: self.shortcuts_button.configure(
                    text="> Shortcuts"
                ))
            # if the caller especify, unbinds the shortcuts button (when the button is already selected)
            else:
                self.shortcuts_button.unbind("<Enter>")
                self.shortcuts_button.unbind("<Leave>")
                
        def settings_page_pressed(self):
            """Called when the settings page button is pressed"""       

            # change the settings button to bold and the shortcuts button to normal
            self.settings_button.configure(state="disabled", font=(CONFIG["default_font"], 14, "bold"), text="  > Settings")
            self.shortcuts_button.configure(state="normal", font=(CONFIG["default_font"], 14), text="> Shortcuts")
            # bind shortcuts button again and unbind settings button
            self.bind_hover(False, True)
            # grab the main menu window and toggle the page
            self.prefs_window.toggle_page("settings")

        def shortcut_page_pressed(self):
            """Called when the shortcuts page button is pressed"""

            # change the shortcuts button to bold and the settings button to normal
            self.shortcuts_button.configure(state="disabled", font=(CONFIG["default_font"], 14, "bold"), text="  > Shortcuts")
            self.settings_button.configure(state="normal", font=(CONFIG["default_font"], 14), text="> Settings")
            # bind the settings button again and unbind shortcuts button
            self.bind_hover(True, False)
            # grab the main menu window and toggle the page
            self.prefs_window.toggle_page("shortcuts")
        
    class SettingsPage(CTkFrame):
        """Create the settings page for the preferences window"""

        def __init__(self, parent):
            super().__init__(master=parent)

            self.configure(fg_color=COLOR_CONFIG["main_color"])
            # create the page title
            self.title_label = CTkLabel(
                self,
                text="Settings",
                font=(CONFIG["default_font"], 20, "bold"),
                fg_color=COLOR_CONFIG["main_color"], 
                text_color=COLOR_CONFIG["text_color"], 
                bg_color=COLOR_CONFIG["main_color"], 
                justify="left",
                anchor="w"
            )
            self.title_label.pack(fill="x")
            # create a title / content separator
            self.separator = CTkLabel(
                self,
                text="_______________________________________\n",
                font=(CONFIG["default_font"], 14),
                fg_color=COLOR_CONFIG["main_color"], 
                text_color=COLOR_CONFIG["secondary_text_color"], 
                bg_color=COLOR_CONFIG["main_color"], 
                justify="left",
                anchor="w"
            )
            self.separator.pack(fill="x")

            # content frame
            self.options_frame = CTkFrame(self, bg_color=COLOR_CONFIG["main_color"], fg_color=COLOR_CONFIG["main_color"])
            self.options_frame.pack(fill="both", expand=True)
            
            # store the created buttons for reference
            self.buttons_dictionary = []
            
            # create a button for each option in preferences dict
            for row_index, (text, value) in enumerate(PREFERENCES.items()):
                
                # create a new row for each option
                self.options_frame.rowconfigure(row_index, weight=1)

                button = CTkCheckBox(
                    self.options_frame,
                    text=text,
                    font=(CONFIG["default_font"], 14),
                    fg_color=COLOR_CONFIG["text_color"], 
                    text_color=COLOR_CONFIG["text_color"], 
                    bg_color=COLOR_CONFIG["main_color"],
                    checkmark_color=COLOR_CONFIG["main_color"],
                    corner_radius=0,
                    border_width=2,
                    checkbox_height=15,
                    checkbox_width=15,
                    hover_color=COLOR_CONFIG["secondary_text_color"],
                    border_color=COLOR_CONFIG["secondary_text_color"],
                    command= lambda: self.option_clicked()
                )
                button.pack(fill="x", anchor="w", pady=10, padx=10)
                # if the option is true in the preferences, check the box
                if value:
                    button.select()
                # append the last button to the dictionary
                self.buttons_dictionary.append(button)
                
            # creating close button
            self.close_button = CTkButton(
                self,
                text="Close",
                font=(CONFIG["font"], 14), 
                fg_color=COLOR_CONFIG["button_color"],
                hover_color=COLOR_CONFIG["button_hover"], 
                bg_color=COLOR_CONFIG["main_color"],
                text_color=COLOR_CONFIG["button_text"], 
                corner_radius=5,
                width=80,
                command= lambda: self.master.master.close_preferences()
            )
            self.close_button.pack(anchor="e", pady=10)
    

        def option_clicked(self, event=None):
            """Update the PREFERENCES each time a checkbox is clicked"""

            for button in self.buttons_dictionary:
                # grab the text of the button
                clicked_option = button.cget("text")
                # grab the value of te button (0 or 1)
                option_value = button.get()
                # update the global dictionary
                PREFERENCES[clicked_option] = bool(option_value)
                # make the changes a true thing
                app.update_preferences()
    
    class ShortcutsPage(CTkFrame):
        """Create the shortcuts page for the preferences window"""

        def __init__(self, parent):
            super().__init__(master=parent)

            self.configure(fg_color=COLOR_CONFIG["main_color"])
            # create the page title
            self.title_label = CTkLabel(
                self,
                text="Shortcuts",
                font=(CONFIG["default_font"], 20, "bold"),
                fg_color=COLOR_CONFIG["main_color"], 
                text_color=COLOR_CONFIG["text_color"], 
                bg_color=COLOR_CONFIG["main_color"], 
                justify="left",
                anchor="w"
            )
            self.title_label.pack(fill="x")
            # create a title / content separator
            self.separator = CTkLabel(
                self,
                text="_______________________________________\n",
                font=(CONFIG["default_font"], 14),
                fg_color=COLOR_CONFIG["main_color"], 
                text_color=COLOR_CONFIG["secondary_text_color"], 
                bg_color=COLOR_CONFIG["main_color"], 
                justify="left",
                anchor="w"
            )
            self.separator.pack(fill="x")

            # configure the shortcuts frame
            self.shortcuts_frame = CTkScrollableFrame(self, fg_color=COLOR_CONFIG["main_color"])
            self.shortcuts_frame.pack(expand=True, fill="both")
            # shortcut column
            self.shortcuts_frame.grid_columnconfigure(0, weight=1)
            # description column
            self.shortcuts_frame.grid_columnconfigure(1, weight=2)

            # dictionary of shortcuts
            shortcuts = {
                "ctrl n": "New file",
                "ctrl o": "Open file",
                "ctrl s": "Save file",
                "ctrl shift s": "Save as file",
                "ctrl =": "Increase margin",
                "ctrl -": "Decrease margin",
                "ctrl .": "Increase font size",
                "ctrl ,": "Decrease font size",
                "ctrl d": "Toggle theme",
                "F1": "Show preferences"
            }
            
            # store the labels for personalization needs
            self.labels_dictionary = []

            # for each key-desc, create a new row and its labels
            for row_index, (key, desc) in enumerate(shortcuts.items()):
                
                # configure a new row 
                self.shortcuts_frame.grid_rowconfigure(row_index, weight=1)

                # create the shortcut label
                key_label = CTkLabel(
                    self.shortcuts_frame, 
                    text=f"< {key} >", 
                    font=(CONFIG["default_font"], 14, "bold"), 
                    fg_color=COLOR_CONFIG["main_color"], 
                    text_color=COLOR_CONFIG["text_color"], 
                    bg_color=COLOR_CONFIG["main_color"], 
                    corner_radius=4,
                    anchor="w"
                    )

                key_label.grid(row=row_index, column=0, sticky="we", ipadx=10)

                # create the shortcut's description label
                description_label = CTkLabel(
                    self.shortcuts_frame, 
                    text=f"{desc}", 
                    font=(CONFIG["default_font"], 14), 
                    fg_color=COLOR_CONFIG["main_color"], 
                    text_color=COLOR_CONFIG["secondary_text_color"], 
                    bg_color=COLOR_CONFIG["main_color"], 
                    anchor="w"
                    )

                description_label.grid(row=row_index, column=1, sticky="we", pady=5)

                # add both labels to the dictionary
                self.labels_dictionary.append((key_label, description_label))
            
            #creating close button
            self.close_button = CTkButton(
                self,
                text="Close",
                font=(CONFIG["font"], 14), 
                fg_color=COLOR_CONFIG["button_color"],
                hover_color=COLOR_CONFIG["button_hover"], 
                bg_color=COLOR_CONFIG["main_color"],
                text_color=COLOR_CONFIG["button_text"], 
                corner_radius=5,
                width=80,
                command= lambda: self.master.master.close_preferences()
            )

            self.close_button.pack(anchor="e", pady=10)

class Popup(CTkToplevel):
    """Simple popups class"""

    def __init__(self, message, only_ok_button):
        super().__init__(master=app)

        # initial attributes
        self.title(" ")
        self.configure(fg_color=COLOR_CONFIG["main_color"])
        self.resizable(width=False, height=False)
        self.attributes("-topmost", True)
        self.spawn_x = int((self.winfo_screenwidth() - 300)/2)
        self.spawn_y = int((self.winfo_screenheight() - 100)/2)
        self.geometry(f"300x100+{self.spawn_x}+{self.spawn_y}")

        # label widget
        self.label = CTkLabel(
            self, 
            text=f"{message}",
            bg_color=COLOR_CONFIG["main_color"], 
            text_color=COLOR_CONFIG["text_color"], 
            font=(CONFIG["font"], 14), 
            wraplength=320
        )
        self.label.pack(padx=10, pady=15)
        
        # confirmation button
        if only_ok_button:
            self.button = CTkButton(
                self, 
                text="Ok",
                font=(CONFIG["font"], 14), 
                fg_color=COLOR_CONFIG["button_color"],
                hover_color=COLOR_CONFIG["button_hover"], 
                bg_color=COLOR_CONFIG["main_color"],
                text_color=COLOR_CONFIG["button_text"], 
                corner_radius=5,
                width=80,
                command=lambda: app.destroy_popup()
            )

            self.button.pack(anchor=CENTER)

# RUN APP


app = MainApp()
app.text_changed()
print()
#app.text_editor.focus_set()
app.mainloop()
