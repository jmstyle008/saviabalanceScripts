from files import readFile
from database import dbConnect
from helpers import helper


path1 = "/Users/user/Downloads/PNG/downloaded/"
path2 = "/Users/user/Downloads/PNG/downloaded/NO_LISTA"

importCsvFilePath = "/Users/user/Downloads/"

importCSVFile = readFile.ReadFile(importCsvFilePath, "products_export_1.csv")
importedData = importCSVFile.readShopifyContent()
dbConn = dbConnect.dbConnect()

# GATHER VENDOR LIST TO INSERT NEW ONES

vendorList = []
typeList = []

for row in importedData:
    vendorList.append(row['Vendor'].strip().upper())
    typeList.append(row['Type'].strip().upper())

vendorUniqueList = list(set(vendorList))
typeUniqueList = list(set(typeList))

helper.validateVendors(vendorUniqueList, helper.getVendorList(dbConn), dbConn)
helper.validateList(typeUniqueList, helper.getTypeList(dbConn), dbConn)
print("Starting to insert a total of {} products into the db".format(len(importedData)))

vendorDB = helper.getVendorList(dbConn)
listDB = helper.getTypeList(dbConn)

for row in importedData:
    findQuery = "select * from product where Variant_SKU = '{}'" .format(
        row['Variant SKU'])
    result = dbConn.runQuery(findQuery)
    if len(result) == 0:
        insertQuery = "INSERT INTO PRODUCT (handle,title,body,vendor_id,type_id, tags, published, option1_name, option1_value, Variant_SKU,variant_grams,variant_inventory_qty, variant_inventory_policy, Variant_Fulfillment_Service, Variant_Price, Variant_Requires_Shipping, Variant_Taxable, Variant_Barcode, Image_Src, Image_Position, Image_Alt, Variant_Weight_Unit, Status) values('{}','{}','{}', {}, {},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
            row["Handle"],
            row['Title'],
            row['Body (HTML)'],
            vendorDB.index(row['Vendor']) + 1,
            listDB.index(row['Type']) + 1,
            row['Tags'],
            row['Published'],
            row['Option1 Name'],
            row['Option1 Value'],
            row['Variant SKU'],
            row['Variant Grams'],
            row['Variant Inventory Qty'],
            row['Variant Inventory Policy'],
            row['Variant Fulfillment Service'],
            row['Variant Price'],
            row['Variant Requires Shipping'],
            row['Variant Taxable'],
            row['Variant Barcode'],
            row['Image Src'],
            row['Image Position'],
            row['Image Alt Text'],
            row['Variant Weight Unit'],
            row['Status']
        )
        dbConn.insertQuery(insertQuery)
