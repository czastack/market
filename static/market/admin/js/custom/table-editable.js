var TableEditable = function () {

    return {

        //main function to initiate the module
        init: function () {
            var itemmenu = document.getElementById('itemmenu');
            var itemmenu_container = document.getElementById('itemmenu_container');
            var nEditing = null;

            function restoreRow(oTable, nRow) {
                var aData = oTable.fnGetData(nRow);
                var jqTds = $('>td', nRow);

                for (var i = jqTds.length - 2; i >= 0; i--) {
                    oTable.fnUpdate(aData[i], nRow, i, false);
                }
                itemmenu_container.appendChild(itemmenu);
                // oTable.fnDraw();
            }

            function editRow(oTable, nRow) {
                var aData = oTable.fnGetData(nRow);
                var jqTds = $('>td', nRow);
                for (var i = jqTds.length - 2; i >= 0; i--) {
                    jqTds[i].innerHTML = '<input type="text" class="form-control input-small" value="' + aData[i] + '">';
                }
                jqTds[jqTds.length - 1].appendChild(itemmenu);
            }

            function saveRow(oTable, nRow) {
                var jqInputs = $('input', nRow);
                for (var i = jqInputs.length - 2; i >= 0; i--) {
                    oTable.fnUpdate(jqInputs[i].value, nRow, i, false);
                }
                itemmenu_container.appendChild(itemmenu);
            }

            function cancelEditRow(oTable, nRow) {
                var jqInputs = $('input', nRow);
                for (var i = jqInputs.length - 2; i >= 0; i--) {
                    oTable.fnUpdate(jqInputs[i].value, nRow, i, false);
                }
                oTable.fnDraw();
            }

            var oTable = $('#sample_editable_1').dataTable({
                // "aLengthMenu": [
                //     [5, 15, 20, -1],
                //     [5, 15, 20, "All"] // change per page values here
                // ],
                // set the initial value
                "iDisplayLength": 5,
                
                "sPaginationType": "bootstrap",
                "oLanguage": {
                    "sLengthMenu": "_MENU_ records",
                    "oPaginate": {
                        "sPrevious": "Prev",
                        "sNext": "Next"
                    }
                },
                "aoColumnDefs": [{
                        'bSortable': false,
                        'aTargets': [0]
                    }
                ]
            });

            jQuery('#sample_editable_1_wrapper .dataTables_filter input').addClass("form-control input-medium input-inline"); // modify table search input
            jQuery('#sample_editable_1_wrapper .dataTables_length select').addClass("form-control input-small"); // modify table per page dropdown
            jQuery('#sample_editable_1_wrapper .dataTables_length select').select2({
                showSearchInput : false //hide search box with special css class
            }); // initialize select2 dropdown

            $('.delete', itemmenu_container).click(function (e) {
                e.preventDefault();
                if (confirm("Are you sure to delete this row ?") == false) {
                    return;
                }
                oTable.fnDeleteRow(nEditing);
                alert("Deleted! Do not forget to do some ajax to sync with backend :)");
            });

            $('.cancel', itemmenu_container).click(function (e) {
                e.preventDefault();
                if ($(this).attr("data-mode") == "new") {
                    oTable.fnDeleteRow(nEditing);
                } else {
                    restoreRow(oTable, nEditing);
                    nEditing = null;
                }
            });

            $('.save', itemmenu_container).click(function (e) {
                /* Editing this row and want to save it */
                saveRow(oTable, nEditing);
                nEditing = null;
                alert("Updated! Do not forget to do some ajax to sync with backend :)");
            });

            $('#sample_editable_1 a.edit').click(function (e) {
                e.preventDefault();

                /* Get the row as a parent of the link that was clicked on */
                var nRow = $(this).parents('tr')[0];

                if (nEditing !== null && nEditing != nRow) {
                    /* Currently editing - but not this row - restore the old before continuing to edit mode */
                    restoreRow(oTable, nEditing);
                    editRow(oTable, nRow);
                    nEditing = nRow;
                } else {
                    /* No edit in progress - let's start one */
                    editRow(oTable, nRow);
                    nEditing = nRow;
                }
            });
        }

    };

}();