# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from _csv import Error
import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_view_exempt, csrf_response_exempt
from django.views.decorators.http import require_http_methods
from datawinners.main.utils import get_database_manager
from datawinners.subjects.SubjectException import InvalidFileFormatException
from datawinners.subjects.forms import SubjectUploadForm
from django.contrib import messages
from mangrove.datastore.entity import get_all_entities, get_by_short_code
from mangrove.errors.MangroveException import CSVParserInvalidHeaderFormatException, XlsParserInvalidHeaderFormatException
from mangrove.form_model.form_model import NAME_FIELD, MOBILE_NUMBER_FIELD, DESCRIPTION_FIELD
from mangrove.transport.player.player import CsvPlayer, CsvParser, XlsPlayer, XlsParser
from mangrove.transport.submissions import SubmissionHandler


def _handle_uploaded_file(request, file, extension):
    manager = get_database_manager(request)
    if extension == '.csv':
        file = file.splitlines()
        csv_player = CsvPlayer(dbm=manager, submission_handler=SubmissionHandler(manager), parser=CsvParser())
        response = csv_player.accept(file)
    elif extension == '.xls':
        xls_player = XlsPlayer(dbm=manager, submission_handler=SubmissionHandler(manager), parser=XlsParser())
        response = xls_player.accept(file)
    else:
        raise InvalidFileFormatException()
    return response


def _laod_all_subjects(request):
    manager = get_database_manager(request)
    rows = get_all_entities(dbm=manager, include_docs=True)
    data = []
    for row in rows:
        type = row['doc']['aggregation_paths']['_type']
        short_code = row['doc']['short_code']
        entity = get_by_short_code(dbm=manager, short_code=short_code, entity_type=type)
        type = '.'.join(type)
        if type.lower() != 'reporter':
            id = row['id']
            name = entity.value(NAME_FIELD)
            location = row['doc']['geometry'].get('coordinates')
            mobile_number = entity.value(MOBILE_NUMBER_FIELD)
            description = entity.value(DESCRIPTION_FIELD)
            result_dict = dict(id=id, name=name, short_name=short_code, type=type, location=location,
                               description=description, mobile_number=mobile_number)
            data.append(result_dict)
    return data


def _tabulate_failures(rows):
    tabulated_data = []
    errors = ''
    for row in rows:
        row[1].errors['row_num'] = row[0] + 2
        if type(row[1].errors['error']) is list:
            for error in row[1].errors['error']:
                errors = errors + ' ' + error
            row[1].errors['error'] = errors
        tabulated_data.append(row[1].errors)
    return tabulated_data

@csrf_view_exempt
@csrf_response_exempt
@login_required(login_url='/login')
def index(request):
    if request.method == 'POST':
        success = False
        success_message = ''
        error_message = None
        failure_imports = None
        try:
            file_name = request.GET.get('qqfile')
            base_name, extension = os.path.splitext(file_name)
            response = _handle_uploaded_file(request=request, file=request.raw_post_data, extension=extension)
            successful_imports = len([index for index in response if index.success])
            total = len(response)
            failure = [i for i in enumerate(response) if not i[1].success]
            failure_imports = _tabulate_failures(failure)
            if total == successful_imports:
                success = True
            success_message = '%s of %s records uploaded' % (successful_imports, total)
        except CSVParserInvalidHeaderFormatException as e:
            error_message = e.message
        except XlsParserInvalidHeaderFormatException as e:
            error_message = e.message
        except InvalidFileFormatException:
            error_message = 'We could not import your list of Subjects. ! \
                        You are using a document format we canʼt import. Please use a Comma Separated Values (.csv) or a Excel (.xls) file!'
        except Exception:
            error_message = 'Some unexpected error happened. Please check the CSV file and import again.'
        all_subjects = _laod_all_subjects(request)
        return HttpResponse(json.dumps({'success': success, 'message': success_message, 'error_message': error_message,
                                    'failure_imports': failure_imports, 'all_subjects':all_subjects}))

    all_subjects = _laod_all_subjects(request)
    return render_to_response('subjects/index.html', {'all_subjects': all_subjects}, context_instance=RequestContext(request))



@csrf_view_exempt
@csrf_response_exempt
@require_http_methods(['POST'])
@login_required(login_url='/login')
def import_subjects_from_project_wizard(request):
    success = False
    success_message = ''
    error_message = None
    failure_imports = None
    try:
        file_name = request.GET.get('qqfile')
        base_name, extension = os.path.splitext(file_name)
        response = _handle_uploaded_file(request=request, file=request.raw_post_data, extension=extension)
        successful_imports = len([index for index in response if index.success])
        total = len(response)
        failure = [index for index in enumerate(response) if not index[1].success]
        failure_imports = _tabulate_failures(failure)
        if total == successful_imports:
            success = True
        success_message = '%s of %s records uploaded' % (successful_imports, total)
    except CSVParserInvalidHeaderFormatException as e:
        error_message = e.message
    except XlsParserInvalidHeaderFormatException as e:
        error_message = e.message
    except InvalidFileFormatException:
        error_message = 'We could not import your list of Subjects. ! \
                    You are using a document format we canʼt import. Please use a Comma Separated Values (.csv) ﬁle or a Excel (.xls) file!'
    except Exception:
        error_message = 'Some unexpected error happened. Please check the CSV file and import again.'
    return HttpResponse(json.dumps({'success': success, 'message': success_message, 'error_message': error_message,
                                    'failure_imports': failure_imports}))
