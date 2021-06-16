from graphene import relay, ObjectType
from graphene_django import DjangoObjectType

from audiences.models import Audience
from content.models import AnswerOption, Question, QuestionImageAsset, QuestionVideoAsset, QuestionAudioAsset
from experiences.models import Level
from collectibles.models import CollectibleCategory, Collectible, StudentTransactionCollectible
from guardians.models import Guardian, GuardianStudent
from achivements.models import Achivement
from organization.models import Organization, OrganizationPersonnel, Group, School, SchoolPersonnel
from plans.models import StudentPlan, StudentPlanTopicGrade
from block.models import BlockConfigurationKeyword, BlockType, BlockTypeConfiguration, Block, BlockConfiguration, BlockPresentation, BlockQuestion, BlockQuestionPresentation
from students.models import Avatar, Student, StudentTopicMastery, StudentGrade, StudentAchivement
from universals.models import UniversalAreaOfKnowledge, UniversalTopic
from kb.models import AreaOfKnowledge, Grade, Topic, TopicGrade, Prerequisite

class BlockConfigurationKeywordSchema(DjangoObjectType):
    class Meta:
        model = BlockConfigurationKeyword
        fields = "__all__"

class BlockTypeSchema(DjangoObjectType):
    class Meta:
        model = BlockType
        fields = "__all__"

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

class QuestionTypeSchema(DjangoObjectType):
    class Meta:
        model = Question
        fields = "__all__"

class AnswerTypeSchema(DjangoObjectType):
    class Meta:
        model = AnswerOption
        fields = "__all__"

class LevelSchema(DjangoObjectType):
    class Meta:
        model = Level
        fields = "__all__"

class CollectibleCategorySchema(DjangoObjectType):
    class Meta:
        model = CollectibleCategory
        fields = "__all__"

class CollectibleSchema(DjangoObjectType):
    class Meta:
        model = Collectible
        fields = "__all__"

class StudentTransactionCollectibleSchema(DjangoObjectType):
    class Meta:
        model = StudentTransactionCollectible
        fields = "__all__"

class GuardianSchema(DjangoObjectType):
    class Meta:
        model = Guardian
        fields = "__all__"

class GuardianStudentSchema(DjangoObjectType):
    class Meta:
        model = GuardianStudent
        fields = "__all__"

class AchivementSchema(DjangoObjectType):
    class Meta:
        model = Achivement
        fields = "__all__"

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

class AudienceSchema(DjangoObjectType):
    class Meta:
        model = Audience
        fields = "__all__"    

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

class StudentAchivementSchema(DjangoObjectType):
    class Meta:
        model = StudentAchivement
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

class GradeSchema(DjangoObjectType):
    class Meta:
        model = Grade
        fields = "__all__"

class TopicSchema(DjangoObjectType):
    class Meta:
        model = Topic
        fields = "__all__"

class TopicGradeSchema(DjangoObjectType):
    class Meta:
        model = TopicGrade
        fields = "__all__"

class PrerequisiteSchema(DjangoObjectType):
    class Meta:
        model = Prerequisite
        fields = "__all__"


class Query(graphene.ObjectType):

    #----------------- Block Configuration Keyword -----------------#

    blocks_configuration_keyword = graphene.List(BlockConfigurationKeywordSchema)
    block_configuration_keyword_by_id = graphene.Field(BlockConfigurationKeywordSchema, id=graphene.String())

    def resolve_blocks_configuration_keyword(root, info, **kwargs):
        # Querying a list
        return BlockConfigurationKeyword.objects.all()

    def resolve_block_configuration_keyword_by_id(root, info, id):
        # Querying a single question
        return BlockConfigurationKeyword.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Block Type -----------------#

    blocks_type = graphene.List(BlockTypeSchema)
    block_type_by_id = graphene.Field(BlockType, id=graphene.String())

    def resolve_blocks_type(root, info, **kwargs):
        # Querying a list
        return BlockType.objects.all()

    def resolve_block_type_by_id(root, info, id):
        # Querying a single question
        return BlockType.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- BlockTypeConfiguration -----------------#

    blocks_type_configuration = graphene.List(BlockTypeConfigurationSchema)
    block_type_configuration_by_id = graphene.Field(BlockTypeConfiguration, id=graphene.String())

    def resolve_blocks_type_configuration(root, info, **kwargs):
        # Querying a list
        return BlockTypeConfiguration.objects.all()

    def resolve_block_type_configuration_by_id(root, info, id):
        # Querying a single question
        return BlockTypeConfiguration.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Block -----------------#

    blocks = graphene.List(BlockSchema)
    block_by_id = graphene.Field(Block, id=graphene.String())

    def resolve_blocks(root, info, **kwargs):
        # Querying a list
        return Block.objects.all()

    def resolve_block_by_id(root, info, id):
        # Querying a single question
        return Block.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- BlockConfiguration -----------------#

    blocks_configuration_type = graphene.List(BlockConfigurationSchema)
    block_configuration_type_by_id = graphene.Field(BlockConfiguration, id=graphene.String())

    def resolve_blocks_configuration(root, info, **kwargs):
        # Querying a list
        return BlockConfiguration.objects.all()

    def resolve_block_configuration_by_id(root, info, id):
        # Querying a single question
        return BlockConfiguration.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- BlockPresentation -----------------#

    blocks_presentation = graphene.List(BlockPresentationSchema)
    block_presentation_by_id = graphene.Field(BlockPresentation, id=graphene.String())

    def resolve_blocks_presentation(root, info, **kwargs):
        # Querying a list
        return BlockPresentation.objects.all()

    def resolve_block_presentation_by_id(root, info, id):
        # Querying a single question
        return BlockPresentation.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- BlockQuestion -----------------#

    blocks_question = graphene.List(BlockQuestionSchema)
    block_question_by_id = graphene.Field(BlockQuestion, id=graphene.String())

    def resolve_blocks_question(root, info, **kwargs):
        # Querying a list
        return BlockQuestion.objects.all()

    def resolve_block_question_by_id(root, info, id):
        # Querying a single question
        return BlockQuestion.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- BlockQuestionPresentation -----------------#

    blocks_question_presentation = graphene.List(BlockQuestionPresentationSchema)
    block_question_presentation_by_id = graphene.Field(BlockQuestionPresentation, id=graphene.String())

    def resolve_blocks_question_presentation(root, info, **kwargs):
        # Querying a list
        return BlockQuestionPresentation.objects.all()

    def resolve_block_question_presentation_by_id(root, info, id):
        # Querying a single question
        return BlockQuestionPresentation.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Question -----------------#

    questions = graphene.List(QuestionTypeSchema)
    question_by_id = graphene.Field(Question, id=graphene.String())

    def resolve_questions(root, info, **kwargs):
        # Querying a list
        return Question.objects.all()

    def resolve_question_by_id(root, info, id):
        # Querying a single question
        return Question.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- AnswerOption -----------------#

    answers_option = graphene.List(AnswerTypeSchema)
    answers_option_by_id = graphene.Field(AnswerOption, id=graphene.String())

    def resolve_answers_option(root, info, **kwargs):
        # Querying a list
        return AnswerOption.objects.all()

    def resolve_answers_option_by_id(root, info, id):
        # Querying a single question
        return AnswerOption.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Level -----------------#

    levels = graphene.List(LevelSchema)
    level_by_id = graphene.Field(Level, id=graphene.String())

    def resolve_levels(root, info, **kwargs):
        # Querying a list
        return Level.objects.all()

    def resolve_level_by_id(root, info, id):
        # Querying a single question
        return Level.objects.get(pk=id)

    #----------------- End Code -----------------#
    
    #----------------- CollectibleCategory -----------------#

    collectibles_category = graphene.List(CollectibleCategorySchema)
    collectible_category_by_id = graphene.Field(CollectibleCategory, id=graphene.String())

    def resolve_collectibles_category(root, info, **kwargs):
        # Querying a list
        return CollectibleCategory.objects.all()

    def resolve_collectible_category_by_id(root, info, id):
        # Querying a single question
        return CollectibleCategory.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Collectible -----------------#

    collectibles = graphene.List(CollectibleSchema)
    collectible_by_id = graphene.Field(Collectible, id=graphene.String())

    def resolve_collectibles(root, info, **kwargs):
        # Querying a list
        return Collectible.objects.all()

    def resolve_collectible_by_id(root, info, id):
        # Querying a single question
        return Collectible.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- StudentTransactionCollectible -----------------#

    students_transaction_collectible = graphene.List(StudentTransactionCollectibleSchema)
    student_transaction_collectible_by_id = graphene.Field(StudentTransactionCollectible, id=graphene.String())

    def resolve_students_transaction_collectible(root, info, **kwargs):
        # Querying a list
        return StudentTransactionCollectible.objects.all()

    def resolve_student_transaction_collectible_by_id(root, info, id):
        # Querying a single question
        return StudentTransactionCollectible.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Guardian -----------------#

    guardians = graphene.List(GuardianSchema)
    guardian_by_id = graphene.Field(Guardian, id=graphene.String())

    def resolve_guardians(root, info, **kwargs):
        # Querying a list
        return Guardian.objects.all()

    def resolve_guardian_by_id(root, info, id):
        # Querying a single question
        return Guardian.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- GuardianStudent -----------------#

    guardians_student = graphene.List(GuardianStudentSchema)
    guardian_student_by_id = graphene.Field(GuardianStudent, id=graphene.String())

    def resolve_guardians_student(root, info, **kwargs):
        # Querying a list
        return GuardianStudent.objects.all()

    def resolve_guardian_student_by_id(root, info, id):
        # Querying a single question
        return GuardianStudent.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Achivement  -----------------#

    achivements = graphene.List(AchivementSchema)
    achivement_by_id = graphene.Field(Achivement, id=graphene.String())

    def resolve_achivements(root, info, **kwargs):
        # Querying a list
        return Achivement.objects.all()

    def resolve_achivement_category_by_id(root, info, id):
        # Querying a single question
        return Achivement.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Organization -----------------#

    organizations = graphene.List(OrganizationSchema)
    organization_by_id = graphene.Field(Organization, id=graphene.String())

    def resolve_organizations(root, info, **kwargs):
        # Querying a list
        return Organization.objects.all()

    def resolve_organization_by_id(root, info, id):
        # Querying a single question
        return Organization.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- OrganizationPersonnel -----------------#

    organizations_personnel = graphene.List(OrganizationPersonnelSchema)
    organization_personnel_by_id = graphene.Field(OrganizationPersonnel, id=graphene.String())

    def resolve_organizations_personnel(root, info, **kwargs):
        # Querying a list
        return OrganizationPersonnel.objects.all()

    def resolve_organization_personnel_by_id(root, info, id):
        # Querying a single question
        return OrganizationPersonnel.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Group -----------------#

    groups = graphene.List(GroupSchema)
    group_by_id = graphene.Field(Group, id=graphene.String())

    def resolve_groups(root, info, **kwargs):
        # Querying a list
        return Group.objects.all()

    def resolve_group_by_id(root, info, id):
        # Querying a single question
        return Group.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- School -----------------#

    schools = graphene.List(SchoolSchema)
    school_by_id = graphene.Field(School, id=graphene.String())

    def resolve_schools(root, info, **kwargs):
        # Querying a list
        return School.objects.all()

    def resolve_school_by_id(root, info, id):
        # Querying a single question
        return School.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- SchoolPersonnel -----------------#

    schools_personnel = graphene.List(SchoolPersonnelSchema)
    school_personnel_by_id = graphene.Field(SchoolPersonnel, id=graphene.String())

    def resolve_schools_personnel(root, info, **kwargs):
        # Querying a list
        return SchoolPersonnel.objects.all()

    def resolve_school_personnel_by_id(root, info, id):
        # Querying a single question
        return SchoolPersonnel.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- StudentPlan -----------------#

    students_plan = graphene.List(StudentPlanSchema)
    student_by_id = graphene.Field(StudentPlan, id=graphene.String())

    def resolve_students_plan(root, info, **kwargs):
        # Querying a list
        return StudentPlan.objects.all()

    def resolve_student_by_id(root, info, id):
        # Querying a single question
        return StudentPlan.objects.get(pk=id)

    #----------------- End Code -----------------#


    #----------------- StudentPlanTopicGrade -----------------#

    students_plan_topic_grade = graphene.List(StudentPlanTopicGradeSchema)
    student_plan_topic_grade_by_id = graphene.Field(StudentPlanTopicGrade, id=graphene.String())

    def resolve_students_plan_topic_grade(root, info, **kwargs):
        # Querying a list
        return StudentPlanTopicGrade.objects.all()

    def resolve_student_plan_topic_grade_by_id(root, info, id):
        # Querying a single question
        return StudentPlanTopicGrade.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Audience -----------------#

    audiences = graphene.List(AudienceSchema)
    audience_by_id = graphene.Field(Audience, id=graphene.String())

    def resolve_audiences(root, info, **kwargs):
        # Querying a list
        return Audience.objects.all()

    def resolve_audience_by_id(root, info, id):
        # Querying a single question
        return Audience.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Avatar -----------------#

    avatars = graphene.List(AvatarSchema)
    avatar_by_id = graphene.Field(Avatar, id=graphene.String())

    def resolve_avatars(root, info, **kwargs):
        # Querying a list
        return Avatar.objects.all()

    def resolve_avatar_by_id(root, info, id):
        # Querying a single question
        return Avatar.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Student -----------------#

    students = graphene.List(StudentSchema)
    student_by_id = graphene.Field(Student, id=graphene.String())

    def resolve_students(root, info, **kwargs):
        # Querying a list
        return Student.objects.all()

    def resolve_student_by_id(root, info, id):
        # Querying a single question
        return Student.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- StudentTopicMastery -----------------#

    students_topic_mastery = graphene.List(StudentTopicMasterySchema)
    student_topic_mastery_by_id = graphene.Field(StudentTopicMastery, id=graphene.String())

    def resolve_students_topic_mastery(root, info, **kwargs):
        # Querying a list
        return StudentTopicMastery.objects.all()

    def resolve_student_topic_mastery_by_id(root, info, id):
        # Querying a single question
        return StudentTopicMastery.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- StudentGrade -----------------#

    students_grade = graphene.List(StudentGradeSchema)
    student_grade_by_id = graphene.Field(StudentGrade, id=graphene.String())

    def resolve_students_grade(root, info, **kwargs):
        # Querying a list
        return StudentGrade.objects.all()

    def resolve_student_grade_by_id(root, info, id):
        # Querying a single question
        return StudentGrade.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- StudentAchivement -----------------#

    students_achivement = graphene.List(StudentAchivementSchema)
    student_achivement_by_id = graphene.Field(StudentAchivement, id=graphene.String())

    def resolve_students_achivement(root, info, **kwargs):
        # Querying a list
        return StudentAchivement.objects.all()

    def resolve_student_achivement_by_id(root, info, id):
        # Querying a single question
        return StudentAchivement.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- UniversalAreaOfKnowledge -----------------#

    universals_area_of_knowledge = graphene.List(UniversalAreaOfKnowledgeSchema)
    universal_area_of_knowledge_by_id = graphene.Field(UniversalAreaOfKnowledge, id=graphene.String())

    def resolve_universals_area_of_knowledge(root, info, **kwargs):
        # Querying a list
        return UniversalAreaOfKnowledge.objects.all()

    def resolve_universal_area_of_knowledge_by_id(root, info, id):
        # Querying a single question
        return UniversalAreaOfKnowledge.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- UniversalTopic -----------------#

    universals_topic = graphene.List(UniversalTopicSchema)
    universal_topic_by_id = graphene.Field(UniversalTopic, id=graphene.String())

    def resolve_universals_topic(root, info, **kwargs):
        # Querying a list
        return UniversalTopic.objects.all()

    def resolve_universal_topic_by_id(root, info, id):
        # Querying a single question
        return UniversalTopic.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- AreaOfKnowledge -----------------#

    areas_of_knowledge = graphene.List(AreaOfKnowledgeSchema)
    area_of_knowledge_by_id = graphene.Field(AreaOfKnowledge, id=graphene.String())

    def resolve_areas_of_knowledge(root, info, **kwargs):
        # Querying a list
        return AreaOfKnowledge.objects.all()

    def resolve_area_of_knowledge_by_id(root, info, id):
        # Querying a single question
        return AreaOfKnowledge.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Grade -----------------#

    grades = graphene.List(GradeSchema)
    grade = graphene.Field(Grade, id=graphene.String())

    def resolve_grades(root, info, **kwargs):
        # Querying a list
        return Grade.objects.all()

    def resolve_grade(root, info, id):
        # Querying a single question
        return Grade.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Topic -----------------#

    topics = graphene.List(TopicSchema)
    topic_by_id = graphene.Field(Topic, id=graphene.String())

    def resolve_topics(root, info, **kwargs):
        # Querying a list
        return Topic.objects.all()

    def resolve_topic_by_id(root, info, id):
        # Querying a single question
        return Topic.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- TopicGrade -----------------#

    topics_grade = graphene.List(TopicGradeSchema)
    topic_grade_by_id = graphene.Field(TopicGrade, id=graphene.String())

    def resolve_topics_grade(root, info, **kwargs):
        # Querying a list
        return TopicGrade.objects.all()

    def resolve_topic_grade_by_id(root, info, id):
        # Querying a single question
        return TopicGrade.objects.get(pk=id)

    #----------------- End Code -----------------#

    #----------------- Prerequisite -----------------#

    prerequisites = graphene.List(PrerequisiteSchema)
    prerequisite_by_id = graphene.Field(Prerequisite, id=graphene.String())

    def resolve_prerequisites(root, info, **kwargs):
        # Querying a list
        return Prerequisite.objects.all()

    def resolve_prerequisite_by_id(root, info, id):
        # Querying a single question
        return Prerequisite.objects.get(pk=id)

    #----------------- End Code -----------------#
