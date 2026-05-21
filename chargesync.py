import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import time

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="ev_charging_db"
)
cursor = conn.cursor()

BG_BASE      = "#0D1117"
BG_PANEL     = "#161B27"
BG_CARD      = "#1C2333"
BG_INPUT     = "#242D3E"
BG_ROW_ODD   = "#1C2333"
BG_ROW_EVEN  = "#202838"

ACCENT_BLUE  = "#3B82F6"
ACCENT_TEAL  = "#06B6D4"
ACCENT_GOLD  = "#F59E0B"
ACCENT_GREEN = "#10B981"
ACCENT_RED   = "#EF4444"
ACCENT_PURPLE= "#8B5CF6"

TEXT_H1      = "#F1F5F9"
TEXT_H2      = "#CBD5E1"
TEXT_BODY    = "#94A3B8"
TEXT_MUTED   = "#475569"

SIDEBAR_W    = 220
BORDER       = "#2D3A50"

FN_HEADING   = ("Georgia",    14, "bold")
FN_SUBHEAD   = ("Georgia",    11, "bold")
FN_LABEL     = ("Helvetica",  10, "bold")
FN_BODY      = ("Helvetica",  10)
FN_ENTRY     = ("Helvetica",  11)
FN_BTN       = ("Helvetica",  10, "bold")
FN_MONO      = ("Courier",     9)
FN_SMALL     = ("Helvetica",   9)

def _apply_treeview_style():
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("EV.Treeview",
        background=BG_ROW_ODD, foreground=TEXT_H2,
        fieldbackground=BG_ROW_ODD, rowheight=36,
        borderwidth=0, font=FN_BODY)
    s.configure("EV.Treeview.Heading",
        background=BG_PANEL, foreground=ACCENT_TEAL,
        font=FN_LABEL, borderwidth=0, relief="flat", padding=8)
    s.map("EV.Treeview",
        background=[("selected", "#253148")],
        foreground=[("selected", TEXT_H1)])


def _lbl(parent, text, font=FN_BODY, fg=TEXT_BODY, **kw):
    bg = kw.pop("bg", None) or parent.cget("bg")
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)


def _sep(parent, color=BORDER, pady=0, padx=0):
    tk.Frame(parent, bg=color, height=1).pack(fill="x", padx=padx, pady=pady)


def _card(parent, padx=24, pady=10):
    outer = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
    outer.pack(fill="x", padx=padx, pady=pady)
    inner = tk.Frame(outer, bg=BG_CARD, padx=20, pady=16)
    inner.pack(fill="x")
    return inner


def field(parent, label_text, readonly=False, accent=ACCENT_BLUE):
    _lbl(parent, label_text, font=FN_LABEL, fg=TEXT_BODY).pack(anchor="w", pady=(10, 3))
    frame = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
    frame.pack(fill="x")
    e = tk.Entry(frame, font=FN_ENTRY, relief="flat", bd=8,
        bg=BG_INPUT, fg=TEXT_H1, insertbackground=accent,
        readonlybackground=BG_PANEL, disabledbackground=BG_PANEL,
        disabledforeground=TEXT_MUTED)
    e.pack(fill="x")
    if readonly:
        e.config(state="readonly")
    return e


def action_btn(parent, text, color=ACCENT_BLUE, command=None):
    import colorsys
    def _dk(hx, f=0.82):
        h = hx.lstrip("#")
        r,g,b = int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255
        return "#{:02x}{:02x}{:02x}".format(int(r*f*255),int(g*f*255),int(b*f*255))
    dark = _dk(color)
    btn = tk.Button(parent, text=text, font=FN_BTN, command=command,
        bg=color, fg=BG_BASE, activebackground=dark, activeforeground=BG_BASE,
        relief="flat", bd=0, cursor="hand2", padx=20, pady=11)
    btn.pack(fill="x", pady=(16,4))
    btn.bind("<Enter>", lambda e: btn.config(bg=dark))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn


def ghost_btn(parent, text, color=ACCENT_BLUE, command=None):
    btn = tk.Button(parent, text=text, font=FN_BTN, command=command,
        bg=BG_CARD, fg=color, activebackground=color, activeforeground=BG_BASE,
        relief="flat", bd=0, cursor="hand2", padx=14, pady=8,
        highlightthickness=1, highlightbackground=color)
    btn.bind("<Enter>", lambda e: btn.config(bg=color, fg=BG_BASE))
    btn.bind("<Leave>", lambda e: btn.config(bg=BG_CARD, fg=color))
    return btn

def _toplevel(title, w, h):
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry(f"{w}x{h}")
    win.configure(bg=BG_BASE)
    win.resizable(True, True)
    tk.Frame(win, bg=ACCENT_BLUE, height=3).pack(fill="x")
    return win


def _form_window(title, accent=ACCENT_BLUE):
    win = _toplevel(title, 580, 600)

    hdr = tk.Frame(win, bg=BG_PANEL, pady=18)
    hdr.pack(fill="x")
    tk.Frame(hdr, bg=accent, width=4, height=32).pack(side="left", padx=(24,14))
    _lbl(hdr, title, font=FN_HEADING, fg=TEXT_H1, bg=BG_PANEL).pack(side="left")
    _sep(win, BORDER)

    canvas = tk.Canvas(win, bg=BG_BASE, highlightthickness=0)
    sb = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
    body = tk.Frame(canvas, bg=BG_BASE)
    body.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=body, anchor="nw")
    canvas.configure(yscrollcommand=sb.set)
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)),"units"))
    sb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    return win, body


def create_table_window(title, columns, query):
    win = _toplevel(title, 980, 560)

    hdr = tk.Frame(win, bg=BG_PANEL, pady=18)
    hdr.pack(fill="x")
    tk.Frame(hdr, bg=ACCENT_TEAL, width=4, height=32).pack(side="left", padx=(24,14))
    _lbl(hdr, title, font=FN_HEADING, fg=TEXT_H1, bg=BG_PANEL).pack(side="left")
    _sep(win, BORDER)

    _apply_treeview_style()
    container = tk.Frame(win, bg=BG_BASE, padx=24, pady=16)
    container.pack(fill="both", expand=True)

    tree_frame = tk.Frame(container, bg=BORDER, padx=1, pady=1)
    tree_frame.pack(fill="both", expand=True)
    tree = ttk.Treeview(tree_frame, style="EV.Treeview", show="headings")
    tree["columns"] = columns
    for col in columns:
        tree.column(col, anchor="center", width=160, minwidth=80)
        tree.heading(col, text=col)
    vsb = ttk.Scrollbar(tree_frame, orient="vertical",   command=tree.yview)
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    hsb.pack(side="bottom", fill="x"); vsb.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)
    tree.tag_configure("odd",  background=BG_ROW_ODD,  foreground=TEXT_H2)
    tree.tag_configure("even", background=BG_ROW_EVEN, foreground=TEXT_H2)
    cursor.execute(query)
    for i, row in enumerate(cursor.fetchall()):
        tree.insert("", tk.END, values=row, tags=("odd" if i%2==0 else "even",))


def _sidebar_dashboard(title, role_icon, accent, menu_items):
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("1020x680")
    win.configure(bg=BG_BASE)
    win.resizable(True, True)
    win.minsize(800, 560)

    main = tk.Frame(win, bg=BG_BASE)
    main.pack(fill="both", expand=True)

    sidebar = tk.Frame(main, bg=BG_PANEL, width=SIDEBAR_W)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tk.Frame(sidebar, bg=accent, height=3).pack(fill="x")

    logo_f = tk.Frame(sidebar, bg=BG_PANEL, pady=22)
    logo_f.pack(fill="x")
    _lbl(logo_f, role_icon, font=("Helvetica",30), fg=accent, bg=BG_PANEL).pack()
    _lbl(logo_f, "EV Charging", font=("Georgia",13,"bold"), fg=TEXT_H1, bg=BG_PANEL).pack()
    _lbl(logo_f, "Management System", font=FN_SMALL, fg=TEXT_MUTED, bg=BG_PANEL).pack()

    _sep(sidebar, BORDER, padx=20, pady=6)

    badge = tk.Frame(sidebar, bg="#1E2A3A", padx=14, pady=8)
    badge.pack(fill="x", padx=14, pady=(0,10))
    _lbl(badge, "DASHBOARD", font=("Helvetica",7,"bold"), fg=TEXT_MUTED, bg="#1E2A3A").pack(anchor="w")
    _lbl(badge, title.replace(" Dashboard","").upper(), font=("Helvetica",10,"bold"), fg=accent, bg="#1E2A3A").pack(anchor="w")

    _sep(sidebar, BORDER, padx=20, pady=(0,6))
    _lbl(sidebar, "  NAVIGATION", font=("Helvetica",8,"bold"), fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w", pady=(2,6))

    right = tk.Frame(main, bg=BG_BASE)
    right.pack(side="left", fill="both", expand=True)

    topbar = tk.Frame(right, bg=BG_PANEL, height=52)
    topbar.pack(fill="x"); topbar.pack_propagate(False)
    tk.Frame(topbar, bg=accent, width=3).pack(side="left", fill="y")
    topbar_lbl = _lbl(topbar, "   Select an action from the sidebar",
                      font=FN_BODY, fg=TEXT_BODY, bg=BG_PANEL)
    topbar_lbl.pack(side="left", padx=10)

    content = tk.Frame(right, bg=BG_BASE)
    content.pack(fill="both", expand=True)

    welcome = tk.Frame(content, bg=BG_BASE, padx=36, pady=32)
    welcome.pack(fill="both", expand=True)
    _lbl(welcome, f"{role_icon}  {title}", font=("Georgia",20,"bold"), fg=TEXT_H1, bg=BG_BASE).pack(anchor="w")
    _lbl(welcome, "Select an item from the left sidebar to get started.",
         font=FN_BODY, fg=TEXT_BODY, bg=BG_BASE).pack(anchor="w", pady=(8,0))
    _sep(welcome, BORDER, pady=20)
    _lbl(welcome, f"Available actions: {len(menu_items)}",
         font=FN_SMALL, fg=TEXT_MUTED, bg=BG_BASE).pack(anchor="w")

    active_ref = [None]

    def nav_click(btn_widget, cb, label):
        if active_ref[0]:
            active_ref[0].config(bg=BG_PANEL, fg=TEXT_BODY)
        btn_widget.config(bg=accent, fg=BG_BASE)
        active_ref[0] = btn_widget
        topbar_lbl.config(text=f"   {label}")
        for w in content.winfo_children():
            w.destroy()
        cb()

    for icon, label, cb in menu_items:
        nb = tk.Button(sidebar,
            text=f"  {icon}  {label}", font=FN_BODY, anchor="w",
            bg=BG_PANEL, fg=TEXT_BODY,
            activebackground=accent, activeforeground=BG_BASE,
            relief="flat", bd=0, cursor="hand2",
            padx=10, pady=9, highlightthickness=0)
        nb.pack(fill="x", padx=8, pady=2)
        nb.bind("<Enter>", lambda e, b=nb: b.config(bg="#1E2D42", fg=TEXT_H1)
                if b != active_ref[0] else None)
        nb.bind("<Leave>", lambda e, b=nb: b.config(bg=BG_PANEL, fg=TEXT_BODY)
                if b != active_ref[0] else None)
        nb.config(command=lambda b=nb, l=label, c=cb: nav_click(b, c, l))

    tk.Frame(sidebar, bg=BG_PANEL).pack(fill="y", expand=True)
    _sep(sidebar, BORDER, padx=14, pady=6)
    close_b = tk.Button(sidebar, text="  ✕  Close Dashboard",
        font=FN_BTN, anchor="w",
        bg=BG_PANEL, fg=ACCENT_RED,
        activebackground=ACCENT_RED, activeforeground=BG_BASE,
        relief="flat", bd=0, cursor="hand2", padx=14, pady=10,
        highlightthickness=1, highlightbackground=ACCENT_RED,
        command=win.destroy)
    close_b.pack(fill="x", padx=10, pady=(0,14))
    close_b.bind("<Enter>", lambda e: close_b.config(bg=ACCENT_RED, fg=BG_BASE))
    close_b.bind("<Leave>", lambda e: close_b.config(bg=BG_PANEL,   fg=ACCENT_RED))

    def _embed(cb):
        def wrapped():
            for w in content.winfo_children(): w.destroy()
            cb()
        return wrapped

    return win, content

def get_next_owner_id():
    cursor.execute("SELECT MAX(OwnerID) FROM EV_OWNER")
    r = cursor.fetchone()[0]; return 1 if r is None else r+1

def get_next_booking_id():
    cursor.execute("SELECT MAX(BookingID) FROM BOOKING")
    r = cursor.fetchone()[0]; return 1 if r is None else r+1

def get_next_payment_id():
    cursor.execute("SELECT MAX(PaymentID) FROM PAYMENT")
    r = cursor.fetchone()[0]; return 1 if r is None else r+1

def get_next_request_id():
    cursor.execute("SELECT MAX(RequestID) FROM MAINTENANCE_REQUEST")
    r = cursor.fetchone()[0]; return 1 if r is None else r+1

def register_owner():
    win, body = _form_window("Register EV Owner", ACCENT_GREEN)
    card = _card(body)
    _lbl(card, "Fill in the new owner's details below",
         font=FN_SMALL, fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w", pady=(0,6))
    labels  = ["Owner ID","Name","Email","Phone","City"]
    entries = []
    for i, lbl in enumerate(labels):
        e = field(card, lbl, accent=ACCENT_GREEN)
        if i == 0:
            e.config(state="normal"); e.insert(0, get_next_owner_id()); e.config(state="readonly")
        entries.append(e)
    def submit():
        try:
            cursor.execute("INSERT INTO EV_OWNER VALUES (%s,%s,%s,%s,%s)",
                tuple(e.get() for e in entries))
            conn.commit(); messagebox.showinfo("Success","Owner registered!"); win.destroy()
        except Exception as ex: messagebox.showerror("Database Error", str(ex))
    action_btn(card, "✓  Register Owner", ACCENT_GREEN, submit)


def register_vehicle():
    win, body = _form_window("Register Vehicle", ACCENT_GREEN)
    card = _card(body)
    _lbl(card, "Add a new EV to the system",
         font=FN_SMALL, fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w", pady=(0,6))
    labels  = ["Vehicle ID","Registration Number","Vehicle Type","Battery Capacity (kWh)","Owner ID"]
    entries = [field(card, l, accent=ACCENT_GREEN) for l in labels]
    def submit():
        try:
            cursor.execute("INSERT INTO VEHICLE VALUES (%s,%s,%s,%s,%s)",
                tuple(e.get() for e in entries))
            conn.commit(); messagebox.showinfo("Success","Vehicle registered!"); win.destroy()
        except Exception as ex: messagebox.showerror("Database Error", str(ex))
    action_btn(card, "✓  Register Vehicle", ACCENT_GREEN, submit)


def book_slot():
    win, body = _form_window("Book Charging Slot", ACCENT_TEAL)
    card = _card(body)
    _lbl(card, "Reserve a charging slot for your EV",
         font=FN_SMALL, fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w", pady=(0,6))
    labels  = ["Booking ID","Booking Date (YYYY-MM-DD)","Duration (hrs)","Vehicle ID","Slot ID"]
    entries = []
    for i, lbl in enumerate(labels):
        e = field(card, lbl, accent=ACCENT_TEAL)
        if i == 0:
            e.config(state="normal"); e.insert(0, get_next_booking_id()); e.config(state="readonly")
        entries.append(e)
    def submit():
        try:
            cursor.execute("INSERT INTO BOOKING VALUES (%s,%s,%s,'Arrived',%s,%s)",
                tuple(e.get() for e in entries))
            conn.commit(); messagebox.showinfo("Success","Slot booked!"); win.destroy()
        except mysql.connector.Error as err:
            if "Slot already booked" in str(err): messagebox.showerror("Conflict","Slot already booked!")
            else: messagebox.showerror("Database Error", str(err))
    action_btn(card, "✓  Book Slot", ACCENT_TEAL, submit)


def process_payment():
    win, body = _form_window("Process Payment", ACCENT_GOLD)
    card = _card(body)
    _lbl(card, "Rate: ₹20 / kWh  —  Amount is auto-calculated",
         font=FN_SMALL, fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w", pady=(0,6))
    labels  = ["Payment ID","Booking ID","Energy Consumed (kWh)","Amount (₹)"]
    entries = []
    for i, lbl in enumerate(labels):
        ro = (i == 0 or i == 3)
        e = field(card, lbl, readonly=ro, accent=ACCENT_GOLD)
        if i == 0:
            e.config(state="normal"); e.insert(0, get_next_payment_id()); e.config(state="readonly")
        entries.append(e)
    def calc(event):
        try:
            amt = int(entries[2].get()) * 20
            entries[3].config(state="normal"); entries[3].delete(0,tk.END)
            entries[3].insert(0, amt); entries[3].config(state="readonly")
        except: pass
    entries[2].bind("<KeyRelease>", calc)
    def submit():
        try:
            cursor.execute("INSERT INTO PAYMENT VALUES (%s,%s,%s,'Success',NOW(),%s)",
                (entries[0].get(), entries[2].get(), entries[3].get(), entries[1].get()))
            conn.commit(); messagebox.showinfo("Success","Payment processed!"); win.destroy()
        except Exception as ex: messagebox.showerror("Database Error", str(ex))
    action_btn(card, "✓  Process Payment", ACCENT_GOLD, submit)


def view_my_bookings():
    win, body = _form_window("My Bookings", ACCENT_TEAL)
    card = _card(body)
    _lbl(card, "Enter your Owner ID to fetch your bookings",
         font=FN_SMALL, fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w", pady=(0,6))
    e = field(card, "Owner ID", accent=ACCENT_TEAL)
    def fetch():
        oid = e.get()
        create_table_window("My Bookings",("BookingID","Owner","Vehicle","Date"),
            f"""SELECT B.BookingID, E.Name, V.RegistrationNumber, B.BookingDate
                FROM BOOKING B JOIN VEHICLE V ON B.VehicleID=V.VehicleID
                JOIN EV_OWNER E ON V.OwnerID=E.OwnerID WHERE V.OwnerID={oid}""")
    action_btn(card, "→  Show My Bookings", ACCENT_TEAL, fetch)


def view_slots():
    create_table_window("Available Slots",
        ("SlotID","StartTime","EndTime","Station","City","Status"),
        """SELECT CS.SlotID, CS.StartTime, CS.EndTime, S.StationName, S.City, CS.SlotStatus
           FROM CHARGING_SLOT CS JOIN CHARGING_STATION S ON CS.StationID=S.StationID
           WHERE CS.SlotStatus='Available'""")


def view_station_bookings():
    win, body = _form_window("Station Bookings", ACCENT_TEAL)
    card = _card(body)
    _lbl(card, "View all bookings at a specific station",
         font=FN_SMALL, fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w", pady=(0,6))
    e = field(card, "Station ID", accent=ACCENT_TEAL)
    def fetch():
        sid = e.get()
        create_table_window("Station Bookings",("BookingID","Vehicle","Date"),
            f"""SELECT B.BookingID, V.RegistrationNumber, B.BookingDate
                FROM BOOKING B JOIN CHARGING_SLOT CS ON B.SlotID=CS.SlotID
                JOIN VEHICLE V ON B.VehicleID=V.VehicleID WHERE CS.StationID={sid}""")
    action_btn(card, "→  Show Bookings", ACCENT_TEAL, fetch)


def view_bookings():
    create_table_window("All Bookings",("BookingID","Owner","Vehicle","Date"),
        """SELECT B.BookingID, E.Name, V.RegistrationNumber, B.BookingDate
           FROM BOOKING B JOIN VEHICLE V ON B.VehicleID=V.VehicleID
           JOIN EV_OWNER E ON V.OwnerID=E.OwnerID""")


def revenue_station():
    create_table_window("Revenue per Station",("Station","Total Revenue (₹)"),
        """SELECT S.StationName, SUM(P.Amount)
           FROM PAYMENT P JOIN BOOKING B ON P.BookingID=B.BookingID
           JOIN CHARGING_SLOT CS ON B.SlotID=CS.SlotID
           JOIN CHARGING_STATION S ON CS.StationID=S.StationID GROUP BY S.StationName""")


def view_requests():
    create_table_window("Maintenance Requests",
        ("RequestID","Type","Status","Station","Vendor"),
        "SELECT RequestID, RequestType, ApprovalStatus, StationID, VendorID FROM MAINTENANCE_REQUEST")


def update_request_status():
    win, body = _form_window("Update Request Status", ACCENT_GREEN)
    card = _card(body)
    _lbl(card, "Approve or reject a pending maintenance request",
         font=FN_SMALL, fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w", pady=(0,6))
    req = field(card, "Request ID",              accent=ACCENT_GREEN)
    sta = field(card, "New Status (Approved / Rejected)", accent=ACCENT_GREEN)
    def update():
        try:
            cursor.execute("UPDATE MAINTENANCE_REQUEST SET ApprovalStatus=%s WHERE RequestID=%s",
                (sta.get(), req.get()))
            conn.commit(); messagebox.showinfo("Updated","Status updated!"); win.destroy()
        except Exception as ex: messagebox.showerror("Error", str(ex))
    action_btn(card, "✓  Update Status", ACCENT_GREEN, update)


def raise_maintenance_request():
    win, body = _form_window("Raise Maintenance Request", ACCENT_GOLD)
    card = _card(body)
    _lbl(card, "Submit a new maintenance ticket",
         font=FN_SMALL, fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w", pady=(0,6))
    labels  = ["Request ID","Date (YYYY-MM-DD)","Request Type","Station ID","Vendor ID"]
    entries = []
    for i, lbl in enumerate(labels):
        e = field(card, lbl, accent=ACCENT_GOLD)
        if i == 0:
            e.config(state="normal"); e.insert(0, get_next_request_id()); e.config(state="readonly")
        entries.append(e)
    def submit():
        try:
            cursor.execute("INSERT INTO MAINTENANCE_REQUEST VALUES (%s,%s,%s,'Pending',%s,%s)",
                tuple(e.get() for e in entries))
            conn.commit(); messagebox.showinfo("Success","Request raised!"); win.destroy()
        except Exception as ex: messagebox.showerror("Database Error", str(ex))
    action_btn(card, "✓  Raise Request", ACCENT_GOLD, submit)

def analytics_dashboard():
    win, body = _form_window("Analytics", ACCENT_GOLD)

    def owner_usage():
        create_table_window("Power Usage by Owner",
            ("Owner","Station","City","Total Power (kWh)"),
            """SELECT E.Name, S.StationName, S.City, SUM(P.EnergyConsumed)
               FROM PAYMENT P JOIN BOOKING B ON P.BookingID=B.BookingID
               JOIN VEHICLE V ON B.VehicleID=V.VehicleID
               JOIN EV_OWNER E ON V.OwnerID=E.OwnerID
               JOIN CHARGING_SLOT CS ON B.SlotID=CS.SlotID
               JOIN CHARGING_STATION S ON CS.StationID=S.StationID
               GROUP BY E.Name, S.StationName, S.City""")

    def top_station():
        create_table_window("Top Station by Usage",("Station","Total Power (kWh)"),
            """SELECT S.StationName, SUM(P.EnergyConsumed) AS Total
               FROM PAYMENT P JOIN BOOKING B ON P.BookingID=B.BookingID
               JOIN CHARGING_SLOT CS ON B.SlotID=CS.SlotID
               JOIN CHARGING_STATION S ON CS.StationID=S.StationID
               GROUP BY S.StationName ORDER BY Total DESC LIMIT 1""")

    def top_owner():
        create_table_window("Top EV Owner",("Owner","Total Power (kWh)"),
            """SELECT E.Name, SUM(P.EnergyConsumed) AS Total
               FROM PAYMENT P JOIN BOOKING B ON P.BookingID=B.BookingID
               JOIN VEHICLE V ON B.VehicleID=V.VehicleID
               JOIN EV_OWNER E ON V.OwnerID=E.OwnerID
               GROUP BY E.Name ORDER BY Total DESC LIMIT 1""")

    reports = [
        ("📊","Power Usage by Owner",  ACCENT_TEAL,  owner_usage),
        ("🏆","Top Station by Usage",  ACCENT_GREEN, top_station),
        ("👑","Top EV Owner",          ACCENT_GOLD,  top_owner),
    ]
    for icon, label, color, cb in reports:
        card = _card(body, pady=8)
        row = tk.Frame(card, bg=BG_CARD); row.pack(fill="x")
        _lbl(row, icon,  font=("Helvetica",20), fg=color, bg=BG_CARD).pack(side="left", padx=(0,14))
        col2 = tk.Frame(row, bg=BG_CARD); col2.pack(side="left")
        _lbl(col2, label, font=FN_SUBHEAD, fg=TEXT_H1, bg=BG_CARD).pack(anchor="w")
        b = ghost_btn(card, "→  View Report", color, cb)
        b.pack(anchor="e", pady=(10,0))

def update_power():
    win, body = _form_window("Update Power Allocation", ACCENT_GREEN)
    card = _card(body)
    _lbl(card, "Update the available power for a charging station",
         font=FN_SMALL, fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w", pady=(0, 6))

    op_e  = field(card, "Operator ID",         accent=ACCENT_GREEN)
    sid_e = field(card, "Station ID",          accent=ACCENT_GREEN)
    cur_row = tk.Frame(card, bg=BG_CARD); cur_row.pack(fill="x", pady=(10, 0))
    _lbl(cur_row, "Current Power:", font=FN_LABEL, fg=TEXT_BODY, bg=BG_CARD).pack(side="left")
    cur_val_lbl = _lbl(cur_row, "—", font=("Helvetica", 11, "bold"),
                       fg=ACCENT_GREEN, bg=BG_CARD)
    cur_val_lbl.pack(side="left", padx=8)

    pwr_e = field(card, "New Available Power", accent=ACCENT_GREEN)

    snapshot = {"value": None}

    def on_sid_focusout(event):
        sid = sid_e.get().strip()
        if not sid:
            return
        try:
            cursor.execute(
                "SELECT AvailablePower FROM POWER_ALLOCATION WHERE StationID = %s",
                (sid,)
            )
            row = cursor.fetchone()
            if row:
                snapshot["value"] = row[0]
                cur_val_lbl.config(text=str(row[0]))
        except:
            pass

    sid_e.bind("<FocusOut>", on_sid_focusout)

    def submit():
        op_id   = op_e.get().strip()
        sid     = sid_e.get().strip()
        new_val = pwr_e.get().strip()
        old_val = snapshot["value"]

        if not op_id or not sid or not new_val:
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
            return

        c = None
        try:
            c = mysql.connector.connect(
                host="localhost", user="root",
                password="root123", database="ev_charging_db"
            )
            c.autocommit = False
            cu = c.cursor()

            cu.execute(
                "SELECT OperatorName FROM charging_operator WHERE OperatorID = %s",
                (op_id,)
            )
            op_row = cu.fetchone()
            if op_row is None:
                c.rollback()
                messagebox.showerror("Invalid Operator",
                    f"No operator found with ID {op_id}.")
                return
            op_name = op_row[0]

            # START TRANSACTION + acquire row lock
            cu.execute("START TRANSACTION")
            cu.execute(
                "SELECT AvailablePower FROM POWER_ALLOCATION "
                "WHERE StationID = %s FOR UPDATE",
                (sid,)
            )

            time.sleep(3)
            row = cu.fetchone()

            if row is None:
                c.rollback()
                messagebox.showerror("Not Found",
                    f"No station found with ID {sid}.")
                return

            current_in_db = row[0]

            # Conflict check
            if old_val is not None and str(current_in_db) != str(old_val):
                c.rollback()
                messagebox.showerror(
                    "Update Conflict",
                    f"Operator: {op_name} (ID: {op_id})\n\n"
                    f"This station was already updated by another operator.\n\n"
                    f"Value when you opened this form:  {old_val}\n"
                    f"Current value in database:             {current_in_db}\n\n"
                    f"Your update has been cancelled.\n"
                    f"Please review the new value and try again."
                )
                cur_val_lbl.config(text=str(current_in_db))
                snapshot["value"] = current_in_db
                return

            # Apply update + COMMIT 
            cu.execute(
                "UPDATE POWER_ALLOCATION SET AvailablePower = %s, LastUpdated = NOW() WHERE StationID = %s",
                (new_val, sid)
            )
            c.commit()

            messagebox.showinfo("Success",
                f"Operator {op_name} (ID: {op_id}) successfully updated\n"
                f"Station {sid} power to {new_val}.")
            win.destroy()

        except mysql.connector.errors.OperationalError:
            try: c.rollback()
            except: pass
            messagebox.showerror("Station Busy",
                "Another operator is currently updating this station.\n"
                "Please wait a moment and try again.")

        except Exception as ex:
            try: c.rollback()
            except: pass
            messagebox.showerror("Error", str(ex))

        finally:
            try: c.close()
            except: pass

    action_btn(card, "✓  Update Power", ACCENT_GREEN, submit)

def owner_dashboard():
    _sidebar_dashboard("EV Owner Dashboard","🚗",ACCENT_GREEN,[
        ("🚗","Register Vehicle",    register_vehicle),
        ("📅","Book Charging Slot",  book_slot),
        ("🔍","Available Slots",     view_slots),
        ("📋","My Bookings",         view_my_bookings),
        ("💳","Process Payment",     process_payment),
    ])

def operator_dashboard():
    _sidebar_dashboard("Operator Dashboard","🏭",ACCENT_TEAL,[
        ("📋","Station Bookings",          view_station_bookings),
        ("💰","Revenue Report",            revenue_station),
        ("📊","Analytics",                 analytics_dashboard),
        ("⚡","Update Power",              update_power),
        ("🔧","Raise Maintenance Req.",    raise_maintenance_request),
    ])

def admin_dashboard():
    _sidebar_dashboard("Admin Dashboard","🛡",ACCENT_GOLD,[
        ("👤","Register Owner",      register_owner),
        ("🚗","Register Vehicle",    register_vehicle),
        ("📅","Book Slot",           book_slot),
        ("📋","All Bookings",        view_bookings),
        ("💳","Process Payment",     process_payment),
        ("💰","Revenue Report",      revenue_station),
    ])

def vendor_dashboard():
    _sidebar_dashboard("Vendor Dashboard","🔧",ACCENT_PURPLE,[
        ("📋","View Requests",         view_requests),
        ("✅","Update Request Status", update_request_status),
    ])

root = tk.Tk()
root.title("EV Charging Management System")
root.geometry("960x640")
root.configure(bg=BG_BASE)
root.resizable(True, True)
root.minsize(820, 580)

main_frame = tk.Frame(root, bg=BG_BASE)
main_frame.pack(fill="both", expand=True)

left = tk.Frame(main_frame, bg=BG_PANEL, width=400)
left.pack(side="left", fill="y")
left.pack_propagate(False)

tk.Frame(left, bg=ACCENT_BLUE, height=3).pack(fill="x")

brand_c = tk.Canvas(left, bg=BG_PANEL, width=400, height=280, highlightthickness=0)
brand_c.pack()

brand_c.create_oval(260,-40,430,130, outline="#1E3A5A",width=1,fill="")
brand_c.create_oval(280,-20,410,110, outline="#1B4F72",width=1,fill="")
brand_c.create_oval(-50,180,150,380, outline="#1E3A5A",width=1,fill="")
brand_c.create_oval(100,210,280,390, outline=ACCENT_BLUE,width=1,fill="")
brand_c.create_text(200,105,text="⚡",font=("Helvetica",60),fill=ACCENT_BLUE,anchor="center")
brand_c.create_text(200,180,text="ChargeSync",font=("Georgia",24,"bold"),fill=TEXT_H1,anchor="center")
brand_c.create_text(200,212,text="EV Charging Management System",font=("Georgia",12),fill=TEXT_BODY,anchor="center")

tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=32, pady=0)

features = [
    ("🔌","Smart Slot Booking",     "Reserve stations in real time"),
    ("💳","Integrated Payments",    "Auto-calculated billing at ₹20/kWh"),
    ("📊","Analytics & Reports",    "Usage insights per owner & station"),
    ("🔒","ACID Transactions",      "Conflict-safe concurrent DB updates"),
]
feat_f = tk.Frame(left, bg=BG_PANEL, padx=36, pady=18)
feat_f.pack(fill="x")

for icon, title, sub in features:
    row = tk.Frame(feat_f, bg=BG_PANEL, pady=8); row.pack(fill="x")
    _lbl(row, icon, font=("Helvetica",18), fg=ACCENT_BLUE, bg=BG_PANEL).pack(side="left",padx=(0,16))
    col2 = tk.Frame(row, bg=BG_PANEL); col2.pack(side="left")
    _lbl(col2, title, font=("Helvetica",10,"bold"), fg=TEXT_H2, bg=BG_PANEL).pack(anchor="w")
    _lbl(col2, sub,   font=FN_SMALL,                fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")

tk.Frame(left, bg=BG_PANEL).pack(fill="y", expand=True)
_sep(left, BORDER, padx=32)
_lbl(left,"Smarter charging. Greener future.",font=("Georgia",9,"italic"),fg=TEXT_MUTED,bg=BG_PANEL).pack(pady=10)

right_f = tk.Frame(main_frame, bg=BG_BASE)
right_f.pack(side="left", fill="both", expand=True)

tk.Frame(right_f, bg=ACCENT_BLUE, height=3).pack(fill="x")

center = tk.Frame(right_f, bg=BG_BASE)
center.pack(expand=True, fill="both", padx=52, pady=30)

_lbl(center,"Select Your Role",font=("Georgia",22,"bold"),fg=TEXT_H1,bg=BG_BASE).pack(anchor="w")
_lbl(center,"Choose a dashboard to continue",font=FN_BODY,fg=TEXT_BODY,bg=BG_BASE).pack(anchor="w",pady=(4,0))
_sep(center, BORDER, pady=18)

roles = [
    ("🚗","EV Owner",  "Register vehicles, book slots & manage payments", ACCENT_GREEN,  owner_dashboard),
    ("🏭","Operator",  "Monitor stations, revenue & maintenance",          ACCENT_TEAL,   operator_dashboard),
    ("🛡","Admin",     "Full system access — owners, bookings & billing",  ACCENT_GOLD,   admin_dashboard),
    ("🔧","Vendor",    "View and update maintenance requests",              ACCENT_PURPLE, vendor_dashboard),
]

for icon, role, desc, color, cmd in roles:
    outer = tk.Frame(center, bg=BORDER, padx=1, pady=1)
    outer.pack(fill="x", pady=7)
    card_bg = BG_CARD

    card = tk.Frame(outer, bg=card_bg, padx=20, pady=14, cursor="hand2")
    card.pack(fill="x")

    stripe = tk.Frame(outer, bg=color, width=4)
    stripe.place(relx=0, rely=0, relheight=1)

    text_col = tk.Frame(card, bg=card_bg)
    text_col.pack(side="left", fill="x", expand=True)
    _lbl(text_col, f"  {icon}  {role}", font=("Helvetica",13,"bold"), fg=TEXT_H1, bg=card_bg).pack(anchor="w")
    _lbl(text_col, f"  {desc}",         font=FN_SMALL,                fg=TEXT_BODY, bg=card_bg).pack(anchor="w",pady=(2,0))

    arr_lbl = _lbl(card, "›", font=("Helvetica",22,"bold"), fg=color, bg=card_bg)
    arr_lbl.pack(side="right", padx=(0,4))

    def _bind_card(frame, c=color, fn=cmd, a=arr_lbl):
        hover_bg = "#1E2D42"
        all_widgets = [frame] + list(frame.winfo_children())
        for ch in frame.winfo_children():
            all_widgets += list(ch.winfo_children())

        def enter(e):
            for w in all_widgets:
                try: w.config(bg=hover_bg)
                except: pass
        def leave(e):
            for w in all_widgets:
                try: w.config(bg=BG_CARD)
                except: pass
        def click(e): fn()
        for w in all_widgets:
            w.bind("<Enter>", enter); w.bind("<Leave>", leave); w.bind("<Button-1>", click)

    _bind_card(card)

_sep(center, BORDER, pady=(18,10))
exit_row = tk.Frame(center, bg=BG_BASE); exit_row.pack(fill="x")
exit_b = tk.Button(exit_row, text="Exit Application", font=FN_BTN,
    bg=BG_CARD, fg=ACCENT_RED, activebackground=ACCENT_RED, activeforeground=BG_BASE,
    relief="flat", bd=0, cursor="hand2", padx=20, pady=8,
    highlightthickness=1, highlightbackground=ACCENT_RED,
    command=root.destroy)
exit_b.pack(side="right")
exit_b.bind("<Enter>", lambda e: exit_b.config(bg=ACCENT_RED, fg=BG_BASE))
exit_b.bind("<Leave>", lambda e: exit_b.config(bg=BG_CARD,    fg=ACCENT_RED))

root.mainloop()
conn.close()
