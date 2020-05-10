function init_ranked_table(table_id, select_id, button_id, csv_button_id, json_button_id, from_json_button_id) {
    var tb = new Tabulator('#'+table_id, {
        height:"200px",
        layout:"fitColumns",
        placeholder:"No Data Set",
        initialSort:[{column:"rank", dir:"asc"}, {column:"level", dir:"asc"}],
        columns:[
            {title:"Word", field:"word", sorter:"string"},
            {title:"PoS", field:"p_o_s", sorter:"string"},
            {title:"Rank", field:"rank", sorter:"string", width:80},
            {title:"Level", field:"level", sorter:"string", hozAlign:"center", width:80},
            {title:"Updated", field:"updated", sorter:"string"},
        ],
    });

    var listName = $('#'+select_id).val();

    // trigger AJAX load on button click
    document.getElementById(button_id).addEventListener("click", function(){
        tb.setData("/ajax_get?ln=" + listName);
    });
    // trigger download of CSV file
    document.getElementById(csv_button_id).addEventListener("click", function(){
        tb.download("csv", listName + "_data.csv");
    });
    // trigger download of JSON file
    document.getElementById(json_button_id).addEventListener("click", function(){
        tb.download("json", listName + "_data.json");
    });
    // trigger load from local JSON file
    document.getElementById(from_json_button_id).addEventListener("click", function(){
        tb.setDataFromLocalFile();
        // TODO: save loaded data to server
    });

    return tb;
}
