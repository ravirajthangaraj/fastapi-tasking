

from pymongo.cursor import Cursor


def modify_object_id(result):
    if isinstance(result, dict):  # for single result
        if result.get('_id'):
            result['_id'] = str(result['_id'])
    elif isinstance(result, Cursor):  # for multiple results
        modified_result = list()
        for res in result:
            if res.get('_id'):
                res['_id'] = str(res['_id'])
                modified_result.append(res)
        return modified_result


def build_response(status_code, message, data, errors):
    pass
