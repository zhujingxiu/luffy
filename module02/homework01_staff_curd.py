#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/10

import os
"""
作业题目：员工信息增删改查程序
作业需求：
    1.可进行模糊查询，语法至少支持下面3种查询语法:
        find name,age from staff_table where age > 22
        find * from staff_table where dept = "IT"
        find * from staff_table where enroll_date like "2013"
    
    2.可创建新员工纪录，以phone做唯一键(即不允许表里有手机号重复的情况)，staff_id需自增。语法如下：
        add staff_table Alex Li,25,134435344,IT,2015-10-29
    
    3.可删除指定员工信息纪录，输入员工id，即可删除。语法如下：
        del from staff where  id=3
    
    4.可修改员工信息，语法如下:
        UPDATE staff_table SET dept="Market" WHERE  dept = "IT" 把所有dept=IT的纪录的dept改成Market
        UPDATE staff_table SET age=25 WHERE  name = "Alex Li"  把name=Alex Li的纪录的年龄改成25
    
    5.以上每条语名执行完毕后，要显示这条语句影响了多少条纪录。 比如查询语句 就显示 查询出了多少条、修改语句就显示修改了多少条等。

"""
HL_OKBLUE = '\033[94m'
HL_OKGREEN = '\033[92m'
HL_FAIL = '\033[91m'
HL_ENDC = '\033[0m'

ERROR_TABLE = HL_FAIL + '表不存在' + HL_ENDC
ERROR_FIELD = HL_FAIL + '字段不存在' + HL_ENDC
ERROR_SYNTAX = HL_FAIL + '语法错误' + HL_ENDC
ERROR_UNKNOWN = HL_FAIL + '操作失败' + HL_ENDC
ERROR_MATCH_FIELDS = HL_FAIL + '字段值不匹配' + HL_ENDC
ERROR_STAFF_EXSITS = HL_FAIL + '员工已存在' + HL_ENDC
ERROR_STAFF_NOTEXSITS = HL_FAIL + '员工不存在' + HL_ENDC

SUCCESS_INITIAL = HL_OKGREEN + '数据已初始化完成' + HL_ENDC
SUCCESS_ADD = HL_OKGREEN + '数据添加成功' + HL_ENDC
SUCCESS_DEL = HL_OKGREEN + '数据删除成功' + HL_ENDC
SUCCESS_EDIT = HL_OKGREEN + '数据修改成功' + HL_ENDC
SUCCESS_FIND = HL_OKGREEN + '数据查找成功' + HL_ENDC
DB_DIR = 'db'
STAFF_TABLE = 'staff_table'
STAFF_FILE = os.path.join(DB_DIR, STAFF_TABLE + '.txt')
keywords = ('find', 'add', 'del', 'update', 'from', 'set', 'where')
logics = ('=', '>', '<', '>=', '<=', '!=', 'like')
db_tables = {
    STAFF_TABLE: ['staff_id', 'name', 'age', 'phone', 'dept', 'enroll_date']
}


def initial():
    """
    初始化数据表
    :return: 
    """
    if not os.path.exists(DB_DIR):
        os.mkdir(DB_DIR)
    if not os.path.exists(STAFF_FILE):
        initial_staffers = """
Alex Li,22,13651054608,IT,2013-04-01
Jack Wang,28,13451024608,HR,2015-01-07
Rain Wang,21,13451054608,IT,2017-04-01
Mack Qiao,44,15653354208,Sales,2016-02-01
Rachel Chen,23,13351024606,IT,2013-03-16
Eric Liu,19,18531054602,Marketing,2012-12-01
Chao Zhang,21,13235324334,Administration,2011-08-08
Kevin Chen,22,13151054603,Sales,2013-04-01
Shit Wen,20,13351024602,IT,2017-07-03
Shanshan Du,26,13698424612,Operation,2017-07-02
        """
        for row in initial_staffers.splitlines():
            if row.count(","):
                insert_staff(row)
        print(SUCCESS_INITIAL)


def error_msg(code):
    """
    错误消息
    :param code: 
    :return: 
    """
    if code == -1:
        msg = ERROR_SYNTAX
    elif code == -2:
        msg = ERROR_TABLE
    elif code == -3:
        msg = ERROR_FIELD
    elif code == -4:
        msg = ERROR_STAFF_EXSITS
    elif code == -5:
        msg = ERROR_MATCH_FIELDS
    elif code == -6:
        msg = ERROR_STAFF_NOTEXSITS
    else:
        msg = ERROR_UNKNOWN
    return msg


def check_table(table):
    """
    检查表是否存在
    :param table: 
    :return: 
    """
    return table in db_tables.keys()


def check_field(table, *args):
    """
    检查表中是否存在字段
    :param table: 
    :param args: 
    :return: 
    """
    fields = []
    if not check_table(table):
        return -2

    if args[0] == '*':
        return db_tables[table]
    for field in args:
        field = field.strip()
        if field not in db_tables[table]:
            return -3
        fields.append(field)
    return fields


def strip_extend(string):
    """
    去除空白双引号单引号
    :param string: 
    :return: 
    """
    return string.strip().strip('"').strip("'")


def check_logic(logic_symbol):
    """
    逻辑判断符是否合法
    :param logic_symbol: 
    :return: 
    """
    return logic_symbol in logics


def do_logic(field_value, logic_symbol, value):
    """
    处理条件字段
    :param field_value: 
    :param logic_symbol: 
    :param value: 
    :return: 
    """
    if not check_logic(logic_symbol.strip()):
        return -1
    value = strip_extend(value)

    option = logic_symbol.strip().lower()
    if option == 'like':
        string = "'%s' in '%s'" % (value, strip_extend(field_value))
    elif option == '=':
        string = "'%s' == '%s' " % (strip_extend(field_value), str(value))
    else:
        string = ''.join([field_value, logic_symbol, value])
    return string


def deserial_staff(line):
    """
    从文件内容反序列成staff字典
    :param line: 
    :return: 
    """
    if line.count(',') != len(db_tables[STAFF_TABLE]) - 1:
        return -5
    return dict(zip(db_tables[STAFF_TABLE], line.strip().split(',')))


def load_staffers():
    """
    获取最新的员工列表数据
    :return: 
    """
    staffers = []
    with open(STAFF_FILE, 'r') as f:
        for row in f:
            staffer = deserial_staff(row)
            if isinstance(staffer, dict):
                staffers.append(staffer)
    return staffers


def split_symbol(where):
    """
    获取条件判断符
    :param where: 
    :return: 
    """
    symbol = ''
    for i in logics[::-1]:
        if i in where:
            symbol = i
            break
    return symbol


def fetch_staffers(fields, where=''):
    """
    查找员工
    :param fields: 
    :param where: 
    :return: 
    """
    has_where = bool(len(where.strip()))
    if has_where:
        logic_symbol = split_symbol(where)
        condition = where.strip().split(logic_symbol)
        if len(condition) != 2:
            return -1
        else:
            field, value = condition
            field = field.strip()
            ret = check_field(STAFF_TABLE, field)
            if isinstance(ret, int):
                return ret

    result = []
    staffers = load_staffers()
    for staffer in staffers:
        if has_where:
            if field not in staffer:
                continue
            statement = do_logic(staffer[field], logic_symbol, value)

            if not eval(statement):
                continue
        tmp = []
        for i in fields:
            tmp.append(staffer[i])
        result.append(tmp)
    return result


def storage_staffers(staffers, rewrite=False):
    """
    员工信息保存到文件
    :param staffers: 员工信息
    :param rewrite: 是否重新更新文件
    :return: 
    """
    with open(STAFF_FILE, 'a+' if not rewrite else 'w') as f:
        for info in staffers:
            f.write("%d,%s,%d,%s,%s,%s%s" % (
                int(info['staff_id']), info['name'], int(info['age']), info['phone'], info['dept'], info['enroll_date'],
                "\n"))

    return 1


def get_increment_id():
    """
    取staff_id增量值
    :return: 
    """
    if not os.path.exists(STAFF_FILE):
        return 1
    increment_id = 0
    with open(STAFF_FILE, 'r') as f:
        for row in f:
            staff = deserial_staff(row)
            if staff and 'staff_id' in staff:
                increment_id = int(staff['staff_id'])

    return increment_id + 1


def check_staff(phone):
    """
    检查是否存在相同手机号的员工
    :param phone: 
    :return: 
    """
    if not os.path.exists(STAFF_FILE):
        return []
    return find_action("staff_id from staff_table where phone = '%s' " % phone)


def insert_staff(info):
    """
    添加员工
    :param info: 
    :return: 
    """
    staff_id = get_increment_id()
    staff = deserial_staff(str(staff_id) + ',' + info)
    if isinstance(staff, int):
        return staff
    if 'phone' not in staff:
        return -1

    if len(check_staff(staff['phone'])):
        return -4
    if storage_staffers([staff]):
        return 1
    return 0


def add_action(content):
    """
    解析添加操作
    :param content: 
    :return: 
    """
    table, row = content.strip().split(' ', 1)
    if not check_table(table):
        return -1

    return insert_staff(row)


def find_fields(content):
    """
    解析查找操作要查询的字段
    :param content: 
    :return: 
    """
    where_index = len(content)
    if 'from' in content:
        from_index = content.index('from')
    else:
        return -1
    if 'where' in content:
        where_index = content.index('where')
    table = content[from_index + len('from'):where_index]

    fields = content[:from_index]

    return check_field(table.strip(), *fields.strip().split(','))


def find_action(content):
    """
    解析查找操作
    :param content: 
    :return: 
    """
    where = ''
    content = content.strip()
    if 'where' in content:
        where = content[content.index('where') + len('where'):]

    return fetch_staffers(find_fields(content), where)


def del_action(content):
    """
    解析删除操作
        1.先找到符合删除条件的员工ID
        2.遍历查找不符合删除条件的员工，添加到新列表
        3.用新列表数据覆盖原文件
    :param content: 
    :return: 
    """
    content = 'staff_id ' + content
    ret = find_action(content)
    if isinstance(ret, int):
        return ret
    if not len(ret):
        return -6
    staffer_ids = []
    for i in ret:
        staffer_ids.append(i[0])
    if isinstance(staffer_ids, list):
        new_staffers = []
        staffers = load_staffers()
        for staffer in staffers:
            if staffer['staff_id'] in staffer_ids:
                continue
            new_staffers.append(staffer)
        storage_staffers(new_staffers, True)
        return len(staffer_ids)

    return False


def format_update_fields(update_fields):
    """
    格式化更新字段值
    :param update_fields: 
    :return: 
    """
    update = {}
    fields = update_fields.strip().split(',')
    for field in fields:
        if '=' in field:
            field_key, field_value = field.strip().split('=')
            update[field_key.strip()] = field_value.strip()

    return update


def edit_action(content):
    """
    解析更新操作
    :param content: 
    :return: 
    """
    where = ''
    pre_table = content
    if 'where' in content:
        pre_table, where = content.split('where')
    if 'set' in pre_table:
        table, fields = pre_table.split('set')
    else:
        return -1

    update_fields = format_update_fields(fields)

    if not len(update_fields):
        return -1
    ret = check_field(STAFF_TABLE, *update_fields.keys())
    if isinstance(ret, int):
        return ret

    content = 'staff_id from %s where %s ' % (table, where)
    ret = find_action(content)
    if isinstance(ret, int):
        return ret
    if not len(ret):
        return -6
    staffer_ids = []
    for i in ret:
        staffer_ids.append(i[0])
    if isinstance(staffer_ids, list):
        new_staffers = []
        staffers = load_staffers()
        for staffer in staffers:
            if staffer['staff_id'] in staffer_ids:
                staffer.update(update_fields)
            new_staffers.append(staffer)
        storage_staffers(new_staffers, True)
        return len(staffer_ids)

    return False


def format_query(query):
    """
    格式化输入字符：
        1.统一逻辑判断符前后的空格
        2.将原字符串的大小写都转为小写
    :param query: 
    :return: 
    """
    if '>=' in query:
        query = query.replace('>=', ' >= ')
    elif '<=' in query:
        query = query.replace('<=', ' <= ')
    elif '!=' in query:
        query = query.replace('!=', ' = ')
    elif '>' in query:
        query = query.replace('>', ' > ')
    elif '<' in query:
        query = query.replace('<', ' < ')
    elif '=' in query:
        query = query.replace('=', ' = ')
    for i in logics[::-1]:
        if i in query:
            query = query.replace('>=', ' >= ')

    query_list = query.strip().split(' ')

    if len(query_list):
        new_query = []
        for i in query_list:
            if not len(i.strip()):
                continue
            if i.strip().lower() in keywords:
                i = i.lower()
            new_query.append(i)
        query = ' '.join(new_query)

    return query


def format_table(header, staffers):
    """
    格式化输出查询结果
    :param header: 标题头
    :param staffers: 
    :return: 
    """
    print("".join([(HL_OKBLUE + "%s" + HL_ENDC) % i.center(20).title() for i in header]))
    for staffer in staffers:
        tmp = [i.center(20) for i in staffer]
        print("".join(tmp))


def format_result(action):
    """
    处理操作结果
    :param action: 
    :return: 
    """
    def sub_action(query):
        ret, msg = action(query)
        affected = 0
        if isinstance(ret, int):
            if ret <= 0:
                print(error_msg(ret))
            else:
                affected = ret
        elif len(ret):
            header = ret.pop()
            affected = len(ret)
            format_table(header, ret)
        if affected:
            print("%s，影响的行数为: \033[94m%d\033[0m " % (msg, affected))

    return sub_action


@format_result
def parse_query(sql):
    """
    解析语句
        1.先解析语句的操作类型，action
        2.到对应的操作函数再做具体解析 content 
    :param sql: 
    :return: 
    """
    query_sql = format_query(sql)
    print('本次执行操作语句：%s' % HL_OKGREEN + query_sql + HL_ENDC)
    action, content = query_sql.split(' ', 1)
    action = action.lower()
    if action == 'add':
        ret = add_action(content)
        msg = SUCCESS_ADD
    elif action == 'del':
        ret = del_action(content)
        msg = SUCCESS_DEL
    elif action == 'update':
        ret = edit_action(content)
        msg = SUCCESS_EDIT
    elif action == 'find':
        ret = find_action(content)
        msg = SUCCESS_FIND
        if isinstance(ret, list):
            ret.append(find_fields(content))
    else:
        ret = -1
        msg = ERROR_UNKNOWN
    return ret, msg


if __name__ == '__main__':
    initial()

    """
    作业需求：
        1.可进行模糊查询，语法至少支持下面3种查询语法:
            find name,age from staff_table where age > 22
            find * from staff_table where dept = "IT"
            find * from staff_table where enroll_date like "2013"
        
        2.可创建新员工纪录，以phone做唯一键(即不允许表里有手机号重复的情况)，staff_id 需自增。语法如下：
            add staff_table Alex Li,25,134435344,IT,2015-10-29
        
        3.可删除指定员工信息纪录，输入员工id，即可删除。语法如下：
            del from staff_table where  staff_id = 3
        
        4.可修改员工信息，语法如下:
            UPDATE staff_table SET dept="Market" WHERE  dept = "IT" 把所有dept=IT的纪录的dept改成Market
            UPDATE staff_table SET age=25 WHERE  name = "Alex Li"  把name=Alex Li的纪录的年龄改成25
        5.以上每条语名执行完毕后，要显示这条语句影响了多少条纪录。 比如查询语句 就显示 查询出了多少条、修改语句就显示修改了多少条等。
    
    作业问题：
        1.第三题的输入员工ID删除的 应该是：
            del from staff where  staff_id=3
    """
    exit_option = True
    while exit_option:
        query_sql = input('请输入操作语句(q|Q，退出)>>:').strip()
        if query_sql.lower() == 'q':
            exit_option = False
            continue
        # query_sql = 'UPDATE staff_table SET age=25 where  staff_id = 3'
        parse_query(query_sql)
