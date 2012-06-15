
function unifyHeights(sel) {
    var max = 0;
    children = $(sel).children('.dt-cell').children()
    children.each(function(){
        var height = $(this).height();
        if ( height > max ) { max = height; }
    });
    children.css('height', max);
}

// Unifies heights of the cells of each dotted row.
// This is important for their borders to be continuous
function unifyHeightsOfDottedCells(document) {
    $(document).ready(function(){
        $(".dt-row").each(function(){
            unifyHeights($(this))
        });
    });
}

