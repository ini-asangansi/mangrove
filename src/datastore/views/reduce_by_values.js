function(key, values, rereduce) {
		current = values[0];
		for(i in values){
			x = values[i];
    			if (x.timestamp > current.timestamp) current = x;
		}
		return current;

}