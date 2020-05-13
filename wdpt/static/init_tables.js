var ajaxCount = 0;

function on_ajax_success(msg) {
    console.info(msg);
    $('#ajax-response').html("[" + ++ajaxCount + "] AJAX " + msg);
}

function on_ajax_error(msg) {
    console.error(msg);
    $('#ajax-response').html("[" + ++ajaxCount + "] AJAX " + msg);
}

function init_ranked_table(table_id, select_id) {
    var listName = $('#'+select_id).val();
    var tb = new Tabulator('#'+table_id, {
        height:"200px",
        layout:"fitColumns",
        ajaxURLGenerator:function(url, config, params){
            var paramsStr = Object.keys(params).map(function (key) {
                return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
            }).join('&');
            var listName = $('#'+select_id).val();
            return "/ajax/get/ranked/?ln=" + listName + "&" + paramsStr;
        },
        //ajaxProgressiveLoad:"scroll",
        placeholder:"No Data Set",
        initialSort:[{column:"rank", dir:"asc"}, {column:"level", dir:"asc"}],
        columns:[
            {title:"Word", field:"word", sorter:"string"},
            {title:"PoS", field:"p_o_s", sorter:"string"},
            {title:"Rank", field:"rank", sorter:"string", width:80},
            {title:"Level", field:"level", sorter:"string", hozAlign:"center", width:80},
            {title:"Known", field:"known", width:90, hozAlign:"center", formatter:"tickCross", sorter:"boolean"},
            {title:"Updated", field:"updated", sorter:"string"},
        ],
        rowDblClick:function(e, row){
            $.ajax({
                url: "ajax/put/ranked/clicked/",
                data: row.getData(),
                type: "post",
                success: function(resp, textStatus, xhr){
                    on_ajax_success("ranked-clicked: " + textStatus + ", msg = " + resp.msg);
                    reload_tables("ranked-clicked");
                },
                error: function(jqXHR, textStatus, error){
                    on_ajax_error("ranked-clicked: " + textStatus + ", error = " + error);
                }
            })
        },
    });
    $('#'+select_id).change(function() {
        tb.setData(); // reload data from ajaxURL
    });
    return tb;
}

function init_userwords_table(table_id, select_id) {
    var listName = $('#'+select_id).val();
    var tb = new Tabulator('#'+table_id, {
        height:"200px",
        layout:"fitColumns",
        ajaxURLGenerator:function(url, config, params){
            var paramsStr = Object.keys(params).map(function (key) {
                return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
            }).join('&');
            var listName = $('#'+select_id).val();
            return "/ajax/get/userwords/?ln=" + listName + "&" + paramsStr;
        },
        placeholder:"No Data Set",
        initialSort:[{column:"urank", dir:"asc"}],
        columns:[
            {title:"Word", field:"word", sorter:"string"},
            {title:"PoS", field:"p_o_s", sorter:"string"},
            {title:"URank", field:"urank", sorter:"string", width:80},
            {title:"Phrase1", field:"phrase1", sorter:"string", editor:"input"},
            {title:"Updated", field:"updated", sorter:"string"},
        ],
        rowDblClick:function(e, row){
            $.ajax({
                url: "ajax/put/userwords/clicked/",
                data: row.getData(),
                type: "post",
                success: function(resp, textStatus, xhr){
                    on_ajax_success("userwords-clicked: " + textStatus + ", msg = " + resp.msg);
                    reload_tables("userwords-clicked");
                },
                error: function(jqXHR, textStatus, error){
                    on_ajax_error("userwords-clicked: " + textStatus + ", error = " + error);
                }
            })
        },
        cellEdited:function(cell){
            $.ajax({
                url: "ajax/put/userwords/edited/",
                data: cell.getRow().getData(),
                type: "post",
                success: function(resp, textStatus, xhr){
                    on_ajax_success("cellEdited: " + textStatus + ", msg = " + resp.msg);
                },
                error: function(jqXHR, textStatus, error){
                    on_ajax_error("cellEdited: " + textStatus + ", error = " + error);
                }
            })
        },
    });
    $('#'+select_id).change(function() {
        tb.setData(); // reload data from ajaxURL
    });
    return tb;
}

function init_table_buttons(tb, select_id, button_id, csv_button_id, json_button_id, from_json_button_id) {
    // trigger AJAX load on button click
    document.getElementById(button_id).addEventListener("click", function(){
        tb.setData(); // reload data from ajaxURL
    });
    // trigger download of CSV file
    document.getElementById(csv_button_id).addEventListener("click", function(){
        var listName = $('#'+select_id).val();
        tb.download("csv", listName + "_data.csv");
    });
    // trigger download of JSON file
    document.getElementById(json_button_id).addEventListener("click", function(){
        var listName = $('#'+select_id).val();
        tb.download("json", listName + "_data.json");
    });
    // trigger load from local JSON file
    document.getElementById(from_json_button_id).addEventListener("click", function(){
        tb.setDataFromLocalFile().then(function() {
            // save loaded data to server
            var listName = $('#'+select_id).val();
            $.ajax({
                url: "ajax/put/ranked/import/?ln=" + listName,  // TODO: ranked => ranked/userwords
                data: JSON.stringify(tb.getData()),
                dataType: 'json',
                type: "post",
                success: function(resp, textStatus, xhr){
                    on_ajax_success("ranked-import: " + textStatus + ", msg = " + resp.msg);
                },
                error: function(jqXHR, textStatus, error){
                    on_ajax_error("ranked-import: " + textStatus + ", error = " + error);
                }
            })
        })
    });
}
