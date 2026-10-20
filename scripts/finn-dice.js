/**
 * Finn Saltão: Dados Orelha-de-Prata
 * Registra um sistema de dados customizado no Dice So Nice.
 *
 * - Colorsets: finn_prata (aço + latão), finn_inspiracao, finn_arcano
 * - Sistema "finn": d20 com faces de engrenagem (1 = corda partida, 20 = alaúde)
 *
 * Depois de instalar: Configurações > Dice So Nice > Aparência,
 * escolha o sistema "Finn Saltão" para o d20.
 */

const MODULE_PATH = "modules/finn-dice";

const COLORSETS = {
  finn_prata: {
    name: "finn_prata",
    description: "Orelha-de-Prata (aço e latão)",
    category: "Finn Saltão",
    foreground: "#C9A24B",
    background: "#8E99A4",
    outline: "#2B2F36",
    edge: "#5C6670",
    texture: "metal",
    material: "metal",
    font: "Georgia",
    visibility: "visible"
  },
  finn_inspiracao: {
    name: "finn_inspiracao",
    description: "Inspiração Bárdica (latão polido)",
    category: "Finn Saltão",
    foreground: "#1B2A4A",
    background: "#C9A24B",
    outline: "#F3E3B3",
    edge: "#8A6A22",
    texture: "bronze01",
    material: "metal",
    font: "Georgia",
    visibility: "visible"
  },
  finn_arcano: {
    name: "finn_arcano",
    description: "Engrenagem arcana (bronze e brasa)",
    category: "Finn Saltão",
    foreground: "#FFB347",
    background: "#4A2F1A",
    outline: "#1A0F08",
    edge: "#7A4B26",
    texture: "bronze03",
    material: "metal",
    font: "Georgia",
    visibility: "visible"
  }
};

function faces(suffix = "") {
  // d20: índice 0 = face 1, índice 19 = face 20
  return Array.from({ length: 20 }, (_, i) => {
    const n = String(i + 1).padStart(2, "0");
    return `${MODULE_PATH}/assets/faces/d20_${n}${suffix}.png`;
  });
}

Hooks.once("diceSoNiceReady", (dice3d) => {
  // 1) Colorsets (o segundo argumento "no" não força nenhum como padrão)
  for (const cs of Object.values(COLORSETS)) {
    dice3d.addColorset(cs, "no");
  }

  // 2) Sistema de dados do Finn
  dice3d.addSystem({ id: "finn", name: "Finn Saltão (Orelha-de-Prata)" }, "default");

  // 3) Preset do d20 com faces customizadas + relevo
  dice3d.addDicePreset({
    type: "d20",
    labels: faces(),
    bumpMaps: faces("_bump"),
    system: "finn",
    colorset: "finn_prata"
  });

  console.log("finn-dice | sistema de dados registrado");
});
