/**
 * Finn Saltão: Dados Orelha-de-Prata (kit completo para o Dice So Nice)
 *
 * Sistema "finn" com d4, d6, d8, d10, d12, d20 e d100:
 *  - d4   : texto, colorset aço e latão
 *  - d6   : dano de Bola de Fogo (bronze, números cor de brasa)
 *  - d8   : Inspiração Bárdica (latão, números azul-marinho, nota musical)
 *  - d10, d12, d100 : aço com engrenagens douradas
 *  - d20  : engrenagens, corda partida no 1 e alaúde no 20
 *
 * Depois de instalar: Configurações > Dice So Nice > Aparência,
 * escolha o sistema "Finn Saltão" na lista de dados.
 */

const MODULE_ID = "finn-dice";
const MODULE_PATH = `modules/${MODULE_ID}`;
const SYSTEM_ID = "finn";
const SYSTEM_NAME = "Finn Saltão (Orelha-de-Prata)";
const SYSTEM_GROUP = "Finn Saltão";

// Ordem das faces do d10 e do d100: por padrão 1..9 e depois "0" (valor 10).
// Se o número que aparece no dado não bater com o resultado no chat,
// troque para true (coloca a face "0" / "00" na frente).
const D10_ZERO_FIRST = false;

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

// Dados com imagem nas faces. "rotate" = d10/d100, cuja última face é o "0"/"00".
const IMAGE_DICE = [
  { type: "d6",   count: 6,  colorset: "finn_arcano" },
  { type: "d8",   count: 8,  colorset: "finn_inspiracao" },
  { type: "d10",  count: 10, colorset: "finn_prata", rotate: true },
  { type: "d12",  count: 12, colorset: "finn_prata" },
  { type: "d20",  count: 20, colorset: "finn_prata" },
  { type: "d100", count: 10, colorset: "finn_prata", rotate: true }
];

function faces(die, count, suffix = "", rotate = false) {
  const list = Array.from({ length: count }, (_, i) => {
    const n = String(i + 1).padStart(2, "0");
    return `${MODULE_PATH}/assets/faces/${die}_${n}${suffix}.png`;
  });
  if (rotate && D10_ZERO_FIRST) list.unshift(list.pop());
  return list;
}

async function registerSystem(dice3d) {
  try {
    // API atual do Dice So Nice: classe DiceSystem
    const url = foundry?.utils?.getRoute
      ? foundry.utils.getRoute("modules/dice-so-nice/api.js")
      : "/modules/dice-so-nice/api.js";
    const { DiceSystem } = await import(url);
    dice3d.addSystem(new DiceSystem(SYSTEM_ID, SYSTEM_NAME, "default", SYSTEM_GROUP));
  } catch (err) {
    // Versões antigas do Dice So Nice: forma legada
    console.warn(`${MODULE_ID} | DiceSystem indisponível, usando addSystem legado`, err);
    dice3d.addSystem({ id: SYSTEM_ID, name: SYSTEM_NAME }, "default");
  }
}

Hooks.once("diceSoNiceReady", async (dice3d) => {
  // 1) Colorsets
  for (const cs of Object.values(COLORSETS)) dice3d.addColorset(cs);

  // 2) Sistema
  await registerSystem(dice3d);

  // 3) d4: só texto (o Dice So Nice desenha 3 números por face)
  dice3d.addDicePreset({
    type: "d4",
    labels: ["1", "2", "3", "4"],
    system: SYSTEM_ID,
    colorset: "finn_prata",
    font: "Georgia"
  });

  // 4) Demais dados: imagens nas faces + relevo
  for (const die of IMAGE_DICE) {
    dice3d.addDicePreset({
      type: die.type,
      labels: faces(die.type, die.count, "", die.rotate),
      bumpMaps: faces(die.type, die.count, "_bump", die.rotate),
      system: SYSTEM_ID,
      colorset: die.colorset
    });
  }

  // 5) Pré-carrega as texturas para não travar na primeira rolagem
  try {
    if (typeof dice3d.preloadPresets === "function") await dice3d.preloadPresets(SYSTEM_ID);
  } catch (err) {
    console.warn(`${MODULE_ID} | preloadPresets falhou (não é crítico)`, err);
  }

  console.log(`${MODULE_ID} | kit de dados do Finn registrado`);
});
