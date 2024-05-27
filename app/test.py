metadata = {'masterdata.csv': {'table_name': 'MASTERFILE', 
                               'column_names': ['ITM', 'DES', 'TYPE', 'FAM'], 
                               'column_mapping': {'ITM': 'DESCRIPTION', 'DES': 'ITEM_TYPE', 'TYPE': 'ITEM', 'FAM': 'PRODFAM'}}, 
            'prodfam_data.csv': {'table_name': 'PRODFAM', 'column_names': ['PRODFAM', 'DESCRIPTION'], 'column_mapping': {'PRODFAM': 'DESCRIPTION', 'DESCRIPTION': 'PRODFAM'}}}

for file in metadata:
    print(file)
    order = []
    # print(file)
    # print(x[file]['column_mapping'])
    filcol = metadata[file]['column_mapping']
    for col in filcol:
        # print(y[col])
        order.append(filcol[col])
    if metadata[file]['table_name'] == 'MASTERFILE':
        print('masterfile')
        print(order)
    elif metadata[file]['table_name'] == 'PRODFAM':
        print('prodfam')
        print(order)
