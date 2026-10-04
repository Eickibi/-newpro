import os
os.environ["INVENTORY_DATA_DIR"] = "test_data_dir"
import data_handler as dh
import services as svc
import advanced as adv
import shutil

if os.path.exists("test_data_dir"):
    shutil.rmtree("test_data_dir")
os.makedirs("test_data_dir")

db, _ = dh.load_all()
svc.bootstrap(db)
adv.bootstrap(db)
user = db["users"]["admin"]

sku = "TEST-LOT"
db["products"][sku] = svc._new_product({"sku": sku, "name": "Test", "category": "A", "unit": "pcs", "cost_price": 10, "selling_price": 20, "reorder_point": 5}, user)

adv.create_warehouse(db, user, {"id": "W2", "name": "W2", "location": "L2"})

adv.create_lot(db, user, {"sku": sku, "warehouse": "MAIN", "lot": "L001", "quantity": 10, "unit_cost": 10.0, "expiry": "2030-01-01"})
print("MAIN stock:", db["warehouse_stock"]["MAIN"].get(sku))

adv.transfer(db, user, {"sku": sku, "from_warehouse": "MAIN", "to_warehouse": "W2", "quantity": 5, "reason": "test"})
print("MAIN stock after transfer:", db["warehouse_stock"]["MAIN"].get(sku))
print("W2 stock after transfer:", db["warehouse_stock"]["W2"].get(sku))

try:
    svc.stock_move(db, user, {"sku": sku, "warehouse": "W2", "type": "OUTBOUND", "quantity": 2, "reason": "sell", "cost_method": "FEFO"})
    print("Success: Outbound from W2")
except svc.ServiceError as e:
    print(f"Error during outbound from W2: {e.message}")
