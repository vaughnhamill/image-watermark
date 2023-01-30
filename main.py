import tkinter
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from PIL import Image, ImageTk, ImageDraw, ImageFont


class App(Tk):
    def __init__(self):
        super().__init__()
        # Initialize watermark window, frames and variables
        self.title("Image Watermarker")
        self.geometry('1300x1000')
        self.resizable(width=True, height=True)
        self.top_frame = ttk.Frame(self)
        self.top_frame.grid(column=0, row=0)
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.grid(column=0, row=1)
        self.f_types = [("Jpg Files", "*.jpg"), ("Jpeg Files", "*.jpeg"), ("Png Files", "*.png")]
        self.positions = ["Top Left", "Top Center", "Top Right", "Middle Left", "Middle Center", "Middle Right", "Bottom Left", "Bottom Center", "Bottom Right"]

        # Initialize buttons
        import_btn = ttk.Button(self.top_frame, text="Import File", command=self.filename)
        import_btn.grid(column=0, row=0)
        watermark_btn = ttk.Button(self.top_frame, text="Create Watermark", command=self.watermark_win)
        watermark_btn.grid(column=1, row=0)
        save_as_btn = ttk.Button(self.top_frame, text="Save As", command=self.save)
        save_as_btn.grid(column=2, row=0)
        self.img_label = ttk.Label(self.bottom_frame)
        self.img_label.grid(column=0, row=0)

    # Retrieve filename
    def filename(self):
        self.filename = fd.askopenfilename(filetypes=self.f_types)
        self.open_img()

    # Open image and show on root level. Returns Image type
    def open_img(self):
        self.basewidth = 1000
        try:
            img = Image.open(self.filename)
        except AttributeError:
            tkinter.messagebox.showinfo("Import Error", "Please import an image first.")

        wpercent = (self.basewidth / float(img.size[0]))
        self.hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((self.basewidth, self.hsize), Image.LANCZOS)
        imgpi = ImageTk.PhotoImage(img)
        self.img_label.config(image=imgpi)
        self.img_label.image = imgpi
        return img

    # Save Image type to .png and ask new filename
    def save(self):
        new_filename = fd.asksaveasfilename()
        self.img.save(new_filename+".png", "png", quality=99)

    # Open and initialize watermarker window
    def watermark_win(self):
        self.root2 = Toplevel(self)
        self.root2.title("Watermarks")
        self.root2.geometry('400x250')
        self.create_wm()

    # Create buttons with variables for watermarker information
    def create_wm(self):
        l1 = ttk.Label(self.root2, text="Watermark text")
        l1.pack()
        self.entry = ttk.Entry(self.root2)
        self.entry.pack()

        l2 = ttk.Label(self.root2, text="Color of watermark. Use Hex codes or 'red', 'blue', 'green', etc.")
        l2.pack()
        self.color = ttk.Entry(self.root2)
        self.color.pack()

        l3 = ttk.Label(self.root2, text="Font style")
        l3.pack()
        self.font_type = ttk.Entry(self.root2)
        self.font_type.pack()

        l3 = ttk.Label(self.root2, text="Font size")
        l3.pack()
        self.font_size = ttk.Entry(self.root2)
        self.font_size.pack()

        l4 = ttk.Label(self.root2, text="Watermark Location")
        l4.pack()
        self.pos_variable = StringVar(self.root2)
        self.pos_variable.set(self.positions[0])
        self.wm_opt = ttk.OptionMenu(self.root2, self.pos_variable, *self.positions)
        self.wm_opt.pack()

        enter = Button(self.root2, text="Enter", command=self.add_wm)
        enter.pack(side=BOTTOM)

    # Add watermark to image and destroy if inputted values are good
    def add_wm(self):
        self.img = self.open_img()
        wm_img = ImageDraw.Draw(self.img)
        try:
            font = ImageFont.truetype(f"{self.font_type.get()}.ttf", int(self.font_size.get()))
            xy = self.wm_location()
            wm_img.text(xy=(xy[0], xy[1]),
                        text=self.entry.get(),
                        fill=self.color.get(),
                        font=font
                        )
            good_values = True
        except ValueError:
            tkinter.messagebox.showinfo("Value Error", "Please try another color and/or font size.", parent=self.root2)
        except OSError:
            tkinter.messagebox.showinfo("Font Error", "Please try another font type.", parent=self.root2)

        if good_values:
            self.img = self.img.resize((self.basewidth, self.hsize), Image.LANCZOS)
            imgpi = ImageTk.PhotoImage(self.img)
            self.img_label.config(image=imgpi)
            self.img_label.image = imgpi
            self.img_label.grid(column=0, row=0)
            self.root2.destroy()

    # Position watermark on image based on input
    def wm_location(self):
        wm_loc = self.pos_variable.get()
        size = self.img.size
        if wm_loc == "Top Left":
            x = size[0] * 0.1
            y = size[1] * 0.1
            xy = [x, y]
            return xy
        elif wm_loc == "Top Center":
            x = size[0] * 0.5
            y = size[1] * 0.1
            xy = [x, y]
            return xy
        elif wm_loc == "Top Right":
            x = size[0] * 0.9
            y = size[1] * 0.1
            xy = [x, y]
            return xy
        elif wm_loc == "Middle Left":
            x = size[0] * 0.1
            y = size[1] * 0.5
            xy = [x, y]
            return xy
        elif wm_loc == "Middle Center":
            x = size[0] * 0.5
            y = size[1] * 0.5
            xy = [x, y]
            return xy
        elif wm_loc == "Middle Right":
            x = size[0] * 0.9
            y = size[1] * 0.5
            xy = [x, y]
            return xy
        elif wm_loc == "Bottom Left":
            x = size[0] * 0.1
            y = size[1] * 0.9
            xy = [x, y]
            return xy
        elif wm_loc == "Bottom Center":
            x = size[0] * 0.5
            y = size[1] * 0.9
            xy = [x, y]
            return xy
        elif wm_loc == "Bottom Right":
            x = size[0] * 0.9
            y = size[1] * 0.9
            xy = [x, y]
            return xy


# Initialize class and run watermarker app
root = App()
root.mainloop()
