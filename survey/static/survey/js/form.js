/// <reference path="../typings/jquery/jquery.d.ts" />
/// <reference path="../typings/jquery.validation/jquery.validation.d.ts" />
/// <reference path="../typings/local-js-cookie.d.ts" />
/// <reference path="map.ts" />
var FormManager = (function () {
    function FormManager(form_url, post_url) {
        var _this = this;
        this.listeners = [];
        this.onSubmit = function (event) {
            console.log("FormManager.onSubmit begin");
            var _formManager = _this;
            var contribution = {};
            if ($('#sidebar-questionnaire-form').valid()) {
                $('.sidebar').hide();
                $('#sidebar-spinner-done').hide();
                $('#sidebar-spinner').show();
                _this.fields.forEach(function (field) {
                    contribution[field] = $('#' + field).val();
                });
                $.ajax({
                    method: 'POST',
                    url: _this.post_url,
                    data: contribution,
                    headers: { 'X-CSRFToken': Cookies.get('csrftoken') }
                }).done(function (response) {
                    console.log("received response on post");
                    _formManager.listeners.forEach(function (listener) {
                        listener.formSubmitted();
                    });
                });
            }
            console.log("FormManager.onSubmit end");
        };
        this.onCancel = function () {
            _this.listeners.forEach(function (listener) {
                listener.formCancelled();
            });
        };
        this.form_url = form_url;
        this.post_url = post_url;
        this.prepareValidator();
        $('#sidebar-questionnaire-cancel').click(this.onCancel);
        $('#sidebar-questionnaire-submit').click(this.onSubmit);
    }
    FormManager.prototype.prepareValidator = function () {
        $.validator.setDefaults({
            highlight: function (element) {
                $(element).closest('.form-group').addClass('has-error');
            },
            unhighlight: function (element) {
                $(element).closest('.form-group').removeClass('has-error');
            },
            errorElement: 'span',
            errorClass: 'help-block',
            errorPlacement: function (error, element) {
                if (element.parent('.input-group').length) {
                    error.insertAfter(element.parent());
                }
                else {
                    error.insertAfter(element);
                }
            }
        });
        $('#sidebar-questionnaire-form').validate();
    };
    FormManager.prototype.presentIntro = function () {
        $('.sidebar').hide();
        $('#sidebar-intro').show();
    };
    FormManager.prototype.presentForm = function (type, feature) {
        $('.sidebar').hide();
        this.acquireForm(feature);
    };
    FormManager.prototype.presentConfirmation = function () {
        $('#sidebar');
    };
    FormManager.prototype.acquireForm = function (feature) {
        var _formManager = this;
        $.ajax({
            method: 'POST',
            url: this.form_url,
            data: { feature: JSON.stringify(feature) },
            headers: { 'X-CSRFToken': Cookies.get('csrftoken') }
        }).done(function (response) {
            _formManager.fields = response.fields;
            $('#sidebar-questionnaire-form').replaceWith($.parseHTML(response.fragment));
            $('#sidebar-questionnaire-form').validate({ debug: true });
            $('#sidebar-questionnaire').show();
        });
    };
    FormManager.prototype.addListener = function (listener) {
        this.listeners.push(listener);
    };
    return FormManager;
})();
//# sourceMappingURL=form.js.map