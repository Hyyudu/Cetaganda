	$(document).ready(function(){

		planet_radius = 30;
		pw_radius = 70;
		mapX=0;
		mapY=0;

		var planets = planet_map();
		
		function getRange(point1, point2)	{
			return Math.sqrt(Math.pow(point1[0]-point2[0],2) + Math.pow(point1[1] - point2[1],2))
		}

		function getPlanetByCoords(mapX, mapY, id)	{
			for (name in planets)	{
				planet = planets[name];
				if (id == 'map_old')	{
					range = getRange(planet.coords, [mapX, mapY])
					if (range<=pw_radius)	{
						res = {id: name, planet_name: planet.name+" (t)", on_orbit: false, code: planet.planet_code+1}
						if (range <= planet_radius)
							res = {id: name, planet_name: planet.name+" (p)", on_orbit: true, code: planet.planet_code}
						return res;
					}
				}
				else	{	// new map
					range = getRange(planet.new_coords, [mapX, mapY])
					if (range<planet_radius)	{
						res = {id: name, planet_name: planet.name+" (p)", on_orbit: true, code: planet.planet_code}
						return res;
					}
					range = getRange(planet.new_pw, [mapX, mapY])
					if (range<planet_radius)	{
						res = {id: name, planet_name: planet.name+" (t)", on_orbit: false, code: planet.planet_code+1}
						return res;
					}					
				
				}
			}
		}
		
		function getPlanetOnMouse(e)	{
			var map_id = e.currentTarget.id
			mapX = Math.round(e.offsetX/$('#'+map_id)[0].width*1000);
			mapY = Math.round(e.offsetY/$('#'+map_id)[0].height*1000);
			
			planet = getPlanetByCoords(mapX, mapY, map_id, 1)
			
			return planet;
		}


		
		function codes2names()	{
			val = $('#id_route').val().trim()
			arr = val.split(' ')
			out = []
			for (i in arr)
				out.push(planet_by_code(arr[i]))
			$('#planned_movements').html(out.join(' - '))
		}
		
		$('#id_route').on('input', codes2names)

		
		$('.starmap').click(function(e) {
			var planet = getPlanetOnMouse(e);
			console.log(planet)
			if (planet)	{
				$('#id_route').val($('#id_route').val().trim()+" "+planet.code)
				codes2names()
			}
		});
		
		$('.starmap').mousemove(function(e){
			
			var planet = getPlanetOnMouse(e);
			var text = mapX+":"+mapY;
			if (planet)	{
				text+=" - "+planet.planet_name;
			}
			$('#coords').html(text)
		});

		codes2names();

	});