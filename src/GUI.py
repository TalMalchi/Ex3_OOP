import math

from src.GraphAlgo import GraphAlgo
from src.DiGraph import DiGraph
import pygame as pg
from pygame.locals import *
from src.DiGraph import DiGraph
from src.NodeData import NodeData


class GUI:
    def __init__(self, g: DiGraph):
        self.graph = g

    def normalize_x(self, screen_x_size, currNodeVal) -> float:
        return (currNodeVal - NodeData.min_value['x']) / (
                NodeData.max_value['x'] - NodeData.min_value['x']) * (screen_x_size - 20) + 10

    def normalize_y(self, screen_y_size, currNodeVal) -> float:
        return (currNodeVal - NodeData.min_value['y']) / (
                NodeData.max_value['y'] - NodeData.min_value['y']) * (screen_y_size - 20) + 10

    def draw_graph_nodes(self, screen, screen_x_size, screen_y_size):
        for node in self.graph.get_all_v().values():
            x = node.get_x()
            y = node.get_y()

            # Normalizing values to be between the size of the canvas
            x = self.normalize_x(screen_x_size, x)
            y = self.normalize_y(screen_y_size, y)

            pg.draw.circle(screen, (0, 0, 0), (x, y), 5)
            pg.display.update()  # update screen

    def draw_graph_edges(self, screen, screen_x_size, screen_y_size):
        for edgeSrcID in self.graph.get_all_v().keys():
            for edgeDestID in self.graph.all_out_edges_of_node(edgeSrcID):
                src_node = self.graph.getNode(edgeSrcID)
                src_node_x = src_node.get_x()
                src_node_y = src_node.get_y()
                dest_node = self.graph.getNode(edgeDestID)
                dest_node_x = dest_node.get_x()
                dest_node_y = dest_node.get_y()

                src_node_x = self.normalize_x(screen_x_size, src_node_x)
                src_node_y = self.normalize_y(screen_y_size, src_node_y)
                dest_node_x = self.normalize_x(screen_x_size, dest_node_x)
                dest_node_y = self.normalize_y(screen_y_size, dest_node_y)

                pg.draw.line(screen, (0, 0, 0), (src_node_x, src_node_y), (dest_node_x, dest_node_y), 2)

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
                    self.draw_graph_nodes(screen, pg.display.Info().current_w, pg.display.Info().current_h)
                    pg.display.update()
