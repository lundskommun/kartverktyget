/// <reference path="../typings/jquery/jquery.d.ts" />
/// <reference path="map.ts" />
/// <reference path="form.ts" />
var ClientApplication = (function () {
    function ClientApplication() {
        this.mapManager = new MapManager();
        this.mapManager.addListener(this);
        this.formManager = new FormManager(survey_settings.form_url, survey_settings.post_url);
        this.formManager.addListener(this);
    }
    ClientApplication.prototype.featureCreated = function (type, feature) {
        console.log("Got feature");
        console.log(feature);
        this.mapManager.disableControls();
        this.formManager.presentForm(type, feature);
    };
    ClientApplication.prototype.formSubmitted = function () {
        this.mapManager.enableControls();
        this.formManager.presentIntro();
    };
    ClientApplication.prototype.formCancelled = function () {
        this.mapManager.undoCreated();
        this.mapManager.enableControls();
        this.formManager.presentIntro();
    };
    ClientApplication.prototype.prepareCollection = function () {
        this.mapManager.enableControls();
        this.formManager.presentIntro();
    };
    ClientApplication.prototype.prepareResults = function (features_url) {
        this.mapManager.showFeatures(features_url);
    };
    ClientApplication.prototype.centerMap = function () {
        this.mapManager.centerMap();
    };
    return ClientApplication;
})();
Raven.config(generic_settings.raven_dsn);
var ca = new ClientApplication();
function adjustMapHeight() {
    var height = $(window).height();
    var pixels = (80 * height) / 100;
    var pixels_s = pixels + 'px';
    $("#map").css('height', pixels_s);
    ca.centerMap();
}
$(document).ready(function () {
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
//# sourceMappingURL=app.js.map