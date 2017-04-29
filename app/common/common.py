#coding: utf-8
import os
import string
import random


def generate_code(size=8, chars=string.ascii_lowercase+string.digits):
    """ 生成8位数随机码 """
    return ''.join(random.choice(chars) for _ in range(size))


def strdecode(text):
    if not isinstance(text, unicode):
        try:
            text = text.decode('utf-8')
        except UnicodeDecodeError:
            text = text.decode('gbk', 'ignore')
        return text
    return text


def description_diff(old, diff):
    """
    描述diff中的信息
    @old: 旧的内容
    @diff: diff
    @ret: 描述diff的信息
    """
    # 描述diff
    description = ""
    index = 0
    for op, data in diff:
        if len(description)>400:
            # 如果描述大于400个字符则后面的不就记录了
            break
        if op == 1:
            if description:
                description+=" " # 添加换行
            description += "增加：{0}".format(data.encode("utf-8"))
        elif op == -1:
            if description:
                description+=" " # 添加换行
            description += "删除：{0}".format(old[index:index+data].encode("utf-8"))
            index+=data
        else:
            index+=data
    if len(description)>400:
        description = description[:400]+"..."
    return description


def merge_diff(old, diff):
    """ 根据diff合并old """
    # 新的内容
    new = ''
    index = 0   # 指向old字符串位置游标
    for op, data in diff:
        if op ==1:
            # data为增加的字符
            new+=data
        elif op==-1:
            # data为删除的字符
            index+=data
        else:
            # data为不往后不变的字符数
            new+=old[index:index+data]
            index+=data
    return new


