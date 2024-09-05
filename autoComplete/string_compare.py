
import difflib
import math


def del_prefix_suffix_insert(actions):
    # indices_to_del = []
    #
    # for i, action in enumerate(actions):
    #
    #     if action[0] == 'insert':
    #         indices_to_del.append(i)
    #     else:
    #         break
    # for i, action in zip(range(len(actions) - 1, -1, -1), reversed(actions)):
    #     if action[0] == 'insert':
    #         indices_to_del.append(i)
    #     else:
    #         break
    #
    # clean_actions = tuple(filter(lambda x: x[0] not in indices_to_del, enumerate(actions)))
    # clean_actions = tuple([element[1] for element in clean_actions])

    start_index = 0
    end_index = len(actions)

    # Find the first non-'insert' from the start
    while start_index < end_index and actions[start_index][0] == 'insert':
        start_index += 1

    # Find the first non-'insert' from the end
    while end_index > start_index and actions[end_index - 1][0] == 'insert':
        end_index -= 1

    clean_actions = actions[start_index:end_index]

    return clean_actions

def del_equal(actions):
    # indices_to_del = []
    #
    # for i, action in enumerate(actions):
    #
    #     if action[0] == 'equal':
    #         indices_to_del.append(i)
    #
    #
    #
    # clean_actions = tuple(filter(lambda x: x[0] not in indices_to_del, enumerate(actions)))
    # clean_actions = tuple([element[1] for element in clean_actions])

    clean_actions = list(filter(lambda item: item[0] != 'equal', actions))

    return clean_actions

def get_good_letters_num(actions):
    good_letters_num = 0
    for action in actions:
        if action[0] == 'equal':
            good_letters_num += action[2] - action[1]

    return good_letters_num

def get_penalty(actions, original):

    if len(actions) == 0:
        return 0

    (action,
     start_edit_index_input, end_edit_index_input,
     start_index_original, end_index_original) = actions[0]

    if (len(actions) > 1 or end_edit_index_input - start_edit_index_input > 1
            or end_index_original - start_index_original > 1):
        return math.inf

    if action == 'replace':
        if start_edit_index_input >= 4:  # same penalty for 5th letter and further
            return 1
        else:
            return 5 - start_edit_index_input

    elif action == 'insert':
        if start_edit_index_input >= 4:  # same penalty for 5th letter and further
            return 2
        else:
            # if a same letter appears twice
            if original[start_index_original] == original[end_index_original]:
                start_edit_index_input += 1

            return 10 - start_edit_index_input * 2

    elif action == 'delete':
        if start_edit_index_input >= 4:  # same penalty for 5th letter and further
            return 2
        else:
            return 10 - (start_edit_index_input + 1) * 2



def get_score(input_str: str, original: str):

    actions = difflib.SequenceMatcher(None, input_str, original).get_opcodes()

    clean_actions = del_prefix_suffix_insert(actions)

    score = get_good_letters_num(clean_actions) * 2

    clean_actions = del_equal(clean_actions)

    score -= get_penalty(clean_actions, original)

    return score


if __name__ == '__main__':
    s1 = "to be"
    s2 = "word to be or not to be"

    print(get_score(s1, s2))




