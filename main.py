import tkinter as tk
from tkinter import messagebox, simpledialog
import qrcode
from PIL import Image, ImageTk, ImageDraw, ImageFont
import re
import tempfile
import os
from tkinter import filedialog

# Validate the format of the email address
def validate_email(email):
    # Regular expression to check if the email is valid
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Validate that the name contains more than one word
def validate_name(name):
    return len(name.split()) > 1  # Check if more than one word is entered

# Generate a QR code based on the provided data
def create_qr_code(data):
    # Configuration for the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

# Create the badge image with the QR code and user data
def create_badge_image(data):
    badge_width, badge_height = 400, 300
    badge = Image.new('RGB', (badge_width, badge_height), 'white')
    draw = ImageDraw.Draw(badge)
    font = ImageFont.load_default()

    draw.text((10, 10), f"Name: {data['Name']}", fill="black", font=font)
    draw.text((10, 40), f"Email: {data['Email']}", fill="black", font=font)
    if data['Twitter']:
        draw.text((10, 70), f"Twitter: {data['Twitter']}", fill="black", font=font)
    if data['GitHub']:
        draw.text((10, 100), f"GitHub: {data['GitHub']}", fill="black", font=font)

    # Adding the QR code to the badge
    qr_image = create_qr_code(str(data))
    qr_image.thumbnail((150, 150))
    badge.paste(qr_image, (250, 75))

    return ImageTk.PhotoImage(badge)

# Function to create a badge based on user input
def create_badge():
    # Check for required fields: name and email
    if not name_entry.get() or not email_entry.get():
        messagebox.showerror("Error", "Name and Email are required.")
        return
    if not validate_email(email_entry.get()):
        messagebox.showerror("Error", "Invalid Email address.")
        return
    if not validate_name(name_entry.get()):
        messagebox.showerror("Error", "Please enter both first and last name.")
        return

    # Format Twitter handle if provided
    twitter = twitter_entry.get()
    if twitter and not twitter.startswith('@'):
        twitter = '@' + twitter

    # Collect data from the input fields
    data = {
        "Name": name_entry.get(),
        "Email": email_entry.get(),
        "Twitter": twitter,
        "GitHub": github_entry.get()
    }

    # Generate and display the badge
    badge_photo = create_badge_image(data)
    badge_label.config(image=badge_photo)
    badge_label.image = badge_photo
    badge_label.grid(row=5, column=0, columnspan=2)

    # Enable the print button
    print_button.config(state=tk.NORMAL)

# Function to clear all input fields and hide the badge
def clear_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    twitter_entry.delete(0, tk.END)
    github_entry.delete(0, tk.END)
    badge_label.grid_forget()  # Hide the badge
    print_button.config(state=tk.DISABLED) # Disable the print button

# Function to save the badge as an image file
def print_badge():
    # Open file dialog to choose save location
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        # Generate the badge image and save it
        badge_image = create_badge_image({
            "Name": name_entry.get(),
            "Email": email_entry.get(),
            "Twitter": twitter_entry.get(),
            "GitHub": github_entry.get()
        })
        badge_image._PhotoImage__photo.write(file_path, format="png")
        messagebox.showinfo("Print", f"Badge saved as {file_path}")

# Create a function to configure row and column expansion
def configure_grid():
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(5, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

# GUI setup
root = tk.Tk()
root.title("QRCode Badge Generator")

# Creating and placing labels and input fields in the grid
tk.Label(root, text="Name:").grid(row=0, column=0)
tk.Label(root, text="Email:").grid(row=1, column=0)
tk.Label(root, text="Twitter:").grid(row=2, column=0)
tk.Label(root, text="GitHub:").grid(row=3, column=0)

name_entry = tk.Entry(root)
email_entry = tk.Entry(root)
twitter_entry = tk.Entry(root)
github_entry = tk.Entry(root)

name_entry.grid(row=0, column=1)
email_entry.grid(row=1, column=1)
twitter_entry.grid(row=2, column=1)
github_entry.grid(row=3, column=1)

# Creating and placing buttons in the grid
create_button = tk.Button(root, text="Create", command=create_badge)
cancel_button = tk.Button(root, text="Cancel", command=clear_fields)
print_button = tk.Button(root, text="Print", command=print_badge, state=tk.DISABLED)

create_button.grid(row=4, column=0)
cancel_button.grid(row=4, column=1)
print_button.grid(row=6, column=0, columnspan=2)

badge_label = tk.Label(root) # Placeholder for the badge image

# Add a function to handle window resize
def on_resize(event):
    configure_grid()

# Binding the resize event to the on_resize function
root.bind("<Configure>", on_resize)

# Configure the grid layout and run the application
configure_grid()
root.mainloop()
