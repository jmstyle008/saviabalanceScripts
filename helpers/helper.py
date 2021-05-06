def getVendorList(dbConn):
    vendorListDB = dbConn.runQuery("select id, name from product_vendor")
    vendorDB = []
    for vendor in vendorListDB:
        vendorDB.insert(vendor[0] - 1, vendor[1])
    return vendorDB


def getTypeList(dbConn):
    typeListDB = dbConn.runQuery("select id, name from product_type")
    listDB = []
    for typelist in typeListDB:
        listDB.insert(typelist[0] - 1, typelist[1])
    return listDB


def validateVendors(uniqueList, baseList, dbConn):
    for vendor in uniqueList:
        if vendor not in baseList:
            insertQuery = "insert into product_vendor (name,vendor,available) values('" + \
                vendor + "','" + vendor + "',1)"
            dbConn.insertQuery(insertQuery)


def validateList(uniqueList, baseList, dbConn):
    for vendor in uniqueList:
        if vendor not in baseList:
            insertQuery = "insert into product_type (name) values('" + \
                vendor + "')"
            dbConn.insertQuery(insertQuery)
