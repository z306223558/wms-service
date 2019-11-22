# coding=utf-8

import xlwt
from django.http import HttpResponse
from io import BytesIO
from django.utils.http import urlquote


def export_excel(request, objects, save_type, model):
    # 获取excel的名字
    if save_type == 'user':
        file_name = u'学生注册信息列表'
    else:
        file_name = u'学生答题记录列表'
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename={}.xls'.format(urlquote(file_name))
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet(file_name)

    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x17;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)
    # 写入文件标题
    # fields = model._meta.fields
    # for i in range(len(fields)):
    #     if isinstance(fields[i].verbose_name,str):
    fields = get_fields_by_type(save_type)
    for i in range(len(fields)):
        sheet.write(0, i, fields[i], style_heading)
    # 然后开始写入数据
    data_row = 1
    if save_type == 'user':
        queryset = model.objects.filter(user__date_joined__gte='2019-06-26')
        for data in queryset:
            fill_row_data_user(sheet, data_row, data)
            data_row += 1
    else:
        queryset = model.objects.filter(create_time__gte='2019-06-26')
        for data in queryset:
            fill_row_data_answer(sheet, data_row, data)
            data_row += 1
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


def get_fields_by_type(save_type):
    if save_type == 'user':
        return ['手机号', '学生名字', '性别', '年龄', '年级', '学校', '生日', '常住区域', '身份证号', '联系方式', '联系方式2', '个人简介', '注册时间', '学籍号']
    return ['ID', '答题学生姓名', '手机号', '题目名', '题目类型', '学生答案', '参考答案', '是否正确', '答题版本', '是否主观题', '答题时间', '课程名']


def fill_row_data_user(sheet, row_num, data):
    sheet.write(row_num, 0, data.user.mobile)
    sheet.write(row_num, 1, data.name)
    sheet.write(row_num, 2, '女' if data.gender == 'F' else '男')
    sheet.write(row_num, 3, data.age)
    sheet.write(row_num, 4, str(data.grade_level) + '年级')
    sheet.write(row_num, 5, data.school)
    sheet.write(row_num, 6, data.birthday)
    sheet.write(row_num, 7, data.live_area)
    sheet.write(row_num, 8, data.id_card)
    sheet.write(row_num, 9, data.tel_info)
    sheet.write(row_num, 10, data.tel_info_2)
    sheet.write(row_num, 11, data.descriptions)
    sheet.write(row_num, 12, data.user.date_joined.strftime('%Y-%m-%d %H:%I'))
    sheet.write(row_num, 13, data.school_number)


def fill_row_data_answer(sheet, row_num, data):
    sheet.write(row_num, 0, data.id)
    try:
        sheet.write(row_num, 1, data.user.profile.name)
    except Exception as e:
        sheet.write(row_num, 1, '未填写信息')
    sheet.write(row_num, 2, data.user.mobile)
    sheet.write(row_num, 3, data.questions.question_title)
    sheet.write(row_num, 4, data.questions.question_type)
    sheet.write(row_num, 5, data.answer_text)
    sheet.write(row_num, 6, data.questions.question_answer)
    sheet.write(row_num, 7, '正确' if data.is_right else '错误')
    sheet.write(row_num, 8, data.answer_version)
    sheet.write(row_num, 9, '是' if data.is_text else '否')
    sheet.write(row_num, 10, data.create_time.strftime('%Y-%m-%d %H:%I'))
    sheet.write(row_num, 11, data.questions.course.name)
