from files import readFile
from database import dbConnect
from helpers import helper


path1 = "/Users/user/Downloads/PNG/downloaded/"
path2 = "/Users/user/Downloads/PNG/downloaded/NO_LISTA"

importCsvFilePath = "/Users/user/Downloads/"

imagePath = readFile.ReadFile(path1)


importCSVFile = readFile.ReadFile(importCsvFilePath, "products_export_1.csv")
importedData = importCSVFile.readShopifyContent()
dbConn = dbConnect.dbConnect()

productListToAdd = "select p.id , title, body, handle, pv.\"name\" as brand , pt.\"name\" as departamento , variant_sku , eleventa_name "
productListToAdd += "from product p join product_vendor pv on pv.id = p.vendor_id join product_type pt on pt.id = type_id where handle = 'TBD' order by vendor_id , type_id ;"

products2Upload = dbConn.runQuery(productListToAdd)

productList = []
for image in imagePath.listFiles():
    productBreakDown = image.split("_")
    for product in products2Upload:
        sku = product[6]
        if sku == productBreakDown[0] and productBreakDown[1].find("1") == 0:
            id = product[0]
            title = product[1]
            body = product[2]
            brand = product[4]
            prodType = product[5]
            eleventaName = product[7]
            handle = brand.lower().replace(" ", "-") + "-" + title.lower().replace(" ",
                                                                                   "-").replace("(", "-").replace(")", "-")
            handle = handle.replace(
                "--", "-").replace(".", "").replace(",", "").strip()
            productList.append(product)
            tags = handle.replace("-", ',')
            published = 'TRUE'
            image_position = 1
            image_alt = tags.replace(",", " ")
            image_source = "https://cdn.shopify.com/s/files/1/0561/9669/4225/files/" + image
            updateQuery = "UPDATE PRODUCT SET handle = '{}', published = '{}', tags = '{}', image_position = {}, image_alt = '{}', image_src = '{}' where variant_sku = '{}'".format(
                handle,
                published,
                tags,
                image_position,
                image_alt,
                image_source,
                sku)
            # will update all possible products
            dbConn.insertQuery(updateQuery)
