function init_ranked_table(table_id, select_id) {
    var listName = $('#'+select_id).val();
    var tb = new Tabulator('#'+table_id, {
        height:"200px",
        layout:"fitColumns",
        ajaxURL:"/ajax_get/?ln=" + listName,
        ajaxParams:{'tb':'ranked'},
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
                url: "ajax_put/?act=fromRanked",
                data: row.getData(),
                type: "post",
                success: function(resp, textStatus, xhr){
                    console.info("AJAX fromRanked: " + textStatus + ", msg = " + resp.msg);
                },
                error: function(jqXHR, textStatus, error){
                    console.error("AJAX fromRanked: " + textStatus + ", error = " + error);
                }
            })
        },
    });
    return tb;
}

function init_userwords_table(table_id, select_id) {
    var listName = $('#'+select_id).val();
    var tb = new Tabulator('#'+table_id, {
        height:"200px",
        layout:"fitColumns",
        ajaxURL:"/ajax_get?ln=" + listName,
        ajaxParams:{'tb':'userwords'},
        placeholder:"No Data Set",
        initialSort:[{column:"urank", dir:"asc"}],
        columns:[
            {title:"Word", field:"word", sorter:"string"},
            {title:"PoS", field:"p_o_s", sorter:"string"},
            {title:"URank", field:"urank", sorter:"string", width:80},
            {title:"Phrase1", field:"phrase1", sorter:"string", editor:"input"},
            {title:"Updated", field:"updated", sorter:"string"},
        ],
        cellEdited:function(cell){
            $.ajax({
                url: "ajax_put/?act=userwordsEdited",
                data: cell.getRow().getData(),
                type: "post",
                success: function(resp, textStatus, xhr){
                    console.info("AJAX cellEdited: " + textStatus + ", msg = " + resp.msg);
                },
                error: function(jqXHR, textStatus, error){
                    console.error("AJAX cellEdited: " + textStatus + ", error = " + error);
                }
            })
        },
    });
    return tb;
}

function init_table_buttons(tb, select_id, button_id, csv_button_id, json_button_id, from_json_button_id) {
    // trigger AJAX load on button click
    document.getElementById(button_id).addEventListener("click", function(){
        var listName = $('#'+select_id).val();
        tb.setData("/ajax_get?ln=" + listName);
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
        tb.setDataFromLocalFile();
        // TODO: save loaded data to server
    });
}
