
import difflib
import math


def del_prefix_suffix_insert(actions):
    indices_to_del = []

    for i, action in enumerate(actions):

        if action[0] == 'insert':
            indices_to_del.append(i)
        else:
            break
    for i, action in zip(range(len(actions) - 1, -1, -1), reversed(actions)):
        if action[0] == 'insert':
            indices_to_del.append(i)
        else:
            break

    clean_actions = tuple(filter(lambda x: x[0] not in indices_to_del, enumerate(actions)))
    clean_actions = tuple([element[1] for element in clean_actions])

    return clean_actions

def del_equal(actions):
    indices_to_del = []

    for i, action in enumerate(actions):

        if action[0] == 'equal':
            indices_to_del.append(i)

    clean_actions = tuple(filter(lambda x: x[0] not in indices_to_del, enumerate(actions)))
    clean_actions = tuple([element[1] for element in clean_actions])

    return clean_actions

def get_good_letters_num(actions):
    good_letters_num = 0
    for action in actions:
        if action[0] == 'equal':
            good_letters_num += action[2] - action[1]

    return good_letters_num

def get_penalty(actions, original):
    for action in actions:
        curr_action, edit_index_input = action[0], action[1]

        if curr_action == 'replace':
            if edit_index_input >= 4:  # same penalty for 5th letter and further
                return 1
            else:
                return 5 - edit_index_input

        elif curr_action == 'insert':
            if edit_index_input >= 4:  # same penalty for 5th letter and further
                return 2
            else:
                if original[action[3]] == original[action[4]]:
                    edit_index_input += 1

                return 10 - edit_index_input * 2

        elif curr_action == 'delete':
            if edit_index_input >= 4:  # same penalty for 5th letter and further
                return 2
            else:
                return 10 - (edit_index_input + 1) * 2

    return 0


def get_score(input_str: str, original: str):

    actions = difflib.SequenceMatcher(None, input_str, original).get_opcodes()

    clean_actions = del_prefix_suffix_insert(actions)

    score = get_good_letters_num(clean_actions) * 2

    clean_actions = del_equal(clean_actions)

    if len(clean_actions) > 1:
        return -math.inf

    score -= get_penalty(clean_actions, original)

    return score



s1 = "tobe or no"
s2 = "word to be or not to be"

print(get_score_dl(s1, s2))




