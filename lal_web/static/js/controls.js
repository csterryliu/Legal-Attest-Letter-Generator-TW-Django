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
    function collect_info(cards) {
        cards.each(function() {
            if ($(this).attr('id') == undefined) {
                console.log($(this).find('.card-text').eq(0).html())
                console.log($(this).find('.card-text').eq(1).html())
            }
        })
    }



    var senders = [];
    var senders_addr = [];
    var receivers = [];
    var receivers_addr = [];
    var ccs = [];
    var ccs_addr = [];

    var all_sender_cards = $('#sender_info').parent().find('.card');
    var all_receiver_cards = $('#receiver_info').parent().find('.card');
    var all_cc_cards = $('#cc_info').parent().find('.card');

    collect_info(all_sender_cards);
    collect_info(all_receiver_cards);
    collect_info(all_cc_cards);
    
}