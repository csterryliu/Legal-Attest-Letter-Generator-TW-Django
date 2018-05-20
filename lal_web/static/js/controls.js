function save_info(thisObj, role) {
    var id_str = '#input_'+role;
    var name = $(id_str).val();
    id_str = id_str+'Addr';
    var addr = $(id_str).val();

    if ($(thisObj).data('is_edit') == true) {
        var card_num = $(thisObj).data('edit_card_num');
        var card_to_be_edited = $(`#${role}_info`).parent().find('div.card.border-primary').eq(card_num - 1);
        card_to_be_edited.find('.card-text.text-dark').eq(0).html(name);
        card_to_be_edited.find('.card-text.text-dark').eq(1).html(addr);
        var card_num = $(thisObj).removeData('edit_card_num');
        return;
    }

    var num_of_cards = $(`#${role}_info`).parent().find('.btn.btn-danger').length;
    var post_data = {
        'role': role,
        'roleName': name,
        'roleAddr': addr,
        'num_of_info': num_of_cards
    };
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
    
    $.ajax({
        type: 'POST',
        url: '/add_info/',
        data: post_data,
        dataType: 'html',
        contentType: 'application/x-www-form-urlencoded; charset=utf-8',
        timeout: 30000
    }).done(function(data) {
        var card_html = data;
        $(card_html).insertBefore(`#${role}_info`);
        var modify_button = $(`#${role}_info`).prev().find('button.btn.btn-primary');
        modify_button.click(retrieve_info_text);
        var del_button = $(`#${role}_info`).prev().find('button.btn.btn-danger');
        del_button.click(delete_an_info);
    }).fail(function() {
        alert('失敗！請重試，或回報為 bug，謝謝。');
    });
}


function delete_all_info() {
    $('div .row .col-sm-4 .card.border-primary').each(function(){
        if ($(this).attr('id') == undefined) {
            $(this).remove();
        }
    })
}

function retrieve_info_text() {
    var info_text = $(this).parent().next().find('.card-text');
    var name = info_text.eq(0).html();
    var addr = info_text.eq(1).html();
    var num_of_this_card = $(this).prev().html().replace('#', '');
    var role = $(this).data('target').split('_')[1];
    $(`#input_${role}`).val(name);
    $(`#input_${role}Addr`).val(addr);
    $(`#add_${role}_modal .modal-footer button.btn-primary`).data('is_edit', true);
    $(`#add_${role}_modal .modal-footer button.btn-primary`).data('edit_card_num', num_of_this_card);
}

function delete_an_info() {
    var card_number = parseInt($(this).prev().prev().html().replace('#', '')) - 1;
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

function reset_form(role) {
    var id_str = '#input_'+role;
    var name = $(id_str).val();
    $(id_str).val('');
    id_str = id_str+'Addr';
    var addr = $(id_str).val();
    $(id_str).val('');
    $(`#add_${role}_modal .modal-footer button.btn-primary`).data('is_edit', false);
}

function generate_pdf() {
    function collect_info(type, cards) {
        cards.each(function() {
            if ($(this).attr('id') == undefined) {
                var info_text = $(this).find('.card-text');
                post_data[type].push([info_text.eq(0).html()]);
                post_data[`${type}_addr`].push(info_text.eq(1).html());
            }
        })
    }

    // show loading icon
    $('div .card.border-dark .card-footer .loader').show()
    // disable button
    $('div .card.border-dark .card-footer button').prop('disabled', true)

    var post_data = {
        'senders': [],
        'senders_addr': [],
        'receivers': [],
        'receivers_addr': [],
        'ccs': [],
        'ccs_addr': [],
        'content': ''
    };

    var all_sender_cards = $('#sender_info').parent().find('.card');
    var all_receiver_cards = $('#receiver_info').parent().find('.card');
    var all_cc_cards = $('#cc_info').parent().find('.card');
    post_data['content'] = $('#content').val();

    collect_info('senders', all_sender_cards);
    collect_info('receivers', all_receiver_cards);
    collect_info('ccs', all_cc_cards);

    var csrf_token = getCookie('csrftoken');

    var post_request = new XMLHttpRequest();
    post_request.open('POST', '/generate/');
    post_request.responseType = 'blob';
    post_request.timeout = 30000;

    post_request.onload = function (event) {
        if (this.status == 200) {
            var d = new Date();
            var filename_date = d.getFullYear() + '-' + 
                (d.getMonth()+1) + '-' + d.getDate() +
                '-' + d.getHours() + '-' + d.getMinutes() + '-' +
                d.getSeconds() + '-' + d.getMilliseconds();
            var pdf_blob = new Blob([this.response], {type: 'application/pdf'});
            var link = document.createElement('a');
            var url = window.URL.createObjectURL(pdf_blob);
            link.href = url;
            link.download = `lal_${filename_date}.pdf`;
            document.body.appendChild(link);
            link.click();
            setTimeout(function(){
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);  
            }, 100);  
        } else {
            alert('失敗！請重試，或回報為 bug，謝謝。');
        }
        // hide loading icon
        $('div .card.border-dark .card-footer .loader').hide()
        // disable button
        $('div .card.border-dark .card-footer button').prop('disabled', false)
    };

    post_request.ontimeout = function (event) {
        alert('連線逾時，請重試。');
    }

    post_request.setRequestHeader('Content-Type', 'application/json; charset=utf-8');
    post_request.setRequestHeader('X-CSRFToken', csrf_token);
    post_request.send(JSON.stringify(post_data));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}