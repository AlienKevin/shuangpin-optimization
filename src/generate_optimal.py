from shuangpin import (
    ShuangpinConfig,
    get_random_digraph_initial_layout,
    get_random_final_layout,
    get_random_variant_to_standard_finals,
    get_random_zero_consonant_final_layout,
    get_score,
    qwerty_layout,
    digraph_initials,
    fixed_finals_to_keys,
    finals,
    zero_consonant_finals,
)
import random
from dataclasses import dataclass
from utils import random_choice_except_index


@dataclass
class Chromosome:
    final_keys: list[str]
    digraph_initial_keys: list[str]
    zero_consonant_final_keys: list[tuple[str, str]]
    variant_to_standard_finals: dict[str, str]


def final_keys_to_layout(
    keys: list[str], variant_to_standard_finals: dict[str, str]
) -> dict[str, str]:
    standard_finals = [
        final for final in finals if final not in variant_to_standard_finals.keys()
    ]
    return {final: keys[i] for i, final in enumerate(standard_finals)}


def digraph_initial_keys_to_layout(keys: list[str]) -> dict[str, str]:
    return {
        digraph_initial: keys[i] for i, digraph_initial in enumerate(digraph_initials)
    }


def zero_consonant_final_keys_to_layout(
    keys: list[tuple[str, str]]
) -> dict[str, tuple[str, str]]:
    return {
        zero_consonant_final: keys[i]
        for i, zero_consonant_final in enumerate(zero_consonant_finals)
    }


def print_final_keys(final_keys: list[str], variant_to_standard_finals: dict[str, str]):
    final_layout = final_keys_to_layout(final_keys, variant_to_standard_finals)
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


def print_variant_to_standard_finals(variant_to_standard_finals: dict[str, str]):
    print(
        "\t".join(
            map(
                lambda item: item[0] + ":" + item[1], variant_to_standard_finals.items()
            )
        )
    )


def print_chromosome(chromosome: Chromosome):
    print_final_keys(chromosome.final_keys, chromosome.variant_to_standard_finals)
    print()
    print_digraph_initial_keys(chromosome.digraph_initial_keys)
    print()
    print_zero_consonant_final_keys(chromosome.zero_consonant_final_keys)
    print()
    print_variant_to_standard_finals(chromosome.variant_to_standard_finals)
    print("\n" + "-" * 30 + "\n", flush=True)


def get_random_chromosome():
    variant_to_standard_finals = get_random_variant_to_standard_finals()
    return Chromosome(
        final_keys=list(get_random_final_layout(variant_to_standard_finals).values()),
        digraph_initial_keys=list(get_random_digraph_initial_layout().values()),
        zero_consonant_final_keys=list(
            get_random_zero_consonant_final_layout().values()
        ),
        variant_to_standard_finals=variant_to_standard_finals,
    )


def score_chromosome(chromosome: Chromosome) -> float:
    return get_score(
        ShuangpinConfig(
            final_layout=final_keys_to_layout(
                chromosome.final_keys, chromosome.variant_to_standard_finals
            ),
            digraph_initial_layout=digraph_initial_keys_to_layout(
                chromosome.digraph_initial_keys
            ),
            zero_consonant_final_layout=zero_consonant_final_keys_to_layout(
                chromosome.zero_consonant_final_keys
            ),
            variant_to_standard_finals=chromosome.variant_to_standard_finals,
        )
    )


# must be divisible by 2
initial_pool_size = 16000


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


def get_key_by_value(dictionary: dict, value):
    return next(key for key, val in dictionary.items() if val == value)


def crossover(receiver: Chromosome, donor: Chromosome) -> Chromosome:
    # randomly replace one of receiver's variant to standard mapping
    # with the donor's mapping
    # if a fixed variant to standard mapping is chosen, the child's
    # mappings is not mutated
    child_variant_to_standard_finals = receiver.variant_to_standard_finals.copy()
    donor_variant = random.choice(list(donor.variant_to_standard_finals.keys()))
    donor_standard = donor.variant_to_standard_finals[donor_variant]
    if (donor_variant, donor_standard) in child_variant_to_standard_finals.items():
        # Mapping already exists in the receiver. Do nothing.
        pass
    elif donor_variant in child_variant_to_standard_finals.keys():
        if donor_standard in child_variant_to_standard_finals.values():
            receiver_variant = get_key_by_value(
                receiver.variant_to_standard_finals, donor_standard
            )
            # swap the mapping
            (
                child_variant_to_standard_finals[donor_variant],
                child_variant_to_standard_finals[receiver_variant],
            ) = (
                child_variant_to_standard_finals[receiver_variant],
                child_variant_to_standard_finals[donor_variant],
            )
        else:
            child_variant_to_standard_finals[donor_variant] = donor_standard
    elif donor_standard in child_variant_to_standard_finals.values():
        receiver_variant = get_key_by_value(
            receiver.variant_to_standard_finals, donor_standard
        )
        del child_variant_to_standard_finals[receiver_variant]
        child_variant_to_standard_finals[donor_variant] = donor_standard
    else:
        # impossible
        raise Exception("impossible combination of variant and standard finals")
    # print("donor:", donor.variant_to_standard_finals)
    # print("receiver:", receiver.variant_to_standard_finals)
    # print("child:", child_variant_to_standard_finals)

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
            (k for k in final_section_keys if k not in fixed_finals_to_keys.values()),
            key=lambda key: donor.final_keys.index(key),
        )
    )
    final_section_keys_in_donor_order = [
        k
        if k in fixed_finals_to_keys.values()
        else next(final_section_keys_ordered_iterator)
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
        variant_to_standard_finals=child_variant_to_standard_finals,
    )


def reproduction(pool: list[Chromosome]) -> list[Chromosome]:
    parents = pool[: initial_pool_size // 2]
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
