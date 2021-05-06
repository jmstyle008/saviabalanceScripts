import os
from database import dbConnect
from files import readFile
from helpers import helper
import datetime
import shutil

newProductQuery = "select * from product where handle <>'TBD' and enabled_online = 0"
dbConn = dbConnect.dbConnect()
path1 = "/Users/user/Downloads/PNG/downloaded/"
path2 = "/Users/user/Downloads/PNG/downloaded/NO_LISTA"

imagePath = readFile.ReadFile(path1)

newProducts = dbConn.runQuery(newProductQuery)
vendorList = helper.getVendorList(dbConn)
typeList = helper.getTypeList(dbConn)

productsToUpdate2DB = []
csvFileCreation = []
csvFields = []

for product in newProducts:
    productDictionary = {}
    imageDictionary = {}
    pid = product[0]
    handle = str(product[1])
    title = product[2]
    body = product[3]
    vendor = vendorList[product[4] - 1]
    prodType = typeList[product[5] - 1]
    tags = product[6]
    published = product[7]
    option1_name = product[8]
    option1_value = product[9]
    variant_sku = product[10]
    variant_grams = product[11]
    variant_inventory_qty = product[12]
    variant_inventory_policy = product[13]
    variant_Fulfillment_Service = product[14]
    variant_price = product[15]
    variant_requires_shipping = product[16]
    variant_taxable = product[17]
    image_source = product[19]
    image_position = product[20]
    image_alt = product[21]
    variant_weight_unit = product[24]
    status = "active"
    enabled_online = 1
    cost_per_item = product[27]

    productDictionary["Handle"] = str(handle)
    productDictionary['Title'] = str(title)
    productDictionary['Body (HTML)'] = str(body)
    productDictionary['Vendor'] = str(vendor)
    productDictionary['Type'] = str(prodType)
    productDictionary['Tags'] = str(tags)
    productDictionary['Published'] = str(published)
    productDictionary['Option1 Name'] = str(option1_name)
    productDictionary['Option1 Value'] = str(option1_value)
    productDictionary['Variant SKU'] = str(variant_sku)
    productDictionary['Variant Grams'] = str(variant_grams)
    productDictionary['Variant Inventory Qty'] = str(variant_inventory_qty)
    productDictionary['Variant Inventory Policy'] = str(
        variant_inventory_policy)
    productDictionary['Variant Fulfillment Service'] = str(
        variant_Fulfillment_Service)
    productDictionary['Variant Price'] = str(variant_price)
    productDictionary['Variant Requires Shipping'] = str(
        variant_requires_shipping)
    productDictionary['Variant Taxable'] = str(variant_taxable)
    productDictionary['Image Src'] = str(image_source)
    productDictionary['Image Position'] = str(image_position)
    productDictionary['Image Alt Text'] = str(image_alt)
    productDictionary['Variant Weight Unit'] = str(variant_weight_unit)
    productDictionary['Cost per item'] = str(cost_per_item)
    productDictionary['Status'] = str(status)

    if(len(csvFields) == 0):
        csvFields = list(productDictionary.keys())

    productsToUpdate2DB.append("update product set status = '{}', enabled_online = '{}' where id = {}".format(
        status,
        enabled_online,
        pid
    ))
    csvFileCreation.append(productDictionary)
    imageArray = []
    for image in imagePath.listFiles():
        imageBreakDown = image.split("_")
        position = imageBreakDown[1][0]

        if imageBreakDown[0] == variant_sku and position == "1":
            shutil.copy2(path1 + "/" + image,
                         "/Library/WebServer/Documents/JN/csvFiles/")
        if imageBreakDown[0] == variant_sku and position != "1":
            imageArray.insert(int(position), image)
        imageArray.sort()
    count = 2
    for image in imageArray:
        imageDictionary = {}
        imageDictionary["Handle"] = handle
        imageDictionary["Image Src"] = "https://cdn.shopify.com/s/files/1/0561/9669/4225/files/" + image
        imageDictionary["Image Position"] = count
        count += 1
        csvFileCreation.append(imageDictionary)
        shutil.copy2(path1 + "/" + image,
                     "/Library/WebServer/Documents/JN/csvFiles/")
imagePath.createCSVFile("/Library/WebServer/Documents/JN/csvFiles", "shopifyUpload{}.csv".format(
    str(datetime.date.today()).replace("-", "_")), csvFields, csvFileCreation)

for query in productsToUpdate2DB:
    dbConn.insertQuery(query)
