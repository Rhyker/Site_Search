import pyodbc


def search_to_use(lot_num, unit_num, house_num, road_name, road_type, suburb, postcode):
    # Checks what variables have been provided and returns the search or error msg to use

    if road_name == '' and suburb == '':
        result = 'No Road Name or Suburb provided, please enter at least one and try again.'
        return result

    if house_num != '' and lot_num != '':
        result = query_builder(1, lot_num, unit_num, house_num, road_name, road_type, suburb, postcode)
    elif house_num != '' and lot_num == '':
        result = query_builder(2, lot_num, unit_num, house_num, road_name, road_type, suburb, postcode)
    elif house_num == '' and lot_num != '':
        result = query_builder(3, lot_num, unit_num, house_num, road_name, road_type, suburb, postcode)
    elif house_num == '' and lot_num == '':
        # result = 'No Lot or House number provided, please enter at least one and try again.'
        result = query_builder(1, lot_num, unit_num, house_num, road_name, road_type, suburb, postcode)
    else:
        result = 'Not enough site information provided (SEARCH_TO_USE(ELSE ERROR))'

    return result


def query_builder(query_number, lot_num, unit_num, house_num, road_name, road_type, suburb, postcode):

    lot_state = "LOT_NUMBER = '" + lot_num + "'"
    unit_state = "BUNIT_ID1 = '" + unit_num + "'"
    house_state = "HSE_NUM1 = '" + house_num + "'"
    road_n_state = "ROAD_NAME = '" + road_name + "'"
    road_t_state = "ROAD_TYPE = '" + road_type + "'"
    suburb_state = "LOCALITY = '" + suburb + "'"
    postcode_state = "POSTCODE = '" + postcode + "'"

    site_info = [lot_num, unit_num, house_num, road_name, road_type, suburb, postcode]
    filter_list = [lot_state, unit_state, house_state, road_n_state, road_t_state, suburb_state, postcode_state]
    filters_to_use = []
    filters = ''

    # Creates a list of use-able filters and appends to a separate list using original items matching index
    for item in site_info:
        if item != '':
            filters_to_use.append(filter_list[site_info.index(item)])

    # Combines the use-able statements to provide the filter list
    for item in filters_to_use:
        filters = filters + item + ' AND '

    # Appends final consistent filter
    filters = filters + "STATE = 'VIC'"

    if query_number == 1 or query_number == 2:
        statement = "SELECT * FROM ADDRESS " \
                    "LEFT JOIN PARCEL_PROPERTY " \
                    "ON PARCEL_PROPERTY.PR_PFI = ADDRESS.PR_PFI " \
                    "LEFT JOIN PARCEL_LOT " \
                    "ON PARCEL_PROPERTY.PARCEL_PFI = PARCEL_LOT.PFI " \
                    "LEFT JOIN [VICMAP_DATA].[dbo].[LOCALITY_ZONES] " \
                    "ON [VICMAP_DATA].[dbo].[LOCALITY_ZONES].LOCALITY_NAME = [VICMAP_DATA].[dbo].[ADDRESS].LOCALITY " \
                    "WHERE " + filters + " ORDER BY ADDRESS.LOCALITY, ADDRESS.ROAD_NAME, ADDRESS.NUM_ADD"
        returned_query = query_sql(statement)
        return returned_query
    elif query_number == 3:
        statement = "SELECT * FROM PARCEL_LOT " \
                    "LEFT JOIN PARCEL_PROPERTY " \
                    "ON PARCEL_LOT.PFI = PARCEL_PROPERTY.PARCEL_PFI " \
                    "LEFT JOIN ADDRESS " \
                    "ON PARCEL_PROPERTY.PR_PFI = ADDRESS.PR_PFI " \
                    "LEFT JOIN [VICMAP_DATA].[dbo].[LOCALITY_ZONES] " \
                    "ON [VICMAP_DATA].[dbo].[LOCALITY_ZONES].LOCALITY_NAME = [VICMAP_DATA].[dbo].[ADDRESS].LOCALITY " \
                    "WHERE " + filters + " ORDER BY ADDRESS.LOCALITY, ADDRESS.ROAD_NAME, ADDRESS.NUM_ADD"

        returned_query = query_sql(statement)
        return returned_query


def query_sql(query):
    try:
        connection = pyodbc.connect(r"Driver={SQL Server};"
                                    r"Server=EAG-ELT-SVR-001;"
                                    r"Database=VICMAP_DATA;"
                                    r"Trusted_Connection=yes;")

        cursor = connection.cursor()
        cursor.execute(query)

        response = cursor.fetchall()

        return response

    except Exception as e:
        # Checks if a network error occurs (Response will be NoneType)
        print(e)
        response = 'General Network Error: Unable to reach database, check your network connection and try again.'
        return response
