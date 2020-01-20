import nltk
from collections import Counter
import matplotlib.pyplot as plt
import statistics
import seaborn as sns

# Only needed on the first run
# nltk.download('stopwords')
# nltk.download('universal_tagset')

def read_chapters():
    chapters = ['']
    last_chapter = -1

    with open('little-women.txt') as file:
        for line in file:
            if 'CHAPTER' in line:
                last_chapter += 1
                chapters.append('')
            elif last_chapter >= 0:
                chapters[last_chapter] += ' '
                chapters[last_chapter] += line.strip()
    return chapters

def read_parts():
    parts = ['']
    last_chapter = 0

    with open('little-women.txt') as file:
        for line in file:
            if 'LITTLE WOMEN PART 2' in line:
                last_chapter += 1
                parts.append('')
            else:
                parts[last_chapter] += ' '
                parts[last_chapter] += line.strip()
    return parts

def count_characters(chapters):
    characters = {'Amy': [], 'Jo': [], 'Meg': [], 'Beth': [], 'Laurie': []}
    for chapter in chapters:
        characters_chapter = {'Amy': 0, 'Jo': 0, 'Meg': 0, 'Beth': 0, 'Laurie': 0}
        for word in chapter.split():
            if word in characters:
                characters_chapter[word] = characters_chapter.get(word, 0) + 1
        for name, val in characters.items():
            characters[name].append(characters_chapter[name])


    # Average over every 6 chapters to smooth out the graph
    averaged_characters = {'Amy': [], 'Jo': [], 'Meg': [], 'Beth': [], 'Laurie': []}

    for name, counts in characters.items():
        i = 1
        to_average = []
        indices = []
        for num in counts:
            to_average.append(num)
            if i % 6 == 0:
                averaged_characters[name].append(statistics.mean(to_average))
                to_average = []
                indices.append(i)
            i += 1

    sns.set()
    for name, counts in averaged_characters.items():
        ax = sns.lineplot(indices, counts, label=name)
    plt.legend()
    ax.set(xlabel='Chapter', ylabel='Mentions')
    plt.show()

def get_top_nouns(all_text):
    words_tagged = nltk.pos_tag(nltk.word_tokenize(all_text.lower()), tagset='universal')
    words = [word[0] for word in words_tagged if word[1] == 'NOUN' and word[0] not in ['teddy','professor','one','nothing','day','anything','something','amy','jo','laurie','beth','meg','march','mrs.','mr.','john','things','way','brooke','hannah','laurence','miss','bhaer','i','kate','demi','moffat','sallie']]

    counter = Counter()
    for word in words:
        counter[word] += 1

    return counter


def get_most_distinctive(part, whole):
    ratios = {}
    for word, count in part.items():
        if count > 25 and word in whole:
            ratios[word] = count / whole[word]

    sorted_words = sorted(ratios.items(), key=
    lambda kv: (kv[1], kv[0]), reverse=True)

    return sorted_words[:10]

def get_counts_parts(parts):
    counts_part1 = get_top_nouns(parts[0])
    counts_part2 = get_top_nouns(parts[1])
    counts_all = get_top_nouns(parts[0] + parts[1])

    print('most distinctive part 1')
    part1 = get_most_distinctive(counts_part1, counts_all)

    print('most distinctive part 2')
    part2 = get_most_distinctive(counts_part2, counts_all)

    print('+------------------------+------------------------+')
    print('| PART 1                 | PART 2                 |')
    print('+------------------------+------------------------+')
    for i in range(10):
        print('| {:<18}'.format(part1[i][0]), end='')
        print("{:.2f} ".format(part1[i][1]), end='')
        print('| {:<18}'.format(part2[i][0]), end='')
        print("{:.2f} |".format(part2[i][1]))
    print('+------------------------+------------------------+')

if __name__ == "__main__":
    chapters = read_chapters()
    count_characters(chapters)

    parts = read_parts()
    get_counts_parts(parts)



