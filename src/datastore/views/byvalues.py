# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

__author__ = 'jwishnie'


_map = '''
function(doc) {
    var isNotNull = function(o) {
        return !((o === undefined) || (o == null));
    };
    if (doc.document_type == 'DataRecord' && isNotNull(doc.entity_backing_field)) {
        var value = {entity_type: { value:doc.entity_backing_field.entity_type }, document_type: { value:doc.entity_backing_field.document_type}};
        var date = new Date(doc.reported_on);
        if (isNotNull(doc.entity_backing_field) && isNotNull(doc.entity_backing_field.attributes)) {
            var attributes = doc.entity_backing_field.attributes;
            for (index in attributes) {
                if (isNotNull(attributes[index]) && isNotNull(attributes[index]['value'])) {
                    var attribute_object = attributes[index];
                    attribute_object['timestamp_for_view'] = date.getTime();
                    value[index] = attributes[index];
                }
            }
        }
        for (index in doc.attributes) {
            var attributes = doc.attributes;
            if (isNotNull(attributes[index]) && isNotNull(attributes[index]['value'])) {
                var attribute_object = attributes[index];
                attribute_object['timestamp_for_view'] = date.getTime();
                value[index] = attributes[index];
            }
        }
        var key = [doc.entity_backing_field.entity_type, doc.entity_backing_field._id, date.getFullYear(), date.getMonth() + 1, date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()];
        emit(key, value);
    }
}
'''

_reduce = '''
function(key, values, rereduce) {
    var isNull = function(o) {
        return (o === undefined) || (o == null);
    };

    var current = { entity_id : {value: key[0][0][1] } };

    for (value in values) {
        for (index in values[value]) {
            if (isNull(current[index]) || values[value][index].timestamp_for_view > current[index].timestamp_for_view) {
                current[index] = values[value][index];
            }
        }
    }
    return current;
}
'''