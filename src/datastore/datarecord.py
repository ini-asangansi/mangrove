# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from datastore.database import get_db_manager
import entity
from utils import is_sequence, utcnow


def submit(entity_id,data,source):
    assert entity_id is not None
    assert is_sequence(data)

    # create and persist a submission doc.
    # source will have channel info ie. Web/SMS etc,,
    # source will also have the reporter info.

    e = entity.get(get_db_manager(),entity_id)
    e.add_data(data=data,event_time=utcnow(),submission_id = "")
    pass
    #    What should be the return parameter