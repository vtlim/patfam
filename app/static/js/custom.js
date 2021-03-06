
// disable console log if not supported by browser
// https://stackoverflow.com/a/1114200
if(typeof console === "undefined") {
    console = { log: function() { } };
}

var nextCard = 2;
function cloneInputCard() {

    // prepare new id's and names
    // https://stackoverflow.com/a/8513046
    var suffix = ('0' + nextCard).slice(-2);
    var newId = "inputCard_" + suffix;
    //var newFormName = "inputForm_" + suffix;
    var newNumName = "inputNum_" + suffix;
    var newTypeName = "inputType_" + suffix;
    var newJurisName = "inputJuris_" + suffix;

    // get the outer most div and clone it
    // https://stackoverflow.com/a/11985200
    var div = document.getElementById('inputCard_01');
    var clone = div.cloneNode(true); // true means clone all childNodes and all event handlers

    // rename the div's id
    clone.id = newId;

    // rename the form name
    //var form = clone.getElementsByTagName("form")[0];
    //form.id = newFormName;

    // rename the child element names and clear/uncheck any user response
    var allInputs = clone.getElementsByTagName("input");
    allInputs = [].slice.call(allInputs, 0);

    for (var i = 0; i < allInputs.length; ++i) {

        var name = allInputs[i].getAttribute("name");

        if (name.includes("Num")) {
            allInputs[i].setAttribute('name', newNumName);
            allInputs[i].value = '';
        }
        if (name.includes("Type")) {
            allInputs[i].setAttribute('name', newTypeName);
            allInputs[i].checked = false;
        }
        if (name.includes("Juris")) {
            allInputs[i].setAttribute('name', newJurisName);
            allInputs[i].checked = false;
        }
    }

    // finally, add the cloned element after the latest card
    var lastCard = nextCard - 1;
    var oldCardName = "inputCard_" + ('0' + lastCard).slice(-2);
    var lastdiv = document.getElementById(oldCardName);

    // https://stackoverflow.com/a/11117599
    lastdiv.parentNode.insertBefore(clone, lastdiv.nextSibling);
    nextCard++;
}

function validateForm() {
    var errs = [];

    for (var i = 1; i < nextCard; ++i) {
        var suffix = ('0' + i).slice(-2);

        //var inputNum_value = document.forms["inputForm_" + suffix]["inputNum_" + suffix].value;
        var inputNum_value = document.forms["inputForm_01"]["inputNum_" + suffix].value;
        var inputType_value = document.forms["inputForm_01"]["inputType_" + suffix].value;
        var inputJuris_value = document.forms["inputForm_01"]["inputJuris_" + suffix].value;

        if ((inputNum_value == "") || (inputType_value == "") || (inputJuris_value == "")) {
            errs.push(suffix);
        }
    }

    return errs;
}

function submitForm() {
    var errors = validateForm();
    if (errors.length == 0) {
        console.log("VALIDATION SUCCESS");
        //for (var i = 1; i < nextCard; ++i) {
        //    var suffix = ('0' + i).slice(-2);
        //    document.getElementById("inputForm_" + suffix).submit();
        //}
        alert('pause');
        document.getElementById("inputForm_01").submit();
    } else {
        console.log("VALIDATION ERROR(S): ", errors);
    }
}
