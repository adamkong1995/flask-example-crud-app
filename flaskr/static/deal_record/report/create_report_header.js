$(document).ready(function(){
    var table = document.getElementById("report2");
    var header = table.createTHead();
    var row = header.insertRow(0);

    var h1 = document.createElement("th");
    var h2 = document.createElement("th");
    var h3 = document.createElement("th");
    var h4 = document.createElement("th");
    var h5 = document.createElement("th");
    var h6 = document.createElement("th");
    var h7 = document.createElement("th");
    var h8 = document.createElement("th");
    var h9 = document.createElement("th");
    var h10 = document.createElement("th");
    var h11 = document.createElement("th");

    /*h1.innerHTML = "Group";
    h2.innerHTML = "Strategy";
    h3.innerHTML = "Name";
    h4.innerHTML = "Country";
    h5.innerHTML = "PIC";
    h6.innerHTML = "Deal Size";
    h7.innerHTML = "Priority";
    h8.innerHTML = "Status";
    h9.innerHTML = "Start Date";
    h10.innerHTML = "Exit Date";
    h11.innerHTML = "Description";*/

    h1.setAttribute("width","5%");
    h2.setAttribute("width","7%");
    h3.setAttribute("width","13%");
    h4.setAttribute("width","7%");
    h5.setAttribute("width","3%");
    h5.setAttribute("data-filter-control", "true");
    h6.setAttribute("width","7%");
    h7.setAttribute("width","3%");
    h8.setAttribute("width","7%");
    h9.setAttribute("width","8%");
    h10.setAttribute("width","8%");
    h11.setAttribute("width","32%");

    row.appendChild(h1);
    row.appendChild(h2);
    row.appendChild(h3);
    row.appendChild(h4);
    row.appendChild(h5);
    row.appendChild(h6);
    row.appendChild(h7);
    row.appendChild(h8);
    row.appendChild(h9);
    row.appendChild(h10);
    row.appendChild(h11);
});