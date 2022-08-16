from shuangpin import (
    get_random_digraph_initial_layout,
    get_random_final_layout,
    get_random_zero_consonant_final_layout,
    get_score,
    xiaohe_config,
    qwerty_layout,
    digraph_initials,
    Key,
    get_fixed_final_keys,
)
import random
from dataclasses import dataclass, replace
from utils import random_choice_except_index


@dataclass
class Chromosome:
    final_keys: list[str]
    digraph_initial_keys: list[str]
    zero_consonant_final_keys: list[tuple[str, str]]


def final_keys_to_layout(keys: list[str]) -> dict[str, str]:
    return {final: keys[i] for i, final in enumerate(xiaohe_config.final_layout.keys())}


def digraph_initial_keys_to_layout(keys: list[str]) -> dict[str, str]:
    return {
        digraph_initial: keys[i]
        for i, digraph_initial in enumerate(xiaohe_config.digraph_initial_layout.keys())
    }


def zero_consonant_final_keys_to_layout(
    keys: list[tuple[str, str]]
) -> dict[str, tuple[str, str]]:
    return {
        zero_consonant_final: keys[i]
        for i, zero_consonant_final in enumerate(
            xiaohe_config.zero_consonant_final_layout.keys()
        )
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


def print_zero_consonant_final_keys(zero_consonant_final_keys: list[tuple[str, str]]):
    zero_consonant_final_layout = zero_consonant_final_keys_to_layout(
        zero_consonant_final_keys
    )
    print(
        "\t".join(
            map(
                lambda item: item[0] + ":" + item[1][0] + item[1][1],
                zero_consonant_final_layout.items(),
            )
        )
    )


def print_chromosome(chromosome: Chromosome):
    print_final_keys(chromosome.final_keys)
    print()
    print_digraph_initial_keys(chromosome.digraph_initial_keys)
    print()
    print_zero_consonant_final_keys(chromosome.zero_consonant_final_keys)
    print("\n" + "-" * 30 + "\n", flush=True)


def get_random_chromosome():
    return Chromosome(
        final_keys=list(
            get_random_final_layout(
                xiaohe_config.final_layout, xiaohe_config.variant_to_standard_finals
            ).values()
        ),
        digraph_initial_keys=list(get_random_digraph_initial_layout().values()),
        zero_consonant_final_keys=list(
            get_random_zero_consonant_final_layout(
                xiaohe_config.zero_consonant_final_layout
            ).values()
        ),
    )


def score_chromosome(chromosome: Chromosome) -> float:
    return get_score(
        replace(
            xiaohe_config,
            final_layout=final_keys_to_layout(chromosome.final_keys),
            digraph_initial_layout=digraph_initial_keys_to_layout(
                chromosome.digraph_initial_keys
            ),
            zero_consonant_final_layout=zero_consonant_final_keys_to_layout(
                chromosome.zero_consonant_final_keys
            ),
        )
    )


# must be divisible by 2
initial_pool_size = 4000


# Generate 2,000 random candidate chromosomes
def initialization():
    return [get_random_chromosome() for _ in range(initial_pool_size)]


# Evaluate each candidate layout and sort them in ascending order
# from lower score (more optimal chromosome) to higher score (less optimal chromosome)
def evaluation(pool: list[Chromosome]):
    return sorted(pool, key=lambda chromosome: score_chromosome(chromosome))


# Select the 1,000 best chromosomes from the sorted chromosome pool
# and add 1,000 new random chromosomes to the pool
def selection(pool: list[Chromosome]):
    return pool[: initial_pool_size // 2] + [
        get_random_chromosome() for _ in range(initial_pool_size // 2)
    ]


def crossover(
    receiver: Chromosome, donor: Chromosome, fixed_final_keys: set[Key]
) -> Chromosome:
    # crossover finals
    final_section_length = random.randint(2, 5)
    final_section_start = random.randint(
        0, len(donor.final_keys) - final_section_length
    )
    final_section_keys = receiver.final_keys[
        final_section_start : final_section_start + final_section_length
    ]
    child_final_keys = receiver.final_keys.copy()
    final_section_keys_ordered_iterator = iter(
        sorted(
            (k for k in final_section_keys if k not in fixed_final_keys),
            key=lambda key: donor.final_keys.index(key),
        )
    )
    final_section_keys_in_donor_order = [
        k if k in fixed_final_keys else next(final_section_keys_ordered_iterator)
        for k in final_section_keys
    ]
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

    # mutate zero-consonant finals in receiver
    # there are only 4 zero-consonant finals that can be remapped
    zero_consonant_final_mutation_index = random.randint(0, 3)
    child_zero_consonant_final_keys = receiver.zero_consonant_final_keys.copy()
    donor_zero_consonant_final_key = donor.zero_consonant_final_keys[
        zero_consonant_final_mutation_index
    ]
    # Only replace with donor's if it doesn't conflict with existing mappings
    if donor_zero_consonant_final_key not in child_zero_consonant_final_keys:
        child_zero_consonant_final_keys[
            zero_consonant_final_mutation_index
        ] = donor_zero_consonant_final_key

    return Chromosome(
        final_keys=child_final_keys,
        digraph_initial_keys=child_digraph_initial_keys,
        zero_consonant_final_keys=child_zero_consonant_final_keys,
    )


def reproduction(
    pool: list[Chromosome], fixed_final_keys: set[Key]
) -> list[Chromosome]:
    parents = pool[:8000]
    for i, receiver in enumerate(parents):
        for _ in range(10):
            donor = random_choice_except_index(parents, i)
            child = crossover(receiver, donor, fixed_final_keys)
            pool.append(child)
    # print("len(pool): ", len(pool))
    return pool


def genetic_algorithm():
    fixed_final_keys = get_fixed_final_keys(
        xiaohe_config.final_layout, xiaohe_config.variant_to_standard_finals
    )
    pool = initialization()
    for i in range(100):
        print(i, score_chromosome(pool[0]))
        print_chromosome(pool[0])

        pool = evaluation(pool)
        pool = selection(pool)
        pool = reproduction(pool, fixed_final_keys)
    return pool[0]


genetic_algorithm()
