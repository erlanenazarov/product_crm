/**
 * Created by erlan on 1/5/17.
 */

//notUrl

function getNotification() {
    $.ajax({
        url: notUrl,
        method: 'POST',
        data: {'csrf_token': token},
        dataType: 'JSON',
        success: function (response) {

        }
    })
}