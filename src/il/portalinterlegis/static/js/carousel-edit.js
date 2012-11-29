// TODO: simpificar o javascript: mover coisas para templates e scss
$(function() {
    $( "#carousel-edit-panels" ).sortable({
        update: function(event, ui) {
            var order = $(this).sortable('toArray').toString();
            $.post(location.pathname, {reorder:order});
        }
    });
    $( "#carousel-edit-panels" ).disableSelection();
    $( ".framecarousel" ).addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" )
        .find( ".framecarousel-header" )
        .addClass( "ui-widget-header ui-corner-all" )
        .prepend( "<span class='ui-icon ui-icon-minusthick'></span>")
        .end()
        .find( ".framecarousel-content" );

    $( ".framecarousel-header .ui-icon" ).click(function() {
        var answer = confirm("Quer apagar esse painel?")
        if (answer){
            var panel = $(this).parents(".framecarousel:first");
            $.post(location.pathname, {remove:panel.attr('id')});
            panel.fadeOut(300, function() {
                $(this).remove();
            });
        }
    });
	$("#carousel-add-button").button({
        icons: {primary: "ui-icon-plusthick"}
    });
});


$(function() {
    $( "#carousel-edit-panels-products-and-services" ).sortable({
        update: function(event, ui) {
            var order = $(this).sortable('toArray').toString();
            $.post(location.pathname, {reorder:order});
        }
    });
    $( "#carousel-edit-panels-products-and-services" ).disableSelection();
    $( ".framecarousel-products-and-services" ).addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" )
        .find( ".framecarousel-header-products-and-services" )
        .addClass( "ui-widget-header ui-corner-all" )
        .prepend( "<span class='ui-icon ui-icon-minusthick'></span>")
        .end()
        .find( ".framecarousel-content-products-and-services" );

    $( ".framecarousel-header-products-and-services .ui-icon" ).click(function() {
        var answer = confirm("Quer apagar esse painel?")
        if (answer){
            var panel = $(this).parents(".framecarousel-products-and-services:first");
            $.post(location.pathname, {remove:panel.attr('id')});
            panel.fadeOut(300, function() {
                $(this).remove();
            });
        }
    });
	$("#carousel-add-button-products-and-services").button({
        icons: {primary: "ui-icon-plusthick"}
    });
});
