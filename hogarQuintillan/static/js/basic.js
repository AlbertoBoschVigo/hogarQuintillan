document.addEventListener('DOMContentLoaded', function (){
    //Get the button:
    const mybuttonR = document.getElementById("myBtnTopR");
    const mybuttonL = document.getElementById("myBtnTopL");

    mybuttonR.onclick = () => {
        document.body.scrollTop = 0; // For Safari
        document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    }
    mybuttonL.onclick = () => {
        document.body.scrollTop = 0; // For Safari
        document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    }   

    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = () => {
        //console.log('OnScroll');
        if (window.scrollY >= 20) {
            //console.log('Muestro boton');
            mybuttonR.style.display = "block";   
            mybuttonL.style.display = "block";
        }
        else{
            //console.log('Escondo boton');
            mybuttonR.style.display = "none";
            mybuttonL.style.display = "none";
        };
    };

});