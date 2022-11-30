import math
import pygame
import random
pygame.init()


# ------------------------------------------------------------------------------------------------------------------------------------
class DrawInformation:
    # This class is for initializing the attributes which are going to be used
    # throughout the game. It is better than declaring them globally 
    black = 0, 0, 0
    white = 255, 255, 255
    green = 0, 255, 0
    red = 255, 0, 0
    
    bg_color = white

    # Gradients: the three colors bar are going to have
    gradients = [ (128, 128, 128), (160,160,160), (192,192,192) ]   # these are 3 shades of grey

    side_pad = 100      # padding 
    top_pad = 150       # padding

    # Font
    regular_font = pygame.font.SysFont('comicsans', 20)
    large_font = pygame.font.SysFont('comicsans', 30)


    def __init__(self,width,height, sortingList):
        # This constructor is initializing the game's display
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((self.width, self.height))    # creating display
        pygame.display.set_caption("Sorting Algorithm Visualization")

        self.set_list(sortingList)
    
    def set_list(self, lst):
        # This method is setting up the list 
        self.lst = lst
        self.min_val = min(self.lst)
        self.max_val = max(self.lst)

        self.bar_width = (self.width - self.side_pad) / len(self.lst)
        self.bar_height = math.floor((self.height - self.top_pad) / (self.max_val - self.min_val))
        self.start_x = self.side_pad // 2       # to get whole nummber


# ------------------------------------------------------------------------------------------------------------------------------------


def draw(draw_info, algo_name, ascending):
    # This function is going to fill up the game display screen according
    # to our desired characteristics provided
    # 
    # We are filling the screen with bg color, then printing the statement on it 
    # and then at the end, printing the list on it.
    
    draw_info.window.fill(draw_info.bg_color)

    title = draw_info.large_font.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.green)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2,3))

    controls = draw_info.regular_font.render("R - Reset | SPACE - Start Sorting | A - ascending | D - Descending", 1, draw_info.black)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2,35))

    sorting = draw_info.regular_font.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.black)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2,65))


    draw_list(draw_info)        # drawing rectangular list value representation
    pygame.display.update()     # this will draw the updated screen


# ------------------------------------------------------------------------------------------------------------------------------------


def draw_list(draw_info, color_positions = {}, clear_bg = False):
    # this will draw the rectangular bar representation of data of the list
    
    theList = draw_info.lst

    if clear_bg: 
        clear_rect = (draw_info.side_pad//2, draw_info.top_pad, 
                        draw_info.width - draw_info.side_pad, draw_info.height - draw_info.top_pad)     # this is to clear the whole list for a bit 
        pygame.draw.rect(draw_info.window, draw_info.bg_color, clear_rect)


    for i, value in enumerate(theList):
        # enumerate is going to give index and value
        x = draw_info.start_x + i * draw_info.bar_width     # this is the top left x coordinate of the rectangle. This is how rect are made in pygame
        y = draw_info.height - (value - draw_info.min_val) * draw_info.bar_height   # that is range

        color = draw_info.gradients[i%3]    # this is going to give values 0,1,2 and that helps since we only have 3 colors in gradient
        
        if i in color_positions:
            color = color_positions[i]
        
        pygame.draw.rect(draw_info.window, color, (x,y, draw_info.bar_width, draw_info.height))     # calculate precise height please

    if clear_bg:
        pygame.display.update()


# ------------------------------------------------------------------------------------------------------------------------------------


def generate_starting_list(n, min_val, max_val):
    # This function is going to generate an unsorted list with 
    # provided minimum and maximum value 
    unsorted_list = []

    for i in range(n):
        value = random.randint(min_val, max_val)
        unsorted_list.append(value)

    return unsorted_list


# ------------------------------------------------------------------------------------------------------------------------------------


def bubble_sort(draw_info, ascending=True):
    theList = draw_info.lst

    for i in range(len(theList) - 1):
        for j in range(len(theList) - 1 -i):
            num1 = theList[j]
            num2 = theList[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                theList[j], theList[j+1] = theList[j+1], theList[j]
                draw_list(draw_info, {j: draw_info.green, j+1 : draw_info.red}, True)    
                yield True
    
    return theList


# ------------------------------------------------------------------------------------------------------------------------------------


def insertion_sort(draw_info, ascending=True):
    theList = draw_info.lst

    for i in range(1, len(theList)):
        current = theList[i]

        while True:
            ascending_sort = i > 0 and theList[i - 1] > current and ascending
            descending_sort = i > 0 and theList[i-1] < current and not ascending 

            if not ascending_sort and not descending_sort:
                break
            
            theList[i] = theList[i-1]
            i = i-1
            theList[i] = current
            draw_list(draw_info, {i: draw_info.green, i-1: draw_info.red}, True)
            yield True
    return theList 


# ------------------------------------------------------------------------------------------------------------------------------------


def main():
    continue_condition = True
    clock = pygame.time.Clock()
    fps = 60

    #sorting
    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    # For the unsorted list
    n = 50
    min_val = 0
    max_val = 100
    unsorted_list = generate_starting_list(n,min_val,max_val)

    # instantiating the screen
    draw_info = DrawInformation(800, 600, unsorted_list)

    while continue_condition:
        clock.tick(fps)

        if sorting:
            # This right here will continue the sorting
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False

        else:
            draw(draw_info, sorting_algo_name, ascending)     # this is drawing the screen every frame


        for event in pygame.event.get():    
            # this is event.get will get us list of all the events occured
            # since the last time this was called

            if event.type == pygame.QUIT:
                # Hitting the red cross 
                continue_condition = False
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                unsorted_list = generate_starting_list(n,min_val,max_val)
                draw_info.set_list(unsorted_list)   # this is going to reset the list internally in drawing information as well
                sorting = False     # stop sorting if you reset the list
            
            elif event.key == pygame.K_SPACE and sorting == False:
                # This right here will start the sorting 
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info,ascending)
            
            elif event.key == pygame.K_a and (not sorting):
                ascending = True
            elif event.key == pygame.K_d and (not sorting):
                ascending = False
            
            elif event.key == pygame.K_i and (not sorting):
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"

            elif event.key == pygame.K_b and (not sorting):
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

    pygame.quit()

if __name__ == "__main__":
    main()

# Credit:
# video: https://www.youtube.com/watch?v=twRidO-_vqQ