import unittest


from modules.sql_modules.sql_string_helper import search_by_fully_qualified_name


class TestStringHelper(unittest.TestCase):
    def test_search_by_fully_qualified_name(self):
        search_what = 'tbl_name'
        test_cases = [('tbl_name', True),
                      ('dbo.tbl_name', True),
                      ('stg.tbl_name', False),
                      ('dbo.[tbl_name]', True)]

        for ref, result in test_cases:
            sql = f"""create sp as 
                select * from {ref}"""
            pos = search_by_fully_qualified_name(search_in=sql, search_what=search_what)
            if result:
                assert pos
                print(f'{ref=};{pos=}')
            else:
                assert pos is None



if __name__ == '__main__':

    unittest.main()
