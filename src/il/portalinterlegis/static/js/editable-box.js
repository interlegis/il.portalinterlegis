
      function endsWith(str, suffix) {
          return str.indexOf(suffix, str.length - suffix.length) !== -1;
      };

      function removeSuffix(str, suffix) {
          if (endsWith(str, suffix)) {
              return str.substring(0, str.length - suffix.length)
          } else {
              return str
          }
      };

// jQuery function
/*global common_content_filter:false */
jQuery(function($) {
  $('.editable-box-link').each(function() {
      $(this).prepOverlay({
          subtype: 'iframe',
          filter: '#content',
          formselector: 'form',
          config: {
              closeOnClick: true,
              mask: {
                  color: '#000000',
                  opacity: 0.8
              },
              onClose: function() {
                  location.reload();
              }
          },
      });
  });

  // Check if tiledata is available and valid
  if (typeof(tiledata) !== 'undefined') {

      // Check action
      if (tiledata.action === 'cancel' || tiledata.action === 'save') {
          // Close dialog
          window.parent.jQuery('.link-overlay').each(function() {
              try {
                  window.parent.jQuery(this).overlay({api: true}).close();
              } catch(e) { }
          });
      }
  }
  $(document).bind('loadInsideOverlay', function() {
        $('textarea.mce_editable').each(function() {
          var id = $(this).attr('id'),
              config = new TinyMCEConfig(id);
          //var config = new TinyMCEConfig($(this).attr('id'));
          delete InitializedTinyMCEInstances[id];
          config.init();
        });
    });

});