import math

import pygame as pg
from pygame.locals import *
from src.DiGraph import DiGraph
from src.NodeData import NodeData


def init(g: DiGraph):
    gui = GUI(g)
    gui.init_gui()


def normalize_x(screen_x_size, currNodeVal) -> float:
    return (currNodeVal - NodeData.min_value['x']) / (
            NodeData.max_value['x'] - NodeData.min_value['x']) * (screen_x_size - 20) + 10


def normalize_y(screen_y_size, currNodeVal) -> float:
    return (currNodeVal - NodeData.min_value['y']) / (
            NodeData.max_value['y'] - NodeData.min_value['y']) * (screen_y_size - 20) + 10


def distance(point1, point2) -> float:
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def drawArrowForEdge(screen, screen_x_size, screen_y_size, src_node_x, src_node_y, dest_node_x, dest_node_y):
    """Function to draw an arrowhead in the direction of the line
    adapted from https://stackoverflow.com/questions/43527894/drawing-arrowheads-which-follow-the-direction-of-the-line-in-pygame/43529178"""
    start = (src_node_x, src_node_y)
    end = (dest_node_x, dest_node_y)
    rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
    pg.draw.polygon(screen, (0, 0, 0), (  # drawing a rectangle to represent the arrowhead
        (end[0] + 5 * math.sin(math.radians(rotation)), end[1] + 5 * math.cos(math.radians(rotation))),
        (end[0] + 5 * math.sin(math.radians(rotation - 120)), end[1] + 5 * math.cos(math.radians(rotation - 120))),
        (end[0] + 5 * math.sin(math.radians(rotation + 120)), end[1] + 5 * math.cos(math.radians(rotation + 120)))))


def quadratic(a, b, c):
    x1 = ((-b) + math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    x2 = ((-b) - math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    return x1, x2


class GUI:
    circle_rad = 5

    def __init__(self, g: DiGraph):
        self.graph = g

    def draw_graph_nodes(self, screen, screen_x_size, screen_y_size):
        for node in self.graph.get_all_v().values():
            x = node.get_x()
            y = node.get_y()

            # Normalizing values to be between the size of the canvas
            x = normalize_x(screen_x_size, x)
            y = normalize_y(screen_y_size, y)

            pg.draw.circle(screen, (0, 0, 0), (x, y), GUI.circle_rad)

            y -= 15
            if y < 5:
                y += 15
                x += 15
            if x > screen_x_size - 5:
                x -= 15
                y -= 15
            if y > screen_y_size - 5:
                y -= 15
                x += 15
            font = pg.font.SysFont('Arial', 20)
            text = font.render(str(node.get_id()), True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            screen.blit(text, text_rect)

    def draw_graph_edges(self, screen, screen_x_size, screen_y_size):
        for edgeSrcID in self.graph.get_all_v().keys():
            for edgeDestID in self.graph.all_out_edges_of_node(edgeSrcID):
                src_node = self.graph.getNode(edgeSrcID)
                src_node_x = src_node.get_x()
                src_node_y = src_node.get_y()
                dest_node = self.graph.getNode(edgeDestID)
                dest_node_x = dest_node.get_x()
                dest_node_y = dest_node.get_y()

                src_node_x = normalize_x(screen_x_size, src_node_x)
                src_node_y = normalize_y(screen_y_size, src_node_y)
                dest_node_x = normalize_x(screen_x_size, dest_node_x)
                dest_node_y = normalize_y(screen_y_size, dest_node_y)

                # Below we find the point on the edge that ends at the circles' circumference, for more info see wiki
                m = (dest_node_y - src_node_y) / (dest_node_x - src_node_x)
                b = dest_node_y - (m * dest_node_x)

                a1 = ((m ** 2) + 1)
                b1 = ((-2) * dest_node_x - (2 * dest_node_y * m) + (2 * m * b))
                c1 = ((dest_node_x ** 2) + (dest_node_y ** 2) - (2 * b * dest_node_y) + (b ** 2) - (
                        (GUI.circle_rad + 5) ** 2))
                x1, x2 = quadratic(a1, b1, c1)
                y1 = (m * x1) + b
                y2 = (m * x2) + b
                point1 = [x1, y1]
                point2 = [x2, y2]
                if distance([src_node_x, src_node_y], point1) < distance([src_node_x, src_node_y], point2):
                    dest_node_x = point1[0]
                    dest_node_y = point1[1]
                else:
                    dest_node_x = point2[0]
                    dest_node_y = point2[1]

                pg.draw.line(screen, (0, 0, 0), (src_node_x, src_node_y), (dest_node_x, dest_node_y), 2)
                drawArrowForEdge(screen, screen_x_size, screen_y_size, src_node_x, src_node_y, dest_node_x, dest_node_y)

    def init_gui(self):
        pg.init()
        clock = pg.time.Clock()
        pg.display.set_caption('Graph UI')
        screen_x_size = 800
        screen_y_size = 600
        screen = pg.display.set_mode((screen_x_size + 20, screen_y_size + 20), HWSURFACE | DOUBLEBUF | RESIZABLE)
        screen.fill((255, 255, 255))  # white background
        self.draw_graph_edges(screen, screen_x_size, screen_y_size)
        self.draw_graph_nodes(screen, screen_x_size, screen_y_size)
        pg.display.update()

        running = True
        while running:  # main pygame loop, always include this
            for event in pg.event.get():  # required for OS events
                if event.type == pg.QUIT:  # user closed window
                    running = False
                elif event.type == VIDEORESIZE:
                    screen.fill((255, 255, 255))  # white background
                    self.draw_graph_nodes(screen, pg.display.Info().current_w, pg.display.Info().current_h)
                    self.draw_graph_edges(screen, pg.display.Info().current_w, pg.display.Info().current_h)
                    clock.tick(30)
                    pg.display.update()
