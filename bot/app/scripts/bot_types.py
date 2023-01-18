import enum

class ProductType(enum.Enum):
    '''
    Type of product (Indications All products can be obtained from the database)
    '''
    all = 'items_All'
    cases = 'items_Cases'
    headphones = 'items_Headphones'

    def get_type_by_value(value:str):
        '''
        Convert string to product type
        '''
        for val in ProductType:
            if val.value == value:
                return val
        print('[ERROR] There is no such type')