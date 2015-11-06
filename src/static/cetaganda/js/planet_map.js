function planet_map()	{
	return  {
			"archipelag": {
				"planet_code": 23,
				"links": ['hegen_hub', 'klein', 'illirika'],
				"name": 'Архипелаг Джексона',
				"coords" : [179, 307],
				"new_coords": [85,336],
				"new_pw": [105,479]
			},
			"barrayar": {
				"planet_code": 7,
				"links": ['komarra'],
				"name": 'Барраяр',
				"coords" : [905,640],
				"new_coords": [920,516],
				"new_pw": [848,613]
			},
			"beta": {
				"planet_code": 31,
				"links": ['dagula', 'escobar', 'sergiyar'],
				"name": 'Колония Бета',
				"coords" : [426,804],
				"new_coords": [338,792],
				"new_pw": [443,871]
			},
			"vervan": {
				"planet_code": 15,
				"links": ['hegen_hub', 'illirika'],
				"name": 'Верван',
				"coords" : [129,106],
				"new_coords": [196,85],
				"new_pw": [28,83]
			},
			"dagula": {
				"planet_code": 5,
				"links": ['hegen_hub', 'xi_kita', 'marilak', 'earth', 'beta'],
				"name": 'Дагула',
				"coords" : [438,562],
				"new_coords": [354,565],
				"new_pw": [413,498]
			},
			"earth": {
				"planet_code": 1,
				"links": ['dagula', 'hegen_hub', 'sigma_kita', 'escobar'],
				"name": 'Земля',
				"coords" : [574,500],
				"new_coords": [510,541],
				"new_pw": [614,500]
			},
			"sergiyar": {
				"planet_code": 29,
				"links": ['escobar','beta', 'komarra'],
				"name": 'Сергияр',
				"coords" : [673,797],
				"new_coords": [764,889],
				"new_pw": [653,883]
			},
			"illirika": {
				"planet_code": 17,
				"links": ['vervan', 'archipelag', 'tau_kita'],
				"name": 'Иллирика',
				"coords" : [101,896],
				"new_coords": [170,813],
				"new_pw": [45,920]
			},
			"klein": {
				"planet_code": 25,
				"links": ['archipelag', 'escobar'],
				"name": 'Станция Клайн',
				"coords" : [270,664],
				"new_coords": [149,689],
				"new_pw": [280,673]
			},
			"komarra": {
				"planet_code": 3,
				"links": ['sergiyar', 'earth', 'tau_kita', 'ro_kita', 'barrayar'],
				"name": 'Комарра',
				"coords" : [759,638],
				"new_coords": [663,615],
				"new_pw": [769,663]
			},
			"ksi_kita": {
				"planet_code": 19,
				"links": ['sigma_kita','dagula', 'eta_kita'],
				"name": 'Кси Кита',
				"coords" : [663,145],
				"new_coords": [690,95],
				"new_pw": [795,138]
			},
			"marilak": {
				"planet_code": 35,
				"links": ['dagula', 'sigma_kita'],
				"name": 'Марилак',
				"coords" : [463,254],
				"new_coords": [573,187],
				"new_pw": [478,214]
			},
			"mu_kita": {
				"planet_code": 13,
				"links": ['hegen_hub', 'eta_kita'],
				"name": 'Мю Кита',
				"coords" : [458,62],
				"new_coords": [364,85],
				"new_pw": [463,95]
			},
			"ro_kita": {
				"planet_code": 9,
				"links": ['komarra', 'eta_kita'],
				"name": 'Ро Кита',
				"coords" : [871,422],
				"new_coords": [716,459],
				"new_pw": [835,447]
			},
			"sigma_kita": {
				"planet_code": 37,
				"links": ['earth', 'marilak', 'eta_kita', 'ksi_kita'],
				"name": 'Сигма Кита',
				"coords" : [671,339],
				"new_coords": [828,334],
				"new_pw": [695,339]
			},
			"tau_kita": {
				"planet_code": 33,
				"links": ['komarra', 'illirika'],
				"name": 'Тау Кита',
				"coords" : [911,903],
				"new_coords": [905,779],
				"new_pw": [950,905]
			},
			"hegen_hub": {
				"planet_code": 21,
				"links": ['archipelag', 'vervan', 'mu_kita', 'earth', 'dagula'],
				"name": 'Хеген Хаб',
				"coords" : [321,353],
				"new_coords": [264,447],
				"new_pw": [316,302]
			},
			"eskobar": {
				"planet_code": 27,
				"links": ['klein', 'earth', 'beta', 'sergiyar'],
				"name": 'Эскобар',
				"coords" : [564,693],
				"new_coords": [540,818],
				"new_pw": [544,694]
			},
			"eta_kita": {
				"planet_code": 11,
				"links": ['mu_kita', 'sigma_kita', 'ksi_kita', 'ro_kita'],
				"name": 'Эта Кита',
				"coords" : [858,102],
				"new_coords": [941,233],
				"new_pw": [924,87]
			}
		};

}

function planet_by_code(code)	{
	if (planet_by_code.data == undefined)	{
		d = {}
		planets = planet_map()
		for (name in planets)	{
			planet = planets[name]
			d[planet.planet_code] = planet.name+" (p)"
			d[planet.planet_code+1] = planet.name+ " (t)"
		}
		planet_by_code.data = d
	}
	return planet_by_code.data[code] ? planet_by_code.data[code] : "(неверный код)"
}