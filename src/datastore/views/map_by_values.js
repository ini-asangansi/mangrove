function(doc) {
    var isNotNull = function(o) {
        return !((o === undefined) || (o == null));
    };
    if (doc.document_type == 'DataRecord' && isNotNull(doc.entity_backing_field)) {
        var value = {entity_type: { value:doc.entity_backing_field.aggregation_paths['_type'] }, document_type: { value:doc.entity_backing_field.document_type}};
        var date = new Date(doc.event_time);

        for (index in doc.data) {
            var data = doc.data;
            if (isNotNull(data[index]) && isNotNull(data[index]['value'])) {
                var attribute_object = data[index];
                attribute_object['timestamp_for_view'] = date.getTime();
                value[index] = data[index];
            }
        }
        var key = [doc.entity_backing_field.aggregation_paths['_type'], doc.entity_backing_field._id, date.getFullYear(), date.getMonth() + 1, date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()];
        emit(key, value);
    }
}