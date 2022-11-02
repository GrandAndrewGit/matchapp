
let input = document.getElementById("id_csv_file");
let csvName = document.getElementById("csvName");
let isEmpty = 0;

input.addEventListener("change", ()=>{
    let csvFile = document.querySelector("#first-input-wrapper input[type=file]").files[0];
    csvName.innerText = csvFile.name;
    isEmpty = isEmpty + 1; 
    if (isEmpty >= 2) {
        document.getElementById("submit-upload").disabled = false;
    }
})

let inputXml = document.getElementById("id_xml_file");
let xmlName = document.getElementById("xmlName");

inputXml.addEventListener("change", ()=>{
    let xmlFile = document.querySelector("#second-input-wrapper input[type=file]").files[0];
    xmlName.innerText = xmlFile.name;
    isEmpty = isEmpty + 1; 
    if (isEmpty >= 2) {
        document.getElementById("submit-upload").disabled = false;
    }
})
