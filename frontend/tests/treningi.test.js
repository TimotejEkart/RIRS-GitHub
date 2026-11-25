import { beforeEach, describe, expect, it, vi } from "vitest";

// serija: [vaja, ponovitve, teža], prazen niz = prazno polje
function vrstica([vaja, ponovitve, teza] = ["", "", ""]) {
  const izbrana = vaja ? " selected" : "";
  return `<tr class="serija">
    <td><select name="vaja"><option value=""></option><option value="1"${izbrana}>Počep</option></select></td>
    <td><input name="ponovitve" value="${ponovitve}"></td>
    <td><input name="teza_kg" value="${teza}"></td>
    <td><input type="checkbox" name="DELETE" checked></td>
  </tr>`;
}

function stran({ serije = [], praznih = 0, treningov = 0, gumbi = true } = {}) {
  const vrstice = [...serije.map(vrstica), ...Array.from({ length: praznih }, () => vrstica())].join("");
  const kartice = Array.from({ length: treningov }, (_, i) => `<article class="trening">${i}</article>`).join("");
  document.body.innerHTML = `
    <table><tbody id="serije">${vrstice}</tbody></table>
    ${gumbi ? '<button id="dodaj-serijo" hidden></button>' : ""}
    <section class="pretekli">${kartice}</section>
    ${gumbi ? '<button id="nalozi-starejse" hidden></button>' : ""}`;
}

async function zazeni() {
  vi.resetModules();
  await import("../static/js/treningi.js");
}

const vidne = (sel) => [...document.querySelectorAll(sel)].filter((e) => !e.hidden).length;
const vidneSerije = () => vidne("#serije tr.serija");
const vidniTreningi = () => vidne(".pretekli .trening");
const gumb = (id) => document.getElementById(id);

describe("serije na strani Treningi", () => {
  beforeEach(() => (document.body.innerHTML = ""));

  it("pri praznem obrazcu pokaže tri vrstice in gumb za dodajanje", async () => {
    stran({ praznih: 9 });
    await zazeni();
    expect(vidneSerije()).toBe(3);
    expect(gumb("dodaj-serijo").hidden).toBe(false);
  });

  it("vsak klik na gumb doda eno vrstico", async () => {
    stran({ praznih: 9 });
    await zazeni();
    gumb("dodaj-serijo").click();
    expect(vidneSerije()).toBe(4);
    gumb("dodaj-serijo").click();
    expect(vidneSerije()).toBe(5);
  });

  it("ko so vidne vse vrstice, gumb izgine", async () => {
    stran({ praznih: 5 });
    await zazeni();
    gumb("dodaj-serijo").click();
    gumb("dodaj-serijo").click();
    expect(vidneSerije()).toBe(5);
    expect(gumb("dodaj-serijo").hidden).toBe(true);
  });

  it("izpolnjene vrstice ostanejo vidne in za njimi ena prazna", async () => {
    stran({ serije: [["1", "8", "80"], ["1", "8", "80"], ["", "10", ""], ["1", "6", "90"]], praznih: 5 });
    await zazeni();
    expect(vidneSerije()).toBe(5);
  });

  it("obkljukano polje za odstranitev ne šteje kot izpolnjena vrstica", async () => {
    stran({ praznih: 9 });
    await zazeni();
    // vse vrstice imajo obkljukan checkbox, pa so vseeno vidne samo tri
    expect(vidneSerije()).toBe(3);
  });

  it("pri treh ali manj vrsticah gumba ne pokaže", async () => {
    stran({ praznih: 3 });
    await zazeni();
    expect(vidneSerije()).toBe(3);
    expect(gumb("dodaj-serijo").hidden).toBe(true);
  });
});

describe("pretekli treningi", () => {
  it("pokaže pet treningov, vsak klik naloži naslednjih pet", async () => {
    stran({ treningov: 12 });
    await zazeni();
    expect(vidniTreningi()).toBe(5);
    gumb("nalozi-starejse").click();
    expect(vidniTreningi()).toBe(10);
    expect(gumb("nalozi-starejse").hidden).toBe(false);
    gumb("nalozi-starejse").click();
    expect(vidniTreningi()).toBe(12);
    expect(gumb("nalozi-starejse").hidden).toBe(true);
  });

  it("brez gumbov na strani ničesar ne skrije", async () => {
    stran({ praznih: 9, treningov: 12, gumbi: false });
    await zazeni();
    expect(vidneSerije()).toBe(9);
    expect(vidniTreningi()).toBe(12);
  });
});
