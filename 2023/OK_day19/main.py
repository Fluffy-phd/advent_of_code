import numpy as np

def eval_part(part, commands):
    active_command = commands['in']

    while True:
        for c in active_command:
            if c[0] == 'o':
                if c[-1] == 'R':
                    return False
                if c[-1] == 'A':
                    return True
                active_command = commands[c[-1]]
                break

            val2compare = part[c[0]]
            op = c[1]
            valref = c[2]
            if op == '<':
                if val2compare < valref:
                    if c[-1] == 'R':
                        return False
                    if c[-1] == 'A':
                        return True
                    active_command = commands[c[-1]]
                    break
            elif op == '>':
                if val2compare > valref:
                    if c[-1] == 'R':
                        return False
                    if c[-1] == 'A':
                        return True
                    active_command = commands[c[-1]]
                    break
            elif op == '=':
                if val2compare == valref:
                    if c[-1] == 'R':
                        return False
                    if c[-1] == 'A':
                        return True
                    active_command = commands[c[-1]]
                    break
            # print(c, val2compare, op, valref)

        # break

def part1():

    commands = {}
    parts = []


    with open('input.txt', 'r') as f:
        lines = f.readlines()

        isworkflow = True
        for line in lines:
            tmp = line.strip()

            if len(tmp) == 0:
                isworkflow = False
                continue

            if isworkflow:
                t_ = tmp.split('{')
                workflow_name = t_[0]
                workflow_rules_ = t_[1][:-1].split(',')
                workflow_rules = []
                for wr in workflow_rules_:
                    t__ = wr.split(':')

                    if len(t__) > 1:
                        var = t__[0][0]
                        op = t__[0][1]
                        val = int(t__[0][2:])
                        tgt = t__[1]
                    else:
                        var = 'o'
                        op = 'o'
                        val = 'o'
                        tgt = t__[0]

                    workflow_rules.append((var, op, val, tgt))


                commands[workflow_name] = workflow_rules

            else:
                new_part = {}
                t_ = tmp[1:-1].split(',')
                for t__ in t_:
                    new_part[t__[0]] = int(t__[2:])
                # print(new_part)
                parts.append(new_part)

    # print(parts)
    # print(commands)

    answer = 0
    for part in parts:
        accepted = eval_part(part, commands)

        if accepted:
            answer += part['x'] + part['m'] + part['a'] + part['s']

    print(answer)

def divide_part(current_part, val_name, c, d):
    a = current_part[val_name][0]
    b = current_part[val_name][1]

    if d == '>':
        # A > c 
        # accept c+1 ... b
        # forward a ... c
        i1 = c + 1
        i2 = b
        j1 = a
        j2 = c

        if i1 > i2:
            part_accepted = None
        else:
            part_accepted = current_part.copy()
            part_accepted[val_name] = (max(c + 1, a), b)

        if j1 > j2:
            part_forwarded = None
        else:
            part_forwarded = current_part.copy()
            part_forwarded[val_name] = (a, min(c, b))
    else:
        # A < c 
        # accept a ... c - 1 
        # forward c ... b
        i1 = a
        i2 = c - 1
        j1 = c
        j2 = b

        if i1 > i2:
            part_accepted = None
        else:
            part_accepted = current_part.copy()
            part_accepted[val_name] = (a, min(c - 1, b))

        if j1 > j2:
            part_forwarded = None
        else:
            part_forwarded = current_part.copy()
            part_forwarded[val_name] = (max(a, c), b)

    return (part_accepted, part_forwarded)


def part2():

    commands = {}

    with open('input.txt', 'r') as f:
        lines = f.readlines()

        for line in lines:
            tmp = line.strip()

            if len(tmp) == 0:
                break

            t_ = tmp.split('{')
            workflow_name = t_[0]
            workflow_rules_ = t_[1][:-1].split(',')
            workflow_rules = []
            for wr in workflow_rules_:
                t__ = wr.split(':')

                if len(t__) > 1:
                    var = t__[0][0]
                    op = t__[0][1]
                    val = int(t__[0][2:])
                    tgt = t__[1]
                else:
                    var = 'o'
                    op = 'o'
                    val = 'o'
                    tgt = t__[0]

                workflow_rules.append((var, op, val, tgt))


            commands[workflow_name] = workflow_rules


    part = {
        'x' : (1, 4000),
        'm' : (1, 4000),
        'a' : (1, 4000),
        's' : (1, 4000),
    }

    active_commands = [('in', part)]
    accepted_configurations = []


    while len(active_commands) > 0:
        active_commands_new = []

        for node_name, p in active_commands:
            if node_name == 'A':
                accepted_configurations.append(p)
                print('accepting', p)
                continue
            if node_name == 'R':
                continue

            cmd = commands[node_name]

            current_part = p.copy()
            for sub_cmd in cmd:
                print('verifying command', sub_cmd, 'on part', current_part)

                val_name = sub_cmd[0]
                if val_name == 'o':
                    active_commands_new.append((sub_cmd[-1], current_part))
                    print('  reached a default action, sending', current_part, 'to %s' % (sub_cmd[-1]))
                    break
                
                dividing_value = sub_cmd[2]
                part_accepted, part_forwarded = divide_part(current_part, val_name, dividing_value, sub_cmd[1])

                if part_accepted is not None:
                    active_commands_new.append((sub_cmd[-1], part_accepted))
                    current_part = part_forwarded
                    print('  accepting subpart', part_accepted, ' forwarding part', current_part)

        active_commands = active_commands_new

    answer = 0
    for conf in accepted_configurations:
        print(conf)
        answer += (conf['x'][1] - conf['x'][0] + 1) * (conf['a'][1] - conf['a'][0] + 1) * (conf['m'][1] - conf['m'][0] + 1) * (conf['s'][1] - conf['s'][0] + 1)
    print(answer)



# part1()
part2()

