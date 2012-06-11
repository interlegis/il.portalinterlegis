// jQuery function
/*global common_content_filter:false */
jQuery(function($) {
  $('.editable-box').each(function() {
      var id = $(this).attr('id');
      var current = window.location;
      var edithref = current + '/box_' + id;
      $('<a class="editable-box-link" href="' + edithref + '"><img src="pencil_icon.png" width="16" height="16" alt="Edite esta caixa"/></a>')
        .appendTo($(this))
        .prepOverlay({
            subtype: 'ajax',
            filter: '#content',
            formselector: 'form',
            config: {
              closeOnClick: false,
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