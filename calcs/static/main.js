$(document).ready(function() {
    window.counter = 0;
    window.template = Handlebars.compile($("#element-template").text());
    
    $('form#calc').submit(function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
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
        return false
    });

    $('#add_line').click(function (e){
        e.preventDefault();
        e.stopImmediatePropagation();
        $("div#line_forms").append(window.template({count: window.counter++}));
        console.log('Added a new form line_' + window.counter);
        return false
    });

    $(document).on("click", ".remove", function (e)
    {
        e.preventDefault();
        e.stopImmediatePropagation();
        var elementId = $(this).data('element-id');
        $(`#${elementId}`).remove();
        return false
    })


    $('form#graph').submit(function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var queryString = $(this).serialize();
        $('#graph-container').empty();
        $('<img>', {src:"http://0.0.0.0:5000/graph_request?"+queryString}).appendTo('#graph-container');

        return false
    });

    $('#plot').click(function (e){
        e.preventDefault();
        e.stopImmediatePropagation();
        var that = $(this);
        var axesData = {};
        var value;
        for (value of $("#graph").serializeArray()) {
            axesData[value.name] = value.value;
        };
        for (value in axesData){
            console.log(value, axesData[value]);
        }
        console.log(axesData);
        var lines = new Array();
        $(".graph-form").each(function(index){
            var temp = {};
            for (value of $(this).serializeArray()) {
                temp[value.name] = value.value;
            };
            lines.push(temp);
        });
        var data = {
            axesData: axesData,
            lines: lines
        }
        // make POST request with `formsData` encoded as JSON
        var data = JSON.stringify(data);

        $.ajax({
            type: 'POST',
            url: 'http://0.0.0.0:5000/graph_request',
            dataType: "text",
            contentType: "application/json",
            data: data
        })

            .done(function (image_base64) {
                alert('Receieved image');
                var image = new Image();
                image.src = 'data:image/png;base64,' + image_base64;
                $('#graph-container').empty();
                $('#graph-container').append(image);
            })

            .fail(function (jqXHR, textStatus, errorThrown) {
                alert(`Did not recieve file`)
                //$('#result').html(jqXHR.responseJSON.error);
                console.log(textStatus);
                console.log(errorThrown);
            });
        return false
    });


});