# serializers
from rest_framework import serializers, exceptions
from utils import logger
from apps.course.models import *
from django.core.exceptions import ImproperlyConfigured, PermissionDenied


class QuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = "__all__"


class CourseSampleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'image_thumb', 'start_time', 'course_subject', 'course_level', 'is_active',)


class QuestionsImageUrlSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuestionsImage
        fields = ('image',)


class QuestionSampleSerializers(serializers.ModelSerializer):
    questions_images = QuestionsImageUrlSerializers(many=True)

    class Meta:
        model = Questions
        exclude = ("update_time", 'create_time', 'create_user', 'course', 'question_answer',)


class CourseDetailSerializers(serializers.ModelSerializer):
    course_questions = QuestionSampleSerializers(many=True)

    class Meta:
        model = Course
        fields = "__all__"


class CourseQuestionSerializers(serializers.ModelSerializer):
    questions_list = QuestionSampleSerializers(many=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'questions_list')


class QuestionCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Questions
        exclude = ("update_time", 'create_time', 'create_user', 'course')

    def create(self, validated_data):
        question = Questions(**validated_data)
        if question.question_type == 'fill':
            pass
        if question.question_type == 'choose':
            choose_array = ["A", "B", "C", "D", "E", "F", "G"]
            # 如果为选择或单选题，则根据输入默认选项之间以换行符隔开，且所有选则题的选项都为A、B、C、D...
            choose_string = question.question_text.split("\n")
        pass


class QuestionRightAnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('id', 'question_answer',)


class QuestionAnswerCreateSerializers(serializers.ModelSerializer):
    right_answer = serializers.CharField(source='questions.question_answer', required=False)

    class Meta:
        model = QuestionsAnswer
        fields = ('questions', 'answer_text', 'is_right', 'is_text', 'right_answer',)

    def create(self, validated_data):
        """
        根据传入的答案，与正确答案相对比，确定答案正确状态
        :param validated_data:
        :return:
        """
        try:
            question_answer = QuestionsAnswer(**validated_data)
        except ValueError as e:
            raise PermissionDenied("must be login")
        question_type = question_answer.questions.question_type
        right_answer = question_answer.questions.question_answer
        is_right = False
        if question_type == question_type == 'mark':
            if question_answer.answer_text == right_answer:
                is_right = True
        if question_type == 'fill':
            # 这里进行正确与否的判断： 填空题判断 需要文字内容, 大小写不敏感, 顺序无影响，中英文无影响
            # 首先做最简单的判断，答案正好与结果一致
            if question_answer.answer_text != '主观题没有标准答案':
                if question_answer.answer_text != right_answer:
                    # 如果答案不一致，则进行多种情况分析，大小写不敏感, 中文逗号换成英文逗号
                    if right_answer.find('##') != -1:
                        right_answer = right_answer.replace("##", ';')
                    right_answer = right_answer.lower().replace('，', ',')
                    # 对学生答案也得做相同处理
                    student_answer = question_answer.answer_text.lower().replace("，", ',')
                    # 分别将答案进行切分成数组，然后数组挨个进行对比
                    if student_answer == right_answer:
                        is_right = True
                    else:
                        # 然后查看允许调换位置的情况
                        if question_answer.questions.allow_change_index != '':
                            allow_change_arr = question_answer.questions.allow_change_index.split(",")
                            if len(allow_change_arr) != 0:
                                # 如果答案还不对，考虑顺序对答案的影响, 直接排序后看是否相等
                                right_answer_arr = right_answer.split(';')
                                student_answer_arr = student_answer.split(';')
                                right_no_change_arr = []
                                student_no_change_arr = []
                                right_change_arr = []
                                student_change_arr = []
                                for i in range(len(right_answer_arr)):
                                    if str(int(i) + 1) in allow_change_arr:
                                        right_change_arr.append(right_answer_arr[i])
                                        student_change_arr.append(student_answer_arr[i])
                                    else:
                                        right_no_change_arr.append(right_answer_arr[i])
                                        student_no_change_arr.append(student_answer_arr[i])
                                # 这样就将答案切分成了2组，每组2个数组分别是一定要有固定顺序的答案和可以随意调换位置的答案
                                if student_no_change_arr == right_no_change_arr and right_change_arr.sort() == student_change_arr.sort():
                                    # 必须保证拥有固定顺序的答案完全一致且可以调换位置的答案也一致的情况下答案才算正确
                                    is_right = True
                                    note_str = '(其中答案'
                                    for i in allow_change_arr:
                                        note_str += right_answer_arr[int(i) - 1] + ','
                                    note_str += '可以调换位置)'
                                    question_answer.answer_text = question_answer.answer_text + note_str
                else:
                    is_right = True
            else:
                question_answer.is_right = True
        if question_type == 'choose' or question_type == 'line' or question_type == 'sort' or question_type == 'checkbox':
            # 单项选择最简单，对比答案即可
            if question_answer.answer_text == question_answer.questions.question_answer:
                is_right = True
        if question_type == 'change':
            # 改错题的话需要对数据进行梳理了
            right_answer = right_answer.lower().replace('，', ',')
            student_answer = question_answer.answer_text.lower().replace('，', ',').replace('。', '.')
            if right_answer == student_answer:
                is_right = True
        if question_type == 'text':
            # 作文题的提交和成绩显示，应该由老师查看后给出成绩
            question_answer.is_text = True
            question_answer.is_right = True
            question_answer.marked_type = False
        # 这里就是最终写入答案了在写入之前呢，我们要检查库中是否已经存在其他版本的答案了，这里就需要对版本进行更新
        same_question_answer_count = QuestionsAnswer.objects.filter(questions=question_answer.questions,
                                                                    user=question_answer.user).count()
        if not same_question_answer_count:
            # 表示里面不存在历史版本,则直接存入
            question_answer.save()
        else:
            question_answer.answer_version = "v{}".format(str(same_question_answer_count + 1))
            question_answer.save()
        question_answer.is_right = is_right
        question_answer.save()
        return question_answer


class QuestionAnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuestionsAnswer
        fields = "__all__"
