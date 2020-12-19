 'use strict';
 /** place expressions here
 =====================================================================
 =====================================================================
 **/



 var actionsOnReadImage = {
  fileHard : null,

  failedValidate: function() {
    this.fileHard = null;

  },
  successValidate: function() {
    $("#modal-large").iziModal("open");
    $("#content-hasil").hide();
    if (cropper) {
      cropper.destroy();
      cropper = null;
    }
  },
  finished: function() {
    cropper = new Cropper(image[0], {
      strict: true,
      viewMode: 2,
      cropBoxResizable: false,
      aspectRatio: 2 / 3,
      autoCropArea: 0.7,
      cropBoxMovable: true,
      dragMode: 'none',
      center: true,
      zoomOnWheel: false,
    });
  },
};
 /** place common functions here
 =====================================================================
 =====================================================================
 **/

 function validateNoNullVar() {

  for (let i = 0; i < arguments.length; i++) {
    if (arguments[i] == '')
      return false;
    if (arguments[i] == null)
      return false;
    if (arguments[i] == undefined)
      return false;
  }

  return true;

}
function sendCroppedImageToServer(actionsOnSendCroppedImage) {
  let cropper = actionsOnSendCroppedImage.element;
  let canvas = cropper.getCroppedCanvas({
    width: 200,
    height: 300,
  });
  actionsOnSendCroppedImage.startSend(canvas);

}
function swalFireGagal(objects = {}) {
 objects.title = objects.title || 'Gagal !';
 objects.text = objects.text || 'Periksa Kembali !';
 objects.icon = objects.icon || 'warning';
 objects.timer = objects.timer || 1000;
 Swal.fire({
   title: objects.title,
   text: objects.text,
   icon: objects.icon,
   showConfirmButton: false,
   timer: objects.timer,

 })
}

function readImageFromInput(actionsOnReadImage) {
 var eventChange = actionsOnReadImage.event;
 var files = eventChange.target.files;
 var reader;
 var file;
 var url;
 if (!isImageSelected(files)) {
   actionsOnReadImage.failedValidate();
   return;
 } else {
   actionsOnReadImage.successValidate();
 }

 file = files[0];
 actionsOnReadImage.fileHard = file;
 if (URL) {
   setSrcImage(image, URL.createObjectURL(file));
 } else if (FileReader) {
   reader = new FileReader();
   reader.onload = function(e) {
     setSrcImage(image, reader.result)
   };
   reader.readAsDataURL(file);
 }
 actionsOnReadImage.finished()
}

function isImageSelected(files) {
 if (files && files.length <= 0)
   return false;
 return true;
}

function setSrcImage(image, url) {
 if (image instanceof jQuery)
   image.attr('src', url);
 else
   document.querySelector(image).src = url;
}

function setModelTableSelector(tableSelector, objOut) {
 let table = $(tableSelector).DataTable({
   select: 'single',
 });
 table.on('select', function(e, dt, type, indexes) {
   if (type === 'row') {
     objOut.model_id = $(table.rows(indexes).nodes()).data("modelId");
   }
 });
 table.on('deselect', function(e, dt, type, indexes) {
   objOut.model_id = null;
 });
}

function showSpinner() {
     // Initialize
     if ($('.kintone-spinner').length == 0) {
         // Create elements for the spinner and the background of the spinner
         var spin_div = $('<div id ="kintone-spin" class="kintone-spinner"></div>');
         var spin_bg_div = $('<div id ="kintone-spin-bg" class="kintone-spinner"></div>');

         // Append spinner to the body
         $(document.body).append(spin_div, spin_bg_div);

         // Set a style for the spinner
         $(spin_div).css({
           'position': 'fixed',
           'top': '50%',
           'left': '50%',
           'z-index': '510',
           'padding': '26px',
           '-moz-border-radius': '4px',
           '-webkit-border-radius': '4px',
           'border-radius': '4px'
         });
         $(spin_bg_div).css({
           'position': 'fixed',
           'top': '0px',
           'left': '0px',
           'z-index': '500',
           'width': '100%',
           'height': '200%',
           'background-color': '#000',
           'opacity': '0.5',
           'filter': 'alpha(opacity=50)',
           '-ms-filter': "alpha(opacity=50)"
         });

         // Set options for the spinner
         var opts = {
           'color': '#fff'
         };

         // Create the spinner
         new Spin.Spinner(opts).spin(document.getElementById('kintone-spin'));
       }

     // Display the spinner
     $('.kintone-spinner').show();
   }

 // Function to hide the spinner
 function hideSpinner() {
     // Hide the spinner
     $('.kintone-spinner').hide();
   }