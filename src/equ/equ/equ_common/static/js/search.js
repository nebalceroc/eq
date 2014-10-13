function sortBy(sort) {
    var array = $('#results-list > .row');
    if(sort == 1)
        array.sort(sortByRecentlyAdded);
    else if(sort == 2)
        array.sort(sortByLowerPrice);
    else if(sort == 3)
        array.sort(sortByHigherPrice);
    $('#results-list').empty();
    $(array).each(function(i,a) {
        $('#results-list').append(a);
    });
}

function sortByRecentlyAdded(a,b) {
    var date_a = new Date($(a).find('.product-description-thumb .item-date').val());
    var date_b = new Date($(b).find('.product-description-thumb .item-date').val());
    return date_b - date_a;
}

function sortByLowerPrice(a,b) {
    var price_a = parseInt($(a).find('.product-price .item-price-value').text(), 10);
    var price_b = parseInt($(b).find('.product-price .item-price-value').text(), 10);
    return price_a - price_b;
}

function sortByHigherPrice(a,b) {
    var price_a = parseInt($(a).find('.product-price .item-price-value').text(), 10);
    var price_b = parseInt($(b).find('.product-price .item-price-value').text(), 10);
    return price_b - price_a;
}