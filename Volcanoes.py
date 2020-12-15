import folium
import pandas

data=pandas.read_csv("Volcanoes.txt")

lat=list(data["LAT"])
lon=list(data["LON"])
elevation = list(data["ELEV"])
name=list(data["NAME"])

def color_generator(elevation):
    if elevation<1000:
        return "green"
    elif elevation >= 1000 and elevation < 3000:
        return "orange"
    else:
        return "red"

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22 Volcano" target="_blank">%s</a><br>
Height: %s m
"""


map = folium.Map(location=[46.776959526407474, -118.1774030427453], zoom_start = 5)

fgv = folium.FeatureGroup(name="Volcanoes")
for lt, ln, el, na in zip(lat, lon, elevation, name):
    iframe = folium.IFrame(html=html %(na, na, el), width=200, height=100)
    fgv.add_child(folium.Marker(location=(lt,ln), popup=folium.Popup(iframe), icon=folium.Icon(color=color_generator(el))))

fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x:{'fillColor':'green' if x['properties']['POP2005'] < 1000000
else 'yellow' if 1000000 <= x['properties']['POP2005'] < 2000000
else 'black' if 2000000 <= x['properties']['POP2005'] < 50000000 else 'red'}))


map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl())

map.save("Volcanoes.html")
