var app = {};

/**
 * Setup app
 */
app.setupApp = function(){

  // get templates
  app.getTemplates();

  // image file select
  $(document).on('change', '.btn-file :file', function() {
      var input = $(this),
          numFiles = input.get(0).files ? input.get(0).files.length : 1,
          label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
      input.trigger('fileselect', [numFiles, label]);
  });

  $(document).ready( function() {
      $('.btn-file :file').on('fileselect', function(event, numFiles, label) {
        $(this).parents('.input-group').find(':text').val(label);
      });
  });

  // handle download click
  $(document).on('click', '#btnDownload', function(){
    window.open('http://localhost:5000/api/v1/document/' + app.documentId);

  });

  // button generate
  $(document).on('click', '#btnGenerate', function(){
    // create form data
    var formData = new FormData()
    formData.append('title',  $('#title').val());
    formData.append('text',  $('#text').val());
    formData.append('template',  $('#template').val());
    formData.append('image', $('input[type=file]')[0].files[0]);

    // change generate button
    app.changeGenerateDocButton();

    // post ajax request
    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/api/v1/jobs',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
          // store document id
          app.documentId = data.jobsInfoID;

          // check if document is ready
          app.checkIfDocumentIsReady();
        },
        error: function(){
          // change button
          app.changeGenerateDocButton();
        }
    });
  });

}


/**
 * Change generate button
 */
app.changeGenerateDocButton = function(){
  if($('#btnGenerate').hasClass('ready')){
    // flip classes
    $('#btnGenerate').removeClass('ready').addClass('busy');
    $('#btnGenerate').removeClass('btn-primary').addClass('btn-success');

    // change button properties
    $('#btnGenerate').html('<span class="glyphicon glyphicon-flash" aria-hidden="true"></span> Building document...');
  }else{
    // flip classes
    $('#btnGenerate').removeClass('busy').addClass('ready');
    $('#btnGenerate').removeClass('btn-success').addClass('btn-primary');

    // change button properties
    $('#btnGenerate').html('<span class="glyphicon glyphicon-wrench" aria-hidden="true"></span> Generate document');
  }
}


/**
 * Checks if a document is ready (kinda hacky ;-))
 */
app.checkIfDocumentIsReady = function(){
    var counter = 0;

    var intervalObj = setInterval(function(){
      $.ajax({
          type: 'GET',
          url: 'http://localhost:5000/api/v1/document/' + app.documentId + '/exists',
          success: function(data) {
            // change generate button
            app.changeGenerateDocButton();

            // update preview
            app.updatePreview();

            // clear our interval
            clearInterval(intervalObj);
          }
      });

      // after 10 tries exist
      if(counter == 10){
        // change button
        app.changeGenerateDocButton();

        // clear our interval
        clearInterval(intervalObj);
      }

      counter++;
    }, 800);
}

/**
 * Get templates
 */
app.getTemplates = function(){
  $.ajax({
      type: 'GET',
      url: 'http://localhost:5000/api/v1/templates',
      success: function(data) {
        app.populateTemplateDropdown(data);
      }
  });
}

/**
 * Populate dropdown template
 */
app.populateTemplateDropdown = function(templates){
  var dropdownTemplate = $('#template');

  for (template of templates){
    dropdownTemplate.append(
      $('<option></option>').val(template.slice(0, -4)).html(template)
    );
  }

}

/**
 * Update preview
 */
app.updatePreview = function(){
    // clear any previous preview
    $('#preview').html('');

    // add our image
    $('#preview').prepend(
      $('<img>',
        {
          style: 'display: block',
          src: 'http://localhost:5000/api/v1/document/' + app.documentId + '/image'
        }
      )
    );

    // add download button
    $('#preview').append('<button id="btnDownload" class="btn btn-primary"><span class="glyphicon glyphicon-download" aria-hidden="true"></span> Download document</button>');
}

// setup our app
app.setupApp();
