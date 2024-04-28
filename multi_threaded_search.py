import threading
import time

from boyer_moore_search import boyer_moore_search


def file_search(file_path, keywords, results, lock):
    """Функція пошуку ключових слів у файлі."""
    try:
        with open(file_path, 'r', encoding='windows-1251') as file:
            content = file.read()
        for keyword in keywords:
            position = boyer_moore_search(content, keyword)
            if position != -1:
                with lock:
                    if keyword not in results:
                        results[keyword] = []
                    results[keyword].append(file_path)
    except Exception as e:
        print(f"Не вдалось обробити файл {file_path}: {e}")


def thread_function(file_list, keywords, results, lock):
    """Функція потоку для пошуку ключових слів у списку файлів."""
    for file_path in file_list:
        if isinstance(file_path, str):  # Перевірка на коректність шляху
            file_search(file_path, keywords, results, lock)


def multi_threaded_search(file_paths, keywords):
    """Основна функція для запуску багатопотокового пошуку."""
    start_time = time.time()
    num_threads = min(4, len(file_paths))
    threads = []
    results = {}
    lock = threading.Lock()

    files_per_thread = len(file_paths) // num_threads
    for i in range(num_threads):
        start_index = i * files_per_thread
        end_index = start_index + files_per_thread if i != num_threads - 1 else len(file_paths)
        thread_files = file_paths[start_index:end_index]
        thread = threading.Thread(target=thread_function, args=(thread_files, keywords, results, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Час виконання пошуку: {end_time - start_time:.6f} секунди")
    print(f"Результати пошуку: {results}")
    return results


if __name__ == '__main__':
    file_paths = ["files/article1.txt", "files/article2.txt"]  # Список шляхів файлів для пошуку
    keywords = ["структури", "даних"]  # Список ключових слів
    multi_threaded_search(file_paths, keywords)
