
import Levenshtein as ls

def del_prefix_suffix_insert(input_str: str, actions: list[tuple[str, int, int]]):

    indices_to_del = []

    for i, action in enumerate(actions):

        if action[0] == 'insert' and (action[1] == 0 or action[1] >= len(input_str) - 1):
            indices_to_del.append(i)

    actions = tuple(filter(lambda x: x[0] not in indices_to_del, enumerate(actions)))
    actions = tuple([element[1] for element in actions])

    return actions


def get_cost(input_str: str, original: str) -> int:

    actions = ls.editops(input_str, original)

    actions = del_prefix_suffix_insert(input_str, actions)

    good_letters_num = len(input_str) - len(actions)

    cost = good_letters_num * 2
    print('Base cost: ' + str(cost))

    deduction = 0

    print('Actions: ', end='')
    print(actions)

    for action, _ in zip(actions, range(len(input_str))):

        current_action, edit_index = action[0], action[1]

        if current_action == 'replace':
            if edit_index >= 4:      # same penalty for 5th letter and further
                deduction = 1
            else:
                deduction = 5 - edit_index

            break

        elif current_action == 'delete' or current_action == 'insert':
            if edit_index >= 4:      # same penalty for 5th letter and further
                deduction = 2
            else:
                deduction = 10 - edit_index * 2

            break


    cost -= deduction

    return cost

s1 = "to ze or no"
s2 = "word to be or not to be"

print(get_cost(s1, s2))