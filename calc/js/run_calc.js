function parseBool(string) {
  return Boolean(string);
}

const {calculate, Generations, Pokemon, Move, Field} = require('@smogon/calc');
// Get parameters from subprocess
const [
    genstr, attackerName, defenderName, moveName, attackerItem, defenderItem, attackerNature, defenderNature, attackerLvl, defenderLvl, num_targets, 
    attackerAttackType, attackerAttackingStatEV,attackerAttackingStatBoost, defenderDefenceType, defenderHpEv, defenderDefenceEv, defenderDefendingStatBoost,
    attackerAbility, defenderAbility, Weather, Terrain, gravityon, aurabreak,fairyaura, darkaura, beadsofruin,swordofruin,tabletsofruin,vesselofruin,
    defenderReflect,defenderLightScreen,defenderForesight,attackerTailwind,defenderTailwind,attackerHelpingHand,defenderAuroraVeil,defenderFriendGuard,defenderFlowerGift,defenderBattery, attackerBattery,
    attackerStatus,defenderStatus
] = process.argv.slice(2);
console.log("Received params")
// Set Generation
const genint = parseInt(genstr);
const gen = Generations.get(genint);

// Set attacker EVs
let attackerEvs = {
  atk: 0,
  spa: 0,
  spe: 0,
}
if (attackerAttackType == "physical"){
  attackerEvs.atk = parseInt(attackerAttackingStatEV);
} else {attackerEvs.spa = parseInt(attackerAttackingStatEV)}

// Set defender EVs
let defenderEVs = {
  hp: parseInt(defenderHpEv),
  atk: 0,
  def: 0,
  spd: 0,
  spe: 0,
}
if (defenderDefenceType == "physical"){
  defenderEVs.def = parseInt(defenderDefenceEv);
} else {defenderEVs.spd = parseInt(defenderDefenceEv)}
console.log("Defined EVs")
// Defender Side Field Effects
const theDefenderSide = {
  isReflect: parseBool(defenderReflect),
  isLightScreen: parseBool(defenderLightScreen),
  isForesight: parseBool(defenderForesight),
  isTailwind: parseBool(defenderTailwind),
  isFlowerGift: parseBool(defenderFlowerGift),
  isFriendGuard: parseBool(defenderFriendGuard),
  isAuroraVeil: parseBool(defenderAuroraVeil),
  isBattery: parseBool(defenderBattery),
}
console.log("Defined defender side")
// Attacker side Field Effects
const theAttackerSide = {
  isTailwind: parseBool(attackerTailwind),
  isBattery: parseBool(attackerBattery),
  isHelpingHand: parseBool(attackerHelpingHand),
}

// Move Definition
let move = new Move(gen, moveName);
// If only 1 target make sure 100% of damage is applied
if (parseInt(num_targets) == 1) {
  move.spreadModifier = 1.0;
}
console.log("Defined move")
// Set field effects
fieldEffects = new Field({
  defenderSide: theDefenderSide,
  attackerSide: theAttackerSide,
  isGravity: parseBool(gravityon),
  isAuraBeak: parseBool(aurabreak),
  isFairyAura: parseBool(fairyaura),
  isDarkAura: parseBool(darkaura),
  isBeadsOfRuin: parseBool(beadsofruin),
  isSwordOfRuin: parseBool(swordofruin),
  isTabletsOfRuin: parseBool(tabletsofruin),
  isVesselOfRuin: parseBool(vesselofruin),
  gameType: 'Doubles',
});

if (Weather != "None") {
  fieldEffects.weather = Weather;
}
if (Terrain != "None") {
  fieldEffects.terrain = Terrain;
}

// if (Weather != "None") {
//   if (Terrain != "None") {
//     fieldEffects = new Field({
//       defenderSide: theDefenderSide,
//       attackerSide: theAttackerSide,
//       weather: Weather,
//       terrain: Terrain,
//       isGravity: parseBool(gravityon),
//       isAuraBeak: parseBool(aurabreak),
//       isFairyAura: parseBool(fairyaura),
//       isDarkAura: parseBool(darkaura),
//       isBeadsOfRuin: parseBool(beadsofruin),
//       isSwordOfRuin: parseBool(swordofruin),
//       isTabletsOfRuin: parseBool(tabletsofruin),
//       isVesselOfRuin: parseBool(vesselofruin),
//       gameType: 'Doubles',
//     });
//   } else {
//     fieldEffects = new Field({
//       defenderSide: theDefenderSide,
//       attackerSide: theAttackerSide,
//       weather: Weather,
//       isGravity: parseBool(gravityon),
//       isAuraBeak: parseBool(aurabreak),
//       isFairyAura: parseBool(fairyaura),
//       isDarkAura: parseBool(darkaura),
//       isBeadsOfRuin: parseBool(beadsofruin),
//       isSwordOfRuin: parseBool(swordofruin),
//       isTabletsOfRuin: parseBool(tabletsofruin),
//       isVesselOfRuin: parseBool(vesselofruin),
//       gameType: 'Doubles',
//     });
//   }
// } else {
//     if (Terrain != "None") {
//       fieldEffects = new Field({
//         defenderSide: theDefenderSide,
//         attackerSide: theAttackerSide,
//         terrain: Terrain,
//         isGravity: parseBool(gravityon),
//         isAuraBeak: parseBool(aurabreak),
//         isFairyAura: parseBool(fairyaura),
//         isDarkAura: parseBool(darkaura),
//         isBeadsOfRuin: parseBool(beadsofruin),
//         isSwordOfRuin: parseBool(swordofruin),
//         isTabletsOfRuin: parseBool(tabletsofruin),
//         isVesselOfRuin: parseBool(vesselofruin),
//         gameType: 'Doubles',
//       });
//     } else {
//     fieldEffects = new Field({
//         defenderSide: theDefenderSide,
//         attackerSide: theAttackerSide,
//         isGravity: parseBool(gravityon),
//         isAuraBeak: parseBool(aurabreak),
//         isFairyAura: parseBool(fairyaura),
//         isDarkAura: parseBool(darkaura),
//         isBeadsOfRuin: parseBool(beadsofruin),
//         isSwordOfRuin: parseBool(swordofruin),
//         isTabletsOfRuin: parseBool(tabletsofruin),
//         isVesselOfRuin: parseBool(vesselofruin),
//         gameType: 'Doubles',
//       });
//   }
// }

console.log("Defined Field");
// Calculate damage values
const result = calculate(
  gen,
  new Pokemon(gen, attackerName, {
    ability: attackerAbility,
    item: attackerItem,
    nature: attackerNature,
    evs: attackerEvs,
    boosts: {spa: parseInt(attackerAttackingStatBoost)},
    level: attackerLvl,
  }),
  new Pokemon(gen, defenderName, {
    ability: defenderAbility,
    item: defenderItem,
    nature: defenderNature,
    evs: defenderEVs,
    boosts: {spd: parseInt(defenderDefendingStatBoost)},
    level: defenderLvl,
  }),
  move,
  fieldEffects,
);


// Print the result
console.log(JSON.stringify(result.damage));
