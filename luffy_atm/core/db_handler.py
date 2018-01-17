#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15
import os
import json
from conf import settings
from core import utils


def get_logics():
    """
    限制逻辑判断符
    :return: 
    """
    return '=', '>', '<', '>=', '<=', '!=', 'like'


def check_logic(logic_symbol):
    """
    逻辑判断符是否合法
    :param logic_symbol: 
    :return: 
    """
    return logic_symbol in get_logics()


def do_logic(field_value, logic_symbol, value):
    """
    处理条件字段
    :param field_value: 
    :param logic_symbol: 
    :param value: 
    :return: 
    """
    if not check_logic(logic_symbol.strip()):
        print('逻辑符非法')
        return False
    value = utils.strip_extend(value) if isinstance(value, str) else str(value)
    field_value = utils.strip_extend(field_value) if isinstance(field_value, str) else str(field_value)
    option = logic_symbol.strip().lower()
    if option == 'like':
        string = "'%s' in '%s'" % (value, field_value)
    elif option == '=':
        string = "'%s' == '%s' " % (field_value, value)
    else:
        string = "'%s' %s '%s' " % (field_value, logic_symbol, value)
    return string


def check_field(table, *args):
    """
    检查表中是否存在字段
    :param table: 
    :param args: 
    :return: 
    """
    fields = []
    if args[0] == '*':
        return settings.DATABASE['tables'][table]['structure'].keys()
    for field in args:
        field = field.strip()
        if field not in settings.DATABASE['tables'][table]['structure'].keys():
            print('字段 %s 不匹配' % field)
            return False
        fields.append(field)
    return fields


def data_api(action, table, **kwargs):
    """
    仅提供增加修改查询操作
        1.查询语句中所有保留关键字大写
    :param action: FIND ADD UPDATE 
    :param table: 表名 
    :param kwargs: 附加参数 : where，用于条件过滤；set，用于设置更新字段；fields，查询指定字段
    :return: 
    """
    db_params = settings.DATABASE
    if db_params['engine'] == 'file_storage':
        actions = {
            'add': add_action,
            'update': update_action,
            'find': find_action,
        }
    elif db_params['engine'] == 'mysql':
        actions = {
            'add': add_formatter,
            'update': update_formatter,
            'find': find_formatter,
        }
    else:
        print("暂不支持存储引擎 %s " % db_params['engine'])
        return False
    if action not in actions.keys():
        print('错误的查询操作类型')
        return False
    ret = actions[action](table, **kwargs)

    return ret


def fetch_all(table):
    """
    获取表全部记录
    :param table: 
    :return: 
    """
    records = os.listdir(settings.DATABASE['tables'][table]['file_path'])
    if not records:
        return []
    result = []
    for record in records:
        with open(os.path.join(settings.DATABASE['tables'][table]['file_path'], record)) as f:
            entry = json.load(f)
            if isinstance(entry, dict):
                # 检查表结构是否完整 and set(entry.keys()).issubset(settings.DATABASE['tables'][table]['structure'])
                result.append(entry)
    return result


def find_action(table, **kwargs):
    """
    获取符合条件的记录
    :param table: 
    :param kwargs: 
    :return: 
    """
    fields = kwargs.get('fields', ('*',))
    where = kwargs.get('where')
    ret = check_field(table, *fields)
    if isinstance(ret, int):
        return ret
    result = []
    records = fetch_all(table)
    if not len(records):
        return result
    for record in records:
        available = True
        if where:
            for i in where:
                if 'field' not in i:
                    available = False
                    break
                if 'logic' not in i:
                    logic_symbol = '='
                else:
                    logic_symbol = i['logic']
                statement = do_logic(record[i['field']], logic_symbol, i['value'])
                if not eval(statement):
                    available = False
                    break
        if not available:
            continue
        tmp = {}
        for field in ret:
            tmp[field] = record[field] if field in record else ''
        result.append(tmp)
    return result


def update_action(table, **kwargs):
    """
    更新符合条件的记录
    :param table: 
    :param kwargs: 
    :return: 
    """
    fields = kwargs.get('set')
    if not fields:
        print('语法错误')
        return False
    where = kwargs.get('where')
    ret = find_action(table, **{'where': where})
    if isinstance(ret, int) or not len(ret):
        print(ret)
        return ret
    # 不可修改保留字段的值
    if set(settings.DATABASE['tables'][table]['file_name']).issubset(fields.keys()):
        print('不可修改保留字段的值')
        return False
    update_count = 0
    for record in ret:
        record.update(fields)
        file_name = db_file_name(table, record)
        if file_name:
            storage_db(file_name, record)
            update_count += 1
        else:
            continue
    return update_count


def add_action(table, **kwargs):
    """
    添加记录
    :param table: 
    :param kwargs: 
    :return: 
    """
    fields = kwargs.get('fields')
    ret = check_field(table, *fields)
    if isinstance(ret, int):
        return ret
    file_name = db_file_name(table, fields)

    if file_name:
        storage_db(file_name, fields)
        return True

    return False


def storage_db(file, info):
    """
    存储记录到文件
    :param file: 
    :param info: 
    :return: 
    """
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(info, f)
    return True


def db_file_name(table, entry):
    """
    表文件命名
    :param table: 
    :param entry: 
    :return: 
    """
    file_rule = settings.DATABASE['tables'][table].get('file_rule', "join")
    fields = settings.DATABASE['tables'][table]['file_name']
    if not isinstance(fields, tuple):
        print("存储文件名称，命名字段 %s 异常" % type(fields))
        return False
    tmp = []
    for i in fields:
        if i in entry:
            tmp.append(entry[i] if isinstance(entry[i], str) else str(entry[i]))
        else:
            continue
    if not tmp:
        print('存储文件名称，字段 %s 异常' % ",".join(fields))
        return False
    if file_rule == 'md5':
        filename = utils.hash_md5("".join(tmp))
    elif file_rule == 'join':
        filename = "_".join(tmp)
    else:
        print('存储文件名称，命名规则 %s 异常' % file_rule)
        return False

    return os.path.join(settings.DATABASE['tables'][table]['file_path'], "%s.json" % filename)


def add_formatter(table, **kwargs):
    """
    添加语句生成器
    :param table: 
    :param kwargs: 
    :return: 
    """
    ret = check_field(table, *kwargs.keys())
    if isinstance(ret, int):
        return ret
    dic = []
    for i in kwargs:
        dic.append({'field': i, 'value': kwargs[i]})
    return " ".join(['INSERT INTO', table, 'VALUES(', assignment(dic), ')'])


def update_formatter(table, **kwargs):
    """
    更新语句生成器
    :param table: 
    :param kwargs: 
    :return: 
    """
    set_fields = kwargs.get('set')
    ret = check_field(table, *set_fields.keys())
    if isinstance(ret, int):
        return ret
    dic = []
    for i in set_fields:
        dic.append({'field': i, 'value': set_fields[i]})
    query = ['UPDATE', table, 'SET', assignment(dic)]

    conditions = kwargs.get('where')
    if conditions:
        query.append('WHERE')
        query.append(assignment(conditions, ' AND '))

    return " ".join(query)


def find_formatter(table, **kwargs):
    """
    检索语句生成器
    :param table:表名 
    :param kwargs: 条件
    :return: 
    """
    fields = kwargs.get('fields')
    ret = check_field(table, *fields)
    if isinstance(ret, int):
        return ret
    query = ['SELECT', ",".join(ret), 'FROM', table]
    conditions = kwargs.get('where')
    if conditions:
        query.append('WHERE')
        query.append(assignment(conditions, ' AND '))

    return " ".join(query)


def format_value(value, symbol='"'):
    """
    格式化字段值
    :param value: 
    :param symbol: 
    :return: 
    """
    return utils.append_symbol(value, start=symbol, end=symbol) if isinstance(value, str) else value


def assignment(fields, join_symbol=' , '):
    """
    格式化条件语句
    :param fields: 
    :param join_symbol: 连接符
    :return: 
    """
    li = []
    for i in fields:
        if 'logic' not in i:
            logic_symbol = '='
        else:
            logic_symbol = i['logic']

        li.append(" ".join([i['field'], logic_symbol, str(format_value(i['value']))]))

    return join_symbol.join(li)
