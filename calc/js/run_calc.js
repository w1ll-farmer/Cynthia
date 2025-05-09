const {calculate, Generations, Pokemon, Move} = require('@smogon/calc');
// Get parameters from subprocess
const [
    genstr, attackerName, defenderName, moveName, attackerItem, defenderItem, attackerNature, defenderNature, attackerLvl, defenderLvl, num_targets, 
    attackerAttackType, attackerAttackingStatEV,attackerAttackingStatBoost, defenderDefenceType, defenderHpEv, defenderDefenceEv, defenderDefendingStatBoost
] = process.argv.slice(2);

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

// Calculate damage values
const result = calculate(
  gen,
  new Pokemon(gen, attackerName, {
    item: attackerItem,
    nature: attackerNature,
    evs: attackerEvs,
    boosts: {spa: parseInt(attackerAttackingStatBoost)},
    level: attackerLvl,
  }),
  new Pokemon(gen, defenderName, {
    item: defenderItem,
    nature: defenderNature,
    evs: defenderEVs,
    boosts: {spd: parseInt(defenderDefendingStatBoost)},
    level: defenderLvl,
  }),
  new Move(gen, moveName),
);


// Print the result
console.log(JSON.stringify(result.damage));
