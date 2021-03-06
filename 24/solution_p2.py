import sys
import re
import math

pat = re.compile('^(\d+) units each with (\d+) hit points( \(.+\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)$')

immune = []
infection = []

class UnitGroup:
    def __init__(self, nunits, hp, imm_weak, damage, att_type, init):
        self.nunits = nunits
        self.hp = hp
        self.imm_weak = imm_weak
        self.damage = damage
        self.att_type = att_type
        self.init = init

    def clone(self):
        return UnitGroup(self.nunits, self.hp, self.imm_weak,
                         self.damage, self.att_type, self.init)

    @property
    def eff_power(self):
        return self.nunits * self.damage

    @property
    def dead(self):
        return self.nunits <= 0

    @property
    def strength(self):
        return self.nunits * self.hp

    def immune_to(self, type):
        return 'imm' in self.imm_weak and type in self.imm_weak['imm']

    def weak_to(self, type):
        return 'weak' in self.imm_weak and type in self.imm_weak['weak']

    def effective_damage_to(self, other):
        base = self.eff_power
        if other.immune_to(self.att_type):
            return 0
        if other.weak_to(self.att_type):
            return base * 2
        return base

    def attack(self, other):
        if self.dead:
            return False
        damage = self.effective_damage_to(other)
        new_strength = other.strength - damage
        new_units = int(math.ceil(new_strength / other.hp))
        if other.nunits == new_units:
            return False
        other.nunits = new_units
        return True

    def __str__(self):
        return 'UnitGroup(n=%d, hp=%d, dmg=%d, init=%d)' % (
            self.nunits, self.hp, self.damage, self.init)
    

state = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    if line == 'Immune System:':
        state = 1
        continue
    if line == 'Infection:':
        state = 2
        continue
    if state in [1, 2]:
        m = pat.match(line)
        extras = {}
        if m.group(3):
            params = m.group(3)
            params = params[params.index('(') + 1:params.index(')')]
            params = params.split(';')
            weak = []
            imm = []
            for category in params:
                category = category.strip()
                if category.startswith('weak'):
                    chose = weak
                elif category.startswith('immune'):
                    chose = imm
                chose.extend(map(str.strip, category[category.index('to ') + 3:].split(',')))
            extras['weak'] = set(weak)
            extras['imm'] = set(imm)
        units, hp, damage, init = map(int, m.group(1, 2, 4, 6))
        att_type = m.group(5)

        group = UnitGroup(units, hp, extras, damage, att_type, init)
        if state == 1:
            immune.append(group)
        else:
            infection.append(group)

class Team:

    def __init__(self, groups):
        self.groups = groups
        self.cleanup()

    def clone(self):
        return Team(list(map(UnitGroup.clone, self.groups)))

    def set_target(self, target):
        self.target = target

    def select_targets(self):
        target_pool = list(self.target.groups)
        target_map = {}
        for group in sorted(self.groups, key=lambda g: (g.eff_power, g.init), reverse=True):
            target = self.best_target(target_pool, group)
            if target:
                target_pool.remove(target)
            target_map[group] = target
            if not target_pool:
                break
        return target_map

    def best_target(self, pool, group):
        def best_target_sort(enemy):
            return (
                group.effective_damage_to(enemy),
                enemy.eff_power,
                enemy.init
            )
        best = sorted(pool, key=best_target_sort, reverse=True)[0]
        if group.effective_damage_to(best) == 0:
            return None
        return best

    def cleanup(self):
        self.groups = [g for g in self.groups if not g.dead]

    @property
    def remain(self):
        return len(self.groups) != 0

    @property
    def unit_count(self):
        return sum(map(lambda g: g.nunits, self.groups))

def fight(immune, infection):
    battle = {}
    battle.update(immune.select_targets())
    battle.update(infection.select_targets())
    any_progress = False
    for (attack, defend) in sorted(battle.items(), key=lambda i: i[0].init, reverse=True):
        if defend is None:
            continue
        if attack.dead or defend.dead:
            continue
        progress = attack.attack(defend)
        if progress:
            any_progress = True
    immune.cleanup()
    infection.cleanup()
    return any_progress

immune_orig = Team(immune)
infection_orig = Team(infection)
def simulation(boost=0):
    immune = immune_orig.clone()
    infection = infection_orig.clone()
    for g in immune.groups:
        g.damage += boost
    immune.set_target(infection)
    infection.set_target(immune)
    while immune.remain and infection.remain:
        any_progress = fight(immune, infection)
        if not any_progress:
            break
    return immune, infection

def find_solution():
    boost = 1
    phase = 'upper'
    upper_limit = None
    lower_limit = 1
    while True:
        if phase == 'search':
            boost = ((upper_limit - lower_limit) // 2) + lower_limit
        #print(lower_limit, upper_limit, boost)
        immune, infection = simulation(boost)
        if upper_limit == lower_limit:
            break
        if infection.remain:
            if phase == 'upper':
                boost *= 2
            elif phase == 'search':
                if lower_limit == boost:
                    boost += 1
                lower_limit = boost
        else:
            if phase == 'upper':
                upper_limit = boost
                phase = 'search'
            elif phase == 'search':
                upper_limit = boost
    print(immune.unit_count)

find_solution()    
