let pasoActualPag = 1;

function siguientePaso() {
    if (pasoActualPag < 3) {
        pasoActualPag += 1;
    }
}

let formulario1 = document.getElementById("main-form-1");
let formulario2 = document.getElementById("main-form-2");
let formulario3 = document.getElementById("main-form-3");


if (pasoActualPag === 1) {
    formulario1.style.display = "block";
    formulario2.style.display = "none";
    formulario3.style.display = "none";
} else if (pasoActualPag === 2) {
    formulario1.style.display = "none";
    formulario2.style.display = "block";
    formulario3.style.display = "none";
} else if (pasoActualPag === 3) {
    formulario1.style.display = "none";
    formulario2.style.display = "none";
    formulario3.style.display = "block";
}