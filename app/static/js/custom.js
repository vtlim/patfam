
numCards = 1;
function cloneInputCard() {

    // prepare new id's and names
    // https://stackoverflow.com/a/8513046
    suffix = ('0' + numCards).slice(-2);
    newId = "inputCard_" + suffix;
    newNumName = "inputNum_" + suffix;
    newTypeName = "inputType_" + suffix;
    newJurisName = "inputJuris_" + suffix;

    // get the outer most div and clone it
    // https://stackoverflow.com/a/11985200
    var div = document.getElementById('inputCard_01');
    var clone = div.cloneNode(true); // true means clone all childNodes and all event handlers

    // rename the div's id
    clone.id = newId;

    // rename all the 'name' attributes in the clone
    //clone.getElementsByName("inputType_01")[0].setAttribute('name', newNumName)

    // TODO START HERE
     var allInputs = clone.getElementsByTagName("input");
    // console.log(allInputs.getElementsByTagName("inputType_01"));
    // var typeNames = clone.getElementsByTagName("inputType_01");
    // console.log(typeNames)
    // var jurisNames = clone.getElementsByName("inputJuris_01");

    allInputs = [].slice.call(allInputs, 0);
    for (var i = 0; i < allInputs.length; ++i)
        var name = allInputs[i].getAttribute("name");
        console.log(name);
        //allInputs[i].setAttribute('name', newJurisName);

    // typeNames = [].slice.call(typeNames, 0);
    // for (var i = 0; i < typeNames.length; ++i)
    //     typeNames[i].setAttribute('name', newTypeName);

    // jurisNames = [].slice.call(jurisNames, 0);
    // for (var i = 0; i < jurisNames.length; ++i)
    //     jurisNames[i].setAttribute('name', newJurisName);

    // finally, add the cloned element to html body
    document.body.appendChild(clone);
    numCards++;
}
