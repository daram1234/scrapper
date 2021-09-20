const h1 = document.querySelector("h1")
const main = document.querySelector("main");
const submit = document.querySelector("form");
const load = document.querySelector(".loading");
const HIDDEN = "hidden";

function loading(e){
    h1.classList.add(HIDDEN)
    main.classList.add(HIDDEN);
    load.classList.remove(HIDDEN);
}
submit.addEventListener("submit", loading)