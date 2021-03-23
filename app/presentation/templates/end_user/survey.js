$(document).ready(function () {
    Formio.createForm(document.getElementById('survey-form'), survey_form).then((form) => {
                $.each(default_values, function (k, v) {
            try {
                form.getComponent(k).setValue(v);
            } catch (error ) {
                return;
            }
        });
        form.on('submit', function(submitted) {
            window.location.href = Flask.url_for(survey_endpoint, {form_data: JSON.stringify(submitted.data)});
        });
    });
});


