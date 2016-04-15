var MapManager = (function () {
    function MapManager() {
        var _this = this;
        this.listeners = [];
        this.map = L.map('map');
        this.onCreated = function (e) {
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
            _this.listeners.forEach(function (listener) {
                listener.featureCreated(feature_type, feature.toGeoJSON());
            });
            _this.lastLayerAdded = feature;
            _this.map.addLayer(feature);
        };
        console.log("MapManager.constructor begin");
        var osmLayer = L.tileLayer('/osm/hydda/full/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: '&copy; <a href="http://openstreetmap.se/">OpenStreetMap Sverige</a>'
        });
        var aerialLayer = L.tileLayer.wms("http://kartor.lund.se/geoserver/wms", {
            layers: 'lund:orto14wgs84',
            format: 'image/jpeg',
            attribution: "&copy; Lantmäteriet"
        });
        var baseLayers = {
            "OpenStreetMap": osmLayer,
            "Flygfoto": aerialLayer
        };
        this.map.addLayer(osmLayer);
        L.control.layers(baseLayers, {}).addTo(this.map);
        this.drawControl = new L.Control.Draw();
        var options = {
            circle: false,
            rectangle: false
        };
        if (!map_settings.allow_polygons) {
            options['polygon'] = false;
        }
        this.drawControl.setDrawingOptions(options);
        this.map.on('draw:created', this.onCreated);
        console.log("MapManager.constructor end");
    }
    MapManager.prototype.centerMap = function () {
        this.map.setView(map_settings.center_point, 13);
    };
    MapManager.prototype.enableControls = function () {
        console.log("MapManager.enableControls begin");
        this.map.addControl(this.drawControl);
        console.log("MapManager.enableControls end");
    };
    MapManager.prototype.disableControls = function () {
        console.log("MapManager.disableControls begin");
        this.map.removeControl(this.drawControl);
        console.log("MapManager.disableControls end");
    };
    MapManager.prototype.showFeatures = function (features_url) {
        var _map = this.map;
        $.ajax({
            url: features_url
        }).done(function (response) {
            L.geoJson(response, {
                onEachFeature: function (feature, layer) {
                    layer.bindPopup(feature.properties.description);
                }
            }).addTo(_map);
        });
    };
    MapManager.prototype.undoCreated = function () {
        this.map.removeLayer(this.lastLayerAdded);
    };
    MapManager.prototype.addListener = function (listener) {
        this.listeners.push(listener);
    };
    return MapManager;
})();
var FeatureType;
(function (FeatureType) {
    FeatureType[FeatureType["Point"] = 0] = "Point";
    FeatureType[FeatureType["Line"] = 1] = "Line";
    FeatureType[FeatureType["Polygon"] = 2] = "Polygon";
})(FeatureType || (FeatureType = {}));
//# sourceMappingURL=map.js.map