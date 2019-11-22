from datetime import datetime
from django.db import models
from django.utils.html import format_html


class Course(models.Model):
    """
    课程model类
    """
    Course_Subject_Choice = (
        ("English", "英语"),
        ("Math", "数学"),
        ("Chinese", "语文"),
        ("Others", "其他")
    )

    Course_Level_Choice = (
        ("6", "小学六年级"),
        ("7", "初一"),
        ("8", "初二"),
        ("5", "小学5年级")
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="课程名", default="")
    image_thumb = models.ImageField(upload_to="course", verbose_name="课程封面图", width_field="url_width",
                                    height_field="url_height")
    url_width = models.IntegerField(verbose_name="图片宽度", default=500)
    url_height = models.IntegerField(verbose_name="图片高度", default=500)
    video = models.FileField(upload_to="course/video/", verbose_name="课程视频", default=None)
    descriptions = models.TextField(verbose_name="课程简介，这里应该为富文本编辑器的代码")
    start_time = models.DateTimeField(verbose_name="课程开始时间")
    create_time = models.DateTimeField(verbose_name="课程创建时间", auto_created=True, auto_now=True)
    update_time = models.DateTimeField(verbose_name="课程更新时间", auto_now=True, auto_created=True)
    create_user = models.ForeignKey(to="user.User", related_name="create_user", on_delete=models.CASCADE, null=True, blank=True, default=None)
    end_time = models.DateTimeField(verbose_name="课程结束时间")
    is_active = models.BooleanField(verbose_name="课程是否可用", default=False)
    course_level = models.CharField(choices=Course_Level_Choice, verbose_name="课程使用年级", default="6", max_length=100)
    teacher = models.ForeignKey(to="user.User", to_field="id", verbose_name="课程的老师", related_name="teacher",
                                on_delete=models.CASCADE, default=None, blank=True, null=True)
    allow_number = models.IntegerField(verbose_name="课程允许参加的人数", default=50)
    is_full = models.BooleanField(verbose_name="课程预订是否已满", default=False)
    course_subject = models.CharField(choices=Course_Subject_Choice, verbose_name="课程科目类别", default="English",
                                      max_length=100)
    course_tag = models.CharField(verbose_name="课程左上角角标文字", default="", max_length=40, blank=True, null=True)
    course_price = models.FloatField(verbose_name="课程价格", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = "课程"


class Questions(models.Model):
    """
    问题model类
    """
    Question_Types = (
        ("fill", "填空题"),
        ("choose", "单选择题"),
        ("line", "连线题"),
        ("mark", "标记题"),
        ("sort", "排序题"),
        ("text", "作文题"),
        ("change", "改错题"),
        ("checkbox", "多选题"),
    )

    Mark_Types = (
        ("line", "下划线"),
        ("circle", "圈线"),
    )

    id = models.AutoField(primary_key=True)
    question_title = models.CharField(verbose_name="问题题目", default="题目如下：", max_length=255)
    question_name = models.CharField(verbose_name="问题名称", max_length=255, default="默认题目", null=True)
    question_text = models.TextField(verbose_name="问题文本", null=True, default=None, blank=True)
    question_type = models.CharField(choices=Question_Types, verbose_name="问题类型", max_length=40, default="fill")
    allow_change_index = models.CharField(verbose_name="填空题允许交换位置的正确答案的索引", max_length=100, default="", blank=True)
    question_answer = models.CharField(verbose_name="问题答案", null=True, default=None, blank=True, max_length=255)
    show_time = models.IntegerField(verbose_name="问题弹出的时间秒数", default=10)
    wait_time = models.IntegerField(verbose_name="回答问题的时间", default=30)
    task_info = models.TextField(verbose_name="问题具体内容设置", default=None, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name="课程创建时间", auto_created=True, auto_now=True)
    update_time = models.DateTimeField(verbose_name="课程更新时间", auto_now=True, auto_created=True)
    create_user = models.ForeignKey(to="user.User", on_delete=models.CASCADE, null=True, blank=True, default=None)
    course = models.ForeignKey(to="Course", verbose_name="对应的课程", to_field="id", on_delete=models.CASCADE, default=None,
                               related_name="course_questions")
    # mark 选项
    mark_type = models.CharField(choices=Mark_Types, verbose_name="标记题型时标记类型", default="line", max_length=100)
    # 题目是否是图片类别的
    image_type = models.BooleanField(default=False, verbose_name="题目中是否存在图片")

    def __str__(self):
        return self.question_name + " " + self.question_type

    class Meta:
        verbose_name = '课程问题'
        verbose_name_plural = "课程问题"
        ordering = ['show_time', ]


class QuestionsImage(models.Model):
    """
    问题图片类
    """
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="questions_images", width_field="url_width",
                              height_field="url_height", verbose_name="图片地址")
    sort = models.IntegerField(verbose_name="图片排序", default=1)
    bind_text = models.CharField(verbose_name="与图片绑定的文本内容", max_length=255, default="")
    url_width = models.IntegerField(verbose_name="图片宽度", default=500)
    url_height = models.IntegerField(verbose_name="图片高度", default=500)
    questions = models.ForeignKey(verbose_name="对应的问题内容", to="Questions", to_field="id", on_delete=models.CASCADE,
                                  related_name="questions_images", default=None)
    create_user = models.ForeignKey(to="user.User", on_delete=models.SET_DEFAULT, null=True, default=None)

    def __str__(self):
        return self.questions.question_title + " " + self.bind_text

    class Meta:
        verbose_name = '问题图片'
        verbose_name_plural = "问题图片"


class CourseImage(models.Model):
    """
    课程详细图片类
    """
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="course_images", width_field="url_width",
                              height_field="url_height", verbose_name="图片地址")
    sort = models.IntegerField(verbose_name="图片排序", default=1)
    name = models.CharField(verbose_name="图片名称", max_length=255, default="图片")
    url_width = models.IntegerField(verbose_name="图片宽度", default=500)
    url_height = models.IntegerField(verbose_name="图片高度", default=500)
    course = models.ForeignKey(to="Course", verbose_name="对应的课程", to_field="id", on_delete=models.CASCADE, default=None,
                               related_name="course_images")
    create_user = models.ForeignKey(to="user.User", on_delete=models.SET_DEFAULT, null=True, default=None)

    def __str__(self):
        return self.course.name + " " + str(self.sort)

    class Meta:
        verbose_name = '课程图片'
        verbose_name_plural = "课程图片"


class QuestionsAnswer(models.Model):
    """
    学生提交做题答案
    """
    id = models.AutoField(primary_key=True)
    questions = models.ForeignKey("Questions", verbose_name="回答的问题", to_field="id", on_delete=models.CASCADE,
                                  default=None, related_name="user_answers")
    user = models.ForeignKey(to="user.User", on_delete=models.CASCADE, verbose_name="回答问题的学生", null=True, default=None)
    answer_text = models.TextField(verbose_name="学生作答的答案")
    is_right = models.BooleanField(verbose_name="答案是否正确", default=False, blank=True)
    answer_version = models.CharField(verbose_name="学生答案的版本", default="v1", blank=True, max_length=20)
    is_text = models.BooleanField(verbose_name="是否是作文题", default=False, blank=True)
    marked_type = models.BooleanField(verbose_name="作文题老师查看状态", default=False, blank=True)
    answer_score = models.IntegerField(verbose_name="答案分数", default=0, blank=True)
    create_time = models.DateTimeField(verbose_name="提交时间", auto_created=True, auto_now=True)

    def __str__(self):
        return self.user.username + " " + self.questions.question_title

    class Meta:
        verbose_name = '答题记录'
        verbose_name_plural = '答题记录'



