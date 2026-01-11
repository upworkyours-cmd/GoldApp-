import flet as ft
import yfinance as yf

# قاعدة البيانات
pricing_db = {
    "خاتم عيار 21":     {"wastage": 1.1, "making": 150},
    "إسوارة رفيعة":      {"wastage": 1.1, "making": 180},
    "سلسلة جنزير":       {"wastage": 1.1, "making": 200},
    "طقم كامل (ثقيل)":  {"wastage": 1.1, "making": 350},
    "سبيكة (بدون مصنعية)": {"wastage": 1.0, "making": 0}
}

def main(page: ft.Page):
    page.title = "نظام تسعير الذهب"
    page.window_width = 400
    page.window_height = 700
    page.scroll = "auto"
    page.rtl = True
    page.vertical_alignment = ft.MainAxisAlignment.START

    # العناصر
    txt_grams = ft.TextField(label="الوزن (جرام)", keyboard_type=ft.KeyboardType.NUMBER)
    dd_design = ft.Dropdown(
        label="التصميم", 
        options=[ft.dropdown.Option(k) for k in pricing_db.keys()],
        value=list(pricing_db.keys())[0]
    )
    lbl_result = ft.Text("0.00 درهم", size=30, weight="bold", color="green")
    lbl_status = ft.Text("جاهز", color="grey")

    def calc(e):
        try:
            lbl_status.value = "جاري الحساب..."
            page.update()
            if not txt_grams.value: return
            
            grams = float(txt_grams.value)
            design = pricing_db[dd_design.value]
            
            # جلب سعر الذهب
            try:
                gold = yf.Ticker("GC=F")
                price = gold.history(period="1mo")['Close'].iloc[-1]
            except:
                price = 2000 # سعر احتياطي في حال فشل النت
                
            # الحساب
            p_24_aed = (price * 3.6725) / 31.1035
            p_18 = p_24_aed * 0.75
            cost = (grams * p_18 * design["wastage"]) + design["making"]
            profit = 2.25 if cost < 10000 else 1.80
            final = cost * (1 + profit/100)
            
            lbl_result.value = f"{final:.2f} درهم"
            lbl_status.value = "تم بنجاح ✅"
            page.update()
        except Exception as ex:
            lbl_status.value = "خطأ"
            print(ex)
            page.update()

    btn = ft.ElevatedButton("احسب", on_click=calc)
    page.add(ft.Column([ft.Text("تسعير الذهب", size=24), txt_grams, dd_design, btn, lbl_status, lbl_result]))

ft.app(target=main)
