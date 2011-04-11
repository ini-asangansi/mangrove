function(doc) {
 

for (k in doc.data){
	var date = new Date(doc.event_time);
	key = [doc.entity_backing_field.aggregation_paths['_type'], 
	doc.entity_backing_field._id,k,date.getUTCFullYear(), date.getUTCMonth() + 1,
	date.getUTCDate(), date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds()];
	doc.data[k]["timestamp"] = date.getTime()
	emit(key, doc.data[k]);
}


}