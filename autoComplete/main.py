import autocomplete as ac
import string_compare as str_cmp
import time
import heapq
from math import inf


from collections import Counter


def is_almost_anagram(sentence1: str, sentence2: str) -> bool:
    sentence1 = sentence1.replace(" ", "").lower()
    sentence2 = sentence2.replace(" ", "").lower()

    count1 = Counter(sentence1)
    count2 = Counter(sentence2)

    missing_letters = 0
    for char, count in count1.items():
        if count2[char] < count:
            missing_letters += count - count2[char]
        if missing_letters > 1:
            return False

    return True


def get_top_completions(user_input, sentences, top_n=5):
    best_matches = []

    perfect = 0
    for index in range(len(sentences)):
        if len(user_input) <= len(sentences[index]) and is_almost_anagram(user_input, sentences[index]):
            score = str_cmp.get_score(user_input, sentences[index])
            if score == len(user_input) * 2:
                perfect += 1
            if score != -inf:
                if len(best_matches) < top_n:
                    heapq.heappush(best_matches, (score, index))
                else:
                    heapq.heappushpop(best_matches, (score, index))
            if perfect == top_n:
                break

    top_completions = [sentence[1] for sentence in best_matches]

    return top_completions


def main():
    data = ac.extract_zip_into_database()
    sentences = [sentence['cleaned_line'] for sentence in data]
    s= sentences[:10]
    print("System is online!")

    while True:
        # Get the substring from the user
        user_input = input("Enter your text (or type 'exit' to quit):\n")

        if user_input == 'exit':
            print("Exiting the system.")
            break

        user_input = ac.clean_line(user_input)

        # Start timing the search
        start_time = time.time()

        best_matches = get_top_completions(user_input, sentences)

        # End timing the search
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Print the original lines from filtered results
        if best_matches:
            for i in range(len(best_matches)):
                match_index = best_matches[i]
                # match_index = best_matches[len(best_matches) - i - 1]
                print(f"{i+1}. {data[match_index]['original_line']}"
                      f" ({data[match_index]['file_name']} "
                      f"{data[match_index]['line_number']})")
        else:
            print("No matches found.")

        print(f"Search runtime: {elapsed_time:.2f} seconds")


if __name__ == '__main__':
    main()

