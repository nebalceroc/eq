$(document).ready(function() {
    $('.pagination').each(function() {
        var list = $(this).parent().parent().find('#results-list').children();
        if(list.length > 10) {
            list = $(list).slice(10);
            list.attr('style','display:none;');
            
            var pages = Math.ceil(list.length / 10)+1;
            var previous = $(this).find('li:last-child');
            if(pages < 10) {
                for(var i = 1; i <= pages; i++) {
                    $(previous).before($('<li><a>'+i+'</a></li>'));
                }
            } else {
                for(var i = 1; i <= 10; i++) {
                    $(previous).before($('<li><a>'+i+'</a></li>'));
                }
            }
            if(pages > 1) {
                $(this).find('li:last-child').removeClass('disabled');
            } else if(pages === 1) {
                $(this).find('li:eq(1)').addClass('disabled');
            }
            $(this).find('li:eq(1)').addClass('active');

            $(this).delegate('li:not(.disabled) a', 'click', function() {
                var paginator = $(this).closest('.pagination');
                var list = $(paginator).parent().parent().find('#results-list').children();
                if($(this).parent().is(':first-child')) {
                    var previous = $(paginator).find('li.active').prev().find('a');
                    var first_row = $(previous).text() * 10 - 9;
                    reload_list(previous, list, first_row);
                } else if($(this).parent().is(':last-child')) {
                    var next = $(paginator).find('li.active').next().find('a');
                    var first_row = $(next).text() * 10 - 9;
                    reload_list(next, list, first_row);
                    var page = parseInt($(paginator).find('li.active').text(), 10);
                    if(page% 10 === 0) {
                        var links = $(paginator).find('li:nth-child(n+1) a');
                        for(var i = page+1; i <= page+10; i++) {
                            if(!$(links[i]).parent().is(':last-child')) {
                                (links[i]).text(i);
                            }
                        }
                    }
                } else {
                    if(!$(this).parent().hasClass('active')) {
                        // Get first row index
                        var first_row = $(this).text() * 10 - 9;
                        reload_list(this, list, first_row);
                    }
                }
            });
        } else {
            $('.pagination').attr('style', 'display:none;');
        }
    });
});

function reload_list(elem, list, first_row) {
    // Hide all rows
    $(list).attr('style', 'display:none;');
    // Select rows from first to the end and select subarray until 10 rows
    var selected = $(list).slice(first_row-1);
    // Show the rows selected
    $(selected).removeAttr('style');
    // Select the active link
    var active = $(elem).closest('.pagination').find('li.active');
    // Remove active class to active link since it is no longer the active link
    $(active).removeClass('active');
    // Check if the active link is the first numbered to remove disabled from previous link
    // If the active is the last numbered, remove disabled from the next link
    if($(active).is(':nth-child(2)')) {
        $(elem).closest('.pagination').find('li:first-child').removeClass('disabled');
    } else if($(active).next().is($(elem).closest('.pagination').find('li:last-child'))) {
        $(elem).closest('.pagination').find('li:last-child').removeClass('disabled');
    }
    // Add active class to clicked link
    $(elem).parent().addClass('active');
    // Re-disable previous or next link according to clicked link index
    if($(elem).parent().next().is($(elem).closest('.pagination').find('li:last-child'))) {
        $(elem).closest('.pagination').find('li:last-child').addClass('disabled');
    } else if($('.pagination li:first-child').next().is($(elem).parent())) {
        $(elem).closest('.pagination').find('li:first-child').addClass('disabled');
    }
}