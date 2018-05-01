"""Запуск внешней программы для конвертации файлов jpg к меньшему размеру."""

import os
import subprocess


def locate_and_make_result_dir(name_result_dir):
    """Проверка наличия директории (при необходимости - создания)."""
    result_dir = os.path.join(os.path.dirname(__file__), name_result_dir)
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    return result_dir


def runmultiprocess(source_dir, result_dir, file):
    """Запуск программы конвертации в асинхронном режиме."""
    source_file = os.path.join(source_dir, file)
    result_file = os.path.join(result_dir, file)
    convert_file = os.path.join(os.getcwd(), 'convert.exe')

    if os.path.isfile(result_file):
        os.remove(result_file)

    multiprocess = subprocess.Popen([convert_file,  source_file,
                                     '-resize', '200', result_file])
    return multiprocess


def waitfinishprocess(multiporcesses):
    """Проверка окончания работы запущенных процессов."""
    finish_processes = False
    while not finish_processes:
        finish_processes = True
        for process in multiporcesses:
            if process.poll() is None:
                finish_processes = False
    return finish_processes


def main():
    """Процедура инициализации."""
    multiporcesses = list()
    result_dir = locate_and_make_result_dir('Result')
    source_dir = os.path.join(os.getcwd(), 'Source')
    files = os.listdir(source_dir)

    for file in files:
        multiporcesses.append(runmultiprocess(source_dir, result_dir, file))

    finish_processes = waitfinishprocess(multiporcesses)

    print('Обработка файлов закончена. Результат - {}'.
          format(finish_processes))


main()
