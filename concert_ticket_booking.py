import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime  
import random

class CinemaTicketSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Concert Ticket System")
        self.root.geometry("900x600")
        
        # Create tab control
        self.tabControl = ttk.Notebook(root)
        
        # Create tabs
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        
        self.tabControl.add(self.tab1, text="Booking")
        self.tabControl.add(self.tab2, text="Manage Bookings")
        self.tabControl.pack(expand=1, fill="both")
        
        
        self.data_file = r"C:\Rangsit University\First Year (2nd Sem)\DIT102\Final\concert_bookings.csv"
        self.init_data_file()
        
        
        self.selected_seats = set()
        
        
        self.create_booking_tab()
        
        
        self.create_manage_tab()
        
        
        self.load_data()
    
    def init_data_file(self):
        if not os.path.exists(self.data_file):  # Check if the file already exists
            with open(self.data_file, 'w', newline='') as file:
                writer = csv.writer(file)
               
                writer.writerow(['booking_id', 'seat_no', 'customer_name', 'email', 'concert_date', 'concert_time', 'seat_type', 'price', 'booking_date', 'addons', 'payment_method', 'payment'])
    
    def generate_unique_booking_id(self):
        existing_ids = set()
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  
                for row in reader:
                    existing_ids.add(row[0])  

        while True:
            booking_id = str(random.randint(100000, 999999))
            if booking_id not in existing_ids:
                return booking_id

    def create_booking_tab(self):
        # Screen label
        screen_label = tk.Label(self.tab1, text="STAGE", bg="black", fg="white", font=("Arial", 16, "bold"))
        screen_label.pack(pady=10, fill=tk.X)

        # Seat layout frame
        seat_frame = ttk.Frame(self.tab1)
        seat_frame.pack(pady=20)

        # Create seats (5 rows, 10 columns)
        self.seats = {}
        for row in range(5):
            for col in range(10):
                seat_no = f"{chr(65+row)}{col+1}"
                seat_btn = tk.Button(
                    seat_frame,
                    text=seat_no,
                    width=5,
                    height=2,
                    bg="lightblue",
                    fg="black",
                    font=("Arial", 10, "bold"),
                    command=lambda s=seat_no: self.toggle_seat(s),
                )
                seat_btn.grid(row=row, column=col, padx=2, pady=2)
                self.seats[seat_no] = seat_btn

        # Booking form
        form_frame = ttk.LabelFrame(self.tab1, text="Booking Form", padding=(10, 10))
        form_frame.pack(pady=20, padx=20, fill=tk.X)

        
        ttk.Label(form_frame, text="Selected Seat:", foreground="blue").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.selected_seat_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.selected_seat_var, state="readonly", width=15).grid(row=0, column=1, padx=5, pady=5)

       
        ttk.Label(form_frame, text="Customer Name:", foreground="blue").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.customer_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.customer_name_var, width=15).grid(row=0, column=3, padx=5, pady=5)

       
        ttk.Label(form_frame, text="Concert Name:", foreground="blue").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.concert_name_var = tk.StringVar(value="EDM Festival")  # Default to "EDM Festival"
        ttk.Entry(form_frame, textvariable=self.concert_name_var, state="readonly", width=15).grid(row=0, column=5, padx=5, pady=5)

       
        ttk.Label(form_frame, text="Email:", foreground="blue").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_var, width=15).grid(row=1, column=1, padx=5, pady=5)

        
        ttk.Label(form_frame, text="Booking Date:", foreground="blue").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.booking_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))  # Default to today's date
        self.booking_date_entry = ttk.Entry(form_frame, textvariable=self.booking_date_var, state="readonly", width=15)
        self.booking_date_entry.grid(row=1, column=3, padx=5, pady=5)

        
        ttk.Label(form_frame, text="Concert Time:", foreground="blue").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.concert_time_var = tk.StringVar(value="6 PM to 3 AM")  # Fixed time
        ttk.Entry(form_frame, textvariable=self.concert_time_var, state="readonly", width=25).grid(row=2, column=1, padx=5, pady=5)

       
        ttk.Label(form_frame, text="Seat Type:", foreground="blue").grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.seat_type_var = tk.StringVar(value="Regular")
        ttk.Entry(form_frame, textvariable=self.seat_type_var, state="readonly", width=13).grid(row=2, column=3, padx=5, pady=5)

        
        ttk.Label(form_frame, text="Add-ons:", foreground="green").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.popcorn_var = tk.BooleanVar()  # Food
        self.drink_var = tk.BooleanVar()  # Drink
        self.snack_var = tk.BooleanVar()  # Hoodie
        self.exclusive_pack_var = tk.BooleanVar()  # Exclusive Pack

        ttk.Checkbutton(form_frame, text="Food (400 THB)", variable=self.popcorn_var, command=self.calculate_total_price).grid(row=3, column=1, padx=5, pady=5)
        ttk.Checkbutton(form_frame, text="Drink (250 THB)", variable=self.drink_var, command=self.calculate_total_price).grid(row=3, column=2, padx=5, pady=5)
        ttk.Checkbutton(form_frame, text="Hoodie (1000 THB)", variable=self.snack_var, command=self.calculate_total_price).grid(row=3, column=3, padx=5, pady=5)
        ttk.Checkbutton(form_frame, text="Exclusive Pack (3000 THB)", variable=self.exclusive_pack_var, command=self.calculate_total_price).grid(row=3, column=4, padx=5, pady=5)

        
        ttk.Label(form_frame, text="Payment Method:", foreground="blue").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.payment_method_var = tk.StringVar(value="Cash")  # Default payment method
        payment_methods = ["Cash", "Credit Card", "Digital Wallet"]
        ttk.Combobox(form_frame, textvariable=self.payment_method_var, values=payment_methods, state="readonly", width=15).grid(row=4, column=1, padx=5, pady=5)

      
        ttk.Button(form_frame, text="Book Ticket", command=self.book_ticket).grid(row=6, column=0, columnspan=4, pady=10)

        
        self.total_price_var = tk.StringVar(value="Total Price: 0 THB")
        ttk.Label(self.tab1, textvariable=self.total_price_var, font=("Arial", 12, "bold"), foreground="red").pack(pady=10)
    
    def create_manage_tab(self):
        # Search frame
        search_frame = ttk.Frame(self.tab2)
        search_frame.pack(pady=10, fill=tk.X, padx=10)

        # Search label and entry
        ttk.Label(search_frame, text="Search:", font=("Arial", 12, "bold"), foreground="blue").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=5)

        # Search and Show All buttons
        ttk.Button(search_frame, text="Search", command=self.search_booking, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Show All", command=self.load_data, style="Accent.TButton").pack(side=tk.LEFT, padx=5)

        # Data table frame
        table_frame = ttk.Frame(self.tab2)
        table_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Add Treeview with horizontal and vertical scrollbars
        self.tree = ttk.Treeview(
            table_frame,
            columns=('booking_id', 'seat_no', 'customer_name', 'email', 'concert_details', 'seat_type', 'price', 'booking_date', 'addons', 'payment_method', 'payment'),
            show='headings',
            height=15
        )

        # Define column headings
        self.tree.heading('booking_id', text='Booking ID', anchor=tk.W)
        self.tree.heading('seat_no', text='Seat No', anchor=tk.W)
        self.tree.heading('customer_name', text='Customer Name', anchor=tk.W)
        self.tree.heading('email', text='Email', anchor=tk.W)
        self.tree.heading('concert_details', text='Concert Details', anchor=tk.W)  # Combined column
        self.tree.heading('seat_type', text='Seat Type', anchor=tk.W)
        self.tree.heading('price', text='Price', anchor=tk.W)
        self.tree.heading('booking_date', text='Booking Date', anchor=tk.W)
        self.tree.heading('addons', text='Add-ons', anchor=tk.W)
        self.tree.heading('payment_method', text='Payment Method', anchor=tk.W)
        self.tree.heading('payment', text='Payment Status', anchor=tk.W)

        # Adjust column widths
        self.tree.column('booking_id', width=100, anchor=tk.W)
        self.tree.column('seat_no', width=120, anchor=tk.W)
        self.tree.column('customer_name', width=150, anchor=tk.W)
        self.tree.column('email', width=150, anchor=tk.W)
        self.tree.column('concert_details', width=200, anchor=tk.W)  # Adjust width for combined column
        self.tree.column('seat_type', width=100, anchor=tk.W)
        self.tree.column('price', width=100, anchor=tk.W)
        self.tree.column('booking_date', width=120, anchor=tk.W)
        self.tree.column('addons', width=150, anchor=tk.W)
        self.tree.column('payment_method', width=150, anchor=tk.W)
        self.tree.column('payment', width=150, anchor=tk.W)

        # Add vertical scrollbar
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=v_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscroll=h_scrollbar.set)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Pack the Treeview
        self.tree.pack(fill=tk.BOTH, expand=True)

        
        action_frame = ttk.Frame(self.tab2)
        action_frame.pack(pady=10)

        # Edit and Delete buttons
        ttk.Button(action_frame, text="Edit", command=self.edit_booking, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Delete", command=self.delete_booking, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
    
    def toggle_seat(self, seat_no):
        if self.seats[seat_no]['bg'] == 'red':
            messagebox.showwarning("Seat Taken", "This seat is already booked!")
            return

        if seat_no in self.selected_seats:
            # Unselect the seat
            self.selected_seats.remove(seat_no)
            self.seats[seat_no].config(bg='lightblue')
        else:
            # Select the seat
            self.selected_seats.add(seat_no)
            self.seats[seat_no].config(bg='yellow')

        # Update selected seats display
        self.selected_seat_var.set(", ".join(self.selected_seats))
        self.update_seat_type()
        self.calculate_total_price()

    def update_seat_type(self):
        # Determine seat type based on row letter
        seat_types = {
            'A': "Premium",
            'B': "VIP",
            'C': "VIP",
            'D': "Regular",
            'E': "Regular"
        }
        
        if not self.selected_seats:
            self.seat_type_var.set("")
            return
            
        # Get the first character (row) of the first selected seat
        # This assumes all selected seats are in the same row
        row_letter = next(iter(self.selected_seats))[0]
        seat_type = seat_types.get(row_letter, "Regular")
        self.seat_type_var.set(seat_type) 

    def calculate_total_price(self):
        # Seat pricing
        seat_prices = {
            'A': 10000,  # VIP
            'B': 7000,   # Premium
            'C': 6000,   # Premium
            'D': 4000,   # Silver
            'E': 3500    # Normal
        }

        total_price = 0
        for seat in self.selected_seats:
            row = seat[0] 
            total_price += seat_prices.get(row, 0)

        # Add-ons pricing
        if self.popcorn_var.get():  # Food
            total_price += 400
        if self.drink_var.get():  # Drink
            total_price += 250
        if self.snack_var.get():  # Hoodie
            total_price += 1000
        if self.exclusive_pack_var.get():  # Exclusive Pack
            total_price += 3000

        # Update total price display
        self.total_price_var.set(f"{total_price} THB")
    
    def book_ticket(self):
        if not self.selected_seats:
            messagebox.showerror("Error", "Please select at least one seat")
            return

        customer_name = self.customer_name_var.get()
        email = self.email_var.get()
        concert_time = self.concert_time_var.get()
        concert_name = self.concert_name_var.get()
        seat_type = self.seat_type_var.get()
        total_price = self.total_price_var.get().replace("Total Price: ", "")  
        booking_date = self.booking_date_var.get()
        payment_method = self.payment_method_var.get()

        if not all([customer_name, email, concert_time, concert_name, booking_date]):
            messagebox.showerror("Error", "Please fill all required fields")
            return

        # Add-ons
        addons = []
        if self.popcorn_var.get():
            addons.append("Food")
        if self.drink_var.get():
            addons.append("Drink")
        if self.snack_var.get():
            addons.append("Hoodie")
        if self.exclusive_pack_var.get():
            addons.append("Exclusive Pack")

        # Combine seats into a single row
        seat_no_combined = ", ".join(self.selected_seats)
        booking_id = self.generate_unique_booking_id()

        # Save booking to CSV
        #with open(self.data_file, 'a', newline='') as file:
           # writer = csv.writer(file)
            #writer.writerow([
                #booking_id, seat_no_combined, customer_name, email, concert_time,
                #seat_type, total_price, booking_date, ", ".join(addons), payment_method, "Pending"
            #])

        # Show confirmation message box
        self.show_confirmation_message(
            customer_name, email, concert_time, concert_name, seat_type, total_price,
            booking_date, list(self.selected_seats), addons, payment_method
        )
    
    def show_confirmation_message(self, customer_name, email, concert_time, concert_name, seat_type, total_price, booking_date, selected_seats, addons, payment_method):
        # Create a confirmation message box
        confirmation_window = tk.Toplevel(self.root)
        confirmation_window.title("Confirm Booking")
        confirmation_window.geometry("400x550")
        confirmation_window.resizable(False, False)
        
       
        confirmation_frame = ttk.Frame(confirmation_window, padding=20)
        confirmation_frame.pack(fill=tk.BOTH, expand=True)
        
        # Confirmation header
        tk.Label(confirmation_frame, text="Please confirm your booking details:", 
                 font=("Arial", 12, "bold"), fg="blue").pack(pady=(0, 15))
        
        # Details frame
        details_frame = ttk.Frame(confirmation_frame)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Customer details
        tk.Label(details_frame, text=f"Customer: {customer_name}", font=("Arial", 10)).pack(anchor="w", pady=2)
        tk.Label(details_frame, text=f"Email: {email}", font=("Arial", 10)).pack(anchor="w", pady=2)
        
        # Concert details
        tk.Label(details_frame, text=f"Concert: {concert_name}", font=("Arial", 10)).pack(anchor="w", pady=2)
        tk.Label(details_frame, text=f"Time: {concert_time}", font=("Arial", 10)).pack(anchor="w", pady=2)
        tk.Label(details_frame, text=f"Date: {booking_date}", font=("Arial", 10)).pack(anchor="w", pady=2)
        
        # Seat details
        tk.Label(details_frame, text=f"Seat Type: {seat_type}", font=("Arial", 10)).pack(anchor="w", pady=2)
        tk.Label(details_frame, text=f"Selected Seats: {', '.join(selected_seats)}", font=("Arial", 10)).pack(anchor="w", pady=2)
        
        # Add-ons
        addon_text = ", ".join(addons) if addons else "None"
        tk.Label(details_frame, text=f"Add-ons: {addon_text}", font=("Arial", 10)).pack(anchor="w", pady=2)
        
        # Payment method
        tk.Label(details_frame, text=f"Payment Method: {payment_method}", font=("Arial", 10)).pack(anchor="w", pady=2)
        
        # Price
        tk.Label(details_frame, text=f"Total Price: {total_price}", 
                 font=("Arial", 12, "bold"), fg="red").pack(anchor="w", pady=(10, 5))
        
        # Buttons frame
        buttons_frame = ttk.Frame(confirmation_frame)
        buttons_frame.pack(pady=15)
        
        # Process button
        def process_booking():
            try:
               
                file_exists = os.path.exists(self.data_file)

                
                with open(self.data_file, 'a+', newline='') as file:
                    writer = csv.writer(file)
                    file.seek(0)
                    reader = csv.reader(file)
                    existing_bookings = list(reader)

                    
                    if not file_exists or not existing_bookings:
                        writer.writerow(['booking_id', 'seat_no', 'customer_name', 'email', 'concert_time', 'concert_name', 'seat_type', 'price', 'booking_date', 'addons', 'payment_method', 'payment'])

                   
                    seat_no_combined = ", ".join(selected_seats)
                    booking_id = self.generate_unique_booking_id()
                    writer.writerow([
                        booking_id, seat_no_combined, customer_name, email, concert_time, concert_name,
                        seat_type, total_price, booking_date, ", ".join(addons), payment_method, "Pending"
                    ])

                     

                    # Mark seats as booked
                    for seat_no in selected_seats:
                        self.seats[seat_no].config(bg='red')

                # Clear form and reset selection
                self.reset_booking_form()

                # Refresh the manage bookings tab data
                self.load_data()

                # Close confirmation window
                confirmation_window.destroy()

                # Show ticket message box
                self.show_ticket(booking_id, customer_name, concert_name, concert_time, selected_seats, total_price)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save booking: {e}")

        ttk.Button(buttons_frame, text="Confirm Booking", command=process_booking).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=confirmation_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_ticket(self, booking_id, customer_name, concert_name, concert_time, selected_seats, total_price):
        ticket_window = tk.Toplevel(self.root)
        ticket_window.title("Your Ticket")
        ticket_window.geometry("400x500")  
        ticket_window.resizable(False, False)

        # Ticket title
        tk.Label(ticket_window, text="Your Ticket", font=("Arial", 16, "bold"), fg="green").pack(pady=10)

        # Booking ID
        tk.Label(ticket_window, text=f"Booking ID: {booking_id}", font=("Arial", 12, "bold"), fg="blue").pack(anchor="w", padx=10, pady=5)

        # Ticket details
        tk.Label(ticket_window, text=f"Customer Name: {customer_name}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(ticket_window, text=f"Concert Name: {concert_name}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(ticket_window, text=f"Concert Time: {concert_time}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(ticket_window, text=f"Selected Seats: {', '.join(selected_seats)}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        #tk.Label(ticket_window, text=f"Event Date: 2025-8-24", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(ticket_window, text=f"Total Price: {total_price}", font=("Arial", 12, "bold"), fg="red").pack(anchor="w", padx=10, pady=5)

        # Close button
        ttk.Button(ticket_window, text="Close", command=ticket_window.destroy).pack(pady=20)
    
    def reset_booking_form(self):
        self.selected_seats.clear()
        self.selected_seat_var.set("")
        self.customer_name_var.set("")
        self.email_var.set("")
        self.concert_time_var.set("6 PM - 3 AM")  
        self.booking_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.payment_method_var.set("Cash")
        self.popcorn_var.set(False)
        self.drink_var.set(False)
        self.snack_var.set(False)
        self.exclusive_pack_var.set(False)
        self.total_price_var.set("Total Price: 0 THB")
    
    def load_data(self):
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        
        for seat_btn in self.seats.values():
            seat_btn.config(bg='lightblue')

        # Load data from the CSV file
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    reader = csv.reader(file)
                    header = next(reader) 
                    for row in reader:
                        if len(row) < 12:  
                            print(f"Skipping invalid row: {row}") 
                            continue  
                        
                       
                        concert_details = f"{row[4]} - {row[5]}"
                        row[4] = concert_details
                        del row[5]  
                        
                        
                        print(f"Inserting row into Treeview: {row}")
                        
                        # Insert the modified row into the Treeview
                        self.tree.insert('', 'end', values=row)
                        
                        # Mark booked seats
                        for seat_no in row[1].split(", "):
                            seat_no = seat_no.strip()  # Remove any extra spaces
                            if seat_no in self.seats:
                                self.seats[seat_no].config(bg='red')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")
                print(f"Load data error: {e}")  
    
    def search_booking(self):
        search_text = self.search_var.get().lower()

        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Search in all fields
        with open(self.data_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if any(search_text in str(field).lower() for field in row):  # Check all fields for a match
                    if len(row) >= 12:  # Make sure we have enough columns
                        # Format concert details properly (combining concert_time and concert_name)
                        modified_row = row.copy()
                        concert_details = f"{row[4]} - {row[5]}"
                        modified_row[4] = concert_details
                        del modified_row[5]  # Remove the concert_name column after combining
                        self.tree.insert('', 'end', values=modified_row)
                    else:
                        # Handle case where row doesn't have enough columns
                        self.tree.insert('', 'end', values=row)
    
    def edit_booking(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a booking to edit")
            return

        item = self.tree.item(selected_item)
        values = item['values']
        
        
        print(f"Selected item values: {values}")
        
     
        if len(values) < 11: 
            messagebox.showerror("Error", "Invalid booking data. Cannot edit this booking.")
            return
        
        # Extract all values from the selected item
        booking_id = values[0]
        seat_no = values[1]
        customer_name = values[2]
        email = values[3]
        concert_details = values[4]  # Combined column (Concert Date and Time)
        seat_type = values[5]
        price = values[6]
        booking_date = values[7]
        addons_str = values[8]
        payment_method = values[9]
        payment_status = values[10]

        # Create edit dialog
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Booking")
        edit_window.geometry("500x650")
        edit_window.resizable(False, False)

        # Create a scrollable frame
        main_frame = ttk.Frame(edit_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create form layout
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
       
        ttk.Label(form_frame, text="Booking ID:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        booking_id_var = tk.StringVar(value=booking_id)
        ttk.Entry(form_frame, textvariable=booking_id_var, state='readonly', width=25).grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        
        ttk.Label(form_frame, text="Customer Name:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        customer_name_var = tk.StringVar(value=customer_name)
        ttk.Entry(form_frame, textvariable=customer_name_var, width=25).grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
    
        ttk.Label(form_frame, text="Email:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        email_var = tk.StringVar(value=email)
        ttk.Entry(form_frame, textvariable=email_var, width=25).grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
     
        ttk.Label(form_frame, text="Concert Details:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        concert_details_var = tk.StringVar(value=concert_details)
        ttk.Entry(form_frame, textvariable=concert_details_var, state='readonly', width=25).grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        
     
        ttk.Label(form_frame, text="Seat No:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        seat_no_var = tk.StringVar(value=seat_no)
        ttk.Entry(form_frame, textvariable=seat_no_var, state='readonly', width=25).grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)
        
     
        ttk.Label(form_frame, text="Seat Type:", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)
        seat_type_var = tk.StringVar(value=seat_type)
        ttk.Entry(form_frame, textvariable=seat_type_var, state='readonly', width=25).grid(row=5, column=1, sticky=tk.W, pady=5, padx=5)
        
    
        ttk.Label(form_frame, text="Booking Date:", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky=tk.W, pady=5, padx=5)
        booking_date_var = tk.StringVar(value=booking_date)
        ttk.Entry(form_frame, textvariable=booking_date_var, state='readonly', width=25).grid(row=6, column=1, sticky=tk.W, pady=5, padx=5)
        
     
        ttk.Label(form_frame, text="Price:", font=("Arial", 10, "bold")).grid(row=7, column=0, sticky=tk.W, pady=5, padx=5)
        price_var = tk.StringVar(value=price)
        ttk.Entry(form_frame, textvariable=price_var, width=25, state='readonly').grid(row=7, column=1, sticky=tk.W, pady=5, padx=5)
        
   
        ttk.Label(form_frame, text="Add-ons:", font=("Arial", 10, "bold")).grid(row=8, column=0, sticky=tk.W, pady=5, padx=5)
        addons_var = tk.StringVar(value=addons_str)
        ttk.Entry(form_frame, textvariable=addons_var, width=25).grid(row=8, column=1, sticky=tk.W, pady=5, padx=5)
        
     
        ttk.Label(form_frame, text="Payment Method:", font=("Arial", 10, "bold")).grid(row=9, column=0, sticky=tk.W, pady=5, padx=5)
        payment_method_var = tk.StringVar(value=payment_method)
        payment_methods = ["Cash", "Credit Card", "Digital Wallet"]
        ttk.Combobox(form_frame, textvariable=payment_method_var, values=payment_methods, state="readonly", width=22).grid(row=9, column=1, sticky=tk.W, pady=5, padx=5)
        
   
        ttk.Label(form_frame, text="Payment Status:", font=("Arial", 10, "bold")).grid(row=10, column=0, sticky=tk.W, pady=5, padx=5)
        payment_status_var = tk.StringVar(value=payment_status)
        payment_statuses = ["Pending", "Completed", "Cancelled"]
        ttk.Combobox(form_frame, textvariable=payment_status_var, values=payment_statuses, state="readonly", width=22).grid(row=10, column=1, sticky=tk.W, pady=5, padx=5)
        
    
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=15)
        
        def save_changes():
            try:
               
                concert_details = concert_details_var.get()
             
                if " - " in concert_details:
                    parts = concert_details.split(" - ", 1)
                    concert_time = parts[0]
                    concert_name = parts[1] if len(parts) > 1 else "EDM Festival"
                else:
                    concert_time = concert_details
                    concert_name = "EDM Festival"
                
                # Collect updated data
                updated_data = [
                    booking_id_var.get(),
                    seat_no_var.get(),
                    customer_name_var.get(),
                    email_var.get(),
                    concert_time,  # Separate time 
                    concert_name,  # Separate name
                    seat_type_var.get(),
                    price_var.get(),
                    booking_date_var.get(),
                    addons_var.get(),
                    payment_method_var.get(),
                    payment_status_var.get()
                ]
                
               
                if not customer_name_var.get() or not email_var.get():
                    messagebox.showerror("Error", "Customer name and email cannot be empty!")
                    return
                
            
                all_bookings = []
                found = False
                
                with open(self.data_file, 'r') as file:
                    reader = csv.reader(file)
                    header = next(reader)  # Save header
                    for row in reader:
                        if str(row[0]) == str(booking_id):
                            all_bookings.append(updated_data)
                            found = True
                        else:
                            all_bookings.append(row)
                
                if found:
                 
                    with open(self.data_file, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(header)
                        writer.writerows(all_bookings)
                    
                    # Close window and show success message
                    edit_window.destroy()
                    messagebox.showinfo("Success", "Booking updated successfully!")
                    
                    # Refresh the data display
                    self.load_data()
                else:
                    messagebox.showerror("Error", f"Booking ID {booking_id} not found in the data file!")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update booking: {e}")
                print(f"Exception details: {e}")  # For debugging
        
        # Save Button
        ttk.Button(buttons_frame, text="Save Changes", command=save_changes).pack(side=tk.LEFT, padx=10)
        
        # Cancel Button
        ttk.Button(buttons_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.LEFT, padx=10)
    
    def delete_booking(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a booking to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this booking?"):
            item = self.tree.item(selected_item)
            values = item['values']
            booking_id = str(values[0])  
            
          
            bookings = []
            deleted_seats = []
            found = False
            
            try:
                with open(self.data_file, 'r') as file:
                    reader = csv.reader(file)
                    header = next(reader) 
                    for row in reader:
                        if str(row[0]) == booking_id:  # Convert to string for proper comparison
                            found = True
                            # Save the seat numbers to reset their color
                            deleted_seats = [seat.strip() for seat in row[1].split(',')]
                        else:
                            bookings.append(row)
                
                if found:
                    # Write updated data back to file
                    with open(self.data_file, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(header)
                        writer.writerows(bookings)
                    
                    # Reset seat colors for deleted booking
                    for seat in deleted_seats:
                        if seat in self.seats:
                            self.seats[seat].config(bg='lightblue')
                    
                    self.load_data()  # Refresh the data
                    messagebox.showinfo("Success", f"Booking {booking_id} deleted successfully!")
                else:
                    messagebox.showwarning("Warning", f"Booking {booking_id} not found in the data file.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete booking: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CinemaTicketSystem(root)
    root.mainloop()