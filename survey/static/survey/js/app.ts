/// <reference path="../typings/jquery/jquery.d.ts" />
/// <reference path="map.ts" />
/// <reference path="form.ts" />

class ClientApplication implements MapListener, FormListener {
    private mapManager;
    private formManager;

    constructor() {
        this.mapManager = new MapManager();
        this.mapManager.addListener(this);

        this.formManager = new FormManager(survey_settings.form_url, survey_settings.post_url);
        this.formManager.addListener(this);
    }

    public featureCreated(type:FeatureType, feature:string):void {
        console.log("Got feature");
        console.log(feature);
        this.mapManager.disableControls();
        this.formManager.presentForm(type, feature);
    }

    public formSubmitted():void {
        this.mapManager.enableControls();
        this.formManager.presentIntro();
    }

    public formCancelled():void {
        this.mapManager.undoCreated();
        this.mapManager.enableControls();
        this.formManager.presentIntro();
    }

    public prepareCollection() {
        this.mapManager.enableControls();
        this.formManager.presentIntro();
    }

    public prepareResults(features_url: string) {
        this.mapManager.showFeatures(features_url);
    }

    public centerMap() {
        this.mapManager.centerMap();
    }
}

Raven.config(generic_settings.raven_dsn);

var ca = new ClientApplication();

function adjustMapHeight() {
    var height = $(window).height();
    var pixels = (80 * height) / 100;
    var pixels_s = pixels + 'px';
    $("#map").css('height', pixels_s);
    ca.centerMap();
}

$(document).ready(function() {
    adjustMapHeight();
    $(window).bind('resize', adjustMapHeight);
});

$(document).ajaxError(function (event, jqXHR, ajaxSettings, thrownError) {
    Raven.captureMessage(thrownError || jqXHR.statusText, {
        extra: {
            type: ajaxSettings.type,
            url: ajaxSettings.url,
            data: ajaxSettings.data,
            status: jqXHR.status,
            error: thrownError || jqXHR.statusText,
            response: jqXHR.responseText.substring(0, 100)
        }
    });
});




