from shuangpin import (
    get_random_digraph_initial_layout,
    get_random_final_layout,
    get_score,
    xiaohe_config,
)
import random
from dataclasses import dataclass, replace
from utils import random_choice_except_index


@dataclass
class Chromosome:
    final_keys: list[str]
    digraph_initial_keys: list[str]


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
            final_layout={
                final: chromosome.final_keys[i]
                for i, final in enumerate(xiaohe_config.final_layout.keys())
            },
            digraph_initial_layout={
                digraph_initial: chromosome.digraph_initial_keys[i]
                for i, digraph_initial in enumerate(
                    xiaohe_config.digraph_initial_layout.keys()
                )
            },
        )
    )


# Generate 2,000 random candidate chromosomes
def initialization():
    return [get_random_chromosome() for _ in range(2000)]


# Evaluate each candidate layout and sort them in ascending order
# from lower score (more optimal chromosome) to higher score (less optimal chromosome)
def evaluation(pool: list[Chromosome]):
    return sorted(pool, key=lambda chromosome: score_chromosome(chromosome))


# Select the 1,000 best chromosomes from the sorted chromosome pool
# and add 1,000 new random chromosomes to the pool
def selection(pool: list[Chromosome]):
    return pool[:1000] + [get_random_chromosome() for _ in range(1000)]


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
    child_digraph_initial_keys[
        digraph_initial_mutation_index
    ] = donor.digraph_initial_keys[digraph_initial_mutation_index]
    return Chromosome(
        final_keys=child_final_keys,
        digraph_initial_keys=child_digraph_initial_keys,
    )


def reproduction(pool: list[Chromosome]):
    parents = pool[:1000]
    for i, receiver in enumerate(parents):
        for _ in range(10):
            donor = random_choice_except_index(parents, i)
            child = crossover(receiver, donor)
            pool.append(child)
    print("len(pool): ", len(pool))
    return pool


def genetic_algorithm():
    pool = initialization()
    for i in range(100):
        print(i, score_chromosome(pool[0]))
        pool = evaluation(pool)
        pool = selection(pool)
        pool = reproduction(pool)
    return pool[0]


genetic_algorithm()
