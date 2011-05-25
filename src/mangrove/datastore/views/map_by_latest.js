function(doc) {
  if (!doc.void) {
    for (k in doc.data){
      value = {};
	var date = new Date(doc.event_time);
        dt = [date.getUTCFullYear(), date.getUTCMonth() + 1,
            date.getUTCDate(), date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds()];
      key = [doc.entity_backing_field.aggregation_paths['_type'],
             doc.entity_backing_field._id,k];
      key = key.concat(dt);
      emit(key, value);
    }
  }
  
}

