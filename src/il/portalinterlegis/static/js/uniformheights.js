function unifyHeights(row_sel, cell_sel) {
    $(row_sel).each(function(){
        var max = 0;
        children = $(this).children(cell_sel).children()
        children.each(function(){
            var height = $(this).height();
            if ( height > max ) { max = height; }
        });
        children.css('height', max);
    });
};

// Unifies heights of the cells of each dotted row.
// This is important for their borders to be continuous
// (This operation should happen generally after DOM manipulations)
$(function() {
    $(document).ready(function(){
        unifyHeights('.dt-row', '.dt-cell')
        unifyHeights('.row', '.cell')
    });
});
