// read the .csv file
val einst = sc.textFile("blak-einstaklingar.csv")
einst.count  
// we have 4498 but the first line is header :(
einst.take(1)
// lets get rid of that
val einst_hless = einst.filter( line => !(line.contains("EinstID") ) )
einst.count
einst_hless.count 

// We want to find all the rows that have just on name 
val einst_one_name = einst_hless.filter( line => line.split(";")(1).split(" ").size < 2 )

// now lets key both RDDs 
val eon_key = einst_one_name.map( line => (line.split(";")(1).split(" ")(0), line) )
val e_key = einst_hless.map( line => (line.split(";")(1).split(" ")(0), line) )

// we can see what this looks like with 
eon_key.take(10).foreach(println)

// now we want the names list grouped so we get an arry of all the same first names. 
val e_key_gr = e_key.groupByKey().map( x => (x._1, x._2.toArray) )

// Now let's join them 
val x = eon_key.join(e_key_gr)
// now I can look at what I got (I have broken it down below)
x.take(10)(2)
res33: (String, (String, Array[String])) = 
	(Lúðvík, // the key 
		(4160;Lúðvík;1996-09-02 00:00:00.000;"kk ";;;NULL;NULL;NULL;;;;2013-04-28 10:50:35.960;0, // ROW from eon_key RDD
			Array( // Array of same key values from e_key_gr RDD
				4160;Lúðvík;1996-09-02 00:00:00.000;"kk ";;;NULL;NULL;NULL;;;;2013-04-28 10:50:35.960;0, 
				866;Lúðvík Kristinsson;1969-03-31 00:00:00.000;"kk ";;;;;;;;;2001-04-17 12:12:41.047;NULL, 
				2299;Lúðvík Kristinsson;1969-03-31 00:00:00.000;"kk ";;;NULL;NULL;NULL;;;;2007-04-26 11:38:05.860;NULL, 
				4167;Lúðvík Már Matthíasson;1996-09-02 00:00:00.000;"kk ";HK;;NULL;NULL;NULL;;;;2013-09-03 21:00:29.950;0, 
				604;Lúðvík Smárason;1961-08-29 00:00:00.000;"kk ";Reynir Hellissandi;;;;;4366771;4366771;;2000-04-04 16:28:39.790;NULL
			)
		)
	)
// I can now create code that looks at the ROW from eon_key RDD and try to match it with a "full name"
// the e_key_gr RDD (i.e. the full einstaklingar CSV file.)
// remember, I exclude matching it to my self. 