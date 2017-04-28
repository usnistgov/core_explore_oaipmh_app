var timeout_oaipmh = null;

/*
* Waits for Jquery to be ready
* */
var defer_loadListProviderOaiPmh = function(){
    $(document).ready(function() {
        $('#error-div-oaipmh').hide();
        loadListProviderOaiPmh();
    })
};

// Waiting JQuery
onjQueryReady(defer_loadListProviderOaiPmh);

/*
* Loads provider's list from oaipmh search
* */
loadListProviderOaiPmh = function() {
    $('#error-div-oaipmh').hide();
    var query_id = $("#query_id").html();
    $.ajax({
        url: getDataSourceOaiPmhUrl,
        type : "GET",
        data: {
            id_query: query_id
        },
        success: function(data){
            // Displays oaipmh search's data sources
            $("#list-data-sources-oaipmh-content").html(data);
            // Adds action on each oaipmh search's checkbox
            $("input.checkbox-oaipmh:checkbox").on("click",
                                                   {id_query: query_id},
                                                   updateQueryDataSourcesOaiPmhTimeout);
        },
        error: function(data){
            if (data.responseText != ""){
                showErrorMessageOaiPmh(data.responseText);
            }else{
                return true;
            }
        }
    });
};

/*
* Updates the timeout and updates query data sources when done.
* */
updateQueryDataSourcesOaiPmhTimeout = function(event){
    // Clears timeout
    if(timeout_oaipmh) {
        clearTimeout(timeout_oaipmh);
    }
    // Starts timeout
    timeout_oaipmh = setTimeout(updateQueryDataSourcesOaiPmh(event), 500);
};

/*
* AJAX: Updates query data sources
* */
updateQueryDataSourcesOaiPmh = function(event){
    $.ajax({
        url: updateQueryDataSourcesOaiPmhUrl,
        type : "GET",
        data: {
            'id_query': event.data.id_query,
            'id_instance': event.target.value,
            'to_be_added': event.target.checked
        },
        success: function(data){
        },
        error: function(data){
            if (data.responseText != ""){
                showErrorMessageOaiPmh(data.responseText);
            }else{
                return (true);
            }
        }
    });
};

/*
* Shows label error with message
* */
showErrorMessageOaiPmh = function(message){
    $('#error-div-oaipmh').show();
    $('#error-message').text(message);
};