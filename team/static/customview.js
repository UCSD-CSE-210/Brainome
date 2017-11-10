var trace_3d, layout_3d;
var updates_3d = []
var groups_3d = []

function loadClusterPlots() {
    var grouping = $('#tsneGrouping option:selected').val();
    $.ajax({
        type: "GET",
        url: './plot/cluster/' + species + '/' + grouping,
        success: function(data) {
            Plotly.newPlot("plot-2d-cluster", Object.values(data["traces_2d"]), data["layout2d"]);
            $('#loading_2dtsne').html("");
            if("traces_3d" in data){
                if($('#toggle-3d').prop('checked')) {
                    Plotly.newPlot("plot-3d-cluster", Object.values(data["traces_3d"]), data["layout3d"]);
                    save3DData(data["traces_3d"],data["layout3d"]);
                }
                else {
                    save3DData(data["traces_3d"], data["layout3d"]);
                    $('#toggle-3d').bootstrapToggle('enable');
                }
            }
            else {
                save3DData(null, null);
            }
        }
    });   
}

function initGeneNameSearch() {
    geneNameSelector = $('#geneName').select2({
        placeholder: 'Search..',
        allowClear: true,
        ajax: {
            url: './gene/names/' + species,
            dataType: 'json',
            delay: 500,
            data: function(params) {
                return {
                    q: params.term
                };
            },
            processResults: function(data) {
                geneSearchCache = data;
                return {
                    results: $.map(data, function(gene) {
                        return {
                            text: gene.geneName,

                            id: gene.geneID
                        }
                    })
                }
            },
            cache: true
        },
        minimumInputLength: 1
    });

    // Initialise selector
//    if (typeof(Storage) !== 'undefined') {
//        var defaultGene = localStorage.getItem('lastViewed');
//        if (defaultGene == null) {
//            defaultGene = 'Gad2'; // No entry, set default to Gad2.
//        }
//    } else {
//        // Browser has no localStorage support, we'll just do Gad2.
//        var defaultGene = 'Gad2';
//    }

    var defaultGene = 'Gad2';

    $.getJSON({
        url: './gene/names/' + species + '?q=' + defaultGene,
        success: function(data) {
            data.forEach(function(gene) {
                var option = new Option(gene.geneName, gene.geneID, true, true);
                geneNameSelector.append(option);
                $('#epiBrowserLink').attr('href', generateBrowserURL(gene));
                $('#epiBrowserLink').removeClass('disabled');
            });
            updateGeneElements();
            updateDataTable();
        }
    });
}

function updateMCHClusterPlot() {
    var levelType = $('input[name=levels]').filter(':checked').val();
    var geneSelected = $('#geneName option:selected').val();
    var pValues = pSlider.getValue();
    if (geneSelected != 'Select..') {
        $.ajax({
            type: "GET",
            url: './plot/mch/' + species + '/' + geneSelected + '/' + levelType + '/' + pValues[0] + '/' + pValues[1],
            success: function(data) {
                $('#plot-mch-scatter').html("");
                $('#plot-mch-scatter').html(data);
            }
        });
    }
}


function updateMCHBoxPlot() {
    var levelType = $('input[name=levels]').filter(':checked').val();
    var geneSelected = $('#geneName option:selected').val();
    if ($('#orthologsToggle').prop('checked')) {
        return updateMCHCombinedBoxPlot(mmu_gID, hsa_gID);
    }
    if ($('#outlierToggle').prop('checked')) {
        var outlierOption = 'outliers';
    } else {
        var outlierOption = 'false';
    }
    $.ajax({
        type: "GET",
        url: './plot/box/' + species + '/' + geneSelected + '/' + levelType + '/' + outlierOption,
        success: function(data) {
            $('#plot-mch-box').html(data);
        }
    });

}

function updateMCHCombinedBoxPlot(mmu_gid, hsa_gid) {
    var levelType = $('input[name=levels]').filter(':checked').val();
    if ($('#outlierToggle').prop('checked')) {
        var outlierOption = 'outliers';
    } else {
        var outlierOption = 'false';
    }
    $.ajax({
        type: "GET",
        url: './plot/box_combined/' + species + '/' + mmu_gid + '/' + hsa_gid + '/' + levelType + '/' + outlierOption,
        success: function(data) {
            $('#plot-mch-box').html(data);
        }
    });
}

function updateGeneElements() {
    var geneSelected = $('#geneName option:selected').val();
    console.log(geneSelected);
    console.log($("#geneName").select2('data'));
    if (geneSelected != 'Select..') {
        if (typeof(Storage) !== 'undefined') {
            localStorage.setItem('lastViewed', $('#geneName option:selected').text());
        }
        if($("#geneName").select2('data').length == 1){
            updateMCHClusterPlot();
        }
        else if($("#geneName").select2('data').length > 1) {
            createHeatMap();
        }
        updateOrthologToggle();
        updateMCHBoxPlot();
        try {
            var annojURL;
            geneSearchCache.forEach(function(gene) {
                if (gene.geneID == geneSelected) {
                    annojURL = generateBrowserURL(gene);
                }
            });
            $('#epiBrowserLink').attr('href', annojURL);
        } catch (e) {}

    }
}

function generateBrowserURL(gene) {
    if (species == 'mmu') {
        var base = 'http://brainome.ucsd.edu/annoj/CEMBA/index_mm.html'; // Mouse
    } else {
        var base = 'http://brainome.ucsd.edu/annoj/sc_wgbs/index_hs.html'; // Human
    }

    if (gene.strand == '+') {
        var position = gene.start;
    } else {
        var position = gene.end;
    }
    return base + '?assembly=' + gene.chrom + '&position=' + position;
}

function updateOrthologToggle() {
    var geneSelected = $('#geneName option:selected').val();
    
    $.ajax({
        type: "GET",
        url: './gene/orthologs/' + species + '/' + geneSelected,
        success: function(data) {
            if (data.mmu_gID == null || data.hsa_gID == null) {
                $('#orthologsToggle').bootstrapToggle('off');
                $('#orthologsToggle').bootstrapToggle('disable');
            } else {
                mmu_gID = data.mmu_gID;
                hsa_gID = data.hsa_gID;
                $('#orthologsToggle').bootstrapToggle('enable');
                if ($('#orthologsToggle').prop('checked')) {
                    return updateMCHCombinedBoxPlot(mmu_gID, hsa_gID);
                }
            }
        }
    });
}

function save3DData(trace, layout){
    trace_3d = trace;
    layout_3d = layout;
}

function display3DPlotToggle() {
    if ($('#toggle-3d').prop('checked')){
        $('#loading-3d-plot').html("loading..");
        Plotly.newPlot("plot-3d-cluster", Object.values(trace_3d), layout_3d);
        if($('#tsneGrouping option:selected').val() == 'biosample'){
            for(i = 0; i < groups_3d.length; i++){
                Plotly.restyle("plot-3d-cluster", updates_3d[i], groups_3d[i]);
            }
        }
        $('#loading-3d-plot').html("");
    }
    else {
        Plotly.purge("plot-3d-cluster");
    }
}

function initDataTableClick() {
    $('#geneTable tbody').on('click', 'tr', function () {
        var id = $(this).attr('id');
        $.getJSON({
            url: './gene/id/' + species + '?q=' + id,
            success: function (data) {
                var option = new Option(data.geneName, data.geneID, true, true);
                geneNameSelector.append(option);
                $('#epiBrowserLink').attr('href', generateBrowserURL(data));
                $('#epiBrowserLink').removeClass('disabled')
                updateGeneElements();
                updateDataTable();
            }
        });
    });
}

function updateDataTable() {
    var geneSelected = $('#geneName option:selected').val();
    if (geneSelected != 'Select..') {
        var table = $('#geneTable').DataTable( {
            "destroy": true,
            "processing": true,
            "ordering": false,
            "lengthChange": false,
            "dom": "<'row'<'col-md-3 'f>>" +
                    "<'row'<'col-md-3'tr>>" +
                    "<'row'<'col-md-3'i>>" + 
                    "<'row'<'col-md-3'p>>",
            "pagingType": "simple",
            "ajax": {
                "url": "./gene/corr/" + species + "/" + geneSelected,
                "dataSrc": ""
            },
            "rowId": 'geneID',
            "columns": [
                { "data": "Rank" },
                { "data": "geneName" },
                { "data": "Corr" },
            ]
        });
    }
}

function storeUpdate(update, group, empty=false) {
    if (empty == false){
        updates_3d.push(update);
        groups_3d.push(group);
    }
    else {
        updates_3d = [];
        groups_3d = [];
    }
}

function randomizeClusterColors() {
    $('#randomizeColorBtn').click(function() {
        var grouping = $('#tsneGrouping option:selected').val();
        if (grouping == 'biosample'){
            storeUpdate(empty=true);
            $.ajax({
                type: "GET",
                url: './plot/randomize_colors',
                success: function(data){
                    for(i = 0; i < data['num_colors']; i++){
                        var group = 'cluster_color_' + String(i);
                        var update = {
                            'marker.color': data['colors'][i]
                        };
                        Plotly.restyle("plot-2d-cluster", update, data[group]);
                        if($('#toggle-3d').prop('checked')) {
                            Plotly.restyle("plot-3d-cluster", update, data[group]);
                        }
                        else{
                            storeUpdate(update,data[group]);
                        }
                    }
                }
            });
        }
        else {
            loadClusterPlots();
        }
    });
}

function createHeatMap() {
    var levelType = $('input[name=levels]').filter(':checked').val();
    var pValues = pSlider.getValue();
    var genes = $("#geneName").select2('data');
    var genes_query = "";
    for (i = 0; i < genes.length; i++) {
        genes_query += (genes[i].text + ":" + genes[i].id + "+");
    }
    genes_query = genes_query.slice(0,-1);
    $.ajax({
        type: "GET",
        url: './plot/heat/' + species + '/' + levelType + '/' + pValues[0] + '/' + pValues[1] + '?q=' + genes_query,
        success: function(data) {
            $('#plot-mch-scatter').html("");
            $('#plot-mch-scatter').html('<div class="mch_heatmap">' +
                data + '</div>');
        }
    });
}