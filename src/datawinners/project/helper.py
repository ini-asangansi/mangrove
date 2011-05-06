# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from mangrove.datastore.database import get_db_manager
from mangrove.form_model.field import TextField, IntegerField, SelectField

from mangrove.form_model.form_model import FormModel, get
from mangrove.form_model.validation import IntegerConstraint, TextConstraint
from mangrove.utils.types import is_empty


def create_question(post_dict):
    if post_dict["type"] == "text":
        return _create_text_question(post_dict)
    if post_dict["type"] == "integer":
        return _create_integer_question(post_dict)
    if post_dict["type"] == "select":
        return _create_select_question(post_dict, single_select_flag=True)
    if post_dict["type"] == "select1":
        return _create_select_question(post_dict, single_select_flag=False)


def create_questionnaire(post, dbm=get_db_manager()):
    entity_id_question = TextField(name="What are you reporting on?", question_code="eid", label="Entity being reported on", entity_question_flag=True)
    return FormModel(dbm, entity_type_id=post["entity_type"], name=post["name"], fields=[entity_id_question], form_code='default', type='survey')


def load_questionnaire(questionnaire_id):
    return get(get_db_manager(), questionnaire_id)


def update_questionnaire_with_questions(form_model, question_set):
    form_model.delete_all_fields()
    for question in question_set:
        form_model.add_field(create_question(question))
    return form_model


def get_code_and_title(fields):
    return [(each_field.question_code, each_field.name)for each_field in fields]


def _create_text_question(post_dict):
    max_length_from_post = post_dict.get("max_length")
    min_length_from_post = post_dict.get("min_length")
    max_length = max_length_from_post if not is_empty(max_length_from_post) else None
    min_length = min_length_from_post if not is_empty(min_length_from_post) else None
    length = TextConstraint(min=min_length, max=max_length)
    return TextField(name=post_dict["title"], question_code=post_dict["code"], label="default",
                     entity_question_flag=post_dict.get("is_entity_question"), length=length)


def _create_integer_question(post_dict):
    max_range_from_post = post_dict["range_max"]
    max_range = max_range_from_post if not is_empty(max_range_from_post) else None
    range = IntegerConstraint(min=post_dict["range_min"], max=max_range)
    return IntegerField(post_dict["title"], post_dict["code"], "default", range)


def _create_select_question(post_dict, single_select_flag):
    options = [choice["value"] for choice in post_dict["choices"]]
    return SelectField(post_dict["title"], post_dict["code"], "default", options, single_select_flag=single_select_flag)
