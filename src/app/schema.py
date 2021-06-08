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
        fields = ('id', 'name')

class BlockTypeSchema(DjangoObjectType):
    class Meta:
        model = BlockType
        fields = ('id', 'name', 'slug')

class BlockTypeConfigurationSchema(DjangoObjectType):
    class Meta:
        model = BlockTypeConfiguration
        fields = ('id', 'block_type', 'key', 'data_type', 'value')

class BlockSchema(DjangoObjectType):
    class Meta:
        model = Block
        fields = ('id', 'modality', 'first_presentation_timestamp', 'last_presentation_timestamp', 'type_of', 'student', 'topics', 'questions', 'engangement_points', 'coins_earned', 'battery_points')

class BlockConfigurationSchema(DjangoObjectType):
    class Meta:
        model = BlockConfiguration
        fields = ('id','block', 'key', 'data_type', 'value')

class BlockPresentationSchema(DjangoObjectType):
    class Meta:
        model = BlockPresentation
        fields = ('id', 'hits', 'errors', 'total', 'points', 'start_timestamp', 'end_timestamp')

class BlockQuestionSchema(DjangoObjectType):
    class Meta:
        model = BlockQuestion
        fields = ('id', 'block', 'question', 'chosen_answer', 'is_correct', 'is_answered', 'status')

class BlockQuestionPresentationSchema(DjangoObjectType):
    class Meta:
        model = BlockQuestionPresentation
        fields = ('id', 'question', 'block_question', 'presentation_timestamp', 'submission_timestamp')


class QuestionImageAssetTypeSchema(DjangoObjectType):
    class Meta:
        model = QuestionImageAsset
        fields = ('image')

class QuestionAudioAssetTypeSchema(DjangoObjectType):
    class Meta:
        model = QuestionAudioAsset
        fields = ('audio_file')

class QuestionVideoAssetTypeSchema(DjangoObjectType):
    class Meta:
        model = QuestionVideoAsset
        fields = ('url')

class QuestionTypeSchema(DjangoObjectType):
    class Meta:
        model = Question
        fields = ('id', 'topic', 'question_text' , 'answeroption_set', 'image_assets', 'video_assets', 'audio_assets')

class AnswerTypeSchema(DjangoObjectType):
    class Meta:
        model = AnswerOption
        fields = ('id', 'answer_text', 'explanation', 'is_correct', 'question')


class LevelSchema(DjangoObjectType):
    class Meta:
        model = Level
        fields = ('id', 'name', 'points_required')

class CollectibleCategorySchema(DjangoObjectType):
    class Meta:
        model = CollectibleCategory
        fields = ('id', 'name', 'description', 'slug', 'parent')

class CollectibleSchema(DjangoObjectType):
    class Meta:
        model = Collectible
        fields = ('id', 'name', 'description', 'slug', 'price', 'category')

class StudentTransactionCollectibleSchema(DjangoObjectType):
    class Meta:
        model = StudentTransactionCollectible
        fields = ('id', 'name', 'price', 'purchase_date', 'collectible', 'movement', 'student')


class GuardianSchema(DjangoObjectType):
    class Meta:
        model = Guardian
        fields = ('id', 'name', 'last_name', 'gender', 'user')

class GuardianStudentSchema(DjangoObjectType):
    class Meta:
        model = GuardianStudent
        fields = ('id', 'guardian', 'student')

class AchivementSchema(DjangoObjectType):
    class Meta:
        model = Achivement
        fields = ('id', 'hex_color', 'name', 'slug', 'image', 'level_required', 'engangement_points', 'coins_earned')
        
class OrganizationSchema(DjangoObjectType):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'type_of', 'slug', 'parent', 'student_plan')
        
class OrganizationPersonnelSchema(DjangoObjectType):
    class Meta:
        model = OrganizationPersonnel
        fields = ('id', 'user', 'organization', 'name', 'last_name', 'gender', 'date_of_birth', 'identification_number', 'position')       

class GroupSchema(DjangoObjectType):
    class Meta:
        model = Group
        fields = ('id', 'name', 'internal_code', 'population', 'slug', 'grade', 'area_of_knowledges')       

class SchoolSchema(DjangoObjectType):
    class Meta:
        model = School
        fields = ('id', 'name', 'slug', 'internal_code', 'type_of', 'student_plan', 'organization', 'teacher', 'student', 'group')       

class SchoolPersonnelSchema(DjangoObjectType):
    class Meta:
        model = SchoolPersonnel
        fields = ('id', 'user', 'school', 'name', 'last_name', 'gender', 'date_of_birth', 'identification_number', 'position')       
            
class StudentPlanSchema(DjangoObjectType):
    class Meta:
        model = StudentPlan
        fields = ('id', 'name', 'slug', 'total_credits', 'validity_date', 'audience')       

class StudentPlanTopicGradeSchema(DjangoObjectType):
    class Meta:
        model = StudentPlanTopicGrade
        fields = ('id', 'question', 'topic_grade', 'student_plan', 'credit_value', 'is_aproved')       

class AudienceSchema(DjangoObjectType):
    class Meta:
        model = Audience
        fields = ('id', 'hex_color', 'name', 'slug')       

class AvatarSchema(DjangoObjectType):
    class Meta:
        model = Avatar
        fields = ('id', 'type_of', 'name', 'path', 'width', 'height')
        
class StudentSchema(DjangoObjectType):
    class Meta:
        model = Student
        fields = ('id', 'user', 'first_name', 'last_name', 'dob', 'gender', 'age', 'student_plan', 'group', 'level', 'avatar', 'total_experience_points')


class StudentTopicMasterySchema(DjangoObjectType):
    class Meta:
        model = StudentTopicMastery
        fields = ('id', 'topic', 'student', 'is_mastery', 'is_block', 'date_mastery')

class StudentGradeSchema(DjangoObjectType):
    class Meta:
        model = StudentGrade
        fields = ('id', 'grade', 'student', 'is_finish', 'percentage', 'complete_date')

class StudentAchivementSchema(DjangoObjectType):
    class Meta:
        model = StudentAchivement
        fields = ('id', 'achivement', 'student', 'is_liberate', 'liberation_date')

class UniversalAreaOfKnowledgeSchema(DjangoObjectType):
    class Meta:
        model = UniversalAreaOfKnowledge
        fields = ('id', 'hex_color', 'name', 'slug')

class UniversalTopicSchema(DjangoObjectType):
    class Meta:
        model = UniversalTopic
        fields = ('id', 'name', 'slug', 'area_of_knowledge', 'parent', 'standard_code')

class AreaOfKnowledgeSchema(DjangoObjectType):
    class Meta:
        model = AreaOfKnowledge
        fields = ('id', 'hex_color', 'name', 'slug', 'image', 'audience', 'universal_area_knowledge')

class GradeSchema(DjangoObjectType):
    class Meta:
        model = Grade
        fields = ('id', 'name', 'slug', 'audience')

class TopicSchema(DjangoObjectType):
    class Meta:
        model = Topic
        fields = ('id', 'name', 'slug', 'audience', 'area_of_knowledge', 'parent', 'universal_topic')

class TopicGradeSchema(DjangoObjectType):
    class Meta:
        model = TopicGrade
        fields = ('id', 'grade', 'topic', 'standard_code')

class PrerequisiteSchema(DjangoObjectType):
    class Meta:
        model = Prerequisite
        fields = ('id', 'topic_grade', 'topic', 'information', 'advance_percentage', 'advance_minum')
