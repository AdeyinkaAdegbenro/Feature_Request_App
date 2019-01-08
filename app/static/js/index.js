$(document).ready(function() {
    // show form when `add a feature` button is clicked
    $('#feature-request-button').click(function(e) {
        $('#feature-request-add').css('display', 'none');
        $('#feature-request-form').css('display', 'block')
        $('#requests-table').css('display', 'none')
    })

    // create form validation
    $('.ui.form').form({
        on: 'blur',
        fields: {
          title: {
            identifier: 'title',
            rules: [{
                type: 'empty',
                prompt: 'Please enter a title for your feature request'
            }]
          },

          description: {
            identifier: 'description',
            rules: [{
                type: 'empty',
                prompt: 'Please enter a description for your feature request'
            }]
          },

          client: {
            identifier: 'client',
            rules: [{
                type: 'empty',
                prompt: 'Please select a client for your feature request'
            }]
          },

          client_priority: {
            identifier: 'client_priority',
            rules: [{
                type: 'empty',
                prompt: 'Please enter a client priority value for your feature request'
            }]
          },

          target_date: {
            identifier: 'target_date',
            rules: [{
            type: 'empty',
            prompt: 'Please select a target date'
            }]
          },

          product_area: {
            identifier: 'product_area',
            rules: [{
                type: 'empty',
                prompt: 'Please select a product area for your feature request'
            }]
          }
        }
    })

    // set up date picker for a better UX
    $("#target-date").flatpickr({
        altInput: true,
        altFormat: "F j, Y",
        dateFormat: "Y-m-d",
    });

    // handle form submission
    var feature_form = $('#feature-form')
    feature_form.submit(function( event ) {
        event.preventDefault();
        if (feature_form.form('is valid')) {
            // form is valid
            values = feature_form.serializeArray()
            // send form values to server
            $.ajax({
                type: 'POST',
                url: '/',
                data: JSON.stringify(values),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                success: function submitFormCallback(data) {
                    // show submission confirmation to user
                    $('#feature-request-form').css('display', 'none')
                    $('#form-filled').css('display', 'block')
                    setTimeout(function () {
                        window.location.reload()
                    }, 1000);
                },
                error: function submitFail (err) {
                    console.log(err)
                    // error submitting form
                    $('#error-form').css('display', 'block')
                    setTimeout(function () {
                        window.location.reload()
                    }, 3000);
                }
            })
        }
    });
  });