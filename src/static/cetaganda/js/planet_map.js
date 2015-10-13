function planet_map()	{
	return  {
			"archipelag": {
				"planet_code": 23,
				"links": ['hegen_hub', 'klein', 'illirika'],
				"name": 'Архипелаг Джексона',
				"x": 179,
				"y": 307
			},
			"barrayar": {
				"planet_code": 7,
				"links": ['komarra'],
				"name": 'Барраяр',
				"x": 905,
				"y": 640
			},
			"beta": {
				"planet_code": 31,
				"links": ['dagula', 'escobar', 'sergiyar'],
				"name": 'Колония Бета',
				"x": 426,
				"y": 804
			},
			"vervan": {
				"planet_code": 15,
				"links": ['hegen_hub', 'illirika'],
				"name": 'Верван',
				"x": 129,
				"y": 106
			},
			"dagula": {
				"planet_code": 5,
				"links": ['hegen_hub', 'xi_kita', 'marilak', 'earth', 'beta'],
				"name": 'Дагула',
				"x": 438,
				"y": 562
			},
			"earth": {
				"planet_code": 1,
				"links": ['dagula', 'hegen_hub', 'sigma_kita', 'escobar'],
				"name": 'Земля',
				"x": 574,
				"y": 500
			},
			"sergiyar": {
				"planet_code": 29,
				"links": ['escobar','beta', 'komarra'],
				"name": 'Сергияр',
				"x": 673,
				"y": 797
			},
			"illirika": {
				"planet_code": 17,
				"links": ['vervan', 'archipelag', 'tau_kita'],
				"name": 'Иллирика',
				"x": 101,
				"y": 896
			},
			"klein": {
				"planet_code": 25,
				"links": ['archipelag', 'escobar'],
				"name": 'Станция Клайн',
				"x": 270,
				"y": 664
			},
			"komarra": {
				"planet_code": 3,
				"links": ['sergiyar', 'earth', 'tau_kita', 'ro_kita', 'barrayar'],
				"name": 'Комарра',
				"x": 759,
				"y": 638
			},
			"ksi_kita": {
				"planet_code": 19,
				"links": ['sigma_kita','dagula', 'eta_kita'],
				"name": 'Кси Кита',
				"x": 663,
				"y": 145
			},
			"marilak": {
				"planet_code": 35,
				"links": ['dagula', 'sigma_kita'],
				"name": 'Марилак',
				"x": 463,
				"y": 254
			},
			"mu_kita": {
				"planet_code": 13,
				"links": ['hegen_hub', 'eta_kita'],
				"name": 'Мю Кита',
				"x": 458,
				"y": 62
			},
			"ro_kita": {
				"planet_code": 9,
				"links": ['komarra', 'eta_kita'],
				"name": 'Ро Кита',
				"x": 871,
				"y": 422
			},
			"sigma_kita": {
				"planet_code": 37,
				"links": ['earth', 'marilak', 'eta_kita', 'ksi_kita'],
				"name": 'Сигма Кита',
				"x": 671,
				"y": 339
			},
			"tau_kita": {
				"planet_code": 33,
				"links": ['komarra', 'illirika'],
				"name": 'Тау Кита',
				"x": 911,
				"y": 903
			},
			"hegen_hub": {
				"planet_code": 21,
				"links": ['archipelag', 'vervan', 'mu_kita', 'earth', 'dagula'],
				"name": 'Хеген Хаб',
				"x": 321,
				"y": 353
			},
			"eskobar": {
				"planet_code": 27,
				"links": ['klein', 'earth', 'beta', 'sergiyar'],
				"name": 'Эскобар',
				"x": 564,
				"y": 693
			},
			"eta_kita": {
				"planet_code": 11,
				"links": ['mu_kita', 'sigma_kita', 'ksi_kita', 'ro_kita'],
				"name": 'Эта Кита',
				"x": 858,
				"y": 102
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