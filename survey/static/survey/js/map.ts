class MapManager {
    private listeners: MapListener[] = [ ];
    private map: any = L.map('map');
    private drawControl: any;
    private lastLayerAdded: any;

    constructor() {
        console.log("MapManager.constructor begin");

        var osmLayer = L.tileLayer(
            '/osm/hydda/full/{z}/{x}/{y}.png',
            {
                maxZoom: 18,
                attribution: '&copy; <a href="http://openstreetmap.se/">OpenStreetMap Sverige</a>',
            });

        var aerialLayer = L.tileLayer.wms(
            "http://kartor.lund.se/geoserver/wms",
            {
                layers: 'lund:orto14wgs84',
                format: 'image/jpeg',
                attribution: "&copy; Lantmäteriet",
            }
        );

        var baseLayers = {
            "OpenStreetMap": osmLayer,
            "Flygfoto": aerialLayer,
        };

        this.map.addLayer(osmLayer);
        L.control.layers(baseLayers, { }).addTo(this.map);

        this.drawControl = new L.Control.Draw();
        var options = {
            circle: false,
            rectangle: false,
        }

        if (!map_settings.allow_polygons) {
            options['polygon'] = false;
        }

        this.drawControl.setDrawingOptions(options);
        this.map.on('draw:created', this.onCreated);

        console.log("MapManager.constructor end");
    }

    public centerMap() {
        this.map.setView(map_settings.center_point, 13);
    }

    public enableControls() {
        console.log("MapManager.enableControls begin");
        this.map.addControl(this.drawControl);
        console.log("MapManager.enableControls end");
    }

    public disableControls() {
        console.log("MapManager.disableControls begin");
        this.map.removeControl(this.drawControl);
        console.log("MapManager.disableControls end");
    }

    public showFeatures(features_url: string) {
        var _map = this.map;

        $.ajax({
            url: features_url,
        }).done(function(response) {
            L.geoJson(response, {
                onEachFeature: function (feature, layer) {
                    layer.bindPopup(feature.properties.description);
                }
            }).addTo(_map);
        });
    }

    public onCreated = (e:any) => {
        var string_type = e.layerType;
        var feature_type;
        var feature = e.layer;

        switch (string_type) {
            case "marker":
                feature_type = FeatureType.Point;
                break;
            case "polyline":
                feature_type = FeatureType.Line;
                break;
            case "polygon":
                feature_type = FeatureType.Polygon;
                break;
        }

        this.listeners.forEach((listener) => {
            listener.featureCreated(feature_type, feature.toGeoJSON());
        });

        this.lastLayerAdded = feature;
        this.map.addLayer(feature);
    }

    public undoCreated():void {
        this.map.removeLayer(this.lastLayerAdded);
    }

    public addListener(listener:MapListener) {
        this.listeners.push(listener);
    }
}

enum FeatureType {
    Point,
    Line,
    Polygon,
}

interface MapListener {
    featureCreated(type: FeatureType, feature: string): void;
}


