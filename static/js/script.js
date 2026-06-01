function previewQR(){

    let formData = new FormData();

    formData.append(
        "link",
        document.getElementById("link").value
    );

    formData.append(
        "fill_color",
        document.getElementById("fill_color").value
    );

    formData.append(
        "back_color",
        document.getElementById("back_color").value
    );

    let logo =
        document.getElementById("logo").files[0];

    if(logo){
        formData.append("logo", logo);
    }

    fetch('/preview',{
        method:'POST',
        body:formData
    })
    .then(response => response.json())
    .then(data => {

        if(data.error){
            alert(data.error);
            return;
        }

        document.getElementById("preview").innerHTML = `
            <img
            src="data:image/png;base64,${data.image}"
            alt="QR Code">
        `;
    })
    .catch(error=>{
        console.error(error);
        alert("Failed to generate QR Code");
    });

}

function downloadPNG(){

    let form = new FormData();

    form.append(
        "link",
        document.getElementById("link").value
    );

    fetch('/download_png',{
        method:'POST',
        body:form
    })
    .then(response => response.blob())
    .then(blob => {

        let a = document.createElement("a");

        a.href =
        URL.createObjectURL(blob);

        a.download =
        "qr_code.png";

        a.click();

    });

}

function downloadSVG(){

    let form = new FormData();

    form.append(
        "link",
        document.getElementById("link").value
    );

    fetch('/download_svg',{
        method:'POST',
        body:form
    })
    .then(response => response.blob())
    .then(blob => {

        let a = document.createElement("a");

        a.href =
        URL.createObjectURL(blob);

        a.download =
        "qr_code.svg";

        a.click();

    });

}
