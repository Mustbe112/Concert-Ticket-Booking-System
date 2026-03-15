# 🎵 Concert Ticket Booking System

> A Python desktop application for managing concert ticket bookings with a GUI built using Tkinter.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange?style=flat-square)
![CSV](https://img.shields.io/badge/Storage-CSV-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

---

## 📋 Overview

Concert Ticket Booking System is a Python desktop application that allows users to book seats for a concert (EDM Festival), manage existing bookings, and view ticket receipts — all through a simple graphical interface. Booking data is saved persistently to a CSV file.

---

## ✨ Features

- 🪑 **Interactive seat map** — 5 rows × 10 columns with color-coded availability
- 🎟️ **Ticket booking** with customer name, email, seat selection, and add-ons
- 💰 **Dynamic price calculator** — updates in real time as seats and add-ons are selected
- 🧾 **Booking confirmation popup** and printable ticket window
- 📋 **Manage Bookings tab** — view, search, edit, and delete existing bookings
- 💾 **CSV persistence** — all bookings saved to and loaded from `concert_bookings.csv`
- 🔑 **Unique booking ID** generation using random 6-digit numbers

---

## 🖥️ Application Preview

### Tab 1 — Booking
- A seat map showing available (blue), selected (yellow), and booked (red) seats
- A booking form for customer details, add-ons, and payment method
- A live total price display at the bottom

### Tab 2 — Manage Bookings
- A searchable table of all bookings
- Edit and Delete buttons for managing records

---

## 📁 Project Structure

```
concert-ticket-booking/
├── concert_ticket_booking.py   # Main application file
└── concert_bookings.csv        # Booking data (auto-created on first run)
```

---

## 🪑 Seat Map & Pricing

The venue has **5 rows (A–E)** and **10 columns (1–10)**, with pricing based on the row:

| Row | Seat Type | Price (THB) |
|-----|-----------|-------------|
| A   | Premium   | 10,000      |
| B   | VIP       | 7,000       |
| C   | VIP       | 6,000       |
| D   | Regular   | 4,000       |
| E   | Regular   | 3,500       |

**Seat colors:**
- 🔵 Light Blue — Available
- 🟡 Yellow — Currently selected
- 🔴 Red — Already booked

---

## 🛍️ Add-ons

| Add-on        | Price (THB) |
|---------------|-------------|
| Food          | 400         |
| Drink         | 250         |
| Hoodie        | 1,000       |
| Exclusive Pack| 3,000       |

---

## 💳 Payment Methods

- Cash
- Credit Card
- Digital Wallet

---

## 🗄️ CSV Data Format

Bookings are stored in `concert_bookings.csv` with the following columns:

| Column           | Description                          |
|------------------|--------------------------------------|
| `booking_id`     | Unique 6-digit booking reference     |
| `seat_no`        | Seat number(s) e.g. `A1, A2`        |
| `customer_name`  | Full name of customer                |
| `email`          | Customer email address               |
| `concert_time`   | Fixed time: `6 PM to 3 AM`          |
| `concert_name`   | Concert name: `EDM Festival`         |
| `seat_type`      | Premium / VIP / Regular              |
| `price`          | Total price in THB                   |
| `booking_date`   | Date of booking (auto-filled)        |
| `addons`         | Selected add-ons                     |
| `payment_method` | Cash / Credit Card / Digital Wallet  |
| `payment`        | Payment status: Pending / Completed / Cancelled |

---

## 🚀 How to Run

### Prerequisites
- Python **3.x** installed
- Tkinter (included with standard Python installations)

### Run the Application

```bash
python concert_ticket_booking.py
```

> ⚠️ **Important:** Before running, update the `data_file` path in the code to match your local directory:
> ```python
> self.data_file = r"C:\your\path\to\concert_bookings.csv"
> ```

---

## 📖 How to Use

1. **Launch** the application — the seat map loads with any previously booked seats marked red
2. **Click a seat** on the map to select it (turns yellow); click again to deselect
3. **Fill in** your name and email in the booking form
4. **Check any add-ons** you want — the total price updates automatically
5. **Choose a payment method** and click **Book Ticket**
6. **Review** your details in the confirmation popup, then click **Confirm Booking**
7. A **ticket window** appears with your booking ID and details
8. Switch to the **Manage Bookings** tab to view, search, edit, or delete bookings

---

## ⚠️ Known Limitations

- The `data_file` path is **hardcoded** — must be manually updated per machine
- Concert name (`EDM Festival`) and time (`6 PM to 3 AM`) are fixed/read-only
- No email format validation on the booking form
- Minor CSV column inconsistency between some saved rows (concert_date vs concert_time columns)
- No multi-concert support — currently locked to one event

---

## 🔮 Future Improvements

- [ ] Make the data file path dynamic (relative path or file picker)
- [ ] Support multiple concerts and event dates
- [ ] Add email format validation
- [ ] Export booking report as PDF
- [ ] Add payment status filter in the Manage Bookings tab
- [ ] Add a seat legend/key to the UI

---

## 👤 Author

Developed as a Python GUI coursework/demo project using **Tkinter** and **CSV** for data persistence.
Built at **Rangsit University — DIT102 Final Project**.
