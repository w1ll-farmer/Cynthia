import subprocess
import json

def calc_damage(attacker, defender, move, gen='gen9'):
    result = subprocess.run(
        ['node', 'js/run_calc.js', gen, attacker, defender, move],
        capture_output=True, text=True
    )
    # print("result:", result)
    return result.stdout.strip()

print(calc_damage('Garchomp', 'Togekiss', 'Stone Edge'))
