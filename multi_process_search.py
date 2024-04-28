import time
from multiprocessing import Process, Queue

from boyer_moore_search import boyer_moore_search


def file_search(file_path, keywords, results_queue):
    """Функція пошуку ключових слів у файлі."""
    try:
        with open(file_path, 'r', encoding='windows-1251') as file:
            content = file.read()
        for keyword in keywords:
            position = boyer_moore_search(content, keyword)
            if position != -1:
                results_queue.put((keyword, file_path))
    except Exception as e:
        print(f"Не вдалось обробити файл {file_path}: {e}")


def process_function(file_list, keywords, results_queue):
    """Функція процесу для пошуку ключових слів у списку файлів."""
    for file_path in file_list:
        file_search(file_path, keywords, results_queue)


def multi_process_search(file_paths, keywords):
    """Основна функція для запуску багатопроцесорного пошуку."""
    start_time = time.time()
    num_processes = min(4, len(file_paths))  # Кількість процесів
    processes = []
    results_queue = Queue()  # Черга для збору результатів

    files_per_process = len(file_paths) // num_processes
    for i in range(num_processes):
        start_index = i * files_per_process
        end_index = start_index + files_per_process if i != num_processes - 1 else len(file_paths)
        process_files = file_paths[start_index:end_index]
        process = Process(target=process_function, args=(process_files, keywords, results_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Збираємо результати з черги
    results = {}
    while not results_queue.empty():
        keyword, file_path = results_queue.get()
        if keyword not in results:
            results[keyword] = []
        results[keyword].append(file_path)

    end_time = time.time()
    print(f"Час виконання пошуку: {end_time - start_time:.6f} секунди")
    print(f"Результати пошуку: {results}")
    return results


if __name__ == '__main__':
    file_paths = ["files/article1.txt", "files/article2.txt"]  # Список шляхів файлів для пошуку
    keywords = ["структури", "даних"]  # Список ключових слів
    multi_process_search(file_paths, keywords)
