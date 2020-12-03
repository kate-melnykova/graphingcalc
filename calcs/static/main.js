$(document).ready(function() {
    window.counter = 1;
    window.template = Handlebars.compile($("#element-template").text());
    
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

    $('#add_line').click(function (e){
        e.preventDefault();
        $("div#line_forms").append(window.template({count: window.counter++}));
        console.log('Added a new form line_' + window.counter);
        return false
    });

    $(document).on("click", ".remove", function (e)
    {
        e.preventDefault();
        var elementId = $(this).data('element-id');
        $(`#${elementId}`).remove();
        return false
    })


    $('form#graph').submit(function (e) {
        var queryString = $(this).serialize();
        $('#graph-container').empty();
        $('<img>', {src:"http://0.0.0.0:5000/graph_request?"+queryString}).appendTo('#graph-container');

        e.preventDefault();
    });

    $('#plot').click(function (e){
        e.preventDefault();
        alert('!')
        // collect the data across forms
        // add info about axes
        // send post request with all the data
        var that = $(this);
        var temp = $("#graph").serializeArray();

        var lines = new Array();
        $(".graph-form").each(function(index){
            var lineData = $(this)
            lines.push($(this).serializeArray());
        });
        var data = {
            axesData: axesData,
            lines: lines
        }
        // make POST request with `formsData` encoded as JSON
        var data = JSON.stringify(data);
        /*
        $.ajax({
            type: 'POST',
            url: that.attr('action'),
            data: data
        })

            .done(function (filename) {
                $('#graph-container').empty();
                $('<img>', {src:"http://0.0.0.0:5000/figure?"+filename}).appendTo('#graph-container');
            })

            .fail(function (jqXHR, data, arg3) {
                $('#result').html(jqXHR.responseJSON.error);
                console.log(data);
                console.log(arg3);
            });

         */
        return false
    });

    window.add_line_form_template = '<span id="line_">\n' +
        '<form class="form" id="line_">\n' +
        '    <p>\n' +
        '        <label for="expression">f(x)=</label>\n' +
        '        <input id="expression" name="expression" style="width:80%;" type="text" value="">\n' +
        '    </p>\n' +
        '    <p>\n' +
        '        <label for="xmin">From x=</label>\n' +
        '        <input id="xmin" name="xmin" type="text" value="">\n' +
        '        <label for="xmax">To x=</label>\n' +
        '        <input id="xmax" name="xmax" type="text" value="">\n' +
        '    </p>\n' +
        '    <p>\n' +
        '        <label for="label">Label</label>\n' +
        '        <input id="label" name="label" type="text" value="">\n' +
        '        <label for="include_in_legend">Include in legend</label>\n' +
        '        <input checked id="include_in_legend" name="include_in_legend" type="checkbox" value="y">\n' +
        '    </p>\n' +
        '    <p>\n' +
        '        <label for="linecolor">Line color</label>\n' +
        '        <select id="linecolor" name="linecolor">\n' +
        '            <option value="b">Blue</option>\n' +
        '            <option value="g">Green</option>\n' +
        '            <option value="r">Red</option>\n' +
        '            <option value="c">Cyan</option>\n' +
        '            <option value="m">Magenta</option>\n' +
        '            <option value="y">Yellow</option>\n' +
        '            <option value="k">Black</option>\n' +
        '            <option value="w">White</option>\n' +
        '        </select>\n' +
        '        <label for="linewidth">Line width</label>\n' +
        '        <input id="linewidth" name="linewidth" type="text" value="2.0">\n' +
        '        <label for="linestyle">Line style</label>\n' +
        '        <select id="linestyle" name="linestyle">\n' +
        '            <option selected value="-">Solid</option>\n' +
        '            <option value="--">Dashed</option>\n' +
        '            <option value="-.">Dashed-dot</option>\n' +
        '            <option value=".">Dotted</option>\n' +
        '        </select>\n' +
        '    </p>\n' +
        '    <p>\n' +
        '        <label for="scatterplot">Scatterplot?</label>\n' +
        '        <input id="scatterplot" name="scatterplot" type="checkbox" value="y">\n' +
        '        <label for="n_points">Number of points</label>\n' +
        '        <input id="n_points" name="n_points" type="text" value="1000">\n' +
        '    </p>\n' +
        '    <p>\n' +
        '        <label for="noise">Noise level in %</label>\n' +
        '        <!--\n' +
        '        <input id="rangeInput" type="range" min="0" max="200" oninput="amount.value=rangeInput.value" />\n' +
        '        <input id="amount" type="number" value="100" min="0" max="200" oninput="rangeInput.value=amount.value" />\n' +
        '        <output for="age" id="selected-age"> form.age.data </output>\n' +
        '        form.noise1_number()\n' +
        '        -->\n' +
        '        <input id="noise" max="100" min="0" name="noise1" step="5" style="text-width:80%" type="range" value="0">\n' +
        '    </p>\n' +
        '<br>\n' +
        '    <button value=\'line_\' onclick="delete_line(this.value)">Delete line</button>\n' +
        '</form>\n' +
        '</span>'
});