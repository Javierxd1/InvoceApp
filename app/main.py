from fastapi import FastAPI, Request
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from db import create_all_tables
from app.routers.customers import routerCustomers
from app.routers.transactions import routerTransactions
from app.routers.invoices import routerInvoices
from app.routers.plans import routerPlans


app = FastAPI(lifespan=create_all_tables)

app.include_router(routerCustomers)
app.include_router(routerTransactions)
app.include_router(routerInvoices)
app.include_router(routerPlans)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time() #Mide el tiempo inicial antes del request
    response = await call_next(request) #Función que espera, mientras se ejecuta el request
    process_time = time.time() - start_time #Tiempo final después del request
    print(f"Request realizado a {request.url} se completo en {process_time:.4f} segundos") #Impresión del tiempo
    return response
    

@app.get('/')
async def root():
    return{'message':'Hola Jaiver'}

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}


@app.get("/time/{iso_code}/{format}")
async def get_time_by_iso(iso_code: str,format: str):
    iso = iso_code.upper()
    timeZone = country_timezones.get(iso)

    if timeZone is None:
        return{'error':'ISO code not found'}

    tz = ZoneInfo(timeZone)
    if format == "24":
        current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    elif format == "12":
        current_time = datetime.now(tz).strftime("%Y-%m-%d %I:%M:%S %p")
    else:
        return{'error':'Format not found'}

    return{'current time':current_time}





