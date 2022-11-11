import random 
fish_facts = []

filename = 'fish_facts.txt'
with open(filename, 'r') as f:
    fish_facts = f.readlines()

def get_random_fish_fact():
    return random.choice(fish_facts)


if __name__ == '__main__':
    fact = get_random_fish_fact()
    print(fact)
