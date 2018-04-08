function save_info() {
    console.log('save info');
    var sender = $('#input_sender').val();
    $('#input_sender').val('');
    var sender_addr = $('#input_senderAddr').val();
    $('#input_senderAddr').val('');
    var receiver = $('#input_receiver').val();
    $('#input_receiver').val('');
    var receiver_addr = $('#input_receiverAddr').val();
    $('#input_receiverAddr').val('');
    var cc = $('#input_cc').val();
    $('#input_cc').val('');
    var cc_addr = $('#input_ccAddr').val();
    $('#input_ccAddr').val('');
    var num_of_cards = $('div .row .card.border-primary .btn.btn-danger').length;
    console.log(num_of_cards);
    $.get(`/add_info/?sender=${sender}&senderAddr=${sender_addr}&receiver=${receiver}&receiverAddr=${receiver_addr}&cc=${cc}&ccAddr=${cc_addr}&num_of_info=${num_of_cards}`, function(ret_value){
        var card_html = ret_value;
        $(card_html).insertBefore('#card_add_info');
    });
}


function delete_all_info() {
    var all_info_cards = $('div .row .col-sm-4');
    if (all_info_cards.length > 1) {
        for (var idx = 0; idx < all_info_cards.length-1; idx++) {
            all_info_cards.eq(idx).remove();
        }
    }
}