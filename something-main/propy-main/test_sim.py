import data_handler as dh
import services as svc
import advanced as adv
import cli
import os

db, warnings = dh.load_all()
svc.bootstrap(db)

user = svc.login(db, "admin", "Admin@123")["user"]
full_user = db["users"]["admin"]

def try_call(name, func, *args, **kwargs):
    print(f"Trying {name}...")
    try:
        res = func(*args, **kwargs)
        print(f"Success: {name}")
    except Exception as e:
        import traceback
        traceback.print_exc()

# Seed some data
if "P1" not in db["products"]:
    db["products"]["P1"] = svc._new_product({"sku": "P1", "name": "Prod 1", "category": "C1", "unit": "pcs", "cost_price": 10.0, "selling_price": 20.0, "reorder_point": 5}, full_user)
if "MAIN" not in db["warehouses"]:
    adv.bootstrap(db)

try_call("list_products", svc.list_products, db, full_user, {})
try_call("dashboard", svc.dashboard, db, full_user)
try_call("create_warehouse", adv.create_warehouse, db, full_user, {"id": "W2", "name": "W2", "location": "L2"})
try_call("transfer", adv.transfer, db, full_user, {"sku": "P1", "from_warehouse": "MAIN", "to_warehouse": "W2", "quantity": 5, "reason": "test"})
try_call("stock_count", adv.stock_count, db, full_user, {"warehouse": "MAIN", "items": [{"sku": "P1", "counted": 10}]})
try_call("create_lot", adv.create_lot, db, full_user, {"sku": "P1", "warehouse": "MAIN", "lot": "L1", "quantity": 10, "unit_cost": 10.0, "expiry": "2024-12-31"})
try_call("csv_products", adv.csv_products, db)
try_call("import_products_csv", adv.import_products_csv, db, full_user, "sku,name,category,unit,cost_price,selling_price,reorder_point\nP2,Prod 2,C1,pcs,10,20,5\n")
try_call("allocate_lots", adv.allocate_lots, db, "P1", "MAIN", 5)

