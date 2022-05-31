import pygame
import random

from itertools import repeat

pygame.init()


class GUI:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    BACKGROUND_COLOR = BLACK

    GRADIENT = [
        (0, 255, 0),
        (85, 255, 0),
        (170, 255, 0)
    ]

    SIDE_PAD = 100
    TOP_PAD = 150
    FONT = pygame.font.SysFont("arial", 30)
    LARGE_FONT = pygame.font.SysFont("arial", 40)

    def __init__(self, width, height, arr):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")

        # Leave variable for set_list
        self.arr = None
        self.min_value = 0
        self.max_value = 0
        self.block_width = 0
        self.block_height = 0
        self.starting_x = self.SIDE_PAD // 2
        self.set_list(arr)

    def set_list(self, arr):
        self.arr = arr
        self.min_value = min(arr)
        self.max_value = max(arr)
        self.block_width = (self.width - self.SIDE_PAD) // len(arr)
        self.block_height = (self.height - self.TOP_PAD) // (self.max_value - self.min_value)


def draw(gui, algo_name: str, ascending: bool):
    gui.window.fill(gui.BACKGROUND_COLOR)
    title = gui.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}",
                                  1, gui.BLUE)
    controls = gui.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending",
                               1, gui.WHITE)
    sorting = gui.FONT.render("Q - Quick Sort | B - Bubble Sort | I - Insertion Sort",
                              1, gui.WHITE)
    gui.window.blit(title, (gui.width // 2 - title.get_width() // 2, 5))
    gui.window.blit(controls, (gui.width // 2 - controls.get_width() // 2, 40))
    gui.window.blit(sorting, (gui.width // 2 - sorting.get_width() // 2, 70))
    draw_list(gui)
    pygame.display.update()


def draw_list(gui: GUI, color_position: dict = None, clear_bg: bool = False):
    if color_position is None:
        color_position = {}
    arr = gui.arr
    if clear_bg:
        clear_rect = (gui.SIDE_PAD//2, gui.TOP_PAD,
                      gui.width-gui.SIDE_PAD, gui.height-gui.TOP_PAD)
        pygame.draw.rect(gui.window, gui.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(arr):
        x = gui.starting_x + i * gui.block_width
        y = gui.height - (val - gui.min_value) * gui.block_height

        color = gui.GRADIENT[i % 3]
        if i in color_position:
            color = color_position[i]

        pygame.draw.rect(gui.window, color, (x, y, gui.block_width, gui.height - y))

    if clear_bg:
        pygame.display.update()


def generate_starting_list(n: int, min_value: int, max_value: int):
    arr = list()
    for _ in repeat(None, n):
        arr.append(random.randint(min_value, max_value))

    return arr


def bubble_sort(gui: GUI, ascending: bool):
    arr = gui.arr
    for i in range(len(arr)-1):
        for j in range(len(arr)-1-i):
            num1 = arr[j]
            num2 = arr[j+1]
            if num1 > num2 and ascending or (num1 < num2 and not ascending):
                arr[j], arr[j+1] = arr[j+1], arr[j]
                draw_list(gui, {j: gui.RED, j+1: gui.BLUE}, True)
                yield True


def quick_sort(gui: GUI, ascending: bool):
    # use recursive function and pray it doesn't throw recursion error
    def quicksort(array, start, stop):
        """
        This type of quick sort using 2 pointers
        one point element smaller than pivot and other point bigger than pivot
        until both pointer set, we swap them
        repeat this until both pointer meet
        after this we divide the array then conquer
        repeat this until array of 1 reached
        """
        if stop > start and ascending:
            pivot, left, right = array[start], start, stop
            while left <= right:
                while array[left] < pivot:
                    left += 1
                while array[right] > pivot:
                    right -= 1
                if left <= right:
                    # swap element
                    array[left], array[right] = array[right], array[left]
                    draw_list(gui, {left: gui.RED, right: gui.BLUE}, True)
                    left += 1
                    right -= 1
                    yield True
            yield from quicksort(array, start, right)
            yield from quicksort(array, left, stop)

        if stop > start and not ascending:
            pivot, left, right = array[start], start, stop
            while left <= right:
                while array[left] > pivot:
                    left += 1
                while array[right] < pivot:
                    right -= 1
                if left <= right:
                    array[left], array[right] = array[right], array[left]
                    draw_list(gui, {left: gui.RED, right: gui.BLUE}, True)
                    left += 1
                    right -= 1
                    yield True
            yield from quicksort(array, start, right)
            yield from quicksort(array, left, stop)

    yield from quicksort(gui.arr, 0, len(gui.arr)-1)


def insertion_sort(gui: GUI, ascending: bool):
    # bubble sort but better?
    for i in range(1, len(gui.arr)):
        j = i
        while ((j > 0 and gui.arr[j-1] > gui.arr[j] and ascending)
               or
               (j > 0 and gui.arr[j-1] < gui.arr[j] and not ascending)):
            gui.arr[j], gui.arr[j-1] = gui.arr[j-1], gui.arr[j]
            draw_list(gui, {j: gui.RED, j-1: gui.BLUE}, True)
            j -= 1
            yield True


def main():
    run = True
    clock = pygame.time.Clock()
    fps = 60
    n = 150
    min_value = 1
    max_value = 100
    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    gui = GUI(1000, 600, generate_starting_list(n, min_value, max_value))
    while run:
        clock.tick(fps)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(gui, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                continue

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                gui.set_list(generate_starting_list(n, min_value, max_value))
                sorting = False
                continue
            if event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(gui, ascending)
                continue
            if event.key == pygame.K_a and not sorting:
                ascending = True
                continue
            if event.key == pygame.K_d and not sorting:
                ascending = False
                continue
            if event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
                continue
            if event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
                continue
            if event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
                continue

    pygame.quit()


if __name__ == '__main__':
    main()
