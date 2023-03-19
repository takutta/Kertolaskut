const jatkaAiempaaTab = document.getElementById("jatka-aiempaa-tab");
const uusiPelaajaTab = document.getElementById("uusi-pelaaja-tab");

jatkaAiempaaTab.addEventListener("click", () => {
  const vanhatPelaajat = document.getElementsByName("vanha");
  for (let i = 0; i < vanhatPelaajat.length; i++) {
    vanhatPelaajat[i].checked = false;
    
  }
});

uusiPelaajaTab.addEventListener("click", () => {
  const uusiPelaaja = document.getElementsByName("pelaaja");
  for (let i = 0; i < uusiPelaaja.length; i++) {
    uusiPelaaja[i].checked = false;
  }
});