const {calculate, Generations, Pokemon, Move} = require('@smogon/calc');

const [
    genstr, attackerName, defenderName, moveName, attackerItem, defenderItem, attackerNature, defenderNature, attackerLvl, defenderLvl, num_targets, 
    attackerAttackType, attackerAttackingStatEV,attackerAttackingStatBoost, defenderDefenceType, defenderHpEv, defenderDefenceEv, defenderDefendingStatBoost
] = process.argv.slice(2);
const genint = parseInt(genstr)
const gen = Generations.get(genint); // alternatively: const gen = 5;
const result = calculate(
  gen,
  new Pokemon(gen, attackerName, {
    item: attackerItem,
    nature: attackerNature,
    evs: {spa: parseInt(attackerAttackingStatEV)},
    boosts: {spa: parseInt(attackerAttackingStatBoost)},
    level: attackerLvl,
  }),
  new Pokemon(gen, defenderName, {
    item: defenderItem,
    nature: defenderNature,
    evs: {hp: parseInt(defenderHpEv), spd: parseInt(defenderDefenceEv)},
    boosts: {spd: 0},
    level: defenderLvl,
  }),
  new Move(gen, moveName),
);


// Print the result
console.log(JSON.stringify(result.damage));
