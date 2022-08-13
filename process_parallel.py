import json
import re
from pypinyin import lazy_pinyin
import multiprocessing as mp
import os
import sys
import time
import argparse
from dataclasses import dataclass, field
from collections import defaultdict
from typing import TypeAlias

initial_regex = re.compile("(ch|zh|sh|r|c|b|d|g|f|h|k|j|m|l|n|q|p|s|t|w|y|x|z)")


SingleFreqs: TypeAlias = dict[str, int]
PairFreqs: TypeAlias = dict[(str, str), int]


@dataclass
class Freqs:
    single_freqs: SingleFreqs = field(default_factory=lambda: defaultdict(int))
    pair_freqs: PairFreqs = field(default_factory=lambda: defaultdict(int))


def process_line(line, fields):
    freqs = Freqs()
    data = json.loads(line)
    pinyins = lazy_pinyin(
        " ".join(map(lambda field: data[field], fields)), errors="ignore"
    )
    seq = []
    for pinyin in pinyins:
        match_result = initial_regex.match(pinyin)
        if match_result:
            initial = match_result.groups()[0]
            final = pinyin[len(initial) :]
            freqs.single_freqs[initial] += 1
            seq.append(initial)
            if len(final) > 0:
                freqs.single_freqs[final] += 1
                seq.append(final)
        else:
            final = pinyin
            freqs.single_freqs[final] += 1
            seq.append(final)

    for i, component in enumerate(seq):
        if i < len(seq) - 1:
            next = seq[i + 1]
            freqs.pair_freqs[(component, next)] += 1

    return freqs


# Source: https://nurdabolatov.com/parallel-processing-large-file-in-python
def parallel_read(file_name, fields):
    # Maximum number of processes we can run at a time
    cpu_count = mp.cpu_count()
    print("CPU count: {}".format(cpu_count))

    file_size = os.path.getsize(file_name)
    chunk_size = file_size // cpu_count
    print("Source file size: {}".format(file_size))
    print("Operating on chunk size of {}".format(chunk_size))

    # Arguments for each chunk (eg. [('input.txt', 0, 32), ('input.txt', 32, 64)])
    chunk_args = []
    with open(file_name, "rb") as f:

        def is_start_of_line(position):
            if position == 0:
                return True
            # Check whether the previous character is EOL
            f.seek(position - 1)
            previous_byte = int.from_bytes(f.read(1), byteorder=sys.byteorder)
            # 0b0xxxxxxx is the format of an ASCII character
            previous_is_ascii = not (previous_byte & 0x80)
            # If the previous character is an ASCII character, we check if it is EOL
            if previous_is_ascii and previous_byte == ord("\n"):
                # print("Found start of line at {}".format(position))
                return True
            # else we can't be at the start of a line
            else:
                return False

        def get_next_line_position(position):
            # Read the current line till the end
            f.seek(position)
            f.readline()
            # Return a position after reading the line
            return f.tell()

        chunk_start = 0
        # Iterate over all chunks and construct arguments for `process_chunk`
        while chunk_start < file_size:
            chunk_end = min(file_size, chunk_start + chunk_size)
            # print("Tentative chunk end: {}".format(chunk_end))

            # Make sure the chunk ends at the beginning of the next line
            while not is_start_of_line(chunk_end):
                chunk_end -= 1

            # Handle the case when a line is too long to fit the chunk size
            if chunk_start == chunk_end:
                chunk_end = get_next_line_position(chunk_end)

            # Save `process_chunk` arguments
            args = (file_name, fields, chunk_start, chunk_end)
            print("Identified chunk {}-{}".format(chunk_start, chunk_end))
            chunk_args.append(args)

            # Move to the next chunk
            chunk_start = chunk_end

    with mp.Pool(len(chunk_args)) as p:
        # Run chunks in parallel
        chunk_results = p.starmap(process_chunk, chunk_args)

    result = Freqs()
    # Combine chunk results into `results`
    for chunk_result in chunk_results:
        result = union_freqs(result, chunk_result)
    return result


# Source: https://nurdabolatov.com/parallel-processing-large-file-in-python
def process_chunk(file_name, fields, chunk_start, chunk_end):
    print("Processing chunk {}-{}".format(chunk_start, chunk_end))
    chunk_result = Freqs()
    with open(file_name, "r") as f:
        # Moving stream position to `chunk_start`
        f.seek(chunk_start)

        # Read and process lines until `chunk_end`
        for line in f:
            chunk_start += utf8len(line)
            if chunk_start > chunk_end:
                break
            chunk_result = union_freqs(chunk_result, process_line(line, fields))
    return chunk_result


# Source: https://stackoverflow.com/a/30686735/6798201
def utf8len(s):
    return len(s.encode("utf-8"))


def union_freqs(freq1: Freqs, freq2: Freqs):
    return Freqs(
        union_add(freq1.single_freqs, freq2.single_freqs),
        union_add(freq1.pair_freqs, freq2.pair_freqs),
    )


# Source: https://stackoverflow.com/a/11011911/6798201
def union_add(dict1: dict, dict2: dict):
    return {x: dict1.get(x, 0) + dict2.get(x, 0) for x in set(dict1).union(dict2)}


def serialize_freqs(freqs: Freqs):
    serialize_single_freqs(freqs.single_freqs)
    serialize_pair_freqs(freqs.pair_freqs)


def serialize_single_freqs(freqs: SingleFreqs):
    total_count = sum(freqs.values())
    outputs = dict()
    for (key, count) in sorted(freqs.items(), key=lambda x: x[1], reverse=True):
        percent = count / total_count * 100
        if percent > 0.0001:
            print(key + "\t" + "{:.0f}".format(percent))
            outputs[key] = percent
    print()
    with open("single_freqs.json", "w+") as outfile:
        json.dump(outputs, outfile)


def serialize_pair_freqs(freqs: PairFreqs):
    total_count = sum(freqs.values())
    outputs = dict()
    for (key, count) in sorted(freqs.items(), key=lambda x: x[1], reverse=True):
        percent = count / total_count * 100
        if percent > 0.0001:
            print(
                key[0] + "+" + key[1] + "\t" + "{:.4f}".format(percent),
                end="\t",
            )
            outputs[key[0] + "+" + key[1]] = percent
    print()
    with open("pair_freqs.json", "w+") as outfile:
        json.dump(outputs, outfile)


def measure(func, *args):
    time_start = time.time()
    result = func(*args)
    time_end = time.time()
    print(
        "{name} took {time:.0f}s to complete.".format(
            name=func.__name__, time=time_end - time_start
        )
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute the Freqs of Pinyin initials and finals."
    )
    parser.add_argument(
        "source_type",
        type=str,
        help='Type of source to process. Can be one of "news", "zhihu", or "baike".',
    )
    parser.add_argument(
        "-s",
        "--set",
        type=str,
        help='Which set of source to use. For news, can be one of "valid_small" (the first 17367 lines of "valid"), "valid" or "train", defaults to "valid_small". For zhihu, can be one of "small", "testa", "valid", or "train", defaults to "testa". For baike, can be one of "valid" or "train", defaults to "valid".',
    )
    args = parser.parse_args()
    source_type = args.source_type
    source_set = args.set
    if args.set == None:
        if source_type == "news":
            source_set = "valid_small"
        elif source_type == "zhihu":
            source_set = "testa"
        elif source_type == "baike":
            source_set = "valid"
    file_name = ""
    fields = []
    if source_type == "zhihu":
        file_name = "./data/zhihu/web_text_zh_{}.json".format(source_set)
        fields = ["title", "desc", "content"]
    elif source_type == "news":
        file_name = "./data/news/news2016zh_{}.json".format(source_set)
        fields = ["title", "content"]
    elif source_type == "baike":
        file_name = "./data/baike/baike_qa_{}.json".format(source_set)
        fields = ["title", "answer"]
    print(
        "Processing the {} set of {} with fields {}".format(
            source_set, source_type, ", ".join(fields)
        )
    )
    freqs = measure(parallel_read, file_name, fields)
    serialize_freqs(freqs)
