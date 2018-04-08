function save_info(role) {
    var id_str = '#input_'+role;
    var name = $(id_str).val();
    $(id_str).val('');
    id_str = id_str+'Addr';
    var addr = $(id_str).val();
    $(id_str).val('');
    var num_of_cards = $(`#${role}_info`).parent().find('.btn.btn-danger').length;
    $.get(`/add_info/?role=${role}&roleName=${name}&roleAddr=${addr}&num_of_info=${num_of_cards}`, function(ret_value){
        var card_html = ret_value;
        $(card_html).insertBefore(`#${role}_info`);
        var button = $(`#${role}_info`).prev().find('button');
        button.click(delete_an_info);
    });
}


function delete_all_info() {
    $('div .row .col-sm-4 .card.border-primary').each(function(){
        if ($(this).attr('id') == undefined) {
            $(this).remove();
        }
    })
}

function delete_an_info() {
    console.log('xxxx')
    var card_number = parseInt($(this).prev().html().replace('#', '')) - 1;
    var all_info_cards = $(this).parent().parent().parent().find('.card.border-primary');
    $(this).parent().parent().remove();
    for (var idx=card_number; idx < all_info_cards.length; idx++) {
        var this_card = all_info_cards.eq(idx)
        if (this_card.attr('id') == undefined) {
            this_card.find('span').html('#'+(idx));
        }
    }
}

function clear_content() {
    $('#content').val('');
}

function generate_pdf() {
    console.log('generate')
    var all_info_text = $('div .row .card.border-primary .card-text');
    var senders = [];
    var senders_addr = [];
    var receivers = [];
    var receivers_addr = [];
    var ccs = [];
    var ccs_addr = [];
    for (var idx=0; idx < all_info_text.length; idx+=6) {
        var this_sender = all_info_text.eq(idx).html();
        console.log(this_sender)
        var this_sender_addr = all_info_text.eq(idx+1).html();
        console.log(this_sender_addr)
        var this_receiver = all_info_text.eq(idx+2).html();
        console.log(this_receiver)
        var this_receiver_addr = all_info_text.eq(idx+3).html();
        console.log(this_receiver_addr)
        var this_cc = all_info_text.eq(idx+4).html();
        console.log(this_cc)
        var this_cc_addr = all_info_text.eq(idx+5).html();
        console.log(this_cc_addr)
    }
}