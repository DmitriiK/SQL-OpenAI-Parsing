import unittest


from modules.sql_modules.sql_string_helper import find_sql_objects


class TestStringHelper(unittest.TestCase):

    def test_find_sql_objects(self):
        # Test cases for search_what='my_tbl'
        search_what = 'my_tbl'
        test_cases = [
            ('select * from my_tbl', True),
            ('select * from my_tbl2', False),
            ('select * from dbo.my_tbl', True),
            ('select * from stg.my_tbl', False),
            ('select * from dbo.[my_tbl ]', True),
            ('select * from my_db.stg.my_tbl', False),
            ('select * from my_srv.my_db.stg.my_tbl', False),
        ]
        for search_where, is_match_exp in test_cases:
            result = find_sql_objects(search_where, search_what)
            if is_match_exp:
                assert result, f'Failed on {search_where=}:  {search_what=}'
            else :
                assert not result

    
        
        # Test cases for search_what='stg.my_tbl'
        search_what = 'stg.my_tbl'
        test_cases = [
                ('select * from my_tbl', False),
                ('select * from my_tbl2', False),
                ('select * from dbo.my_tbl', False),
                ('select * from stg.my_tbl', True),
                ('select * from [stg].[my_tbl ]', True),
                ('select * from my_db.stg.my_tbl', False),
                ('select * from my_srv.my_db.stg.my_tbl', False),
            ]
        for search_where, is_match_exp in test_cases:
            result = find_sql_objects(search_where, search_what)
            if is_match_exp:
                assert result, f'Failed on {search_where=}:  {search_what=}'
            else :
                assert not result
        
        print('All tests passed.')

if __name__ == '__main__':

    unittest.main()
