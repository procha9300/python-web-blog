function accountValidation() {
    var element = document.getElementById("entry");

    if (element.getAttribute("data-validation") === "true") {
        return true;
    }
    else {
        alert("Check your email to validate your account.");
        return false;
    }
}


function dataVal() {
    var element = document.getElementById("entry");
    $.ajax(
        {
            url: '/datavalidation',
            method: "POST",
            dataType: "json",
            data: {
            },
            success: function (res) {

                if (res['status'] === 'OK') {
                    element.setAttribute("data-validation", true);
                }
                else {
                    alert("Check your email to validate your account.");
                    element.setAttribute("data-validation", false);
                }

            }
        }
    );
}