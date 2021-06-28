import graphene
import graphql_jwt
import api.schema
from django.conf import settings
from graphene_django_optimizer.types import OptimizedDjangoObjectType
from kb.models import AreaOfKnowledge, Grade, Topic, TopicGrade, Prerequisite
from universals.models import UniversalAreaOfKnowledge, UniversalTopic
from students.models import Avatar, Student, StudentTopicMastery, StudentGrade, StudentAchievement
from block.models import BlockConfigurationKeyword, BlockType, BlockTypeConfiguration, Block
from block.models import BlockConfiguration, BlockPresentation, BlockQuestion, BlockQuestionPresentation
from plans.models import StudentPlan, StudentPlanTopicGrade
from organization.models import Organization, OrganizationPersonnel, Group, School, SchoolPersonnel
from achievements.models import Achievement
from guardians.models import Guardian, GuardianStudent
from graphene_django import DjangoObjectType
from audiences.models import Audience
from content.models import AnswerOption, Question
from experiences.models import Level
from collectibles.models import CollectibleCategory, Collectible, CollectiblePurchaseTransaction

LanguageCodeEnum = graphene.Enum(
    "LanguageCodeEnum",
    [(lang[0].replace("-", "_").upper(), lang[0])
     for lang in settings.LANGUAGES],
)


class BlockConfigurationKeywordSchema(DjangoObjectType):
    class Meta:
        model = BlockConfigurationKeyword
        fields = "__all__"


class BlockTypeSchema(DjangoObjectType):
    class Meta:
        model = BlockType
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class BlockTypeConfigurationSchema(DjangoObjectType):
    class Meta:
        model = BlockTypeConfiguration
        fields = "__all__"


class BlockSchema(DjangoObjectType):
    class Meta:
        model = Block
        fields = "__all__"


class BlockConfigurationSchema(DjangoObjectType):
    class Meta:
        model = BlockConfiguration
        fields = "__all__"


class BlockPresentationSchema(DjangoObjectType):
    class Meta:
        model = BlockPresentation
        fields = "__all__"


class BlockQuestionSchema(DjangoObjectType):
    class Meta:
        model = BlockQuestion
        fields = "__all__"


class BlockQuestionPresentationSchema(DjangoObjectType):
    class Meta:
        model = BlockQuestionPresentation
        fields = "__all__"


class QuestionSchema(DjangoObjectType):
    class Meta:
        model = Question
        fields = "__all__"

    question_text = graphene.String()

    def resolve_question_text(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("question_text", language_code=current_language)


class AnswerOptionSchema(DjangoObjectType):
    class Meta:
        model = AnswerOption
        fields = "__all__"

    answer_text = graphene.String()
    explanation = graphene.String()
    image = graphene.String()
    audio_file = graphene.String()
    video = graphene.String()

    def resolve_answer_text(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("answer_text", language_code=current_language)

    def resolve_image(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("image", language_code=current_language)

    def resolve_explanation(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("explanation", language_code=current_language)

    def resolve_audio_file(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("audio_file", language_code=current_language)

    def resolve_video(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("video", language_code=current_language)


class LevelSchema(DjangoObjectType):
    class Meta:
        model = Level
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class CollectibleCategorySchema(DjangoObjectType):
    class Meta:
        model = CollectibleCategory
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class CollectibleSchema(DjangoObjectType):
    class Meta:
        model = Collectible
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class CollectiblePurchaseTransactionSchema(DjangoObjectType):
    class Meta:
        model = CollectiblePurchaseTransaction
        fields = "__all__"


class GuardianSchema(DjangoObjectType):
    class Meta:
        model = Guardian
        fields = "__all__"


class GuardianStudentSchema(DjangoObjectType):
    class Meta:
        model = GuardianStudent
        fields = "__all__"


class AchievementSchema(DjangoObjectType):
    class Meta:
        model = Achievement
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class OrganizationSchema(DjangoObjectType):
    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationPersonnelSchema(DjangoObjectType):
    class Meta:
        model = OrganizationPersonnel
        fields = "__all__"


class GroupSchema(DjangoObjectType):
    class Meta:
        model = Group
        fields = "__all__"


class SchoolSchema(DjangoObjectType):
    class Meta:
        model = School
        fields = "__all__"


class SchoolPersonnelSchema(DjangoObjectType):
    class Meta:
        model = SchoolPersonnel
        fields = "__all__"


class StudentPlanSchema(DjangoObjectType):
    class Meta:
        model = StudentPlan
        fields = "__all__"


class StudentPlanTopicGradeSchema(DjangoObjectType):
    class Meta:
        model = StudentPlanTopicGrade
        fields = "__all__"


class AudienceSchema(OptimizedDjangoObjectType):
    class Meta:
        model = Audience
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class AvatarSchema(DjangoObjectType):
    class Meta:
        model = Avatar
        fields = "__all__"


class StudentSchema(DjangoObjectType):
    class Meta:
        model = Student
        fields = "__all__"


class StudentTopicMasterySchema(DjangoObjectType):
    class Meta:
        model = StudentTopicMastery
        fields = "__all__"


class StudentGradeSchema(DjangoObjectType):
    class Meta:
        model = StudentGrade
        fields = "__all__"


class StudentAchievementSchema(DjangoObjectType):
    class Meta:
        model = StudentAchievement
        fields = "__all__"


class UniversalAreaOfKnowledgeSchema(DjangoObjectType):
    class Meta:
        model = UniversalAreaOfKnowledge
        fields = "__all__"


class UniversalTopicSchema(DjangoObjectType):
    class Meta:
        model = UniversalTopic
        fields = "__all__"


class AreaOfKnowledgeSchema(DjangoObjectType):
    class Meta:
        model = AreaOfKnowledge
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class GradeSchema(DjangoObjectType):
    class Meta:
        model = Grade
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class TopicSchema(DjangoObjectType):
    class Meta:
        model = Topic
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class TopicGradeSchema(DjangoObjectType):
    class Meta:
        model = TopicGrade
        fields = "__all__"


class PrerequisiteSchema(DjangoObjectType):
    class Meta:
        model = Prerequisite
        fields = "__all__"


class Mutation(api.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()


class Query(api.schema.Query, graphene.ObjectType):

    # ----------------- Block Configuration Keyword ----------------- #

    blocks_configuration_keyword = graphene.List(
        BlockConfigurationKeywordSchema)
    block_configuration_keyword_by_id = graphene.Field(
        BlockConfigurationKeywordSchema, id=graphene.String())

    def resolve_blocks_configuration_keyword(root, info, **kwargs):
        # Querying a list
        return BlockConfigurationKeyword.objects.all()

    def resolve_block_configuration_keyword_by_id(root, info, id):
        # Querying a single question
        return BlockConfigurationKeyword.objects.get(pk=id)

    # ----------------- Block Type ----------------- #

    blocks_type = graphene.List(BlockTypeSchema)
    block_type_by_id = graphene.Field(BlockTypeSchema, id=graphene.String())

    def resolve_blocks_type(root, info, **kwargs):
        # Querying a list
        return BlockType.objects.all()

    def resolve_block_type_by_id(root, info, id):
        # Querying a single question
        return BlockType.objects.get(pk=id)

    # ----------------- BlockTypeConfiguration ----------------- #

    blocks_type_configuration = graphene.List(BlockTypeConfigurationSchema)
    block_type_configuration_by_id = graphene.Field(
        BlockTypeConfigurationSchema, id=graphene.String())

    def resolve_blocks_type_configuration(root, info, **kwargs):
        # Querying a list
        return BlockTypeConfiguration.objects.all()

    def resolve_block_type_configuration_by_id(root, info, id):
        # Querying a single question
        return BlockTypeConfiguration.objects.get(pk=id)

    # ----------------- Block ----------------- #

    blocks = graphene.List(BlockSchema)
    block_by_id = graphene.Field(BlockSchema, id=graphene.String())

    def resolve_blocks(root, info, **kwargs):
        # Querying a list
        return Block.objects.all()

    def resolve_block_by_id(root, info, id):
        # Querying a single question
        return Block.objects.get(pk=id)

    # ----------------- BlockConfiguration ----------------- #

    blocks_configuration_type = graphene.List(BlockConfigurationSchema)
    block_configuration_type_by_id = graphene.Field(
        BlockConfigurationSchema, id=graphene.String())

    def resolve_blocks_configuration(root, info, **kwargs):
        # Querying a list
        return BlockConfiguration.objects.all()

    def resolve_block_configuration_by_id(root, info, id):
        # Querying a single question
        return BlockConfiguration.objects.get(pk=id)

    # ----------------- BlockPresentation ----------------- #

    blocks_presentation = graphene.List(BlockPresentationSchema)
    block_presentation_by_id = graphene.Field(
        BlockPresentationSchema, id=graphene.String())

    def resolve_blocks_presentation(root, info, **kwargs):
        # Querying a list
        return BlockPresentation.objects.all()

    def resolve_block_presentation_by_id(root, info, id):
        # Querying a single question
        return BlockPresentation.objects.get(pk=id)

    # ----------------- BlockQuestion ----------------- #

    blocks_question = graphene.List(BlockQuestionSchema)
    block_question_by_id = graphene.Field(
        BlockQuestionSchema, id=graphene.String())

    def resolve_blocks_question(root, info, **kwargs):
        # Querying a list
        return BlockQuestion.objects.all()

    def resolve_block_question_by_id(root, info, id):
        # Querying a single question
        return BlockQuestion.objects.get(pk=id)

    # ----------------- BlockQuestionPresentation ----------------- #

    blocks_question_presentation = graphene.List(
        BlockQuestionPresentationSchema)
    block_question_presentation_by_id = graphene.Field(
        BlockQuestionPresentationSchema, id=graphene.String())

    def resolve_blocks_question_presentation(root, info, **kwargs):
        # Querying a list
        return BlockQuestionPresentation.objects.all()

    def resolve_block_question_presentation_by_id(root, info, id):
        # Querying a single question
        return BlockQuestionPresentation.objects.get(pk=id)

    # ----------------- Question ----------------- #

    questions = graphene.List(QuestionSchema)
    question_by_id = graphene.Field(QuestionSchema, id=graphene.String())

    def resolve_questions(root, info, **kwargs):
        # Querying a list
        return Question.objects.all()

    def resolve_question_by_id(root, info, id):
        # Querying a single question
        return Question.objects.get(pk=id)

    # ----------------- AnswerOption ----------------- #

    answers_option = graphene.List(AnswerOptionSchema)
    answers_option_by_id = graphene.Field(
        AnswerOptionSchema, id=graphene.String())

    def resolve_answers_option(root, info, **kwargs):
        # Querying a list
        return AnswerOption.objects.all()

    def resolve_answers_option_by_id(root, info, id):
        # Querying a single question
        return AnswerOption.objects.get(pk=id)

    # ----------------- Level ----------------- #

    levels = graphene.List(LevelSchema)
    level_by_id = graphene.Field(LevelSchema, id=graphene.String())

    def resolve_levels(root, info, **kwargs):
        # Querying a list
        return Level.objects.all()

    def resolve_level_by_id(root, info, id):
        # Querying a single question
        return Level.objects.get(pk=id)

    # ----------------- CollectibleCategory ----------------- #

    collectibles_category = graphene.List(CollectibleCategorySchema)
    collectible_category_by_id = graphene.Field(
        CollectibleCategorySchema, id=graphene.String())

    def resolve_collectibles_category(root, info, **kwargs):
        # Querying a list
        return CollectibleCategory.objects.all()

    def resolve_collectible_category_by_id(root, info, id):
        # Querying a single question
        return CollectibleCategory.objects.get(pk=id)

    # ----------------- Collectible ----------------- #

    collectibles = graphene.List(CollectibleSchema)
    collectible_by_id = graphene.Field(CollectibleSchema, id=graphene.String())

    def resolve_collectibles(root, info, **kwargs):
        # Querying a list
        return Collectible.objects.all()

    def resolve_collectible_by_id(root, info, id):
        # Querying a single question
        return Collectible.objects.get(pk=id)

    # ----------------- StudentTransactionCollectible ----------------- #

    students_transaction_collectible = graphene.List(
        CollectiblePurchaseTransactionSchema)
    student_transaction_collectible_by_id = graphene.Field(
        CollectiblePurchaseTransactionSchema, id=graphene.String())

    def resolve_students_transaction_collectible(root, info, **kwargs):
        # Querying a list
        return CollectiblePurchaseTransaction.objects.all()

    def resolve_student_transaction_collectible_by_id(root, info, id):
        # Querying a single question
        return CollectiblePurchaseTransaction.objects.get(pk=id)

    # ----------------- Guardian ----------------- #

    guardians = graphene.List(GuardianSchema)
    guardian_by_id = graphene.Field(GuardianSchema, id=graphene.String())

    def resolve_guardians(root, info, **kwargs):
        # Querying a list
        return Guardian.objects.all()

    def resolve_guardian_by_id(root, info, id):
        # Querying a single question
        return Guardian.objects.get(pk=id)

    # ----------------- GuardianStudent ----------------- #

    guardians_student = graphene.List(GuardianStudentSchema)
    guardian_student_by_id = graphene.Field(
        GuardianStudentSchema, id=graphene.String())

    def resolve_guardians_student(root, info, **kwargs):
        # Querying a list
        return GuardianStudent.objects.all()

    def resolve_guardian_student_by_id(root, info, id):
        # Querying a single question
        return GuardianStudent.objects.get(pk=id)

    # ----------------- Achievement  ----------------- #

    Achievements = graphene.List(AchievementSchema)
    Achievement_by_id = graphene.Field(AchievementSchema, id=graphene.String())

    def resolve_achievements(root, info, **kwargs):
        # Querying a list
        return Achievement.objects.all()

    def resolve_achievement_category_by_id(root, info, id):
        # Querying a single question
        return Achievement.objects.get(pk=id)

    # ----------------- Organization ----------------- #

    organizations = graphene.List(OrganizationSchema)
    organization_by_id = graphene.Field(
        OrganizationSchema, id=graphene.String())

    def resolve_organizations(root, info, **kwargs):
        # Querying a list
        return Organization.objects.all()

    def resolve_organization_by_id(root, info, id):
        # Querying a single question
        return Organization.objects.get(pk=id)

    # ----------------- OrganizationPersonnel ----------------- #

    organizations_personnel = graphene.List(OrganizationPersonnelSchema)
    organization_personnel_by_id = graphene.Field(
        OrganizationPersonnelSchema, id=graphene.String())

    def resolve_organizations_personnel(root, info, **kwargs):
        # Querying a list
        return OrganizationPersonnel.objects.all()

    def resolve_organization_personnel_by_id(root, info, id):
        # Querying a single question
        return OrganizationPersonnel.objects.get(pk=id)

    # ----------------- Group ----------------- #

    groups = graphene.List(GroupSchema)
    group_by_id = graphene.Field(GroupSchema, id=graphene.String())

    def resolve_groups(root, info, **kwargs):
        # Querying a list
        return Group.objects.all()

    def resolve_group_by_id(root, info, id):
        # Querying a single question
        return Group.objects.get(pk=id)

    # ----------------- School ----------------- #

    schools = graphene.List(SchoolSchema)
    school_by_id = graphene.Field(SchoolSchema, id=graphene.String())

    def resolve_schools(root, info, **kwargs):
        # Querying a list
        return School.objects.all()

    def resolve_school_by_id(root, info, id):
        # Querying a single question
        return School.objects.get(pk=id)

    # ----------------- SchoolPersonnel ----------------- #

    schools_personnel = graphene.List(SchoolPersonnelSchema)
    school_personnel_by_id = graphene.Field(
        SchoolPersonnelSchema, id=graphene.String())

    def resolve_schools_personnel(root, info, **kwargs):
        # Querying a list
        return SchoolPersonnel.objects.all()

    def resolve_school_personnel_by_id(root, info, id):
        # Querying a single question
        return SchoolPersonnel.objects.get(pk=id)

    # ----------------- StudentPlan ----------------- #

    students_plan = graphene.List(StudentPlanSchema)
    student_plan_by_id = graphene.Field(
        StudentPlanSchema, id=graphene.String())

    def resolve_students_plan(root, info, **kwargs):
        # Querying a list
        return StudentPlan.objects.all()

    def resolve_student_plan_by_id(root, info, id):
        # Querying a single question
        return StudentPlan.objects.get(pk=id)

    # ----------------- StudentPlanTopicGrade ----------------- #

    students_plan_topic_grade = graphene.List(StudentPlanTopicGradeSchema)
    student_plan_topic_grade_by_id = graphene.Field(
        StudentPlanTopicGradeSchema, id=graphene.String())

    def resolve_students_plan_topic_grade(root, info, **kwargs):
        # Querying a list
        return StudentPlanTopicGrade.objects.all()

    def resolve_student_plan_topic_grade_by_id(root, info, id):
        # Querying a single question
        return StudentPlanTopicGrade.objects.get(pk=id)

    # ----------------- Audience ----------------- #

    audiences = graphene.List(AudienceSchema)
    audience_by_id = graphene.Field(AudienceSchema, id=graphene.String())

    def resolve_audiences(root, info, **kwargs):
        # Querying a list
        return Audience.objects.all()

    def resolve_audience_by_id(root, info, id):
        # Querying a single question
        return Audience.objects.get(pk=id)

    # ----------------- Avatar ----------------- #

    avatars = graphene.List(AvatarSchema)
    avatar_by_id = graphene.Field(AvatarSchema, id=graphene.String())

    def resolve_avatars(root, info, **kwargs):
        # Querying a list
        return Avatar.objects.all()

    def resolve_avatar_by_id(root, info, id):
        # Querying a single question
        return Avatar.objects.get(pk=id)

    # ----------------- Student ----------------- #

    students = graphene.List(StudentSchema)
    student_by_id = graphene.Field(StudentSchema, id=graphene.String())

    def resolve_students(root, info, **kwargs):
        # Querying a list
        return Student.objects.all()

    def resolve_student_by_id(root, info, id):
        # Querying a single question
        return Student.objects.get(pk=id)

    # ----------------- StudentTopicMastery ----------------- #

    students_topic_mastery = graphene.List(StudentTopicMasterySchema)
    student_topic_mastery_by_id = graphene.Field(
        StudentTopicMasterySchema, id=graphene.String())

    def resolve_students_topic_mastery(root, info, **kwargs):
        # Querying a list
        return StudentTopicMastery.objects.all()

    def resolve_student_topic_mastery_by_id(root, info, id):
        # Querying a single question
        return StudentTopicMastery.objects.get(pk=id)

    # ----------------- StudentGrade ----------------- #

    students_grade = graphene.List(StudentGradeSchema)
    student_grade_by_id = graphene.Field(
        StudentGradeSchema, id=graphene.String())

    def resolve_students_grade(root, info, **kwargs):
        # Querying a list
        return StudentGrade.objects.all()

    def resolve_student_grade_by_id(root, info, id):
        # Querying a single question
        return StudentGrade.objects.get(pk=id)

    # ----------------- StudentAchievement ----------------- #

    students_achievement = graphene.List(StudentAchievementSchema)
    student_achievement_by_id = graphene.Field(
        StudentAchievementSchema, id=graphene.String())

    def resolve_students_achievement(root, info, **kwargs):
        # Querying a list
        return StudentAchievement.objects.all()

    def resolve_student_achievement_by_id(root, info, id):
        # Querying a single question
        return StudentAchievement.objects.get(pk=id)

    # ----------------- UniversalAreaOfKnowledge ----------------- #

    universals_area_of_knowledge = graphene.List(
        UniversalAreaOfKnowledgeSchema)
    universal_area_of_knowledge_by_id = graphene.Field(
        UniversalAreaOfKnowledgeSchema, id=graphene.String())

    def resolve_universals_area_of_knowledge(root, info, **kwargs):
        # Querying a list
        return UniversalAreaOfKnowledge.objects.all()

    def resolve_universal_area_of_knowledge_by_id(root, info, id):
        # Querying a single question
        return UniversalAreaOfKnowledge.objects.get(pk=id)

    # ----------------- UniversalTopic ----------------- #

    universals_topic = graphene.List(UniversalTopicSchema)
    universal_topic_by_id = graphene.Field(
        UniversalTopicSchema, id=graphene.String())

    def resolve_universals_topic(root, info, **kwargs):
        # Querying a list
        return UniversalTopic.objects.all()

    def resolve_universal_topic_by_id(root, info, id):
        # Querying a single question
        return UniversalTopic.objects.get(pk=id)

    # ----------------- AreaOfKnowledge ----------------- #

    areas_of_knowledge = graphene.List(AreaOfKnowledgeSchema)
    area_of_knowledge_by_id = graphene.Field(
        AreaOfKnowledgeSchema, id=graphene.String())

    def resolve_areas_of_knowledge(root, info, **kwargs):
        # Querying a list
        return AreaOfKnowledge.objects.all()

    def resolve_area_of_knowledge_by_id(root, info, id):
        # Querying a single question
        return AreaOfKnowledge.objects.get(pk=id)

    # ----------------- Grade ----------------- #

    grades = graphene.List(GradeSchema)
    grade = graphene.Field(GradeSchema, id=graphene.String())

    def resolve_grades(root, info, **kwargs):
        # Querying a list
        return Grade.objects.all()

    def resolve_grade(root, info, id):
        # Querying a single question
        return Grade.objects.get(pk=id)

    # ----------------- Topic ----------------- #

    topics = graphene.List(TopicSchema)
    topic_by_id = graphene.Field(TopicSchema, id=graphene.String())

    def resolve_topics(root, info, **kwargs):
        # Querying a list
        return Topic.objects.all()

    def resolve_topic_by_id(root, info, id):
        # Querying a single question
        return Topic.objects.get(pk=id)

    # ----------------- TopicGrade ----------------- #

    topics_grade = graphene.List(TopicGradeSchema)
    topic_grade_by_id = graphene.Field(TopicGradeSchema, id=graphene.String())

    def resolve_topics_grade(root, info, **kwargs):
        # Querying a list
        return TopicGrade.objects.all()

    def resolve_topic_grade_by_id(root, info, id):
        # Querying a single question
        return TopicGrade.objects.get(pk=id)

    # ----------------- Prerequisite ----------------- #

    prerequisites = graphene.List(PrerequisiteSchema)
    prerequisite_by_id = graphene.Field(
        PrerequisiteSchema, id=graphene.String())

    def resolve_prerequisites(root, info, **kwargs):
        # Querying a list
        return Prerequisite.objects.all()

    def resolve_prerequisite_by_id(root, info, id):
        # Querying a single question
        return Prerequisite.objects.get(pk=id)


schema = graphene.Schema(query=Query, mutation=Mutation)
