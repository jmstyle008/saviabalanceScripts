import math
from files import readFile
from database import dbConnect
from helpers import helper


importCsvFilePath = "/Users/user/Downloads/"

importCSVFile = readFile.ReadFile(importCsvFilePath, "eleventa.csv")
importedData = importCSVFile.readEleventaContent()
dbConn = dbConnect.dbConnect()

newVendors = []
newType = []
for row in importedData:
    newVendors.append(row["MARCA"].strip().upper())
    newType.append(row["DEPARTAMENTO"].strip().upper())
vendorList = set(newVendors)
typeList = set(newType)


helper.validateVendors(vendorList, helper.getVendorList(dbConn), dbConn)
helper.validateList(typeList, helper.getTypeList(dbConn), dbConn)


vendorDB = helper.getVendorList(dbConn)
listDB = helper.getTypeList(dbConn)
for row in importedData:
    query = False
    if row["Venta en linea"] == 'si':
        # find query
        findQuery = "select variant_sku from product where variant_sku = '{}'".format(
            row['CODIGO'])
        # updating existing product
        if len(dbConn.runQuery(findQuery)) > 0:
            query = "UPDATE product set eleventa_name = '{}', cost_per_item = '{}', menudeo = '{}', mayoreo = '{}', variant_price = '{}' where variant_sku = '{}'".format(
                row["ARTICULO"],
                row["COSTO"].replace("$", ""),
                row["MENUDEO"].replace("$", ""),
                row["MAYOREO"].replace("$", ""),
                math.ceil(float(row["ONLINE"].replace("$", ""))),
                row["CODIGO"]
            )
        # creating new product
        else:
            query = "INSERT INTO PRODUCT (handle,title, body, vendor_id, type_id, published, option1_name, option1_value, variant_sku, variant_grams, variant_inventory_qty, variant_inventory_policy, variant_fulfillment_service, variant_price, variant_requires_shipping, variant_taxable, variant_weight_unit, status, enabled_online, cost_per_item, eleventa_name, menudeo, mayoreo) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                "TBD",
                row['ARTICULO'].strip(),
                row['ARTICULO'].strip(),
                vendorDB.index(row['MARCA'].strip().upper()) + 1,
                listDB.index(row['DEPARTAMENTO'].strip().upper()) + 1,
                "FALSE",
                "Title",
                "Default Title",
                row['CODIGO'],
                "100",
                "100",
                "deny",
                "manual",
                row["ONLINE"].replace("$", ""),
                "TRUE",
                "FALSE",
                "g",
                "draft",
                "0",
                row["COSTO"].replace("$", ""),
                row['ARTICULO'],
                row['MENUDEO'].replace("$", ""),
                row['MAYOREO'].replace("$", "")
            )
        if(query is not False):
            dbConn.insertQuery(query)
