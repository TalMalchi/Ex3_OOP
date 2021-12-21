import math

from src.GraphAlgo import GraphAlgo
from src.DiGraph import DiGraph
import pygame as pg
from pygame.locals import *
from src.DiGraph import DiGraph
from src.NodeData import NodeData
from sympy import symbols, Eq, solve


def normalize_x(screen_x_size, currNodeVal) -> float:
    return (currNodeVal - NodeData.min_value['x']) / (
            NodeData.max_value['x'] - NodeData.min_value['x']) * (screen_x_size - 20) + 10


def normalize_y(screen_y_size, currNodeVal) -> float:
    return (currNodeVal - NodeData.min_value['y']) / (
            NodeData.max_value['y'] - NodeData.min_value['y']) * (screen_y_size - 20) + 10


def drawArrowForEdge(screen, screen_x_size, screen_y_size, src_node_x, src_node_y, dest_node_x, dest_node_y):
    # m = (dest_node_y - src_node_y) / (dest_node_x - src_node_x)
    # b = dest_node_y - (m * dest_node_x)
    # # for linear function y = mx + b (see wiki for explanation)
    #
    # # finding B (see wiki for explanation)
    # x, y = symbols('x,y')
    # equation1 = Eq((y - (m * x)), b)
    #
    # c_length = 5
    # equation2 = (((dest_node_y - y) ** 2 + (dest_node_x - x) ** 2), c_length ** 2)
    #
    # b_point = solve((equation1, equation2), (x, y))
    #
    # # choose min distance from C, as it is the only point that is of interest to us (see more info on names in wiki)
    # dist1 = math.sqrt((src_node_x - b_point[0][0]) + (src_node_y - b_point[0][1]))
    # dist2 = math.sqrt((src_node_x - b_point[1][0]) + (src_node_y - b_point[1][1]))
    # if dist1 < dist2:
    #     b_point = [b_point[0][0], b_point[0][1]]
    # else:
    #     b_point = [b_point[1][0], b_point[1][1]]
    #
    # # finding D (the desired node) (see more info on names in wiki)
    # a_length = math.tan(30) * c_length
    # a_m = -1.0 / m
    # a_b = b_point['y'] - (a_m * b_point['x'])
    #
    # x, y = symbols('x,y')
    # equation1 = Eq((y - (a_m * x)), a_b)
    #
    # equation2 = (((b_point['y'] - y) ** 2 + (b_point['x'] - x) ** 2), a_length ** 2)
    # d_point = solve((equation1, equation2), (x, y))
    # first_point = d_point[0]
    # second_point = d_point[1]
    #
    # first_point = [normalize_x(screen_x_size, first_point[0]), normalize_y(screen_y_size, first_point[1])]
    # second_point = [normalize_x(screen_x_size, second_point[0]), normalize_y(screen_y_size, second_point[1])]
    #
    # pg.draw.line(screen, (0, 0, 0), (first_point[0], second_point[1]), (dest_node_x, dest_node_y), 2)
    # pg.draw.line(screen, (0, 0, 0), (second_point[0], second_point[1]), (dest_node_x, dest_node_y), 2)
    start = (src_node_x, src_node_y)
    end = (dest_node_x, dest_node_y)
    rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
    pg.draw.polygon(screen, (0, 0, 0), (
        (end[0] + 5 * math.sin(math.radians(rotation)), end[1] + 5 * math.cos(math.radians(rotation))),
        (end[0] + 5 * math.sin(math.radians(rotation - 120)), end[1] + 5 * math.cos(math.radians(rotation - 120))),
        (end[0] + 5 * math.sin(math.radians(rotation + 120)), end[1] + 5 * math.cos(math.radians(rotation + 120)))), 2)


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
            pg.display.update()  # update screen
            return GUI.circle_rad

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

                # m = (dest_node_y - src_node_y) / (dest_node_x - src_node_x)
                # b = dest_node_y - (m * dest_node_x)

                pg.draw.line(screen, (0, 0, 0), (src_node_x, src_node_y), (dest_node_x, dest_node_y), 2)
                drawArrowForEdge(screen, screen_x_size, screen_y_size, src_node_x, src_node_y, dest_node_x, dest_node_y)

    def init_gui(self):
        pg.init()
        screen_x_size = 800
        screen_y_size = 600
        screen = pg.display.set_mode((screen_x_size + 20, screen_y_size + 20), HWSURFACE | DOUBLEBUF | RESIZABLE)
        screen.fill((255, 255, 255))  # white background
        self.draw_graph_nodes(screen, screen_x_size, screen_y_size)
        self.draw_graph_edges(screen, screen_x_size, screen_y_size)
        pg.display.update()

        running = True
        while running:  # main pygame loop, always include this
            for event in pg.event.get():  # required for OS events
                if event.type == pg.QUIT:  # user closed window
                    running = False
                elif event.type == VIDEORESIZE:
                    screen.fill((255, 255, 255))  # white background
                    circle_rad = self.draw_graph_nodes(screen, pg.display.Info().current_w, pg.display.Info().current_h)
                    self.draw_graph_edges(screen, pg.display.Info().current_w, pg.display.Info().current_h, circle_rad)
                    pg.display.update()
