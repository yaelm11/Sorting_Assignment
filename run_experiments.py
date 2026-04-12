import random
import time
import statistics
import random
import matplotlib.pyplot as plt
import argparse


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # comparing the current key to his neighbor
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]  # shift right the bigger value
            j -= 1
        arr[j + 1] = key  # insert the key to it's right location
    return arr


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False  # help to stop early if array is already sorted
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # swapped
                swapped = True
        if not swapped:
            break
    return arr


def merge_sort(arr):
    #  stop condition if array is soretd / ends
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2

    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    #  merging the sorted arrays
    return merge(left_half, right_half)


def merge(left, right):
    result = []
    i = j = 0

    # choosing the smallest in array
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    #  add the remain numbers (if there are ones)
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def generate_nearly_sorted(n, noise_percentage):
    arr = list(range(n))
    num_swaps = int((n * (noise_percentage / 100)) / 2)

    # swap items
    for i in range(num_swaps):
        idx1 = random.randint(0, n - 1)
        idx2 = random.randint(0, n - 1)
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
    return arr


def plot_results(array_sizes, summary_results, filename, nois_per):
    plt.figure(figsize=(10, 6))

    for name, data in summary_results.items():
        means = data['means']
        stds = data['stds']

        plt.plot(array_sizes, means, label=name, marker='o')

        # coloring the stds
        lower_bound = [m - s for m, s in zip(means, stds)]
        upper_bound = [m + s for m, s in zip(means, stds)]
        plt.fill_between(array_sizes, lower_bound, upper_bound, alpha=0.2)

    plt.xlabel('Array size (n)')
    plt.ylabel('Runtime (seconds)')
    if nois_per == 0:
        plt.title('Runtime Comparison (Random Arrays)')
    else:
        plt.title(f'Runtime Comparison (Nearly sorted, noise ={nois_per}%)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    # שמירת הקובץ כפי שנדרש בהוראות
    plt.savefig(filename)
    plt.show()


def main(algorithms, iterations, array_sizes, file_name, is_random, noise_per=0):
    summary_results = {name: {'means': [], 'stds': []} for name in algorithms}

    for arr_size in array_sizes:
        for name, sort_func in algorithms.items():
            runtimes = []
            for i in range(iterations):
                if is_random:
                    # create random array
                    test_array = [random.randint(0, 1000000) for _ in range(arr_size)]
                else:
                    test_array = generate_nearly_sorted(arr_size, noise_per)
                # measure time
                start = time.perf_counter()
                sort_func(test_array.copy())  # using copy so the original array will not change
                duration = time.perf_counter() - start
                runtimes.append(duration)

            # calculate avg,stds for each sort func
            summary_results[name]['means'].append(statistics.mean(runtimes))
            summary_results[name]['stds'].append(statistics.stdev(runtimes))

    plot_results(array_sizes, summary_results, file_name, noise_per)

def parse_algo_to_exec(ids, algo_map,algorithms):
    updated_dict = {}
    for id in ids:
        if id in algo_map.keys():
            updated_dict[algo_map[id]] = algorithms[algo_map[id]]
    return updated_dict



if __name__ == '__main__':
    algorithms = {
        'bubble_sort': bubble_sort,
        'insertion_sort': insertion_sort,
        'merge_sort': merge_sort
    }
    # mapping of sort kind
    algo_map = {
        '1': 'bubble_sort',
        '3': 'insertion_sort',
        '4': 'merge_sort'
    }
    array_sizes = [100, 500, 1000, 2500, 5000]
    iterations = 5  # to get correct average will repeat every size 5 times

    # part D:
    parser = argparse.ArgumentParser(description="Run sorting experiments")

    parser.add_argument("-a", "--algorithms", type=str,nargs='+', help="Algorithm IDs (e.g., 125)")
    parser.add_argument("-s", "--sizes", type=int, nargs='+', help="Array sizes")
    parser.add_argument("-e", "--experiment", type=int, choices=[1, 2], help="1: 5% noise, 2: 20% noise")
    parser.add_argument("-r", "--repetitions", type=int, default=1, help="Number of repetitions")

    args = parser.parse_args()
    # insert values to variables
    array_sizes_arg = args.sizes if args.sizes else [100, 500, 1000]  # default values if none was given
    reps = args.repetitions if args.repetitions else 1 # number or repetitions
    if args.experiment == 1:
        noise = 5
    elif args.experiment == 2:
        noise = 20
    else:
        noise = 0
    is_random = True if noise == 0 else False



    #  running exp
    if args.algorithms:
        for k in args.algorithms:
            if k not in algo_map.keys():
                print("algorithm isn't supported")
                exit()
        algo_parsed = parse_algo_to_exec(args.algorithms,algo_map,algorithms)
        main(algo_parsed,reps,array_sizes_arg,'result_cmd.png',is_random,noise)
    else:
        print("no argument given- running B,C task")
        main(algorithms, iterations, array_sizes, 'result1.png', True)  # part B
        main(algorithms, iterations, array_sizes, 'result2.png', False, 5)  # part C






