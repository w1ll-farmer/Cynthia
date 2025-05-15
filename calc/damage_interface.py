import subprocess
import json
import time 
def calc_damage(
    attacker:str, defender:str, move:str, attackerItem:str, defenderItem:str, attackerNature:str, defenderNature:str, attackerAbility:str, defenderAbility:str,
    attackerLvl:str="50",
    defenderLvl:str="50",
    num_targets:str="2", 
    attackerAttackType:str="physical",
    attackerAttackingStatEV:str="252",
    attackerAttackingStatBoost:str="0",
    defenderDefenceType:str="physical",
    defenderHpEv:str="252",
    defenderDefenceEv:str="252",
    defenderDefendingStatBoost:str="0",
    gen:str="9",
    Weather:str="None",
    Terrain:str="None",
    gravityon:str="",
    aurabreak:str="",
    fairyaura:str="",
    darkaura:str="",
    beadsofruin:str="",
    swordofruin:str="",
    tabletsofruin:str="",
    vesselofruin:str="",
    defenderReflect:str="",
    defenderLightScreen:str="",
    defenderForesight:str="",
    attackerTailwind:str="",
    defenderTailwind:str="",
    attackerHelpingHand:str="",
    defenderAuroraVeil:str="",
    defenderFriendGuard:str="",
    defenderFlowerGift:str="",
    defenderBattery:str="",
    attackerBattery:str="",
    attackerStatus:str="",
    defenderStatus:str="",
    attackerTeraType:str="",
    defenderTera:str="", 
    attackerAlliesFainted:str="",
    criticalHit:str=""
    ) -> list:
    """Run JavaScript code for damage calculation

    Args:
        attacker (str): Name of pokemon attacking
        defender (str): Name of pokemon defending
        move (str): Name of the move
        attackerItem (str): Item being held by attacker
        defenderItem (str): Item being held by defender
        attackerNature (str): Attacker's nature
        defenderNature (str): Defenders nature
        attackerLvl (str, optional): Attacker's level. Defaults to "50".
        defenderLvl (str, optional): Defender's level. Defaults to "50".
        num_targets (str, optional): The number of targets being affected. Defaults to "1".
        attackerAttackType (str, optional): Is the attack physical or special. Defaults to "physical".
        attackerAttackingStatEV (str, optional): Attacking EV. Defaults to "252".
        attackerAttackingStatBoost (str, optional): Attack boosts. Defaults to "0".
        defenderDefenceType (str, optional): Defence stat being used in calculation. Defaults to "physical".
        defenderHpEv (str, optional): HP EVs. Defaults to "252".
        defenderDefenceEv (str, optional): Defence stat EVs. Defaults to "252".
        defenderDefendingStatBoost (str, optional): Defensive stat boosts. Defaults to "0".
        gen (str, optional): Generation of battle. Defaults to "9".

    Returns:
        list(int): The possible damage rolls
    """
    # Run the damage calculator
    result = subprocess.run(
        ['node', 'js/run_calc.js',
         gen, attacker, defender, move,
         attackerItem, defenderItem, attackerNature,
         defenderNature, attackerLvl, defenderLvl,
         num_targets, attackerAttackType, attackerAttackingStatEV,
         attackerAttackingStatBoost, defenderDefenceType,
         defenderHpEv, defenderDefenceEv, defenderDefendingStatBoost,
         attackerAbility, defenderAbility,
         Weather, Terrain, gravityon, aurabreak, fairyaura, darkaura,
         beadsofruin, swordofruin, tabletsofruin, vesselofruin, defenderReflect,
         defenderLightScreen, defenderForesight, attackerTailwind, defenderTailwind,
         attackerHelpingHand, defenderAuroraVeil, defenderFriendGuard, defenderFlowerGift, defenderBattery,
         attackerBattery, attackerStatus, defenderStatus, attackerTeraType,
         defenderTera, attackerAlliesFainted, criticalHit
        ],
        capture_output=True, text=True
    )
    
    return result.stdout.strip()

start = time.time()
print(calc_damage('Garchomp', 'Togekiss', 'Rock Slide','Choice Band','Choice Scarf','Adamant','Calm', 'Rough Skin', 'Serene Grace', num_targets="2", attackerTeraType="Rock"))
print(calc_damage('Garchomp', 'Togekiss', 'Rock Slide','Choice Band','Choice Scarf','Adamant','Calm', 'Adaptability', 'Serene Grace', num_targets="2", attackerTeraType="Rock"))
print(time.time()-start)