function save_info() {
    console.log('save info');
    var card_html = undefined;
    $.get('/add_info/?sender=王大明', function(ret_value){
        card_html = ret_value;
        console.log(card_html);
    });
    $('#card_add_info').insertBefore(card_html);
}