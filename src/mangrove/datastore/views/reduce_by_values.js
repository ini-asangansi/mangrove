function(key, values, rereduce) {
	if (rereduce == false){
		result = {};
		total = 0;
		count = 0;
		for(i in values){
			count = count + 1;
			x = values[i];
			if (typeof(x.value)=='number') total = total + x.value;
		}
		result.sum = total;
        result.count = count;
        result.entity_id = values[0].entity_id;
        result.field = values[0].field;
        result.location = values[0].location;
		return result;
	}
	else{
        result = {};
		total = 0;
		count = 0;
		for(i in values){
			x = values[i];
			count = count + x.count;
			if (typeof(x.sum)=='number') total = total + x.sum;
		}
        result.sum = total;
        result.count = count;
        result.entity_id = values[0].entity_id;
        result.field = values[0].field;
        result.location = values[0].location;
        return result;
		
	}

}