from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from modules import database, clients, bills
from datetime import date
import random
import json
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

chars = "1234567890qwertyuiopasdfghjklñzxcvbnm"

def get_random_id(len = 10):
    return "".join([random.choice(chars) for x in range(len)])

@app.post("/send")
async def create_product(request: Request):
    res = await request.json()
    print(res)
    product_name = res["product_name"]
    product_description = res["product_description"]
    product_price = res["product_price"]
    product_stock = res["product_stock"]
    product_id = res["product_id"] if res["product_id"].strip() != "" else 'undefined' 
    if product_name.strip() == "" or product_description.strip() == "" or product_price.strip() == "" or product_stock.strip() == "":
        return {"status": False, "alert": "Hay campos vacios"}
    else:
        database.insert_database(product_user_id="josueadmin", product_unique_id=get_random_id(), product_id=product_id, product_name=product_name, product_description=product_description, product_price=product_price, product_image="noimage", product_stock=product_stock, product_is_hidden=False)
        return {"status": True, "alert": "Producto añadido"}

@app.post("/update")
async def update_product(request: Request):
    res = await request.json()
    print(res)
    product_name = res["product_name"]
    product_description = res["product_description"]
    product_price = res["product_price"]
    product_stock = res["product_stock"]
    product_id = res["product_id"] if res["product_id"].strip() != "" else 'undefined' 
    if "product_unique_id" in res:
            product_unique_id = res["product_unique_id"]
            database.update_database("product_name", "product_unique_id", product_unique_id, product_name)
            database.update_database("product_description", "product_unique_id", product_unique_id, product_description)
            database.update_database("product_price", "product_unique_id", product_unique_id, product_price)
            database.update_database("product_stock", "product_unique_id", product_unique_id, product_stock)
            database.update_database("product_id", "product_unique_id", product_unique_id, product_id)
            return {"status": True, "alert": "Producto actualizado"}
    else:
        return {"status": False, "alert": "Hay campos vacios"}
            

@app.post("/get/inventory")
async def get_inventory(request: Request):
    res = await request.json()
    print(res)
    if "product_unique_id" in res:
        id_to_fetch = res["product_unique_id"]
        data = database.fetch_database_by("product_unique_id", id_to_fetch)
        print("pene")
        to_return = []
        if data:
            for item in data:
                to_return.append(
                    {
                        "id": item[0],
                        "product_user_id": item[1],
                        "product_unique_id": item[2],
                        "product_id": item[3],
                        "product_name": item[4],
                        "product_description": item[5],
                        "product_price": item[6],
                        "product_image": item[7],
                        "product_stock": item[8],
                        "product_is_hidden": item[9],
                    }
                )
            print(to_return)
            return {"data": list(reversed(to_return))} # reversed devuelve un iterable
    id_to_fetch = res["id"]
    data = database.fetch_database_by("product_user_id", id_to_fetch)
    columns = ["id", "product_user_id", "product_unique_id", "product_id", "product_name", "product_description", "product_price", "product_image", "product_stock"]
    to_return = []
    if data:
        for item in data:
            to_return.append(
                {
                    "id": item[0],
                    "product_user_id": item[1],
                    "product_unique_id": item[2],
                    "product_id": item[3],
                    "product_name": item[4],
                    "product_description": item[5],
                    "product_price": item[6],
                    "product_image": item[7],
                    "product_stock": item[8],
                    "product_is_hidden": item[9],
                }
            )
        print(to_return)
        return {"data": list(reversed(to_return))} # reversed devuelve un iterable
    else:
        return {"data": []}


@app.post("/hide/inventory")
async def hide_products(request: Request):
    data = await request.json()
    id_to_fetch = data["id"]
    for item in data["toHide"]:
        print(item)
        database.update_database("product_is_hidden", "product_unique_id", item, True)
    print(data)
    data = database.fetch_database_by("product_user_id", id_to_fetch)
    to_return = []
    if data:
        for item in data:
            to_return.append(
                {
                    "id": item[0],
                    "product_user_id": item[1],
                    "product_unique_id": item[2],
                    "product_id": item[3],
                    "product_name": item[4],
                    "product_description": item[5],
                    "product_price": item[6],
                    "product_image": item[7],
                    "product_stock": item[8],
                    "product_is_hidden": item[9],
                }
            )
        print(to_return)
        return {"data": list(reversed(to_return)), "status": True, "alert": "Producto oculto de la vista"} # reversed devuelve un iterable
    else:
        return {"data": []}

@app.post("/show/inventory")
async def hide_products(request: Request):
    data = await request.json()
    id_to_fetch = data["id"]
    for item in data["toShow"]:
        print(item)
        database.update_database("product_is_hidden", "product_unique_id", item, False)
    print(data)
    data = database.fetch_database_by("product_user_id", id_to_fetch)
    to_return = []
    if data:
        for item in data:
            to_return.append(
                {
                    "id": item[0],
                    "product_user_id": item[1],
                    "product_unique_id": item[2],
                    "product_id": item[3],
                    "product_name": item[4],
                    "product_description": item[5],
                    "product_price": item[6],
                    "product_image": item[7],
                    "product_stock": item[8],
                    "product_is_hidden": item[9],
                }
            )
        print(to_return)
        return {"data": list(reversed(to_return)), "status": True, "alert": "Producto mostrado de la vista"} # reversed devuelve un iterable
    else:
        return {"data": []}

@app.get("/create/client")
async def create_cliente():
    return {"date": date.today()}

@app.get("/create/bill")
async def create_cliente():
    return {"bill_id": f"{date.today().year}_{get_random_id(20)}"}

@app.post("/get/clients")
async def get_clients(request: Request):
    res = await request.json()
    print(res)
    data = clients.fetch_database_by("client_for_user_id", res["user_id"])
    items = []
    if data:
        for i in data:
            items.append(
                {
                    "client_unique_id": i[1],
                    "client_for_user_id": i[2],
                    "client_name": i[3],
                    "client_email": i[4],
                    "client_adress": i[5],
                    "client_phone": i[6],
                    "client_notes": i[7],
                    "client_register_date": i[8],
                    "client_is_hidden": i[9],
                    
                }
            )
    print(items)
    return {"data": list(reversed(items))}

@app.post("/get/client")
async def get_client(request: Request):
    res = await request.json()
    print(res)
    data = clients.fetch_database_by("client_unique_id", res["client_id"])
    items = []
    if data:
        for i in data:
            items.append(
                {
                    "client_unique_id": i[1],
                    "client_for_user_id": i[2],
                    "client_name": i[3],
                    "client_email": i[4],
                    "client_adress": i[5],
                    "client_phone": i[6],
                    "client_notes": i[7],
                    "client_register_date": i[8],
                    "client_is_hidden": i[9],
                }
            )
    print(items)
    return {"data": list(reversed(items))}

@app.post("/send/client")
async def client_sended(request: Request):
    res = await request.json()
    if res["client_for_user_id"].strip() != "" and res["client_name"].strip() != "":
        client_for_user_id = res["client_for_user_id"]
        client_name = res["client_name"]
        client_email = res["client_email"]
        client_adress = res["client_adress"]
        client_phone = res["client_phone"]
        client_notes = res["client_notes"]
        client_register_date = res["client_register_date"]
        print(client_for_user_id, client_name, client_email, client_adress, client_phone, client_notes, client_register_date)
        clients.insert_database(client_unique_id=get_random_id(), client_for_user_id=client_for_user_id, client_name=client_name, client_email=client_email, client_adress=client_adress, client_phone=client_phone, client_notes=client_notes, client_register_date=client_register_date, client_is_hidden=False)
        return {"status": True, "alert": "Cliente añadido correctamente"}
    else:
        return {"status": False, "alert": "Hay campos vacíos"}
        
@app.post("/update/client")
async def update_client(request: Request):
    res = await request.json()
    print(res)
    if "user_id" in res and "client_unique_id" in res and res["client_name"].strip() != "":
        client_unique_id = res["client_unique_id"]
        client_name = res["client_name"]
        client_email = res["client_email"]
        client_adress = res["client_adress"]
        client_phone = res["client_phone"]
        client_notes = res["client_notes"]
        clients.update_database("client_name", "client_unique_id", client_unique_id, client_name)
        clients.update_database("client_email", "client_unique_id", client_unique_id, client_email)
        clients.update_database("client_adress", "client_unique_id", client_unique_id, client_adress)
        clients.update_database("client_phone", "client_unique_id", client_unique_id, client_phone)
        clients.update_database("client_notes", "client_unique_id", client_unique_id, client_notes)
        return {"status": True, "alert": "Cliente actualizado con éxito"}
    else:
        return {"status": False, "alert": "Hay campos vacíos"}
    
@app.post("/hide/client")
async def hide_client(request: Request):
    res = await request.json()
    print(res)
    if res["user_id"].strip() != "" and res["to_hide"] != []:
        for item in res["to_hide"]:
            clients.update_database("client_is_hidden", "client_unique_id", item, True)
            
        data = clients.fetch_database_by("client_for_user_id", res["user_id"])
        items = []
        if data:
            for i in data:
                items.append(
                    {
                        "client_unique_id": i[1],
                        "client_for_user_id": i[2],
                        "client_name": i[3],
                        "client_email": i[4],
                        "client_adress": i[5],
                        "client_phone": i[6],
                        "client_notes": i[7],
                        "client_register_date": i[8],
                        "client_is_hidden": i[9],
                    }
                )
        print(items)
        return {"status": True, "alert": "Producto oculto de la vista", "data": list(reversed(items))}
    else:
        return {"status": False, "alert": "Error 03. Contacta soporte"}
    
@app.post("/send/bill")
async def send_bill(request: Request):
    res = await request.json()
    print(res)
    bills.insert_database(bill_unique_id=res["bill_id"], bill_for_user_id=res["user_id"], bill_products=json.dumps(res["products"]), bill_client=res["client"], bill_created_date=date.today(), bill_date=res["bill_date"], bill_status=res["status"])
    data = bills.fetch_database()
    match res["status"]:
        case "Pendiente":
            print("FActura pendiente")
        case "Pagada":
            for product in res["products"]:
                id = product["id"]
                quantity = int(product["quantity"])
                current_quantity = database.fetch_database_by("product_unique_id", id)
                current_quantity = int(current_quantity[0][8])
                final_quantity = current_quantity - quantity
                print(f"----------------- {current_quantity}---------------")
                print(f"----------------- {quantity}---------------")
                database.update_database("product_stock", "product_unique_id", id, final_quantity)
                database.fetch_database()
        case "Anulada":
            print("fac anula")
    return {"status": True, "alert": "Factura generada con éxito"}


@app.post("/get/bills")
async def get_bills(request: Request):
    res = await request.json()
    data = bills.fetch_database_by("bill_for_user_id", res["user_id"])
    print(data)
    to_return = []
    for x in data:
        to_return.append(
            {
                "bill_unique_id": x[1],
                "bill_products": x[3],
                "bill_client": x[4],
                "bill_created_date": x[5],
                "bill_date": x[6],
                "bill_status": x[7],
            }
        )
    return {"data": list(reversed(to_return))}


@app.post("/update/bill/")
async def update_bill(request: Request):
    res = await request.json()
    print(res)
    bill = bills.fetch_database_by("bill_unique_id", res["bill_unique_id"])
    current_bill_status = bill[0][7]
    bill_products = bill[0][3]
    bill_status = res["to_status"]
    print(bill_status)
    if bill_status == "Pagada" and (current_bill_status == "Pendiente" or current_bill_status == "Anulada"):
        for product in json.loads(bill_products):
            current_stock = database.fetch_database_by("product_unique_id", product["id"])
            current_stock = int(current_stock[0][8])
            new_stock = current_stock - int(product["quantity"])
            database.update_database("product_stock", "product_unique_id", product["id"], new_stock)
            bills.update_database("bill_status", "bill_unique_id", res["bill_unique_id"], bill_status) # pagada
    
    elif bill_status != "Pagada" and current_bill_status != "Pagada":
        bills.update_database("bill_status", "bill_unique_id", res["bill_unique_id"], bill_status) # can be either pendiente o anulado
    
    elif bill_status != "Pagada" and current_bill_status == "Pagada":
        for product in json.loads(bill_products):   
            current_stock = database.fetch_database_by("product_unique_id", product["id"])
            current_stock = int(current_stock[0][8])
            new_stock = current_stock + int(product["quantity"])
            database.update_database("product_stock", "product_unique_id", product["id"], new_stock)
            bills.update_database("bill_status", "bill_unique_id", res["bill_unique_id"], bill_status) # pagada
            
