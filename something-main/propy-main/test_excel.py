import data_handler as dh
import services as svc
import advanced as adv
import cli
import os

db, warnings = dh.load_all()
svc.bootstrap(db)

user = svc.login(db, "admin", "Admin@123")["user"]
full_user = db["users"]["admin"]

excel_xml = adv.excel_products(db)

try:
    print("Testing import_products_excel...")
    res = adv.import_products_excel(db, full_user, excel_xml)
    print("Success:", res)
except Exception as e:
    import traceback
    traceback.print_exc()

