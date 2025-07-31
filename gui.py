import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from models import Property
from db import session
import csv
import json

class PropertyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("سیستم ثبت اطلاعات املاک")
        self.root.geometry("900x600")

        self.selected_property_id = None

        self.notebook = ttk.Notebook(root)
        self.tab_form = tk.Frame(self.notebook)
        self.tab_report = tk.Frame(self.notebook)
        self.tab_about = tk.Frame(self.notebook)
        self.tab_architectural = tk.Frame(self.notebook)
        self.tab_building = tk.Frame(self.notebook)
        self.tab_hse = tk.Frame(self.notebook)


        self.notebook.add(self.tab_form, text="فرم ثبت ملک")
        self.notebook.add(self.tab_architectural, text="ضوابط معماری")
        self.notebook.add(self.tab_building, text="ضوابط سازه ای")
        self.notebook.add(self.tab_hse, text="HSE")
        self.notebook.add(self.tab_report, text="گزارش و جستجو")
        self.notebook.add(self.tab_about, text="درباره")
        self.notebook.pack(fill="both", expand=True)

        self.build_form_tab()
        self.build_report_tab()
        self.build_about_tab()  # Build the about tab
        self.build_architectural_tab()
        self.build_building_tab()
        self.build_hse_tab()



    def build_about_tab(self):
        """Build the about tab with software information"""
        # Create a frame for centering content
        center_frame = tk.Frame(self.tab_about)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title_label = tk.Label(
            center_frame, 
            text="درباره نرم‌افزار",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))
        
        # Software description
        description_text = """نسخه تستی نرم‌افزار ثبت و ویرایش اطلاعات پرونده‌های 
معاونت معماری و شهرسازی 
شهرداری ساری

این نرم‌افزار جهت مدیریت و نگهداری اطلاعات املاک و پرونده‌های 
مربوط به معاونت معماری و شهرسازی طراحی شده است.

ایده پرداز:
مهندس امین باغبان مازندرانی
طراحی و توسعه:
محسن فرقانی
github.com/mohsenfor"""

        description_label = tk.Label(
            center_frame,
            text=description_text,
            font=("Arial", 11),
            justify="center",
            fg="#34495e",
            wraplength=600
        )
        description_label.pack(pady=(0, 30))
        
        # Version info
        version_frame = tk.Frame(center_frame)
        version_frame.pack(pady=(0, 20))
        
        version_label = tk.Label(
            version_frame,
            text="نسخه: 1.0.0 (تستی)",
            font=("Nazanin", 10),
            fg="#7f8c8d"
        )
        version_label.pack()
        
        # Developer info
        developer_label = tk.Label(
            version_frame,
            text="توسعه داده شده برای معاونت معماری و شهرسازی",
            font=("Arial", 9),
            fg="#95a5a6"
        )
        developer_label.pack(pady=(5, 0))
        
        # Add a decorative separator
        separator = tk.Frame(center_frame, height=2, bg="#bdc3c7")
        separator.pack(fill="x", pady=(20, 10))
        
        # Copyright info
        copyright_label = tk.Label(
            center_frame,
            text="© ۱۴۰۳ - تمامی حقوق محفوظ است",
            font=("Arial", 8),
            fg="#95a5a6"
        )
        copyright_label.pack()


    def build_form_tab(self):
        canvas = tk.Canvas(self.tab_form)
        scrollbar = tk.Scrollbar(self.tab_form, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas)

        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.build_form()

    def build_form(self):
        row = 0
        self.owner_name = self._add_field("نام مالک", row); row += 1
        self.address = self._add_field("آدرس ملک", row); row += 1
        tk.Label(self.scroll_frame, text="منطقه:").grid(row=row, column=0, sticky='e')
        self.region = ttk.Combobox(self.scroll_frame, values=list(range(1, 5)))
        self.region.grid(row=row, column=1); row += 1
        self.memari_number = self._add_field("شماره ممیزی", row); row += 1
        self.utm_x = self._add_field("UTM X", row); row += 1
        self.utm_y = self._add_field("UTM Y", row); row += 1
        self.sabti_code = self._add_field("پلاک ثبتی", row); row += 1

        row = self._add_section("آیا ملک پروانه دارد؟", row, "permit", ["کاربری", "سطح اشغال", "تعداد طبقات", "تراکم", "مساحت تعریض"])
        row = self._add_section("آیا ملک پایان‌کار دارد؟", row, "final", ["متراژ کلی سقف‌ها", "کاربری موجود", "تعداد طبقات", "کاربری مصوب", "سطح اشغال موجود", "سطح اشغال مصوب"])
        row = self._add_section("آیا رای کمیسیون ماده ۱۰۰ دارد؟", row, "komission", ["شماره سقف", "مساحت سقف موجود", "نوع سازه", "کاربری موجود", "سطح اشغال", "تراکم", "پهنه بندی", "رای صادره", "توضیحات رای صادره", "تاریخ ثبت گزارش", "تاریخ ارسال به کمیسیون"])
        row = self._add_section("آیا گواهی عدم خلاف دارد؟", row, "cert", ["تاریخ گواهی", "متراژ", "طبقات", "پارکینگ", "کاربری"])
        row = self._add_section("ارجاع ناظر به شورا انتظامی", row, "nazir", ["تاریخ", "شماره", "موضوع"])
        row = self._add_section("اخطاریه سد معبر", row, "sedmamno", ["تاریخ", "شماره", "موضوع"])

        tk.Button(self.scroll_frame, text="ذخیره اطلاعات", command=self.save_data).grid(row=row+1, column=0, columnspan=2, pady=20)

    def build_report_tab(self):
        tk.Label(self.tab_report, text="نام مالک:").grid(row=0, column=0)
        self.search_owner = tk.Entry(self.tab_report)
        self.search_owner.grid(row=0, column=1)

        self.search_region = tk.Entry(self.tab_report)
        tk.Label(self.tab_report, text="منطقه:").grid(row=0, column=2)
        self.search_region.grid(row=0, column=3)

        tk.Label(self.tab_report, text="کد ممیزی:").grid(row=1, column=0)
        self.search_memari = tk.Entry(self.tab_report)
        self.search_memari.grid(row=1, column=1)

        self.search_permit = tk.BooleanVar()
        tk.Checkbutton(self.tab_report, text="پروانه دارد", variable=self.search_permit).grid(row=1, column=2)

        self.search_final = tk.BooleanVar()
        tk.Checkbutton(self.tab_report, text="پایان‌کار دارد", variable=self.search_final).grid(row=1, column=3)

        self.search_cert = tk.BooleanVar()
        tk.Checkbutton(self.tab_report, text="گواهی دارد", variable=self.search_cert).grid(row=1, column=4)

        tk.Button(self.tab_report, text="جستجو", command=self.run_query).grid(row=2, column=0)
        tk.Button(self.tab_report, text="خروجی CSV", command=self.export_csv).grid(row=2, column=1)
        tk.Button(self.tab_report, text="ویرایش/حذف", command=self.edit_or_delete_property).grid(row=2, column=2)

        self.tree = ttk.Treeview(self.tab_report, columns=("id", "owner", "address", "region", "memari", "permit", "final", "cert"), show='headings')
        self.tree.heading("id", text="ID")
        self.tree.heading("owner", text="نام مالک")
        self.tree.heading("address", text="آدرس")
        self.tree.heading("region", text="منطقه")
        self.tree.heading("memari", text="کد ممیزی")
        self.tree.heading("permit", text="پروانه")
        self.tree.heading("final", text="پایان‌کار")
        self.tree.heading("cert", text="گواهی")
        self.tree.grid(row=3, column=0, columnspan=6, sticky="nsew")

        self.tab_report.grid_rowconfigure(3, weight=1)
        self.tab_report.grid_columnconfigure(1, weight=1)

    def edit_or_delete_property(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("انتخاب نشده", "لطفاً یک ملک را از جدول انتخاب کنید.")
            return

        item = self.tree.item(selected[0])
        prop_id = item['values'][0]

        def delete():
            if messagebox.askyesno("حذف ملک", "آیا از حذف این ملک مطمئن هستید؟"):
                prop = session.query(Property).get(prop_id)
                session.delete(prop)
                session.commit()
                messagebox.showinfo("حذف شد", "ملک با موفقیت حذف شد.")
                self.run_query()

        def edit():
            self.selected_property_id = prop_id
            prop = session.query(Property).get(prop_id)
            if prop:
                self.fill_form_fields(prop)
                self.notebook.select(self.tab_form)
            else:
                messagebox.showerror("خطا", "ملک مورد نظر یافت نشد.")

        win = tk.Toplevel(self.root)
        win.title("ویرایش یا حذف")
        tk.Button(win, text="ویرایش", width=20, command=lambda:[win.destroy(), edit()]).pack(pady=5)
        tk.Button(win, text="حذف", width=20, command=lambda:[win.destroy(), delete()]).pack(pady=5)

    def fill_form_fields(self, prop):
        self.owner_name.delete(0, tk.END)
        self.owner_name.insert(0, prop.owner_name or "")
        self.address.delete(0, tk.END)
        self.address.insert(0, prop.address or "")
        self.region.set(str(prop.region or ""))
        self.memari_number.delete(0, tk.END)
        self.memari_number.insert(0, prop.memari_number or "")
        self.utm_x.delete(0, tk.END)
        self.utm_x.insert(0, str(prop.utm_x or ""))
        self.utm_y.delete(0, tk.END)
        self.utm_y.insert(0, str(prop.utm_y or ""))
        self.sabti_code.delete(0, tk.END)
        self.sabti_code.insert(0, prop.sabti_code or "")

        if hasattr(prop, 'has_architectural') and prop.has_architectural:
            self.architectural_var.set(1)
            self.toggle_architectural_fields()
            if hasattr(prop, 'architectural_data') and prop.architectural_data:
                try:
                    self.architectural_data = json.loads(prop.architectural_data)
                    if self.architectural_data:
                        first_ceiling = list(self.architectural_data.keys())[0]
                        self.ceiling_number.set(first_ceiling)
                        self.load_ceiling_data()
                except:
                    self.architectural_data = {}

    def _add_field(self, label, row):
        tk.Label(self.scroll_frame, text=label + ":").grid(row=row, column=0, sticky='e', padx=5, pady=2)
        entry = tk.Entry(self.scroll_frame, width=40)
        entry.grid(row=row, column=1, padx=5, pady=2)
        return entry

    def _add_section(self, label, row, attr_name, field_list):
        setattr(self, f"{attr_name}_var", tk.IntVar())
        check = tk.Checkbutton(self.scroll_frame, text=label, variable=getattr(self, f"{attr_name}_var"), command=lambda: self._toggle_fields(attr_name))
        check.grid(row=row, column=0, columnspan=2, pady=4)
        row += 1

        fields = {}
        for f in field_list:
            tk.Label(self.scroll_frame, text=f + ":").grid(row=row, column=0, sticky='e', padx=5)
            entry = tk.Entry(self.scroll_frame, width=40)
            entry.grid(row=row, column=1, padx=5)
            entry.grid_remove()
            fields[f] = entry
            row += 1
        setattr(self, f"{attr_name}_fields", fields)
        return row

    def _toggle_fields(self, attr_name):
        var = getattr(self, f"{attr_name}_var")
        fields = getattr(self, f"{attr_name}_fields")
        for entry in fields.values():
            entry.grid() if var.get() else entry.grid_remove()

    def save_data(self):
        try:
            # Check if we're updating an existing property
            if self.selected_property_id:
                prop = session.query(Property).get(self.selected_property_id)
            else:
                prop = Property()

            # Basic fields
            prop.owner_name = self.owner_name.get()
            prop.address = self.address.get()
            prop.region = int(self.region.get()) if self.region.get() else None
            prop.memari_number = self.memari_number.get()
            prop.utm_x = float(self.utm_x.get()) if self.utm_x.get() else None
            prop.utm_y = float(self.utm_y.get()) if self.utm_y.get() else None
            prop.sabti_code = self.sabti_code.get()
            prop.last_modified = datetime.today().date()
            # Architectural standards section
            prop.has_architectural = bool(self.architectural_var.get())
            if prop.has_architectural:
                # Save current ceiling data before saving to database
                self.save_current_ceiling_data()
                
                # Convert architectural_data to JSON string for database storage
                import json
                prop.architectural_data = json.dumps(self.architectural_data, ensure_ascii=False)
                prop.architectural_last_modified = datetime.today().date()


            # Building standards section
            #prop.has_building = bool(self.building_var.get())
            #if prop.has_building:
                # Save current ceiling data before saving to database
                #self.save_current_ceiling_data()
                
                # Convert building_data to JSON string for database storage
                #import json
                #prop.building_data = json.dumps(self.building_data, ensure_ascii=False)
                #prop.building_last_modified = datetime.today().date()

            # HSE section
            #prop.has_hse = bool(self.hse_var.get())
            #if prop.has_hse:
                #self.save_current_hse_ceiling_data()
                #import json
                #prop.hse_data = json.dumps(self.hse_data, ensure_ascii=False)
                #prop.hse_last_modified = datetime.today().date()



            # Permit section
            prop.has_permit = bool(self.permit_var.get())
            if prop.has_permit:
                f = self.permit_fields
                prop.permit_usage = f["کاربری"].get() or None
                prop.permit_occupancy = float(f["سطح اشغال"].get()) if f["سطح اشغال"].get() else None
                prop.permit_floors = int(f["تعداد طبقات"].get()) if f["تعداد طبقات"].get() else None
                prop.permit_density = float(f["تراکم"].get()) if f["تراکم"].get() else None
                prop.widening_area = float(f["مساحت تعریض"].get()) if f["مساحت تعریض"].get() else None

            # Final section
            prop.has_finalization = bool(self.final_var.get())
            if prop.has_finalization:
                f = self.final_fields
                prop.final_total_area = float(f["متراژ کلی سقف‌ها"].get()) if f["متراژ کلی سقف‌ها"].get() else None
                prop.final_current_usage = f["کاربری موجود"].get() or None
                prop.final_floors = int(f["تعداد طبقات"].get()) if f["تعداد طبقات"].get() else None
                prop.final_approved_usage = f["کاربری مصوب"].get() or None
                prop.final_current_occupancy = float(f["سطح اشغال موجود"].get()) if f["سطح اشغال موجود"].get() else None
                prop.final_approved_occupancy = float(f["سطح اشغال مصوب"].get()) if f["سطح اشغال مصوب"].get() else None

            # Komission section
            prop.has_komission = bool(self.komission_var.get())
            if prop.has_komission:
                f = self.komission_fields
                prop.komission_roof_no = f["شماره سقف"].get() or None
                prop.komission_roof_area = float(f["مساحت سقف موجود"].get()) if f["مساحت سقف موجود"].get() else None
                prop.komission_structure_type = f["نوع سازه"].get() or None
                prop.komission_current_usage = f["کاربری موجود"].get() or None
                prop.komission_occupancy = float(f["سطح اشغال"].get()) if f["سطح اشغال"].get() else None
                prop.komission_density = float(f["تراکم"].get()) if f["تراکم"].get() else None
                prop.komission_zone = f["پهنه بندی"].get() or None
                prop.komission_verdict = f["رای صادره"].get() or None
                prop.komission_description = f["توضیحات رای صادره"].get() or None
                
                # Handle dates
                report_date_str = f["تاریخ ثبت گزارش"].get()
                if report_date_str:
                    try:
                        prop.komission_report_date = datetime.strptime(report_date_str, "%Y-%m-%d").date()
                    except ValueError:
                        prop.komission_report_date = None
                
                sent_date_str = f["تاریخ ارسال به کمیسیون"].get()
                if sent_date_str:
                    try:
                        prop.komission_sent_date = datetime.strptime(sent_date_str, "%Y-%m-%d").date()
                    except ValueError:
                        prop.komission_sent_date = None

            # Certificate section
            prop.has_no_conflict_cert = bool(self.cert_var.get())
            if prop.has_no_conflict_cert:
                f = self.cert_fields
                cert_date_str = f["تاریخ گواهی"].get()
                if cert_date_str:
                    try:
                        prop.cert_date = datetime.strptime(cert_date_str, "%Y-%m-%d").date()
                    except ValueError:
                        prop.cert_date = None
                
                prop.cert_area = float(f["متراژ"].get()) if f["متراژ"].get() else None
                prop.cert_floors = int(f["طبقات"].get()) if f["طبقات"].get() else None
                prop.cert_parking = int(f["پارکینگ"].get()) if f["پارکینگ"].get() else None
                prop.cert_usage = f["کاربری"].get() or None

            # Nazir section
            prop.has_nazir_referral = bool(self.nazir_var.get())
            if prop.has_nazir_referral:
                f = self.nazir_fields
                nazir_date_str = f["تاریخ"].get()
                if nazir_date_str:
                    try:
                        prop.nazir_date = datetime.strptime(nazir_date_str, "%Y-%m-%d").date()
                    except ValueError:
                        prop.nazir_date = None
                
                prop.nazir_number = f["شماره"].get() or None
                prop.nazir_subject = f["موضوع"].get() or None

            # Sedmamno section
            prop.has_sedmamno = bool(self.sedmamno_var.get())
            if prop.has_sedmamno:
                f = self.sedmamno_fields
                sedmamno_date_str = f["تاریخ"].get()
                if sedmamno_date_str:
                    try:
                        prop.sedmamno_date = datetime.strptime(sedmamno_date_str, "%Y-%m-%d").date()
                    except ValueError:
                        prop.sedmamno_date = None
                
                prop.sedmamno_number = f["شماره"].get() or None
                prop.sedmamno_subject = f["موضوع"].get() or None

            

            # Add to session only if it's a new property
            if not self.selected_property_id:
                session.add(prop)
            
            session.commit()
            
            # Reset the selected property ID and clear form
            self.selected_property_id = None
            self.clear_form()
            
            messagebox.showinfo("ثبت موفق", "اطلاعات با موفقیت ذخیره شد.")
            
        except Exception as e:
            session.rollback()
            messagebox.showerror("خطا", f"خطایی رخ داد:\n{str(e)}")

    def clear_form(self):
        """Clear all form fields"""
        self.owner_name.delete(0, tk.END)
        self.address.delete(0, tk.END)
        self.region.set("")
        self.memari_number.delete(0, tk.END)
        self.utm_x.delete(0, tk.END)
        self.utm_y.delete(0, tk.END)
        self.sabti_code.delete(0, tk.END)

        # Clear all sections
        for section in ["permit", "final", "komission", "cert", "nazir", "sedmamno"]:
            var = getattr(self, f"{section}_var")
            fields = getattr(self, f"{section}_fields")
            var.set(0)
            for entry in fields.values():
                entry.delete(0, tk.END)
                entry.grid_remove()

        # Clear architectural section
        if hasattr(self, 'architectural_var'):
            self.architectural_var.set(0)
            self.architectural_data = {}
            if hasattr(self, 'ceiling_number'):
                self.ceiling_number.set("")
            self.toggle_architectural_fields()

        # Clear building section
        if hasattr(self, 'building_var'):
            self.building_var.set(0)
            self.building_data = {}	
            if hasattr(self, 'ceiling_number'):
                self.ceiling_number.set("")
            self.toggle_building_fields()

        
        # Clear HSE section
        if hasattr(self, 'hse_var'):
            self.hse_var.set(0)
            self.hse_data = {}
            if hasattr(self, 'hse_ceiling_number'):
                self.hse_ceiling_number.set("")
            self.toggle_hse_fields()



    def build_report_tab(self):
        tk.Label(self.tab_report, text="نام مالک:").grid(row=0, column=0)
        self.search_owner = tk.Entry(self.tab_report)
        self.search_owner.grid(row=0, column=1)

        self.search_region = tk.Entry(self.tab_report)
        tk.Label(self.tab_report, text="منطقه:").grid(row=0, column=2)
        self.search_region.grid(row=0, column=3)

        tk.Label(self.tab_report, text="کد ممیزی:").grid(row=1, column=0)
        self.search_memari = tk.Entry(self.tab_report)
        self.search_memari.grid(row=1, column=1)

        self.search_permit = tk.BooleanVar()
        tk.Checkbutton(self.tab_report, text="پروانه دارد", variable=self.search_permit).grid(row=1, column=2)

        self.search_final = tk.BooleanVar()
        tk.Checkbutton(self.tab_report, text="پایان‌کار دارد", variable=self.search_final).grid(row=1, column=3)

        self.search_cert = tk.BooleanVar()
        tk.Checkbutton(self.tab_report, text="گواهی دارد", variable=self.search_cert).grid(row=1, column=4)

        tk.Button(self.tab_report, text="جستجو", command=self.run_query).grid(row=2, column=0)
        tk.Button(self.tab_report, text="خروجی CSV", command=self.export_csv).grid(row=2, column=1)
        tk.Button(self.tab_report, text="ویرایش/حذف", command=self.edit_or_delete_property).grid(row=2, column=2)

        # Create the treeview (only once, here in build_report_tab)
        self.tree = ttk.Treeview(self.tab_report, columns=("id", "owner", "address", "region", "memari", "permit", "final", "cert"), show='headings')
        self.tree.heading("id", text="ID")
        self.tree.heading("owner", text="نام مالک")
        self.tree.heading("address", text="آدرس")
        self.tree.heading("region", text="منطقه")
        self.tree.heading("memari", text="کد ممیزی")
        self.tree.heading("permit", text="پروانه")
        self.tree.heading("final", text="پایان‌کار")
        self.tree.heading("cert", text="گواهی")
        self.tree.grid(row=3, column=0, columnspan=6, sticky="nsew")

        self.tab_report.grid_rowconfigure(3, weight=1)
        self.tab_report.grid_columnconfigure(1, weight=1)

    

    def edit_or_delete_property(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("انتخاب نشده", "لطفاً یک ملک را از جدول انتخاب کنید.")
            return

        item = self.tree.item(selected[0])
        prop_id = item['values'][0]
        print("Selected ID:", prop_id)

        def delete():
            if messagebox.askyesno("حذف ملک", "آیا از حذف این ملک مطمئن هستید؟"):
                prop = session.query(Property).get(prop_id)
                if prop:
                    session.delete(prop)
                    session.commit()
                    messagebox.showinfo("حذف شد", "ملک با موفقیت حذف شد.")
                    self.run_query()

        def edit():
            self.selected_property_id = prop_id
            prop = session.query(Property).get(prop_id)
            if prop:
                self.fill_form_fields(prop)
                self.notebook.select(self.tab_form)

        win = tk.Toplevel(self.root)
        win.title("ویرایش یا حذف")
        tk.Button(win, text="ویرایش", width=20, command=lambda:[win.destroy(), edit()]).pack(pady=5)
        tk.Button(win, text="حذف", width=20, command=lambda:[win.destroy(), delete()]).pack(pady=5)

    def fill_form_fields(self, prop):
        """Fill form fields with property data for editing"""
        # Clear form first
        self.clear_form()
        
        # Basic fields
        self.owner_name.insert(0, prop.owner_name or "")
        self.address.insert(0, prop.address or "")
        self.region.set(str(prop.region or ""))
        self.memari_number.insert(0, prop.memari_number or "")
        self.utm_x.insert(0, str(prop.utm_x or ""))
        self.utm_y.insert(0, str(prop.utm_y or ""))
        self.sabti_code.insert(0, prop.sabti_code or "")

        # Permit section
        if hasattr(prop, 'has_permit') and prop.has_permit:
            self.permit_var.set(1)
            self._toggle_fields("permit")
            f = self.permit_fields
            f["کاربری"].insert(0, getattr(prop, 'permit_usage', "") or "")
            f["سطح اشغال"].insert(0, str(getattr(prop, 'permit_occupancy', "") or ""))
            f["تعداد طبقات"].insert(0, str(getattr(prop, 'permit_floors', "") or ""))
            f["تراکم"].insert(0, str(getattr(prop, 'permit_density', "") or ""))
            f["مساحت تعریض"].insert(0, str(getattr(prop, 'widening_area', "") or ""))

        # Final section
        if hasattr(prop, 'has_finalization') and prop.has_finalization:
            self.final_var.set(1)
            self._toggle_fields("final")
            f = self.final_fields
            f["متراژ کلی سقف‌ها"].insert(0, str(getattr(prop, 'final_total_area', "") or ""))
            f["کاربری موجود"].insert(0, getattr(prop, 'final_current_usage', "") or "")
            f["تعداد طبقات"].insert(0, str(getattr(prop, 'final_floors', "") or ""))
            f["کاربری مصوب"].insert(0, getattr(prop, 'final_approved_usage', "") or "")
            f["سطح اشغال موجود"].insert(0, str(getattr(prop, 'final_current_occupancy', "") or ""))
            f["سطح اشغال مصوب"].insert(0, str(getattr(prop, 'final_approved_occupancy', "") or ""))

        # Komission section
        if hasattr(prop, 'has_komission') and prop.has_komission:
            self.komission_var.set(1)
            self._toggle_fields("komission")
            f = self.komission_fields
            f["شماره سقف"].insert(0, getattr(prop, 'komission_roof_no', "") or "")
            f["مساحت سقف موجود"].insert(0, str(getattr(prop, 'komission_roof_area', "") or ""))
            f["نوع سازه"].insert(0, getattr(prop, 'komission_structure_type', "") or "")
            f["کاربری موجود"].insert(0, getattr(prop, 'komission_current_usage', "") or "")
            f["سطح اشغال"].insert(0, str(getattr(prop, 'komission_occupancy', "") or ""))
            f["تراکم"].insert(0, str(getattr(prop, 'komission_density', "") or ""))
            f["پهنه بندی"].insert(0, getattr(prop, 'komission_zone', "") or "")
            f["رای صادره"].insert(0, getattr(prop, 'komission_verdict', "") or "")
            f["توضیحات رای صادره"].insert(0, getattr(prop, 'komission_description', "") or "")
            
            if hasattr(prop, 'komission_report_date') and prop.komission_report_date:
                f["تاریخ ثبت گزارش"].insert(0, prop.komission_report_date.strftime("%Y-%m-%d"))
            if hasattr(prop, 'komission_sent_date') and prop.komission_sent_date:
                f["تاریخ ارسال به کمیسیون"].insert(0, prop.komission_sent_date.strftime("%Y-%m-%d"))

        # Certificate section
        if hasattr(prop, 'has_no_conflict_cert') and prop.has_no_conflict_cert:
            self.cert_var.set(1)
            self._toggle_fields("cert")
            f = self.cert_fields
            if hasattr(prop, 'cert_date') and prop.cert_date:
                f["تاریخ گواهی"].insert(0, prop.cert_date.strftime("%Y-%m-%d"))
            f["متراژ"].insert(0, str(getattr(prop, 'cert_area', "") or ""))
            f["طبقات"].insert(0, str(getattr(prop, 'cert_floors', "") or ""))
            f["پارکینگ"].insert(0, str(getattr(prop, 'cert_parking', "") or ""))
            f["کاربری"].insert(0, getattr(prop, 'cert_usage', "") or "")

        # Nazir section
        if hasattr(prop, 'has_nazir_referral') and prop.has_nazir_referral:
            self.nazir_var.set(1)
            self._toggle_fields("nazir")
            f = self.nazir_fields
            if hasattr(prop, 'nazir_date') and prop.nazir_date:
                f["تاریخ"].insert(0, prop.nazir_date.strftime("%Y-%m-%d"))
            f["شماره"].insert(0, str(getattr(prop, 'nazir_number', "") or ""))
            f["موضوع"].insert(0, getattr(prop, 'nazir_subject', "") or "")

        # Sedmamno section
        if hasattr(prop, 'has_sedmamno') and prop.has_sedmamno:
            self.sedmamno_var.set(1)
            self._toggle_fields("sedmamno")
            f = self.sedmamno_fields
            if hasattr(prop, 'sedmamno_date') and prop.sedmamno_date:
                f["تاریخ"].insert(0, prop.sedmamno_date.strftime("%Y-%m-%d"))
            f["شماره"].insert(0, str(getattr(prop, 'sedmamno_number', "") or ""))
            f["موضوع"].insert(0, getattr(prop, 'sedmamno_subject', "") or "")

        # Architectural section
        if hasattr(prop, 'has_architectural') and prop.has_architectural:
            self.architectural_var.set(1)
            self.toggle_architectural_fields()
            
            # Load architectural data from JSON
            if hasattr(prop, 'architectural_data') and prop.architectural_data:
                import json
                try:
                    self.architectural_data = json.loads(prop.architectural_data)
                    if self.architectural_data and len(self.architectural_data) > 0:
                        # Set first ceiling as default
                        first_ceiling = list(self.architectural_data.keys())[0]
                        self.ceiling_number.set(first_ceiling)
                        self.load_ceiling_data()
                except:
                    self.architectural_data = {}

            
        # Building section
        if hasattr(prop, 'has_building') and prop.has_building:
            self.building_var.set(1)
            self.toggle_building_fields()
            
            # Load building data from JSON
            if hasattr(prop, 'building_data') and prop.building_data:
                import json
                try:
                    self.building_data = json.loads(prop.building_data)
                    if self.building_data and len(self.building_data) > 0:
                        # Set first ceiling as default
                        first_ceiling = list(self.building_data.keys())[0]
                        self.ceiling_number.set(first_ceiling)
                        self.load_ceiling_data()
                except:
                    self.building_data = {}

        
        # HSE section
        if hasattr(prop, 'has_hse') and prop.has_hse:
            self.hse_var.set(1)
            self.toggle_hse_fields()
            
            if hasattr(prop, 'hse_data') and prop.hse_data:
                import json
                try:
                    self.hse_data = json.loads(prop.hse_data)
                    if self.hse_data and len(self.hse_data) > 0:
                        first_ceiling = list(self.hse_data.keys())[0]
                        self.hse_ceiling_number.set(first_ceiling)
                        self.load_hse_ceiling_data()
                except:
                    self.hse_data = {}



    def run_query(self):
        # Clear existing results
        self.tree.delete(*self.tree.get_children())
        query = session.query(Property)

        # Apply filters based on inputs
        owner = self.search_owner.get().strip()
        if owner:
            query = query.filter(Property.owner_name.contains(owner))

        region = self.search_region.get().strip()
        if region.isdigit():
            query = query.filter(Property.region == int(region))

        memari = self.search_memari.get().strip()
        if memari:
            query = query.filter(Property.memari_number.contains(memari))

        # Handle boolean filters properly
        if self.search_permit.get():
            query = query.filter(Property.has_permit == True)

        if self.search_final.get():
            query = query.filter(Property.has_finalization == True)

        if self.search_cert.get():
            query = query.filter(Property.has_no_conflict_cert == True)

        # Display new results
        for prop in query.all():
            self.tree.insert("", "end", values=(
                prop.id,
                prop.owner_name or "",
                prop.address or "",
                prop.region or "",
                prop.memari_number or "",
                "دارد" if getattr(prop, 'has_permit', False) else "ندارد",
                "دارد" if getattr(prop, 'has_finalization', False) else "ندارد",
                "دارد" if getattr(prop, 'has_no_conflict_cert', False) else "ندارد"
            ))

    def export_csv(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return

        headers = [
            "نام مالک", "آدرس", "منطقه", "شماره ممیزی", "UTM X", "UTM Y", "پلاک ثبتی", "تاریخ ثبت",

            # پروانه
            "پروانه دارد؟", "کاربری پروانه", "سطح اشغال پروانه", "تعداد طبقات پروانه", "تراکم پروانه", "مساحت تعریض",

            # پایان‌کار
            "پایان‌کار دارد؟", "متراژ کلی سقف‌ها", "کاربری موجود", "تعداد طبقات", "کاربری مصوب",
            "سطح اشغال موجود", "سطح اشغال مصوب",

            # کمیسیون ماده ۱۰۰
            "رای کمیسیون دارد؟", "شماره سقف", "مساحت سقف موجود", "نوع سازه", "کاربری موجود کمیسیون",
            "سطح اشغال کمیسیون", "تراکم کمیسیون", "پهنه‌بندی", "رای صادره", "توضیحات رای",
            "تاریخ ثبت گزارش", "تاریخ ارسال به کمیسیون",

            # گواهی عدم خلاف
            "گواهی عدم خلاف دارد؟", "تاریخ گواهی", "متراژ گواهی", "طبقات گواهی", "پارکینگ", "کاربری گواهی",

            # ارجاع ناظر
            "ارجاع شورا دارد؟", "تاریخ ارجاع", "شماره ارجاع", "موضوع ارجاع",

            # سد معبر
            "اخطاریه سد معبر دارد؟", "تاریخ اخطار", "شماره اخطار", "موضوع اخطار"
        ]

        try:
            with open(filepath, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

                # Get all properties for export
                query = session.query(Property)

                # Apply same filters as current search
                owner = self.search_owner.get().strip()
                if owner:
                    query = query.filter(Property.owner_name.contains(owner))

                region = self.search_region.get().strip()
                if region.isdigit():
                    query = query.filter(Property.region == int(region))

                memari = self.search_memari.get().strip()
                if memari:
                    query = query.filter(Property.memari_number.contains(memari))

                if self.search_permit.get():
                    query = query.filter(Property.has_permit == True)

                if self.search_final.get():
                    query = query.filter(Property.has_finalization == True)

                if self.search_cert.get():
                    query = query.filter(Property.has_no_conflict_cert == True)

                # Export each property
                for prop in query.all():
                    row = [
                        prop.owner_name or "",
                        prop.address or "",
                        prop.region or "",
                        prop.memari_number or "",
                        prop.utm_x or "",
                        prop.utm_y or "",
                        prop.sabti_code or "",
                        prop.last_modified.strftime("%Y-%m-%d") if prop.last_modified else "",

                        # Permit section
                        "بله" if getattr(prop, 'has_permit', False) else "خیر",
                        getattr(prop, 'permit_usage', "") or "",
                        getattr(prop, 'permit_occupancy', "") or "",
                        getattr(prop, 'permit_floors', "") or "",
                        getattr(prop, 'permit_density', "") or "",
                        getattr(prop, 'widening_area', "") or "",

                        # Final section
                        "بله" if getattr(prop, 'has_finalization', False) else "خیر",
                        getattr(prop, 'final_total_area', "") or "",
                        getattr(prop, 'final_current_usage', "") or "",
                        getattr(prop, 'final_floors', "") or "",
                        getattr(prop, 'final_approved_usage', "") or "",
                        getattr(prop, 'final_current_occupancy', "") or "",
                        getattr(prop, 'final_approved_occupancy', "") or "",

                        # Komission section
                        "بله" if getattr(prop, 'has_komission', False) else "خیر",
                        getattr(prop, 'komission_roof_no', "") or "",
                        getattr(prop, 'komission_roof_area', "") or "",
                        getattr(prop, 'komission_structure_type', "") or "",
                        getattr(prop, 'komission_current_usage', "") or "",
                        getattr(prop, 'komission_occupancy', "") or "",
                        getattr(prop, 'komission_density', "") or "",
                        getattr(prop, 'komission_zone', "") or "",
                        getattr(prop, 'komission_verdict', "") or "",
                        getattr(prop, 'komission_description', "") or "",
                        prop.komission_report_date.strftime("%Y-%m-%d") if getattr(prop, 'komission_report_date', None) else "",
                        prop.komission_sent_date.strftime("%Y-%m-%d") if getattr(prop, 'komission_sent_date', None) else "",

                        # Certificate section
                        "بله" if getattr(prop, 'has_no_conflict_cert', False) else "خیر",
                        prop.cert_date.strftime("%Y-%m-%d") if getattr(prop, 'cert_date', None) else "",
                        getattr(prop, 'cert_area', "") or "",
                        getattr(prop, 'cert_floors', "") or "",
                        getattr(prop, 'cert_parking', "") or "",
                        getattr(prop, 'cert_usage', "") or "",

                        # Nazir section
                        "بله" if getattr(prop, 'has_nazir_referral', False) else "خیر",
                        prop.nazir_date.strftime("%Y-%m-%d") if getattr(prop, 'nazir_date', None) else "",
                        getattr(prop, 'nazir_number', "") or "",
                        getattr(prop, 'nazir_subject', "") or "",

                        # Sedmamno section
                        "بله" if getattr(prop, 'has_sedmamno', False) else "خیر",
                        prop.sedmamno_date.strftime("%Y-%m-%d") if getattr(prop, 'sedmamno_date', None) else "",
                        getattr(prop, 'sedmamno_number', "") or "",
                        getattr(prop, 'sedmamno_subject', "") or ""
                    ]
                    writer.writerow(row)

            messagebox.showinfo("خروجی موفق", f"فایل CSV با موفقیت ذخیره شد:\n{filepath}")

        except Exception as e:
            messagebox.showerror("خطا در خروجی", f"خطایی در ذخیره فایل رخ داد:\n{str(e)}")


    def build_architectural_tab(self):
        """Build the architectural standards tab"""
        # Main frame for architectural tab
        main_frame = tk.Frame(self.tab_architectural)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Checkbox to enable/disable architectural standards
        self.architectural_var = tk.IntVar()
        self.architectural_checkbox = tk.Checkbutton(
            main_frame, 
            text="فعال‌سازی ضوابط معماری", 
            variable=self.architectural_var,
            command=self.toggle_architectural_fields,
            font=("Arial", 12, "bold")
        )
        self.architectural_checkbox.pack(anchor="w", pady=(0, 10))
        
        # Frame for architectural standards form
        self.architectural_frame = tk.LabelFrame(main_frame, text="جدول ضوابط معماری", font=("Arial", 11, "bold"))
        self.architectural_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Ceiling number selection
        ceiling_frame = tk.Frame(self.architectural_frame)
        ceiling_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(ceiling_frame, text="شماره سقف:", font=("Arial", 10)).pack(side="left")
        self.ceiling_number = ttk.Combobox(ceiling_frame, values=list(range(1, 21)), width=5, state="disabled")
        self.ceiling_number.pack(side="left", padx=(5, 10))
        self.ceiling_number.bind("<<ComboboxSelected>>", self.load_ceiling_data)
        
        # Add ceiling button
        self.add_ceiling_btn = tk.Button(
            ceiling_frame, 
            text="افزودن سقف جدید", 
            command=self.add_new_ceiling,
            state="disabled"
        )
        self.add_ceiling_btn.pack(side="left", padx=5)
        
        # Create canvas and scrollbar for the table
        canvas = tk.Canvas(self.architectural_frame)
        scrollbar = tk.Scrollbar(self.architectural_frame, orient="vertical", command=canvas.yview)
        self.table_frame = tk.Frame(canvas)
        
        # Configure scrolling
        self.table_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Define architectural evaluation items
        self.architectural_items = [
            "مطابقت رمپ با نقشه های مصوب یا اجرایی و کنترل عرض و شیب و طول مجاز رمپ",
            "مطابقت راه پله و پاگرد با نقشه های مصوب یا اجرایی شامل عرض،ارتفاع،کف،قرنیز،ارتفاع نردهو....",
            "اجرای پله فرار مطابق نقشه مصوب یا اجرایی و ضوابط شهرداری",
            "اجرای دیوار های پیرامونی و داخلی مطابق نقشه های مصوب یا اجرایی",
            "اجرای صحیح پنجره ها و OKB و عدم اشرافیت مطابق نقشه مصوب یا اجرایی",
            "فاصله بنای موجود با پلاک های اطراف ساختمان مطابق نقشه های مصوب یا اجرایی و ضوابط شهرداری",
            "پیش آمدگی ها و تراس های موجود بنا مطابق نقشه های مصوب یا اجرایی و ضوابط شهرداری",
            "ضوابط نما مطابق ضوابط شهرداری و نقشه های اجرایی"
        ]
        
        # Create table headers
        headers = ["موارد ارزیابی", "تایید", "ناقص", "توضیحات"]
        for j, header in enumerate(headers):
            label = tk.Label(self.table_frame, text=header, font=("Arial", 10, "bold"), relief="ridge", bd=1)
            if j == 0:  # First column wider for evaluation items
                label.grid(row=0, column=j, sticky="ew", padx=1, pady=1, ipadx=10)
                self.table_frame.grid_columnconfigure(j, weight=3)
            elif j == 3:  # Comments column wider
                label.grid(row=0, column=j, sticky="ew", padx=1, pady=1, ipadx=10)
                self.table_frame.grid_columnconfigure(j, weight=2)
            else:
                label.grid(row=0, column=j, sticky="ew", padx=1, pady=1)
                self.table_frame.grid_columnconfigure(j, weight=1)
        
        # Initialize storage for architectural data
        self.architectural_fields = {}
        self.architectural_data = {}  # Will store data for each ceiling
        
        # Create table rows
        self.create_architectural_table()
        
        # Date label
        self.arch_date_label = tk.Label(self.architectural_frame, text="", font=("Arial", 9), fg="gray")
        self.arch_date_label.pack(pady=5)
        
        # Initially disable all fields
        self.toggle_architectural_fields()

    def create_architectural_table(self):
        """Create the architectural standards table"""
        self.architectural_fields = {}
        
        for i, item in enumerate(self.architectural_items, 1):
            # Evaluation item (read-only)
            item_label = tk.Label(
                self.table_frame, 
                text=f"{i}. {item}", 
                font=("Arial", 9), 
                relief="ridge", 
                bd=1, 
                wraplength=300,
                justify="right"
            )
            item_label.grid(row=i, column=0, sticky="ew", padx=1, pady=1, ipadx=5, ipady=5)
            
            # Radio buttons for approval/incomplete
            radio_frame = tk.Frame(self.table_frame)
            radio_frame.grid(row=i, column=1, sticky="ew", padx=1, pady=1)
            
            var = tk.StringVar()
            approve_radio = tk.Radiobutton(radio_frame, text="تایید", variable=var, value="approved", state="disabled")
            approve_radio.pack(anchor="center")
            
            incomplete_frame = tk.Frame(self.table_frame)
            incomplete_frame.grid(row=i, column=2, sticky="ew", padx=1, pady=1)
            
            incomplete_radio = tk.Radiobutton(incomplete_frame, text="ناقص", variable=var, value="incomplete", state="disabled")
            incomplete_radio.pack(anchor="center")
            
            # Comments text field
            comment_text = tk.Text(self.table_frame, height=2, width=25, font=("Arial", 9), state="disabled")
            comment_text.grid(row=i, column=3, sticky="ew", padx=1, pady=1, ipadx=5, ipady=2)
            
            # Store references
            self.architectural_fields[f"item_{i}"] = {
                'var': var,
                'approve_radio': approve_radio,
                'incomplete_radio': incomplete_radio,
                'comment': comment_text
            }

    def toggle_architectural_fields(self):
        """Toggle architectural standards fields based on checkbox"""
        state = "normal" if self.architectural_var.get() else "disabled"
        
        # Enable/disable ceiling number combobox and add button
        self.ceiling_number.config(state=state)
        self.add_ceiling_btn.config(state=state)
        
        # Enable/disable all table fields
        for field_data in self.architectural_fields.values():
            field_data['approve_radio'].config(state=state)
            field_data['incomplete_radio'].config(state=state)
            field_data['comment'].config(state=state)
        
        # Update date label
        if self.architectural_var.get():
            self.arch_date_label.config(text=f"تاریخ ثبت/ویرایش: {datetime.today().strftime('%Y-%m-%d')}")
            if not self.ceiling_number.get():
                self.ceiling_number.set("1")
                self.load_ceiling_data()
        else:
            self.arch_date_label.config(text="")

    def add_new_ceiling(self):
        """Add a new ceiling for architectural standards"""
        current_ceiling = int(self.ceiling_number.get()) if self.ceiling_number.get() else 1
        next_ceiling = current_ceiling + 1
        
        # Save current ceiling data before switching
        self.save_current_ceiling_data()
        
        # Set next ceiling number
        self.ceiling_number.set(str(next_ceiling))
        
        # Clear fields for new ceiling
        self.clear_architectural_fields()
        
        # Update date
        self.arch_date_label.config(text=f"تاریخ ثبت/ویرایش: {datetime.today().strftime('%Y-%m-%d')}")

    def load_ceiling_data(self, event=None):
        """Load data for selected ceiling"""
        ceiling_num = self.ceiling_number.get()
        if not ceiling_num:
            return
        
        # Clear current fields first
        self.clear_architectural_fields()
        
        # Load data if exists for this ceiling
        if ceiling_num in self.architectural_data:
            data = self.architectural_data[ceiling_num]
            for i in range(1, 9):
                field_key = f"item_{i}"
                if field_key in data:
                    item_data = data[field_key]
                    if 'status' in item_data and item_data['status']:
                        self.architectural_fields[field_key]['var'].set(item_data['status'])
                    if 'comment' in item_data and item_data['comment']:
                        self.architectural_fields[field_key]['comment'].delete(1.0, tk.END)
                        self.architectural_fields[field_key]['comment'].insert(1.0, item_data['comment'])

    def save_current_ceiling_data(self):
        """Save current ceiling data to memory"""
        ceiling_num = self.ceiling_number.get()
        if not ceiling_num:
            return
        
        if ceiling_num not in self.architectural_data:
            self.architectural_data[ceiling_num] = {}
        
        for i in range(1, 9):
            field_key = f"item_{i}"
            field_data = self.architectural_fields[field_key]
            
            self.architectural_data[ceiling_num][field_key] = {
                'status': field_data['var'].get() if field_data['var'].get() else None,
                'comment': field_data['comment'].get(1.0, tk.END).strip()
            }

    def clear_architectural_fields(self):
        """Clear all architectural fields"""
        for field_data in self.architectural_fields.values():
            field_data['var'].set("")
            field_data['comment'].delete(1.0, tk.END)



    
    def build_building_tab(self):
        """Build the building standards tab"""
        # Main frame for building tab
        main_frame = tk.Frame(self.tab_building)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Checkbox to enable/disable building standards
        self.building_var = tk.IntVar()
        self.building_checkbox = tk.Checkbutton(
            main_frame, 
            text="فعال‌سازی ضوابط سازه‌ای", 
            variable=self.building_var,
            command=self.toggle_building_fields,
            font=("Arial", 12, "bold")
        )
        self.building_checkbox.pack(anchor="w", pady=(0, 10))
        
        # Frame for building standards form
        self.building_frame = tk.LabelFrame(main_frame, text="جدول ضوابط سازه‌ای", font=("Arial", 11, "bold"))
        self.building_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Additional fields frame
        additional_frame = tk.Frame(self.building_frame)
        additional_frame.pack(fill="x", padx=5, pady=5)
        
        # First row of additional fields
        row1_frame = tk.Frame(additional_frame)
        row1_frame.pack(fill="x", pady=2)
        
        tk.Label(row1_frame, text="شماره سقف:", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        self.ceiling_number = ttk.Combobox(row1_frame, values=list(range(1, 21)), width=8, state="disabled")
        self.ceiling_number.pack(side="left", padx=(0, 15))
        self.ceiling_number.bind("<<ComboboxSelected>>", self.load_ceiling_data)
        
        tk.Label(row1_frame, text="نوع اسکلت سازه:", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        self.skeleton_type = tk.Entry(row1_frame, width=15, state="disabled")
        self.skeleton_type.pack(side="left", padx=(0, 15))
        
        tk.Label(row1_frame, text="نوع سقف سازه:", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        self.ceiling_structure_type = tk.Entry(row1_frame, width=15, state="disabled")
        self.ceiling_structure_type.pack(side="left")
        
        # Second row of additional fields
        row2_frame = tk.Frame(additional_frame)
        row2_frame.pack(fill="x", pady=2)
        
        tk.Label(row2_frame, text="مساحت سقف:", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        self.ceiling_area = tk.Entry(row2_frame, width=12, state="disabled")
        self.ceiling_area.pack(side="left", padx=(0, 15))
        
        tk.Label(row2_frame, text="تعداد سقف مطابق پروانه:", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        self.permit_ceiling_count = tk.Entry(row2_frame, width=8, state="disabled")
        self.permit_ceiling_count.pack(side="left", padx=(0, 15))
        
        # Add ceiling button
        self.add_ceiling_btn = tk.Button(
            row2_frame, 
            text="افزودن سقف جدید", 
            command=self.add_new_ceiling,
            state="disabled"
        )
        self.add_ceiling_btn.pack(side="left", padx=15)
        
        # Create canvas and scrollbar for the table
        canvas = tk.Canvas(self.building_frame)
        scrollbar = tk.Scrollbar(self.building_frame, orient="vertical", command=canvas.yview)
        self.table_frame = tk.Frame(canvas)
        
        # Configure scrolling
        self.table_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Define building evaluation items (building standards)
        self.building_items = [
            "مطابقت نقشه اجرایی با نقشه های مصوب طبق ضابطه (تعداد ستون، فواصل، ابعاد، ...)",
            "رعایت درز انقطاع از پلاک های مجاور",
            "استفاده از ویبراسیون، مواد افزودنی در تاریخ و شرایط آب و هوایی بتن ریزی در کارگاه ساختمانی",
            "شیوه حمل و عمل آوری بتن ریزی",
            "شرایط نگه داری مصالح سازه ای در کارگاه ساختمانی",
            "زمان قالب برداری از سقف، تیر و ستون ها و پایه های اطمینان",
            "اجرای صحیح ابعاد فونداسیون و پی سازه مطابق نقشه های مصوب یا اجرایی",
            "کنترل وال پست ها مطابق نقشه های اجرایی و مصوب بنا"
        ]
        
        # Create table headers
        headers = ["ردیف", "موارد ارزیابی", "تایید", "ناقص", "تاریخ و توضیحات"]
        for j, header in enumerate(headers):
            label = tk.Label(self.table_frame, text=header, font=("Arial", 10, "bold"), relief="ridge", bd=1)
            if j == 0:  # Row number column
                label.grid(row=0, column=j, sticky="ew", padx=1, pady=1, ipadx=5)
                self.table_frame.grid_columnconfigure(j, weight=0)
            elif j == 1:  # Evaluation items column wider
                label.grid(row=0, column=j, sticky="ew", padx=1, pady=1, ipadx=10)
                self.table_frame.grid_columnconfigure(j, weight=4)
            elif j == 4:  # Comments column wider
                label.grid(row=0, column=j, sticky="ew", padx=1, pady=1, ipadx=10)
                self.table_frame.grid_columnconfigure(j, weight=2)
            else:
                label.grid(row=0, column=j, sticky="ew", padx=1, pady=1)
                self.table_frame.grid_columnconfigure(j, weight=1)
        
        # Initialize storage for building data
        self.building_fields = {}
        self.building_data = {}  # Will store data for each ceiling
        
        # Create table rows
        self.create_building_table()
        
        # Date label
        self.arch_date_label = tk.Label(self.building_frame, text="", font=("Arial", 9), fg="gray")
        self.arch_date_label.pack(pady=5)
        
        # Initially disable all fields
        self.toggle_building_fields()

    def create_building_table(self):
        """Create the building standards table"""
        self.building_fields = {}
        
        for i, item in enumerate(self.building_items, 1):
            # Row number
            row_num_label = tk.Label(
                self.table_frame, 
                text=str(i), 
                font=("Arial", 10, "bold"), 
                relief="ridge", 
                bd=1
            )
            row_num_label.grid(row=i, column=0, sticky="ew", padx=1, pady=1, ipadx=5, ipady=5)
            
            # Evaluation item (read-only)
            item_label = tk.Label(
                self.table_frame, 
                text=item, 
                font=("Arial", 9), 
                relief="ridge", 
                bd=1, 
                wraplength=350,
                justify="right"
            )
            item_label.grid(row=i, column=1, sticky="ew", padx=1, pady=1, ipadx=5, ipady=5)
            
            # Radio buttons for approval/incomplete
            radio_frame = tk.Frame(self.table_frame)
            radio_frame.grid(row=i, column=2, sticky="ew", padx=1, pady=1)
            
            var = tk.StringVar()
            approve_radio = tk.Radiobutton(radio_frame, text="تایید", variable=var, value="approved", state="disabled")
            approve_radio.pack(anchor="center")
            
            incomplete_frame = tk.Frame(self.table_frame)
            incomplete_frame.grid(row=i, column=3, sticky="ew", padx=1, pady=1)
            
            incomplete_radio = tk.Radiobutton(incomplete_frame, text="ناقص", variable=var, value="incomplete", state="disabled")
            incomplete_radio.pack(anchor="center")
            
            # Comments text field
            comment_text = tk.Text(self.table_frame, height=2, width=25, font=("Arial", 9), state="disabled")
            comment_text.grid(row=i, column=4, sticky="ew", padx=1, pady=1, ipadx=5, ipady=2)
            
            # Store references
            self.building_fields[f"item_{i}"] = {
                'var': var,
                'approve_radio': approve_radio,
                'incomplete_radio': incomplete_radio,
                'comment': comment_text
            }

    def toggle_building_fields(self):
        """Toggle building standards fields based on checkbox"""
        state = "normal" if self.building_var.get() else "disabled"
        
        # Enable/disable additional fields
        self.ceiling_number.config(state=state)
        self.skeleton_type.config(state=state)
        self.ceiling_structure_type.config(state=state)
        self.ceiling_area.config(state=state)
        self.permit_ceiling_count.config(state=state)
        self.add_ceiling_btn.config(state=state)
        
        # Enable/disable all table fields
        for field_data in self.building_fields.values():
            field_data['approve_radio'].config(state=state)
            field_data['incomplete_radio'].config(state=state)
            field_data['comment'].config(state=state)
        
        # Update date label
        if self.building_var.get():
            self.arch_date_label.config(text=f"تاریخ ثبت/ویرایش: {datetime.today().strftime('%Y-%m-%d')}")
            if not self.ceiling_number.get():
                self.ceiling_number.set("1")
                self.load_ceiling_data()
        else:
            self.arch_date_label.config(text="")

    def add_new_ceiling(self):
        """Add a new ceiling for building standards"""
        current_ceiling = int(self.ceiling_number.get()) if self.ceiling_number.get() else 1
        next_ceiling = current_ceiling + 1
        
        # Save current ceiling data before switching
        self.save_current_ceiling_data()
        
        # Set next ceiling number
        self.ceiling_number.set(str(next_ceiling))
        
        # Clear fields for new ceiling
        self.clear_building_fields()
        
        # Update date
        self.arch_date_label.config(text=f"تاریخ ثبت/ویرایش: {datetime.today().strftime('%Y-%m-%d')}")

    def load_ceiling_data(self, event=None):
        """Load data for selected ceiling"""
        ceiling_num = self.ceiling_number.get()
        if not ceiling_num:
            return
        
        # Clear current fields first
        self.clear_building_fields()
        
        # Load data if exists for this ceiling
        if ceiling_num in self.building_data:
            data = self.building_data[ceiling_num]
            
            # Load additional fields
            if 'skeleton_type' in data:
                self.skeleton_type.delete(0, tk.END)
                self.skeleton_type.insert(0, data['skeleton_type'] or "")
            if 'ceiling_structure_type' in data:
                self.ceiling_structure_type.delete(0, tk.END)
                self.ceiling_structure_type.insert(0, data['ceiling_structure_type'] or "")
            if 'ceiling_area' in data:
                self.ceiling_area.delete(0, tk.END)
                self.ceiling_area.insert(0, data['ceiling_area'] or "")
            if 'permit_ceiling_count' in data:
                self.permit_ceiling_count.delete(0, tk.END)
                self.permit_ceiling_count.insert(0, data['permit_ceiling_count'] or "")
            
            # Load table data
            for i in range(1, 9):
                field_key = f"item_{i}"
                if field_key in data:
                    item_data = data[field_key]
                    if 'status' in item_data and item_data['status']:
                        self.building_fields[field_key]['var'].set(item_data['status'])
                    if 'comment' in item_data and item_data['comment']:
                        self.building_fields[field_key]['comment'].delete(1.0, tk.END)
                        self.building_fields[field_key]['comment'].insert(1.0, item_data['comment'])

    def save_current_ceiling_data(self):
        """Save current ceiling data to memory"""
        ceiling_num = self.ceiling_number.get()
        if not ceiling_num:
            return
        
        if ceiling_num not in self.building_data:
            self.building_data[ceiling_num] = {}
        
        # Save additional fields
        self.building_data[ceiling_num]['skeleton_type'] = self.skeleton_type.get()
        self.building_data[ceiling_num]['ceiling_structure_type'] = self.ceiling_structure_type.get()
        self.building_data[ceiling_num]['ceiling_area'] = self.ceiling_area.get()
        self.building_data[ceiling_num]['permit_ceiling_count'] = self.permit_ceiling_count.get()
        
        # Save table data
        for i in range(1, 9):
            field_key = f"item_{i}"
            field_data = self.building_fields[field_key]
            
            self.building_data[ceiling_num][field_key] = {
                'status': field_data['var'].get() if field_data['var'].get() else None,
                'comment': field_data['comment'].get(1.0, tk.END).strip()
            }

    def clear_building_fields(self):
        """Clear all building fields"""
        # Clear additional fields
        self.skeleton_type.delete(0, tk.END)
        self.ceiling_structure_type.delete(0, tk.END)
        self.ceiling_area.delete(0, tk.END)
        self.permit_ceiling_count.delete(0, tk.END)
        
        # Clear table fields
        for field_data in self.building_fields.values():
            field_data['var'].set("")
            field_data['comment'].delete(1.0, tk.END)



    def build_hse_tab(self):
        """Build the HSE (safety and work protection) standards tab"""
        # Main frame for HSE tab
        main_frame = tk.Frame(self.tab_hse)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Checkbox to enable/disable HSE standards
        self.hse_var = tk.IntVar()
        self.hse_checkbox = tk.Checkbutton(
            main_frame, 
            text="فعال‌سازی ضوابط ایمنی و حفاظت کار (HSE)", 
            variable=self.hse_var,
            command=self.toggle_hse_fields,
            font=("Arial", 12, "bold")
        )
        self.hse_checkbox.pack(anchor="w", pady=(0, 10))
        
        # Frame for HSE standards form
        self.hse_frame = tk.LabelFrame(main_frame, text="جدول ضوابط ایمنی و حفاظت کار (HSE)", font=("Arial", 11, "bold"))
        self.hse_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Additional fields frame - only ceiling number needed for HSE
        additional_frame = tk.Frame(self.hse_frame)
        additional_frame.pack(fill="x", padx=5, pady=5)
        
        # Single row for ceiling number and add button
        row_frame = tk.Frame(additional_frame)
        row_frame.pack(fill="x", pady=2)
        
        tk.Label(row_frame, text="شماره سقف:", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        self.hse_ceiling_number = ttk.Combobox(row_frame, values=list(range(1, 21)), width=8, state="disabled")
        self.hse_ceiling_number.pack(side="left", padx=(0, 15))
        self.hse_ceiling_number.bind("<<ComboboxSelected>>", self.load_hse_ceiling_data)
        
        # Add ceiling button
        self.add_hse_ceiling_btn = tk.Button(
            row_frame, 
            text="افزودن سقف جدید", 
            command=self.add_new_hse_ceiling,
            state="disabled"
        )
        self.add_hse_ceiling_btn.pack(side="left", padx=15)
        
        # Create canvas and scrollbar for the table
        canvas = tk.Canvas(self.hse_frame)
        scrollbar = tk.Scrollbar(self.hse_frame, orient="vertical", command=canvas.yview)
        self.hse_table_frame = tk.Frame(canvas)
        
        # Configure scrolling
        self.hse_table_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.hse_table_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Define HSE evaluation items
        self.hse_items = [
            "نصب علایم هشدار دهنده در داخل و اطراف کارگاه ساختمانی",
            "محصور بودن کارگاه ساختمانی مطابق ضوابط",
            "عدم دپوی مصالح در شوارع و عدم ایجاد سد معبر و تاییدیه کارشناس و نصب علایم هشدار دهنده",
            "وسایل حفاظت فردی کارگران ساختمانی",
            "نصب و مهار اصولی ماشین آلات و تاسیسات واقع در کارگاه ساختمانی",
            "انجام تمامی بیمه های لازم در کارگاه ساختمانی",
            "اجرا و جانمایی صحیح داربست و راهرو های دسترسی و حفاظ در ارتفاع",
            "معرفی ناظر HSE در کارگاه های ساختمانی بزرگ",
            "رعایت بهداشت در دفع فاضلاب، نخاله و جلوگیری از انسداد کانال هدایت آب های سطحی"
        ]
        
        # Create table headers
        headers = ["ردیف", "موارد ارزیابی", "تایید", "ناقص", "توضیحات"]
        for j, header in enumerate(headers):
            label = tk.Label(self.hse_table_frame, text=header, font=("Arial", 10, "bold"), relief="ridge", bd=1)
            if j == 0:  # Row number column
                label.grid(row=0, column=j, sticky="ew", padx=1, pady=1, ipadx=5)
                self.hse_table_frame.grid_columnconfigure(j, weight=0)
            elif j == 1:  # Evaluation items column wider
                label.grid(row=0, column=j, sticky="ew", padx=1, pady=1, ipadx=10)
                self.hse_table_frame.grid_columnconfigure(j, weight=4)
            elif j == 4:  # Comments column wider
                label.grid(row=0, column=j, sticky="ew", padx=1, pady=1, ipadx=10)
                self.hse_table_frame.grid_columnconfigure(j, weight=2)
            else:
                label.grid(row=0, column=j, sticky="ew", padx=1, pady=1)
                self.hse_table_frame.grid_columnconfigure(j, weight=1)
        
        # Initialize storage for HSE data
        self.hse_fields = {}
        self.hse_data = {}  # Will store data for each ceiling
        
        # Create table rows
        self.create_hse_table()
        
        # Date label
        self.hse_date_label = tk.Label(self.hse_frame, text="", font=("Arial", 9), fg="gray")
        self.hse_date_label.pack(pady=5)
        
        # Initially disable all fields
        self.toggle_hse_fields()

    def create_hse_table(self):
        """Create the HSE standards table"""
        self.hse_fields = {}
        
        for i, item in enumerate(self.hse_items, 1):
            # Row number
            row_num_label = tk.Label(
                self.hse_table_frame, 
                text=str(i), 
                font=("Arial", 10, "bold"), 
                relief="ridge", 
                bd=1
            )
            row_num_label.grid(row=i, column=0, sticky="ew", padx=1, pady=1, ipadx=5, ipady=5)
            
            # Evaluation item (read-only)
            item_label = tk.Label(
                self.hse_table_frame, 
                text=item, 
                font=("Arial", 9), 
                relief="ridge", 
                bd=1, 
                wraplength=350,
                justify="right"
            )
            item_label.grid(row=i, column=1, sticky="ew", padx=1, pady=1, ipadx=5, ipady=5)
            
            # Radio buttons for approval/incomplete
            radio_frame = tk.Frame(self.hse_table_frame)
            radio_frame.grid(row=i, column=2, sticky="ew", padx=1, pady=1)
            
            var = tk.StringVar()
            approve_radio = tk.Radiobutton(radio_frame, text="تایید", variable=var, value="approved", state="disabled")
            approve_radio.pack(anchor="center")
            
            incomplete_frame = tk.Frame(self.hse_table_frame)
            incomplete_frame.grid(row=i, column=3, sticky="ew", padx=1, pady=1)
            
            incomplete_radio = tk.Radiobutton(incomplete_frame, text="ناقص", variable=var, value="incomplete", state="disabled")
            incomplete_radio.pack(anchor="center")
            
            # Comments text field
            comment_text = tk.Text(self.hse_table_frame, height=2, width=25, font=("Arial", 9), state="disabled")
            comment_text.grid(row=i, column=4, sticky="ew", padx=1, pady=1, ipadx=5, ipady=2)
            
            # Store references
            self.hse_fields[f"item_{i}"] = {
                'var': var,
                'approve_radio': approve_radio,
                'incomplete_radio': incomplete_radio,
                'comment': comment_text
            }

    def toggle_hse_fields(self):
        """Toggle HSE standards fields based on checkbox"""
        state = "normal" if self.hse_var.get() else "disabled"
        
        # Enable/disable ceiling number and add button
        self.hse_ceiling_number.config(state=state)
        self.add_hse_ceiling_btn.config(state=state)
        
        # Enable/disable all table fields
        for field_data in self.hse_fields.values():
            field_data['approve_radio'].config(state=state)
            field_data['incomplete_radio'].config(state=state)
            field_data['comment'].config(state=state)
        
        # Update date label
        if self.hse_var.get():
            self.hse_date_label.config(text=f"تاریخ ثبت/ویرایش: {datetime.today().strftime('%Y-%m-%d')}")
            if not self.hse_ceiling_number.get():
                self.hse_ceiling_number.set("1")
                self.load_hse_ceiling_data()
        else:
            self.hse_date_label.config(text="")

    def add_new_hse_ceiling(self):
        """Add a new ceiling for HSE standards"""
        current_ceiling = int(self.hse_ceiling_number.get()) if self.hse_ceiling_number.get() else 1
        next_ceiling = current_ceiling + 1
        
        # Save current ceiling data before switching
        self.save_current_hse_ceiling_data()
        
        # Set next ceiling number
        self.hse_ceiling_number.set(str(next_ceiling))
        
        # Clear fields for new ceiling
        self.clear_hse_fields()
        
        # Update date
        self.hse_date_label.config(text=f"تاریخ ثبت/ویرایش: {datetime.today().strftime('%Y-%m-%d')}")

    def load_hse_ceiling_data(self, event=None):
        """Load data for selected ceiling"""
        ceiling_num = self.hse_ceiling_number.get()
        if not ceiling_num:
            return
        
        # Clear current fields first
        self.clear_hse_fields()
        
        # Load data if exists for this ceiling
        if ceiling_num in self.hse_data:
            data = self.hse_data[ceiling_num]
            
            # Load table data
            for i in range(1, 10):  # HSE has 9 items
                field_key = f"item_{i}"
                if field_key in data:
                    item_data = data[field_key]
                    if 'status' in item_data and item_data['status']:
                        self.hse_fields[field_key]['var'].set(item_data['status'])
                    if 'comment' in item_data and item_data['comment']:
                        self.hse_fields[field_key]['comment'].delete(1.0, tk.END)
                        self.hse_fields[field_key]['comment'].insert(1.0, item_data['comment'])

    def save_current_hse_ceiling_data(self):
        """Save current HSE ceiling data to memory"""
        ceiling_num = self.hse_ceiling_number.get()
        if not ceiling_num:
            return
        
        if ceiling_num not in self.hse_data:
            self.hse_data[ceiling_num] = {}
        
        # Save table data
        for i in range(1, 10):  # HSE has 9 items
            field_key = f"item_{i}"
            field_data = self.hse_fields[field_key]
            
            self.hse_data[ceiling_num][field_key] = {
                'status': field_data['var'].get() if field_data['var'].get() else None,
                'comment': field_data['comment'].get(1.0, tk.END).strip()
            }

    def clear_hse_fields(self):
        """Clear all HSE fields"""
        # Clear table fields
        for field_data in self.hse_fields.values():
            field_data['var'].set("")
            field_data['comment'].delete(1.0, tk.END)