# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from copy import copy
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from datawinners.entity.import_data import load_all_subjects, load_all_reporters
from datawinners.main.utils import get_database_manager
from datawinners.project.forms import ProjectProfile
from datawinners.project.models import Project, PROJECT_ACTIVE_STATUS
from datawinners.entity.forms import ReporterRegistrationForm
from datawinners.entity.forms import SubjectUploadForm
from datawinners.entity.views import import_subjects_from_project_wizard
import helper
from datawinners.project import models
from mangrove.datastore.documents import DataRecordDocument
from mangrove.datastore.data import EntityAggregration
from mangrove.datastore.entity import get_all_entity_types
from mangrove.errors.MangroveException import QuestionCodeAlreadyExistsException, EntityQuestionAlreadyExistsException, DataObjectAlreadyExists
from mangrove.form_model.field import field_to_json
from mangrove.form_model.form_model import get_form_model_by_code, FormModel
from mangrove.transport.submissions import get_submissions_made_for_form, SubmissionLogger
from django.contrib import messages
from mangrove.utils.types import is_string
from mangrove.datastore import data, aggregrate as aggregate_module
from mangrove.utils.json_codecs import encode_json
from django.core.urlresolvers import reverse
import datawinners.utils as utils

PAGE_SIZE = 4
NUMBER_TYPE_OPTIONS = ["Latest", "Sum", "Count", "Min", "Max", "Average"]
MULTI_CHOICE_TYPE_OPTIONS = ["Latest", "sum(yes)", "percent(yes)", "sum(no)", "percent(no)"]
DATE_TYPE_OPTIONS = ["Latest"]
GEO_TYPE_OPTIONS = ["Latest"]
TEXT_TYPE_OPTIONS = ["Latest", "Most Frequent"]

class ProjectLinks(object):
    data_analysis_link = ''
    submission_log_link = ''
    overview_link = ''
    activate_project_link = ''


def _make_project_links(project_id, questionnaire_code):
    project_links = ProjectLinks()
    project_links.data_analysis_link = reverse(project_data, args=[project_id, questionnaire_code])
    project_links.submission_log_link = reverse(project_results, args=[project_id, questionnaire_code])
    project_links.overview_link = reverse(project_overview, args=[project_id])
    project_links.activate_project_link = reverse(activate_project, args=[project_id])
    project_links.subjects_link = reverse(subjects, args=[project_id])
    project_links.datasenders_link = reverse(datasenders, args=[project_id])
    project_links.registered_datasenders_link = reverse(registered_datasenders, args=[project_id])
    project_links.registered_subjects_link = reverse(registered_subjects, args=[project_id])
    return project_links


@login_required(login_url='/login')
def questionnaire_wizard(request, project_id=None):
    manager = get_database_manager(request)
    if request.method == 'GET':
        previous_link = reverse(subjects_wizard, args=[project_id])
        project = models.get_project(project_id, manager)
        form_model = helper.load_questionnaire(manager, project.qid)
        fields = form_model.fields
        if form_model.entity_defaults_to_reporter():
            fields = helper.hide_entity_question(form_model.fields)
        existing_questions = json.dumps(fields, default=field_to_json)
        return render_to_response('project/questionnaire_wizard.html',
                {"existing_questions": repr(existing_questions), 'questionnaire_code': form_model.form_code,
                 "previous": previous_link, 'project': project}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def create_profile(request):
    manager = get_database_manager(request)
    entity_list = get_all_entity_types(manager)
    entity_list = helper.remove_reporter(entity_list)
    project_summary = dict(name='New Project')
    if request.method == 'GET':
        form = ProjectProfile(entity_list=entity_list,initial={'activity_report':'yes'})
        return render_to_response('project/profile.html', {'form': form, 'project': project_summary},
                                  context_instance=RequestContext(request))

    form = ProjectProfile(data=request.POST, entity_list=entity_list)
    if form.is_valid():
        entity_type=form.cleaned_data['entity_type']
        project = Project(name=form.cleaned_data["name"], goals=form.cleaned_data["goals"],
                          project_type=form.cleaned_data['project_type'], entity_type=entity_type,
                          devices=form.cleaned_data['devices'], activity_report=form.cleaned_data['activity_report'])
        form_model = helper.create_questionnaire(post=form.cleaned_data, dbm=manager)
        try:
            pid = project.save(manager)
            qid = form_model.save()
            project.qid = qid
            pid = project.save(manager)
        except DataObjectAlreadyExists as e:
            messages.error(request, e.message)
            return render_to_response('project/profile.html', {'form': form, 'project': project_summary},
                                      context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse(subjects_wizard, args=[pid]))
    else:
        return render_to_response('project/profile.html', {'form': form, 'project': project_summary},
                                  context_instance=RequestContext(request))


@login_required(login_url='/login')
def edit_profile(request, project_id=None):
    manager = get_database_manager(request)
    entity_list = get_all_entity_types(manager)
    entity_list = helper.remove_reporter(entity_list)
    project = models.get_project(project_id, dbm=manager)
    if request.method == 'GET':
        form = ProjectProfile(data=project, entity_list=entity_list)
        return render_to_response('project/profile.html', {'form': form, 'project': project},
                                  context_instance=RequestContext(request))

    form = ProjectProfile(data=request.POST, entity_list=entity_list)
    if form.is_valid():
        project.update(manager, form.cleaned_data)
        project.update_questionnaire(manager)

        try:
            pid = project.save(manager)
        except DataObjectAlreadyExists as e:
            messages.error(request, e.message)
            return render_to_response('project/profile.html', {'form': form, 'project': project},
                                      context_instance=RequestContext(request))
        project = models.get_project(pid, manager)
        form_model = helper.load_questionnaire(manager, project.qid)
        entity_type = form.cleaned_data['entity_type']
        form_model.entity_type = [entity_type] if is_string(entity_type) else entity_type
        form_model.save()
        return HttpResponseRedirect(reverse(subjects_wizard, args=[pid]))
    else:
        return render_to_response('project/profile.html', {'form': form, 'project': project},
                                  context_instance=RequestContext(request))


@login_required(login_url='/login')
def save_questionnaire(request):
    manager = get_database_manager(request)
    if request.method == 'POST':
        questionnaire_code = request.POST['questionnaire-code']
        json_string = request.POST['question-set']
        question_set = json.loads(json_string)
        pid = request.POST['pid']
        project = models.get_project(pid, dbm=manager)
        form_model = manager.get(project.qid, FormModel)
        try:
            form_model = helper.update_questionnaire_with_questions(form_model, question_set, manager)
        except QuestionCodeAlreadyExistsException as e:
            return HttpResponseServerError(e)
        except EntityQuestionAlreadyExistsException as e:
            return HttpResponseServerError(e.message)
        else:
            try:
                form_model.form_code = questionnaire_code.lower()
            except DataObjectAlreadyExists as e:
                if e.message.find("Form") >= 0:
                    return HttpResponseServerError("Questionnaire with this code already exists")
                return HttpResponseServerError(e.message)
            form_model.name = project.name
            form_model.entity_id = project.entity_type
            form_model.save()
            return HttpResponseRedirect(reverse(finish, args=[pid]))


@login_required(login_url='/login')
def index(request):
    project_list = []
    rows = models.get_all_projects(dbm=get_database_manager(request))
    for row in rows:
        project_id = row['value']['_id']
        link = reverse(project_overview, args=[project_id])
        activate_link = reverse(activate_project, args=[project_id])
        project = dict(name=row['value']['name'], created=row['value']['created'], type=row['value']['project_type'],
                       link=link, activate_link=activate_link, state=row['value']['state'])
        project_list.append(project)
    return render_to_response('project/index.html', {'projects': project_list},
                              context_instance=RequestContext(request))


@login_required(login_url='/login')
def project_overview(request, project_id=None):
    manager = get_database_manager(request)
    project = models.get_project(project_id, dbm=manager)
    link = reverse(edit_profile, args=[project_id])
    questionnaire = helper.load_questionnaire(manager, project['qid'])
    number_of_questions = len(questionnaire.fields)
    project_links = _make_project_links(project_id, questionnaire.form_code)
    return render_to_response('project/overview.html',
            {'project': project, 'entity_type': project['entity_type'], 'project_links': project_links
             , 'project_profile_link': link, 'number_of_questions': number_of_questions},
                              context_instance=RequestContext(request))


def _get_number_of_rows_in_result(dbm, questionnaire_code):
    submissions_count = get_submissions_made_for_form(dbm, questionnaire_code, count_only=True)
    return submissions_count


def _get_submissions_for_display(current_page, dbm, questionnaire_code, questions, pagination):
    if pagination:
        submissions, ids = get_submissions_made_for_form(dbm, questionnaire_code, page_number=current_page,
                                                         page_size=PAGE_SIZE, count_only=False)
    else:
        submissions, ids = get_submissions_made_for_form(dbm, questionnaire_code, page_number=current_page,
                                                         page_size=None, count_only=False)
    submissions = helper.get_submissions(questions, submissions)
    return submissions, ids


def _load_submissions(current_page, manager, questionnaire_code, pagination=True):
    form_model = get_form_model_by_code(manager, questionnaire_code)
    questionnaire = (questionnaire_code, form_model.name)
    fields = form_model.fields
    if form_model.entity_defaults_to_reporter():
        fields = form_model.fields[1:]
    questions = helper.get_code_and_title(fields)
    rows = _get_number_of_rows_in_result(manager, questionnaire_code)
    results = {'questionnaire': questionnaire,
               'questions': questions}
    if rows:
        submissions, ids = _get_submissions_for_display(current_page - 1, manager, questionnaire_code, copy(questions),
                                                        pagination)
        results.update(submissions=zip(submissions, ids))
    return rows, results


@login_required(login_url='/login')
def project_results(request, project_id=None, questionnaire_code=None):
    manager = get_database_manager(request)
    error_message = ""
    project = models.get_project(project_id, dbm=manager)
    project_links = _make_project_links(project_id, questionnaire_code)
    if request.method == 'GET':
        current_page = int(request.GET.get('page_number') or 1)
        rows, results = _load_submissions(current_page, manager, questionnaire_code)
        if rows is None:
            error_message = "No submissions present for this project"
        return render_to_response('project/results.html',
                {'questionnaire_code': questionnaire_code, 'results': results, 'pages': rows,
                 'error_message': error_message, 'project_links': project_links, 'project': project},
                                  context_instance=RequestContext(request)
        )
    if request.method == "POST":
        data_record_ids = json.loads(request.POST.get('id_list'))
        for each in data_record_ids:
            data_record = manager._load_document(each, DataRecordDocument)
            manager.invalidate(each)
            SubmissionLogger(manager).void_data_record(data_record.submission.get("submission_id"))

        current_page = request.POST.get('current_page')
        rows, results = _load_submissions(int(current_page), manager, questionnaire_code)
        return render_to_response('project/log_table.html',
                {'questionnaire_code': questionnaire_code, 'results': results, 'pages': rows,
                 'success_message': "The selected records have been deleted"}, context_instance=RequestContext(request))


def _format_data_for_presentation(data_dictionary, form_model):
    header_list = helper.get_headers(form_model.fields)
    type_list = helper.get_type_list(form_model.fields[1:])
    if data_dictionary == {}:
        return "[]", header_list, type_list
    data_list = helper.get_values(data_dictionary, header_list) 
    header_list[0] = form_model.entity_type[0] + " Name"
    data_list = helper.convert_to_json(data_list)
    response_string = encode_json(data_list)
    return response_string, header_list, type_list


def _load_data(form_model, manager, questionnaire_code, request):
    header_list = helper.get_headers(form_model.fields)
    aggregation_type_list = json.loads(request.POST.get("aggregation-types"))
    start_time = helper.get_formatted_time_string(request.POST.get("start_time").strip() + " 00:00:00")
    end_time = helper.get_formatted_time_string(request.POST.get("end_time").strip() + " 23:59:59")
    aggregates = helper.get_aggregate_list(header_list[1:], aggregation_type_list)
    aggregates = [aggregate_module.aggregation_factory("latest", form_model.fields[0].name)] + aggregates
    data_dictionary = aggregate_module.aggregate_by_form_code_python(manager, questionnaire_code,
                                                                     aggregates=aggregates, starttime=start_time,
                                                                     endtime=end_time)
    return data_dictionary


@login_required(login_url='/login')
def project_data(request, project_id=None, questionnaire_code=None):
    manager = get_database_manager(request)
    project = models.get_project(project_id, dbm=manager)
    form_model = get_form_model_by_code(manager, questionnaire_code)
    project_links = _make_project_links(project_id, questionnaire_code)

    if request.method == "GET":
        data_dictionary = data.aggregate_for_form(manager, form_code=questionnaire_code,
                                                  aggregates={"*": data.reduce_functions.LATEST},
                                                  aggregate_on=EntityAggregration())
        response_string, header_list, type_list = _format_data_for_presentation(data_dictionary, form_model)
        return render_to_response('project/data_analysis.html',
                {"entity_type": form_model.entity_type[0], "data_list": repr(response_string),
                 "header_list": header_list, "type_list": type_list, 'project_links': project_links, 'project': project}
                                  ,
                                  context_instance=RequestContext(request))
    if request.method == "POST":
        data_dictionary = _load_data(form_model, manager, questionnaire_code, request)
        response_string, header_list, type_list = _format_data_for_presentation(data_dictionary, form_model)
        return HttpResponse(response_string)


@login_required(login_url='/login')
def export_data(request):
    questionnaire_code = request.POST.get("questionnaire_code")
    manager = get_database_manager(request)
    form_model = get_form_model_by_code(manager, questionnaire_code)
    data_dictionary = _load_data(form_model, manager, questionnaire_code, request)
    response_string, header_list, type_list = _format_data_for_presentation(data_dictionary, form_model)
    raw_data_list = json.loads(response_string)
    raw_data_list.insert(0, header_list)
    file_name = request.POST.get(u"project_name")+'_analysis'
    return _create_excel_response(raw_data_list, file_name)


def _create_excel_response(raw_data_list,file_name):
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="%s.xls"'%(file_name,)
    wb = utils.get_excel_sheet(raw_data_list, 'data_log')
    wb.save(response)
    return response


@login_required(login_url='/login')
def export_log(request):
    questionnaire_code = request.POST.get("questionnaire_code")
    manager = get_database_manager(request)
    row_count, results = _load_submissions(1, manager, questionnaire_code, pagination=False)
    header_list = ["From", "To", "Date Receieved", "Submission status", "Void"]
    header_list.extend([each[1] for each in results['questions']])
    raw_data_list = [header_list]
    if row_count:
        submissions, ids = zip(*results['submissions'])
        raw_data_list.extend([list(each) for each in submissions])

    file_name = request.POST.get(u"project_name")+'_log'
    return _create_excel_response(raw_data_list,file_name)


@login_required(login_url='/login')
def subjects_wizard(request, project_id=None):
    if request.method == 'GET':
        manager = get_database_manager(request)
        reg_form = get_form_model_by_code(manager, 'reg')
        previous_link = reverse(edit_profile, args=[project_id])
        entity_types = get_all_entity_types(manager)
        project = models.get_project(project_id, manager)
        helper.remove_reporter(entity_types)
        import_subject_form = SubjectUploadForm()
        return render_to_response('project/subjects_wizard.html',
                {'fields': reg_form.fields, "previous": previous_link, "entity_types": entity_types,
                 'import_subject_form': import_subject_form,
                 'post_url': reverse(import_subjects_from_project_wizard), 'project': project},
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        return HttpResponseRedirect(reverse(questionnaire_wizard, args=[project_id]))


def _format_field_description_for_data_senders(reg_form):
    for field in reg_form.fields:
        temp = field.label.get("eng")
        temp = temp.replace("subject", "data sender")
        field.label.update(eng=temp)


@login_required(login_url='/login')
def datasenders_wizard(request, project_id=None):
    if request.method == 'GET':
        manager = get_database_manager(request)
        reg_form = get_form_model_by_code(manager, 'reg')
        previous_link = reverse(questionnaire_wizard, args=[project_id])
        project = models.get_project(project_id, manager)
        import_reporter_form = ReporterRegistrationForm()
        _format_field_description_for_data_senders(reg_form)
        return render_to_response('project/datasenders_wizard.html',
                {'fields': reg_form.fields[1:], "previous": previous_link,
                 'form': import_reporter_form,
                 'post_url': reverse(import_subjects_from_project_wizard), 'project': project},
                                  context_instance=RequestContext(request))

    if request.method == 'POST':

        return HttpResponseRedirect(reverse(datasenders, args=[project_id]))
    pass


@login_required(login_url='/login')
def activate_project(request, project_id=None):
    manager = get_database_manager(request)
    project = models.get_project(project_id, manager)
    project.state = PROJECT_ACTIVE_STATUS
    project.save(manager)
    return HttpResponseRedirect(reverse(project_overview, args=[project_id]))

@login_required(login_url='/login')
def finish(request, project_id=None):
    return render_to_response('project/finish_and_test.html', context_instance=RequestContext(request))

def _get_project_and_project_link(manager, project_id):
    project = models.get_project(project_id, manager)
    questionnaire = helper.load_questionnaire(manager, project['qid'])
    project_links = _make_project_links(project_id, questionnaire.form_code)
    return project, project_links

@login_required(login_url='/login')
def subjects(request, project_id=None):
    manager = get_database_manager(request)
    project, project_links = _get_project_and_project_link(manager, project_id)
    reg_form = get_form_model_by_code(manager, 'reg')
    return render_to_response('project/subjects.html', {'fields': reg_form.fields, 'project':project, 'project_links':project_links}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def registered_subjects(request, project_id=None):
    manager = get_database_manager(request)
    project, project_links = _get_project_and_project_link(manager, project_id)
    all_data = load_all_subjects(request)
    return render_to_response('project/registered_subjects.html', {'project':project, 'project_links':project_links, 'all_data':all_data}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def registered_datasenders(request, project_id=None):
    manager = get_database_manager(request)
    project, project_links = _get_project_and_project_link(manager, project_id)
    all_data = load_all_reporters(request)
    return render_to_response('project/registered_datasenders.html', {'project':project, 'project_links':project_links, 'all_data':all_data}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def datasenders(request, project_id=None):
    manager = get_database_manager(request)
    project, project_links = _get_project_and_project_link(manager, project_id)
    reg_form = get_form_model_by_code(manager, 'reg')
    _format_field_description_for_data_senders(reg_form)
    return render_to_response('project/datasenders.html', {'fields': reg_form.fields[1:], 'project':project, 'project_links':project_links}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def questionnaire(request, project_id=None):
#    manager = get_database_manager(request)
#    project, project_links = _get_project_and_project_link(manager, project_id)
#    reg_form = get_form_model_by_code(manager, 'reg')
#    _format_field_description_for_data_senders(reg_form)
#    return render_to_response('project/datasenders.html', {'fields': reg_form.fields[1:], 'project':project, 'project_links':project_links}, context_instance=RequestContext(request))
    manager = get_database_manager(request)
    if request.method == 'GET':
        previous_link = reverse(subjects_wizard, args=[project_id])
        project = models.get_project(project_id, manager)
        form_model = helper.load_questionnaire(manager, project.qid)
        fields = form_model.fields
        if form_model.entity_defaults_to_reporter():
            fields = helper.hide_entity_question(form_model.fields)
        existing_questions = json.dumps(fields, default=field_to_json)
        return render_to_response('project/questionnaire.html',
                {"existing_questions": repr(existing_questions), 'questionnaire_code': form_model.form_code,
                 "previous": previous_link, 'project': project}, context_instance=RequestContext(request))

