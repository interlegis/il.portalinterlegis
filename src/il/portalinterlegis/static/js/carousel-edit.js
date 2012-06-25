// TODO: simpificar o javascript: mover coisas para templates e scss
$(function() {
    $( "#carousel-edit-panels" ).sortable({
        update: function(event, ui) {
            var order = $(this).sortable('toArray').toString();
            $.post('edit-carousel', {reorder:order});
        }
    });
    $( "#carousel-edit-panels" ).disableSelection();
    $( ".portlet" ).addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" )
        .find( ".portlet-header" )
        .addClass( "ui-widget-header ui-corner-all" )
        .prepend( "<span class='ui-icon ui-icon-minusthick'></span>")
        .end()
        .find( ".portlet-content" );

    $( ".portlet-header .ui-icon" ).click(function() {
        var answer = confirm("Quer apagar esse painel?")
        if (answer){
            var panel = $(this).parents(".portlet:first");
            $.post('edit-carousel', {remove:panel.attr('id')});
            panel.fadeOut(300, function() {
                $(this).remove();
            });
        }
    });
	$("#carousel-add-button").button({
        icons: {primary: "ui-icon-plusthick"}
    });
});
