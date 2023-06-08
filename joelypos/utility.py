
from django.db import connection


def get_products_list(page_no,page_size, product_name, status_type,cats,color,size):
    with connection.cursor() as cursor:
        cursor.callproc('GET_PRODUCTS_LIST', [page_no,page_size, product_name, status_type,cats,color,size])
        results = cursor.fetchall()
        # Perform additional operations with the cursor if needed
    
    # Close the database connection
    connection.close()
    
    return results