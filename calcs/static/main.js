
$(document).ready(function() {
    window.counter = 1;
    
    $('form#calc').submit(function (e) {
        var that = $(this);
        $.ajax({
            type: 'POST',
            url: that.attr('action'),
            data: that.serialize()
        })

            .done(function (data) {
                $('#result').html(data.expression + ' = ' + data.val);
                window.sessionStorage.setItem(window.counter, data.expression + ' = ' + data.val);
                if (window.counter > 10) {
                    sessionStorage.removeItem(window.counter - 10);
                }

                $('#container').empty();
                _.each(Object.keys(sessionStorage).map(Number).sort(function(a, b){return b-a}),
                    function (i) {
                        $('<div>', {
                            class: 'item',
                            text: sessionStorage.getItem(i)
                        }).appendTo($('#container'))
                    }
                )
                
                window.counter += 1;
            })

            .fail(function (jqXHR, data, arg3) {
                $('#result').html(jqXHR.responseJSON.error);
                console.log(data);
                console.log(arg3);
            });

        e.preventDefault();
    });


    $('form#graph').submit(function (e) {
        var queryString = $(this).serialize();
        $('#graph-container').empty();
        $('<img>', {src:"http://0.0.0.0:5000/graph_request?"+queryString}).appendTo('#graph-container');

        e.preventDefault();
    });

});