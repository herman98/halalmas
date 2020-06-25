$(function () {

  'use strict';

  var console = window.console || { log: function () {} };
  var $image = $('#image');
  var $download = $('#download');
  var $dataX = $('#dataX');
  var $dataY = $('#dataY');
  var $dataHeight = $('#dataHeight');
  var $dataWidth = $('#dataWidth');
  var $dataRotate = $('#dataRotate');
  var $dataScaleX = $('#dataScaleX');
  var $dataScaleY = $('#dataScaleY');
  var options = {
        // aspectRatio: NaN, //16 / 9,
        // preview: '.img-preview',
        // crop: function (e) {
        //   $dataX.val(Math.round(e.x));
        //   $dataY.val(Math.round(e.y));
        //   $dataHeight.val(Math.round(e.height));
        //   $dataWidth.val(Math.round(e.width));
        //   $dataRotate.val(e.rotate);
        //   $dataScaleX.val(e.scaleX);
        //   $dataScaleY.val(e.scaleY);
        // }
      };

  $image.cropper('clear');
  
  // Tooltip
  $('[data-toggle="tooltip"]').tooltip();


  // // Cropper
  // $image.on({
  //   'build.cropper': function (e) {
  //     console.log(e.type);
  //   },
  //   'built.cropper': function (e) {
  //     console.log(e.type);
  //   },
  //   'cropstart.cropper': function (e) {
  //     console.log(e.type, e.action);
  //   },
  //   'cropmove.cropper': function (e) {
  //     console.log(e.type, e.action);
  //   },
  //   'cropend.cropper': function (e) {
  //     console.log(e.type, e.action);
  //   },
  //   'crop.cropper': function (e) {
  //     console.log(e.type, e.x, e.y, e.width, e.height, e.rotate, e.scaleX, e.scaleY);
  //   },
  //   'zoom.cropper': function (e) {
  //     console.log(e.type, e.ratio);
  //   }
  // }).cropper(options);


  // Buttons
  if (!$.isFunction(document.createElement('canvas').getContext)) {
    $('button[data-method="getCroppedCanvas"]').prop('disabled', true);
  }

  if (typeof document.createElement('cropper').style.transition === 'undefined') {
    $('button[data-method="rotate"]').prop('disabled', true);
    $('button[data-method="scale"]').prop('disabled', true);
  }


  // Methods
  $('.docs-buttons').on('click', '[data-method]', function () {
    var $this = $(this);
    var data = $this.data();
    var $target;
    var result;

    if ($this.prop('disabled') || $this.hasClass('disabled')) {
      return;
    }

    if ($image.data('cropper') && data.method) {
      data = $.extend({}, data); // Clone a new one
      $image.cropper('clear');

      if (typeof data.target !== 'undefined') {
        $target = $(data.target);

        if (typeof data.option === 'undefined') {
          try {
            data.option = JSON.parse($target.val());
          } catch (e) {
            console.log(e.message);
          }
        }
      }

      if (data.method === 'rotate') {
        $image.cropper('clear');
      }

      result = $image.cropper(data.method, data.option, data.secondOption);

      if (data.method === 'rotate') {
        // $image.cropper('crop');
        $image.cropper('clear');
      }

      switch (data.method) {
        case 'scaleX':
        case 'scaleY':
          $(this).data('option', -data.option);
          break;

        case 'getCroppedCanvas':
          if (result) {

            // Bootstrap's Modal
            $('#getCroppedCanvasModal').modal().find('.modal-body').html(result);

            if (!$download.hasClass('disabled')) {
              $download.attr('href', result.toDataURL('image/jpeg'));
            }
          }

          break;
      }

      if ($.isPlainObject(result) && $target) {
        try {
          $target.val(JSON.stringify(result));
        } catch (e) {
          console.log(e.message);
        }
      }

    }
  });


  // Keyboard
  $(document.body).on('keydown', function (e) {

    if (!$image.data('cropper') || this.scrollTop > 300) {
      return;
    }

    switch (e.which) {
      case 37:
        e.preventDefault();
        $image.cropper('move', -1, 0);
        break;

      case 38:
        e.preventDefault();
        $image.cropper('move', 0, -1);
        break;

      case 39:
        e.preventDefault();
        $image.cropper('move', 1, 0);
        break;

      case 40:
        e.preventDefault();
        $image.cropper('move', 0, 1);
        break;
    }

  });

});
