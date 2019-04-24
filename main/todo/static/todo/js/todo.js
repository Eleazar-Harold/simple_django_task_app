$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-todo .modal-content").html("");
                $("#modal-todo").modal("show");
            },
            success: function (data) {
                $("#modal-todo .modal-content").html(data.html_form);
                if ($("#id_taskdate").val() === "Invalid date" || $("#id_taskdate").val() === "") {
                    document.getElementById("id_taskdate").value = moment(new Date().toString()).format('MM/DD/Y H:MM:ss');
                }
                jQuery("#id_taskdate").datetimepicker({
                  timepicker: false,
                  format: "m/d/Y h:m:s",
                  formatTime: "h:m:s",
                  formatDate: "m/d/Y",
                  minDate: "-01/05/1970", //yesterday is minimum date(for today use 0 or -1970/01/01)
                  maxDate: "+03/31/1970" //an open week as maximum date in calendar
                });
                if ($("#id_taskdate") !== undefined || $("#id_taskdate") === null || $("#id_taskdate").val() !== "Invalid date") {
                    document.getElementById("id_taskdate").value = moment($('#id_taskdate').val()).format('MM/DD/Y H:MM:ss');
                }
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#todo-table tbody").html(data.html_todo_list);
                    $("#modal-todo").modal("hide");
                }
                else {
                    $("#modal-todo .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    /* Binding */

    // Create todo
    $(".js-create-todo").click(loadForm);
    $("#modal-todo").on("submit", ".js-todo-create-form", saveForm);

    // Update todo
    $("#todo-table").on("click", ".js-update-todo", loadForm);
    $("#modal-todo").on("submit", ".js-todo-update-form", saveForm);

    // Delete todo
    $("#todo-table").on("click", ".js-delete-todo", loadForm);
    $("#modal-todo").on("submit", ".js-todo-delete-form", saveForm);

});
