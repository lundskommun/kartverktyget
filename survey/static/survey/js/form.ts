/// <reference path="../typings/jquery/jquery.d.ts" />
/// <reference path="../typings/jquery.validation/jquery.validation.d.ts" />
/// <reference path="../typings/local-js-cookie.d.ts" />
/// <reference path="map.ts" />


class FormManager {
    private post_url;
    private form_url;
    private listeners: FormListener[] = [ ];
    private fields: string[];

    constructor(form_url: string, post_url: string) {
        this.form_url = form_url;
        this.post_url = post_url;

        this.prepareValidator();

        $('#sidebar-questionnaire-cancel').click(this.onCancel);
        $('#sidebar-questionnaire-submit').click(this.onSubmit);
    }

    private prepareValidator() {
        $.validator.setDefaults({
            highlight: function(element) {
                $(element).closest('.form-group').addClass('has-error');
            },
            unhighlight: function(element) {
                $(element).closest('.form-group').removeClass('has-error');
            },
            errorElement: 'span',
            errorClass: 'help-block',
            errorPlacement: function(error, element) {
                if(element.parent('.input-group').length) {
                    error.insertAfter(element.parent());
                } else {
                    error.insertAfter(element);
                }
            }
        });

        $('#sidebar-questionnaire-form').validate();
    }

    public presentIntro() {
        $('.sidebar').hide();
        $('#sidebar-intro').show();
    }

    public presentForm(type: FeatureType, feature: string) {
        $('.sidebar').hide();
        this.acquireForm(feature);
    }

    public presentConfirmation() {
        $('#sidebar')
    }

    public acquireForm(feature: string) {
        var _formManager = this;

        $.ajax({
            method: 'POST',
            url: this.form_url,
            data: { feature: JSON.stringify(feature) },
            headers: { 'X-CSRFToken': Cookies.get('csrftoken') }
        }).done(function(response) {
            _formManager.fields = response.fields;
            $('#sidebar-questionnaire-form').replaceWith($.parseHTML(response.fragment));
            $('#sidebar-questionnaire-form').validate({ debug: true });
            $('#sidebar-questionnaire').show();
        });
    }

    public onSubmit = (event:any) => {
        console.log("FormManager.onSubmit begin");
        var _formManager = this;
        var contribution = { }

        if ($('#sidebar-questionnaire-form').valid()) {
            $('.sidebar').hide();
            $('#sidebar-spinner-done').hide();
            $('#sidebar-spinner').show();

            this.fields.forEach((field) => {
                contribution[field] = $('#' + field).val();
            });

            $.ajax({
                method: 'POST',
                url: this.post_url,
                data: contribution,
                headers: { 'X-CSRFToken': Cookies.get('csrftoken') }
            }).done(function (response) {
                console.log("received response on post");
                _formManager.listeners.forEach((listener) => {
                    listener.formSubmitted();
                });
            });
        }

        console.log("FormManager.onSubmit end");
    }

    public onCancel = () => {
        this.listeners.forEach((listener) => {
            listener.formCancelled();
        });
    }

    public addListener(listener:FormListener) {
        this.listeners.push(listener);
    }

}

interface FormListener {
    formSubmitted(): void;
    formCancelled(): void;
}

