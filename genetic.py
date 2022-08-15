from shuangpin import (
    get_random_digraph_initial_layout,
    get_random_final_layout,
    get_score,
    xiaohe_config,
    qwerty_layout,
    digraph_initials,
)
import random
from dataclasses import dataclass, replace
from utils import random_choice_except_index


@dataclass
class Chromosome:
    final_keys: list[str]
    digraph_initial_keys: list[str]


def final_keys_to_layout(keys: list[str]) -> dict[str, str]:
    return {final: keys[i] for i, final in enumerate(xiaohe_config.final_layout.keys())}


def digraph_initial_keys_to_layout(keys: list[str]) -> dict[str, str]:
    return {
        digraph_initial: keys[i]
        for i, digraph_initial in enumerate(xiaohe_config.digraph_initial_layout.keys())
    }


def print_final_keys(final_keys: list[str]):
    final_layout = final_keys_to_layout(final_keys)
    # Add the keys not mapped to any final
    for key in qwerty_layout.keys():
        if key not in final_keys:
            final_layout[key] = key
    finals = list(
        map(
            lambda item: item[0],
            sorted(
                final_layout.items(),
                key=lambda item: list(qwerty_layout.keys()).index(item[1]),
            ),
        )
    )
    upper_row = finals[:10]
    home_row = finals[10:19]
    bottom_row = finals[19:26]
    print("\t".join(upper_row))
    print("\t".join(home_row))
    print("\t".join(bottom_row))


def print_digraph_initial_keys(digraph_keys: list[str]):
    print(
        "\t".join(
            map(
                lambda item: item[0] + ":" + item[1],
                zip(digraph_initials, digraph_keys),
            )
        )
    )


def print_chromosome(chromosome: Chromosome):
    print_final_keys(chromosome.final_keys)
    print()
    print_digraph_initial_keys(chromosome.digraph_initial_keys)
    print(flush=True)


def get_random_chromosome():
    return Chromosome(
        final_keys=list(
            get_random_final_layout(
                xiaohe_config.final_layout, xiaohe_config.variant_to_standard_finals
            ).values()
        ),
        digraph_initial_keys=list(get_random_digraph_initial_layout().values()),
    )


def score_chromosome(chromosome: Chromosome) -> float:
    return get_score(
        replace(
            xiaohe_config,
            final_layout=final_keys_to_layout(chromosome.final_keys),
            digraph_initial_layout=digraph_initial_keys_to_layout(
                chromosome.digraph_initial_keys
            ),
        )
    )


# Generate 2,000 random candidate chromosomes
def initialization():
    return [get_random_chromosome() for _ in range(4000)]


# Evaluate each candidate layout and sort them in ascending order
# from lower score (more optimal chromosome) to higher score (less optimal chromosome)
def evaluation(pool: list[Chromosome]):
    return sorted(pool, key=lambda chromosome: score_chromosome(chromosome))


# Select the 1,000 best chromosomes from the sorted chromosome pool
# and add 1,000 new random chromosomes to the pool
def selection(pool: list[Chromosome]):
    return pool[:2000] + [get_random_chromosome() for _ in range(2000)]


def crossover(receiver: Chromosome, donor: Chromosome) -> Chromosome:
    # crossover finals
    final_section_length = random.randint(2, 5)
    final_section_start = random.randint(
        0, len(donor.final_keys) - final_section_length
    )
    final_section_keys = receiver.final_keys[
        final_section_start : final_section_start + final_section_length
    ]
    child_final_keys = receiver.final_keys.copy()
    final_section_keys_in_donor_order = sorted(
        final_section_keys, key=lambda key: donor.final_keys.index(key)
    )
    child_final_keys[
        final_section_start : final_section_start + final_section_length
    ] = final_section_keys_in_donor_order

    # mutate digraph initials in receiver
    # there are only 3 digraph initials in Hanyu Pinyin
    digraph_initial_mutation_index = random.randint(0, 2)
    child_digraph_initial_keys = receiver.digraph_initial_keys.copy()
    donor_digraph_initial_key = donor.digraph_initial_keys[
        digraph_initial_mutation_index
    ]
    # Only replace with donor's if it doesn't conflict with existing mappings
    if donor_digraph_initial_key not in child_digraph_initial_keys:
        child_digraph_initial_keys[
            digraph_initial_mutation_index
        ] = donor_digraph_initial_key
    return Chromosome(
        final_keys=child_final_keys,
        digraph_initial_keys=child_digraph_initial_keys,
    )


def reproduction(pool: list[Chromosome]):
    parents = pool[:2000]
    for i, receiver in enumerate(parents):
        for _ in range(10):
            donor = random_choice_except_index(parents, i)
            child = crossover(receiver, donor)
            pool.append(child)
    # print("len(pool): ", len(pool))
    return pool


def genetic_algorithm():
    pool = initialization()
    for i in range(100):
        print(i, score_chromosome(pool[0]))
        print_chromosome(pool[0])

        pool = evaluation(pool)
        pool = selection(pool)
        pool = reproduction(pool)
    return pool[0]


genetic_algorithm()
