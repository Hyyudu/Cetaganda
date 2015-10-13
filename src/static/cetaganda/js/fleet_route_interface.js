	$(document).ready(function(){

		planet_radius = 30;
		pw_radius = 70;

		var planets = planet_map();

		function getPlanetByCoords(mapX, mapY, cn)	{
			found = 0;
			for (name in planets)	{
				planet = planets[name];
				range = Math.sqrt(Math.pow(planet.x - mapX,2) + Math.pow(planet.y - mapY,2))
				if (range<=pw_radius)	{
					found = 1;
					break;
				}
			}
			if (!found) return null;
			res = {id: name, planet_name: planet.name+" (t)", on_orbit: false, code: planet.planet_code+1}
			if (range<planet_radius)	{
				res.planet_name = planet.name+" (p)";
				res.on_orbit = true;
				res.code = planet.planet_code
			}
			if (cn!=undefined)
				console.log(res)
			return res;
		}

		$('#starmap').click(function(e) {
			var mapX = Math.round(e.offsetX/$('#starmap')[0].width*1000);
			var mapY = Math.round(e.offsetY/$('#starmap')[0].height*1000);
			planet = getPlanetByCoords(mapX, mapY,1)
			if (planet)	{
				$('#id_route').val($('#id_route').val().trim()+" "+planet.code)
				codes2names()
			}
		});
		
		function codes2names()	{
			val = $('#id_route').val().trim()
			arr = val.split(' ')
			out = []
			for (i in arr)
				out.push(planet_by_code(arr[i]))
			$('#planned_movements').html(out.join(' - '))
		}
		
		$('#id_route').on('input', codes2names)

		$('#starmap').mousemove(function(e){
			var mapX = Math.round(e.offsetX/$('#starmap')[0].width*1000);
			var mapY = Math.round(e.offsetY/$('#starmap')[0].height*1000);
			var text = mapX+":"+mapY;
			planet = getPlanetByCoords(mapX, mapY)
			if (planet)	{
				text+=" - "+planet.planet_name;
			}
			$('#coords').html(text)
		});

		codes2names();

	});