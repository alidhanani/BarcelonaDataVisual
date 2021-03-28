import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px
import altair as alt

import streamlit.components.v1 as components

# bootstrap 4 collapse example
components.html(
    """
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
	  integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
	  crossorigin=""/>
	<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
	  integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
	  crossorigin=""></script>
    <div id="accordion">
      <div class="card">
        <div class="card-header" id="headingOne">
          <h5 class="mb-0">
            <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
            Collapsible Group Item #1
            </button>
          </h5>
        </div>
        <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
          <div class="card-body">
            Collapsible Group Item #1 content
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-header" id="headingTwo">
          <h5 class="mb-0">
            <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
            Collapsible Group Item #2
            </button>
          </h5>
        </div>
        <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
          <div class="card-body">
            Collapsible Group Item #2 content
          </div>
        </div>
      </div>
    </div>
    """,
    height=600,
)


# bootstrap 4 collapse example
components.html(
    """
    <h3>Using GeoJSON with Leaflet</h3>

<p>GeoJSON is becoming a very popular data format among many GIS technologies and services — it's simple, lightweight, straightforward, and Leaflet is quite good at handling it. In this example, you'll learn how to create and interact with map vectors created from <a href="http://geojson.org/">GeoJSON</a> objects.</p>

<div id="map" class="map" style="height: 250px"></div>

<script src="sample-geojson.js"></script>
<script>

	var map = L.map('map').setView([39.74739, -105], 13);

	L.tileLayer(MB_URL, {
		attribution: MB_ATTR,
		id: 'mapbox/light-v9',
		tileSize: 512,
		zoomOffset: -1
	}).addTo(map);

	var baseballIcon = L.icon({
		iconUrl: 'baseball-marker.png',
		iconSize: [32, 37],
		iconAnchor: [16, 37],
		popupAnchor: [0, -28]
	});

	function onEachFeature(feature, layer) {
		var popupContent = "<p>I started out as a GeoJSON " +
				feature.geometry.type + ", but now I'm a Leaflet vector!</p>";

		if (feature.properties && feature.properties.popupContent) {
			popupContent += feature.properties.popupContent;
		}

		layer.bindPopup(popupContent);
	}

	L.geoJson({features: [bicycleRental, campus]}, {

		style: function (feature) {
			return feature.properties && feature.properties.style;
		},

		onEachFeature: onEachFeature,

		pointToLayer: function (feature, latlng) {
			return L.circleMarker(latlng, {
				radius: 8,
				fillColor: "#ff7800",
				color: "#000",
				weight: 1,
				opacity: 1,
				fillOpacity: 0.8
			});
		}
	}).addTo(map);

	L.geoJson(freeBus, {

		filter: function (feature, layer) {
			if (feature.properties) {
				// If the property "underConstruction" exists and is true, return false (don't render features under construction)
				return feature.properties.underConstruction !== undefined ? !feature.properties.underConstruction : true;
			}
			return false;
		},

		onEachFeature: onEachFeature
	}).addTo(map);

	var coorsLayer = L.geoJson(null, {

		pointToLayer: function (feature, latlng) {
			return L.marker(latlng, {icon: baseballIcon});
		},

		onEachFeature: onEachFeature
	}).addTo(map);

	coorsLayer.addData(coorsField);

</script>

<p><a href="geojson-example.html">View example on a separate page &rarr;</a></p>

<h3>About GeoJSON</h3>

<p>According to <a href="http://geojson.org">http://geojson.org</a>:</p>

<blockquote>GeoJSON is a format for encoding a variety of geographic data structures. A GeoJSON object may represent a geometry, a feature, or a collection of features. GeoJSON supports the following geometry types: Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, and GeometryCollection. Features in GeoJSON contain a geometry object and additional properties, and a feature collection represents a list of features.</blockquote>

<p>Leaflet supports all of the GeoJSON types above, but <a href="https://tools.ietf.org/html/rfc7946#section-3.2">Features</a> and <a href="https://tools.ietf.org/html/rfc7946#section-3.3">FeatureCollections</a> work best as they allow you to describe features with a set of properties. We can even use these properties to style our Leaflet vectors. Here's an example of a simple GeoJSON feature:</p>

<pre><code>var geojsonFeature = {
	"type": "Feature",
	"properties": {
		"name": "Coors Field",
		"amenity": "Baseball Stadium",
		"popupContent": "This is where the Rockies play!"
	},
	"geometry": {
		"type": "Point",
		"coordinates": [-104.99404, 39.75621]
	}
};
</code></pre>

Beware of the switched order of latitude and longitude in GeoJSON; as per definition in [RFC 7946](https://tools.ietf.org/html/rfc7946) GeoJSON uses coordinates in (lon,lat) order instead of (lat,lon) that Leaflet uses.

<h3>The GeoJSON layer</h3>

<p>GeoJSON objects are added to the map through a <a href="/reference.html#geojson">GeoJSON layer</a>. To create it and add it to a map, we can use the following code:</p>

<pre><code>L.geoJson(geojsonFeature).addTo(map);</code></pre>

<p>GeoJSON objects may also be passed as an array of valid GeoJSON objects.</p>

<pre><code>var myLines = [{
	"type": "LineString",
	"coordinates": [[-100, 40], [-105, 45], [-110, 55]]
}, {
	"type": "LineString",
	"coordinates": [[-105, 40], [-110, 45], [-115, 55]]
}];
</code></pre>

<p>Alternatively, we could create an empty GeoJSON layer and assign it to a variable so that we can add more features to it later.</p>

<pre><code>var myLayer = L.geoJson().addTo(map);
myLayer.addData(geojsonFeature);
</code></pre>

<h3>Options</h3>

<h4>style</h4>

<p>The <code>style</code> option can be used to style features two different ways. First, we can pass a simple object that styles all paths (polylines and polygons) the same way:</p>

<pre><code>var myLines = [{
	"type": "LineString",
	"coordinates": [[-100, 40], [-105, 45], [-110, 55]]
}, {
	"type": "LineString",
	"coordinates": [[-105, 40], [-110, 45], [-115, 55]]
}];

var myStyle = {
	"color": "#ff7800",
	"weight": 5,
	"opacity": 0.65
};

L.geoJson(myLines, {
	style: myStyle
}).addTo(map);</code></pre>

<p>Alternatively, we can pass a function that styles individual features based on their properties. In the example below we check the "party" property and style our polygons accordingly:</p>

<pre><code>var states = [{
	"type": "Feature",
	"properties": {"party": "Republican"},
	"geometry": {
		"type": "Polygon",
		"coordinates": [[
			[-104.05, 48.99],
			[-97.22,  48.98],
			[-96.58,  45.94],
			[-104.03, 45.94],
			[-104.05, 48.99]
		]]
	}
}, {
	"type": "Feature",
	"properties": {"party": "Democrat"},
	"geometry": {
		"type": "Polygon",
		"coordinates": [[
			[-109.05, 41.00],
			[-102.06, 40.99],
			[-102.03, 36.99],
			[-109.04, 36.99],
			[-109.05, 41.00]
		]]
	}
}];

L.geoJson(states, {
	style: function(feature) {
		switch (feature.properties.party) {
			case 'Republican': return {color: "#ff0000"};
			case 'Democrat':   return {color: "#0000ff"};
		}
	}
}).addTo(map);</code></pre>

<h4>pointToLayer</h4>

<p>Points are handled differently than polylines and polygons. By default simple markers are drawn for GeoJSON Points. We can alter this by passing a <code>pointToLayer</code> function in a <a href="/reference.html#geojson-options">GeoJSON options</a> object when creating the GeoJSON layer. This function is passed a <a href="/reference.html#latlng">LatLng</a> and should return an instance of ILayer, in this case likely a <a href="/reference.html#marker">Marker</a> or <a href="/reference.html#circlemarker">CircleMarker</a>.</p>

<p>Here we're using the <code>pointToLayer</code> option to create a CircleMarker:</p>

<pre><code>var geojsonMarkerOptions = {
	radius: 8,
	fillColor: "#ff7800",
	color: "#000",
	weight: 1,
	opacity: 1,
	fillOpacity: 0.8
};

L.geoJson(someGeojsonFeature, {
	pointToLayer: function (feature, latlng) {
		return L.circleMarker(latlng, geojsonMarkerOptions);
	}
}).addTo(map);</code></pre>

<p>We could also set the <code>style</code> property in this example &mdash; Leaflet is smart enough to apply styles to GeoJSON points if you create a vector layer like circle inside the <code>pointToLayer</code> function.</p>

<h4>onEachFeature</h4>

<p>The <code>onEachFeature</code> option is a function that gets called on each feature before adding it to a GeoJSON layer. A common reason to use this option is to attach a popup to features when they are clicked.</p>

<pre><code>function onEachFeature(feature, layer) {
	// does this feature have a property named popupContent?
	if (feature.properties &amp;&amp; feature.properties.popupContent) {
		layer.bindPopup(feature.properties.popupContent);
	}
}

var geojsonFeature = {
	"type": "Feature",
	"properties": {
		"name": "Coors Field",
		"amenity": "Baseball Stadium",
		"popupContent": "This is where the Rockies play!"
	},
	"geometry": {
		"type": "Point",
		"coordinates": [-104.99404, 39.75621]
	}
};

L.geoJson(geojsonFeature, {
	onEachFeature: onEachFeature
}).addTo(map);</code></pre>

<h4>filter</h4>

<p>The <code>filter</code> option can be used to control the visibility of GeoJSON features. To accomplish this we pass a function as the <code>filter</code> option. This function gets called for each feature in your GeoJSON layer, and gets passed the <code>feature</code> and the <code>layer</code>. You can then utilise the values in the feature's properties to control the visibility by returning <code>true</code> or <code>false</code>.</p>

<p>In the example below "Busch Field" will not be shown on the map.</p>

<pre><code>var someFeatures = [{
	"type": "Feature",
	"properties": {
		"name": "Coors Field",
		"show_on_map": true
	},
	"geometry": {
		"type": "Point",
		"coordinates": [-104.99404, 39.75621]
	}
}, {
	"type": "Feature",
	"properties": {
		"name": "Busch Field",
		"show_on_map": false
	},
	"geometry": {
		"type": "Point",
		"coordinates": [-104.98404, 39.74621]
	}
}];

L.geoJson(someFeatures, {
	filter: function(feature, layer) {
		return feature.properties.show_on_map;
	}
}).addTo(map);</code></pre>

<p>View the <a href="geojson-example.html">example page</a> to see in detail what is possible with the GeoJSON layer.</p>
    """,
    height=600,
)

def get_data():
    return pd.read_csv('./archive/unemployment.csv')

st.set_option('deprecation.showPyplotGlobalUse', False)

df = get_data()
min_year = int(df['Year'].min()) 
max_year = int(df['Year'].max()) 
district_names = df['District Name'].unique()
neighborhood_names = df['Neighborhood Name'].unique()

st.title('Barcelona')

#st.table(df.head())

st.sidebar.header('Filter Options')

selected_year = st.sidebar.slider('Year', min_year, max_year)

selected_district = st.sidebar.selectbox('District Name', district_names)

st.sidebar.header('Comparing')

# selected_district_1 = st.sidebar.selectbox('District Name 1', district_names)
# selected_district_2 = st.sidebar.selectbox('District Name 2', district_names)

num_dist = st.sidebar.text_input('Number of district')
all_dist = [] 
if num_dist == "":
    num_dist = "0"
for i in range(0, int(num_dist)):
	all_dist.append(st.sidebar.selectbox('District Name '+str(i), district_names))



#selected_neighborhood = st.sidebar.selectbox('Neighborhood Name', neighborhood_names)
df1 = df[(df['District Name'] == selected_district) 
        & (df['Year'] == selected_year)]
       # & (df['Neighborhood Name'] == selected_neighborhood)]

df1


#number per Neighborhood
st.write("Number per Neighborhood")
d1 = df1.groupby(df['Neighborhood Name'])['Number'].sum()
d1

#number per gender
st.write("Number per Gender")
d2 = df1.groupby(df['Gender'])['Number'].sum()
d2

#number per month
st.write("Number per Month")
d3 = df1.groupby(df['Month'])['Number'].sum()
d3

d3.hist()
plt.show()
st.pyplot()

#st.bar_chart(d3['Month'])

dataframes = []
for i in all_dist:
	df4 = df[(df['District Name'] == i) 
        & (df['Year'] == selected_year)]
       # & (df['Neighborhood Name'] == selected_neighborhood)]
	df4 = df4.groupby(df4["Gender"])["Number"].sum()
	dataframes.append(df4)


# df4 = df[(df['District Name'] == selected_district_1) 
#         & (df['Year'] == selected_year)]
#        # & (df['Neighborhood Name'] == selected_neighborhood)]
# df4 = df4.groupby(df4["Gender"])["Number"].sum()
# df4

# df5 = df[(df['District Name'] == selected_district_2) 
#         & (df['Year'] == selected_year)]
#        # & (df['Neighborhood Name'] == selected_neighborhood)]
# df5 = df5.groupby(df5["Gender"])["Number"].sum()
# df5
newData = []
for i in range(len(dataframes)-1):
	newData.append(pd.merge(dataframes[i], dataframes[i+1], on='Gender'))

#newData = pd.concat(dataframes)
#len(newData)

for i in newData:
	df6 = i.T
	df6.plot.bar(rot=15, title="Car Price vs Car Weight comparision for Sedans made by a Car Company")
	plt.show(block=True)
	st.pyplot()


# df6_Trans = newData[len(newData)-1].T
# # df6 = pd.merge(df4, df5, on='Gender')
# # df6_Trans = df6.T
# df6_Trans

# df6_Trans.plot.bar(rot=15, title="Car Price vs Car Weight comparision for Sedans made by a Car Company")
# plt.show(block=True)
# st.pyplot()

# df6 = df6.groupby(df['Neighborhood Name'])['Number'].sum()
# df6
#fig = px.bar(df, x="Gender", y=["Number_x", "Number_y"], barmode='group', height=400)
# st.dataframe(df) # if need to display dataframe
#st.plotly_chart(fig)
# chart = alt.Chart(y2k_pop).mark_bar().encode(
#     x='age:O',
#     y='sum(people):Q',
#     color=alt.Color('sex:N', scale=alt.Scale(range=["#e377c2","#1f77b4"]))
# )


# df.plot.bar(x='Year', logy=True)
# plt.xticks(rotation=0)
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.show()
# st.pyplot()



