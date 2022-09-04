import pygame
import random
import numpy as np

def draw_cities(cities):
    for city in cities:
        pygame.draw.circle(surface=WIN, color=RED, center=city, radius=5)

def draw_lines_between_cities(cities):
    for i in range(len(cities)-1):
        pygame.draw.line(surface=WIN, color=RED, start_pos=cities[i], end_pos=cities[i+1], width=3)


def calc_dist(p1, p2):
    return np.sqrt((abs(p1[0]-p2[0])**2 + abs(p1[1]-p2[1])**2))

def calc_whole_dist(cities):
    sum = 0
    for i in range(len(cities)-1):
        sum += calc_dist(cities[i], cities[i+1])
    return sum 

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
RED = (255, 30, 70)
FPS = 60
cities_count = 30
cities = []

for i in range(cities_count):
    city = random.randint(0,WIDTH), random.randint(0,HEIGHT)
    cities.append(city)

def salesman_solution(cities):
    for i in range(len(cities)-1):
        shortest = WIDTH+HEIGHT
        for j in range(i+1, len(cities)):
            dist = calc_dist(cities[i], cities[j])
            if dist < shortest:
                #print(dist)
                shortest = dist
                nearest_p = cities[j]
        cities.remove(nearest_p)
        cities.insert(i+1, nearest_p)
        pygame.time.wait(200)
        draw_window()
        #print(cities)
        #print(calc_whole_dist(cities))


def draw_window():
    WIN.fill(WHITE)
    draw_cities(cities)
    draw_lines_between_cities(cities)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    salesman_solution(cities)
    while run:
        #clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()