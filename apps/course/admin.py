import random
from django.contrib import admin
import json
from django.utils.html import format_html
from utils.export_excel import export_excel

from apps.course.models import Course, CourseImage, Questions, QuestionsImage, QuestionsAnswer


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    课程后台管理页面功能定制
    """
    list_display = ['name', 'teacher', 'is_active', 'start_time', 'course_level', 'image_data', 'course_subject',
                    'course_questions_count', 'course_questions_set', 'course_images']
    list_display_links = ['name', ]
    list_filter = ['name', 'teacher', 'is_active', 'course_level', 'course_subject', ]
    list_editable = ['is_active', ]

    # fields = ('name', 'description', 'app_name', 'status')
    exclude = ('create_user', 'teacher', 'is_full', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs
        return qs.filter(create_user=request.user)

    def image_data(self, obj):
        return format_html(
            u'<a href="%s"><img src="%s" height="40px"/></a>' % (obj.image_thumb.url, obj.image_thumb.url))

    # 页面显示的字段名称
    image_data.short_description = u'课程图片'
    image_data.allow_tags = True

    def course_images(self, obj):
        """
        在页面上打通直接跳转到该课程所有图片的页面
        :param obj:
        :return:
        """
        return format_html('<a href="/admin/course/courseimage/?course__id={}">{}</a>'.format(obj.id, "查看"))

    course_images.short_description = "课程图片"
    course_images.allow_tags = True

    def course_questions_count(self, obj):
        """
        返回课程的个数
        :param obj:
        :return:
        """
        return len(obj.course_questions.all())

    course_questions_count.short_description = "课程的问题数量"

    def course_questions_set(self, obj):
        """
        在页面上打通直接跳转到该课程所有的问题页面
        :param obj:
        :return:
        """
        return format_html('<a href="/admin/course/questions/?course__id={}">{}</a>'.format(obj.id, "查看"))

    course_questions_set.short_description = "问题"
    course_questions_set.allow_tags = True


    def save_model(self, request, obj, form, change):
        """
        后台创建课程时，默认使用当前用户为创建用户和老师
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        obj.create_user = request.user
        obj.teacher = request.user
        super().save_model(request, obj, form, change)


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    """
    问题后台管理页面功能定制
    """
    list_display = ['question_name', 'question_title', 'question_type', 'course', 'get_course_show',
                    'get_question_images', 'get_question_answers']
    list_display_links = ['question_name', ]
    list_filter = ('question_type', 'course__name')
    exclude = ('task_info', 'create_user', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        下拉列表中只显示当前用户创建的课程
        :param db_field:
        :param request:
        :param kwargs:
        :return:
        """
        if db_field.name == "course":
            if not request.user.is_superuser:
                kwargs["queryset"] = Course.objects.filter(create_user=request.user)
        return super(QuestionsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        """
        问题列表展示中只展示该用户创建的问题
        :param request:
        :return:
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs
        return qs.filter(create_user=request.user)


    def get_question_images(self, obj):
        """
        在页面上打通直接跳转到该的课程的所有的图片页面
        :param obj:
        :return:
        """
        if obj.image_type:
            return format_html('<a href="/admin/course/questionsimage/?questions_id={}">{}</a>'.format(obj.id, '查看图片'))

    get_question_images.short_description = "问题图片"
    get_question_images.allow_tags = True

    def get_course_show(self, obj):
        """
        在页面上打通直接跳转到该的课程页面
        :param obj:
        :return:
        """
        return format_html('<a href="/admin/course/course/{}/change">{}</a>'.format(obj.course.id, obj.course.name))

    get_course_show.short_description = "所属课程"
    get_course_show.allow_tags = True

    def get_question_answers(self, obj):
        return format_html('<a href="/admin/course/questionsanswer/?questions_id={}">{}</a>'.format(obj.id,
                                                                                                    obj.user_answers.all().count()))

    get_question_answers.short_description = "学生答题情况"
    get_question_answers.allow_tags = True

    def save_model(self, request, obj, form, change):
        """
        根据填写的信息自动生成task_info字段的内容，用于给前台进行使用
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        obj.create_user = request.user

        if obj.question_type == 'fill':
            # 如果是填空题，那么我们需要知道待填空的位置，这里我们使用一个特殊的占位符来代替。使用{}大花括号代表一个词或者一个中文字或者一个数字
            obj.task_info = obj.question_text.replace("{}", "_")
        if obj.question_type == 'choose' or obj.question_type == 'checkbox':
            choose_array = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", ]
            # 如果为选择或单选题，则根据输入默认选项之间以换行符隔开，且所有选则题的选项都为A、B、C、D...
            choose_string = obj.question_text.split("\r\n")
            # 开始将数据进行分离
            choose_string = [s.replace("\n", "").replace("\r", "") for s in choose_string]
            info = []
            for n in range(len(choose_string)):
                temp = {}
                temp[choose_array[n]] = choose_string[n]
                info.append(temp)
            obj.task_info = json.dumps(info)
        if obj.question_type == 'mark':
            # 如果题型为标记，那么直接标记就好
            obj.task_info = obj.question_text
        if obj.question_type == 'line':
            # 如果是连线题呢,并且连线题如果还有图片呢
            couple_string = []
            if obj.image_type:
                # 如果有图片 那我们暂定只能使用一遍是图片一边是文本的情况：
                images = obj.questions_images.all()
                for image in images:
                    image_url = image.image
                    image_bind_text = image.bind_text
                    # 得到 形如：(["哈哈哈哈"，"image_url"),("我"，"image_url"),...]
                    couple_string.append((image_url.url, image_bind_text))
            else:
                # 表示连线题的两边都是文本内容,那就需要对文本进行切分了，规定默认使用 ## 来分割2边的文本，并且 ## 前后为对应关系
                # couple_string 形如：(["哈哈哈哈"，"嘻嘻嘻习"),("我"，"他"),...]
                couple_string = [(couple.split("##")[0], couple.split("##")[1]) for couple in
                                 obj.question_text.split("\r\n")]
            couple_first = []
            couple_two = []

            for n in range(len(couple_string)):
                couple_first.append(couple_string[n][0])
                couple_two.append(couple_string[n][1])
            # 然后打乱顺序
            random.shuffle(couple_first)
            random.shuffle(couple_two)

            # 遍历打乱后数组，然后根据值寻找到正确的答案
            answer_list = []
            for m in range(len(couple_first)):
                for j in range(len(couple_string)):
                    if couple_string[j][0] == couple_first[m]:
                        answer_list.append("{}->{}".format(m+1, couple_string[j][1]))
                        break

            # 组装answer_text
            right_answer = ";".join(answer_list)
            obj.question_answer = right_answer
            obj.task_info = json.dumps(
                {
                    'first_text': couple_two,
                    'two_text': couple_first
                }
            )
        if obj.question_type == 'sort':
            # 排序题, 排序题也分2中情况，待排序的是图片还是文本
            couple_string = []
            if obj.image_type:
                # 表示存在图片,那么表示待排序的都是图片类型的数据
                # 如果有图片 那我们暂定只能使用一遍是图片一边是文本的情况：
                images = obj.questions_images.all().order_by("sort")
                for image in images:
                    image_url = image.image.url
                    image_bind_text = image.sort
                    # 得到 形如：(["哈哈哈哈"，"image_url"),("我"，"image_url"),...]
                    couple_string.append((image_bind_text, image_url))
            else:
                # 如果是文字排序题，则分解question_text的内容 里面的内容按照顺序依次写入, 一行表示一个待排序选项
                wait_sort_text = obj.question_text.split("\r\n")
                couple_string = list(zip(range(1, len(wait_sort_text) + 1), wait_sort_text))
            # 处理好文本后，开始进行打散操作，不管是图片还是文字，现在都已经按照顺序排好
            random.shuffle(couple_string)
            answer_list = []
            question_text = []
            for n in range(len(couple_string)):
                for j in range(len(couple_string)):
                    if n + 1 == couple_string[j][0]:
                        answer_list.append(str(j + 1))
                question_text.append(couple_string[n][1])
            obj.question_answer = ";".join(answer_list)
            obj.task_info = json.dumps(
                {
                    'question_text': question_text
                }
            )
        if obj.question_type == 'text':
            # 作文题，作文题的话直接给出全图的填写框就好，且没有正确答案的
            obj.task_info = obj.question_text
        if obj.question_type == 'change':
            # 改错题的话，改错题得先有正确的一些输入，然后给出对应多的下划线改错左边一栏全部为错误题目，右边一栏则为正确
            # 的答案，填写时一行代表一个题目，前面为题目暨错误的表述后面正确的答案，中间以 ## 隔开
            couple_string = [(couple.split("##")[0], couple.split("##")[1]) for couple in
                             obj.question_text.split("\r\n")]
            couple_first = []
            couple_two = []
            for n in range(len(couple_string)):
                couple_first.append(couple_string[n][0])
                couple_two.append(couple_string[n][1])
            # couple_first 为题目内容， couple_two 为题目答案
            obj.task_info = json.dumps({
                'question_text': couple_first
            })
            obj.question_answer = "##".join(couple_two)
        super().save_model(request, obj, form, change)


@admin.register(QuestionsImage)
class QuestionsImageAdmin(admin.ModelAdmin):
    """
    问题图片管理类，指定问题图片管理界面需要展示的信息
    """
    list_display = ('questions', 'bind_text', 'sort', 'get_question_type')

    def get_question_type(self, obj):
        """
        获取问题图片所属的问题的类型
        :param obj:
        :return:
        """
        return obj.questions.question_type

    get_question_type.short_description = "问题的类别"


@admin.register(QuestionsAnswer)
class QuestionsAnswerAdmin(admin.ModelAdmin):
    """
    问题回答记录后台列表
    """
    list_display = ('id', 'get_question_course_name', 'get_user_show_name', 'is_right', 'answer_text', 'get_question_answer', 'create_time', )
    search_fields = ('user__profile__name', 'user__mobile', 'questions__course__name',)
    list_filter = ('questions__question_name', 'questions__course__name', )
    actions = ('save_excel', )

    def save_excel(self, request, objects):
        response = export_excel(request, objects, 'question_answer', QuestionsAnswer)
        return response
    save_excel.short_description = '导出所有答题数据到excel(请先任意勾选一行数据)'

    def get_user_show_name(self, obj):
        name = obj.user.profile.name
        if not name:
            name = obj.user.username if obj.user.username else obj.user.mobile
        return name
    get_user_show_name.short_description = "答题人"

    def get_question_answer(self, obj):
        return obj.questions.question_answer
    get_question_answer.short_description = "正确答案"

    def get_question_course_name(self, obj):
        return obj.questions.course.name
    get_question_course_name.short_description = "课程名"

admin.site.register(CourseImage)
