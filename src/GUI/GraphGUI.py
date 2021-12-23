import math
import sys

from src.GUI.Menu import *
import pygame as pg
from pygame.locals import *
from src.GraphAlgo import GraphAlgo
from src.NodeData import NodeData
from src.GUI.Button import Button
from src.GUI.InputField import InputField


def init(g: GraphAlgo):
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


def get_away_from_edge_of_screen(x, y, screen_x_size, screen_y_size):
    if y < 5:
        y += 15
        x += 15
    if x > screen_x_size - 5:
        x -= 15
        y -= 15
    if y > screen_y_size - 5:
        y -= 15
        x += 15
    return x, y


def drawArrowForEdge(screen, screen_x_size, screen_y_size, src_node_x, src_node_y, dest_node_x, dest_node_y, colour):
    """Function to draw an arrowhead in the direction of the line
    adapted from https://stackoverflow.com/questions/43527894/drawing-arrowheads-which-follow-the-direction-of-the-line-in-pygame/43529178"""
    start = (src_node_x, src_node_y)
    end = (dest_node_x, dest_node_y)
    rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
    pg.draw.polygon(screen, colour, (  # drawing a rectangle to represent the arrowhead
        (end[0] + 5 * math.sin(math.radians(rotation)), end[1] + 5 * math.cos(math.radians(rotation))),
        (end[0] + 5 * math.sin(math.radians(rotation - 120)), end[1] + 5 * math.cos(math.radians(rotation - 120))),
        (end[0] + 5 * math.sin(math.radians(rotation + 120)), end[1] + 5 * math.cos(math.radians(rotation + 120)))))


def quadratic(a, b, c):
    x1 = ((-b) + math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    x2 = ((-b) - math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    return x1, x2


class GUI:
    circle_rad = 5

    def __init__(self, gr: GraphAlgo):
        self.graph = gr

    def display_temp_text(self, screen, text: str, pos):
        font = pg.font.SysFont('Arial', 15)
        text_out = font.render(text, True, (0, 0, 0), (255, 255, 255))
        textRect = text_out.get_rect()
        textRect.bottomleft = pos
        screen.blit(text_out, textRect)
        pg.display.update()
        return pg.time.get_ticks()  # starter tick

    def draw_graph_nodes(self, screen, screen_x_size, screen_y_size):
        for node in self.graph.g.get_all_v().values():
            x = node.get_x()
            y = node.get_y()

            # Normalizing values to be between the size of the canvas
            x = normalize_x(screen_x_size, x)
            y = normalize_y(screen_y_size, y)

            pg.draw.circle(screen, (0, 0, 0), (x, y), GUI.circle_rad)

            y -= 15
            x, y = get_away_from_edge_of_screen(x, y, screen_x_size, screen_y_size)
            font = pg.font.SysFont('Arial', 20)
            text = font.render(str(node.get_id()), True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            screen.blit(text, text_rect)

    def draw_one_edge(self, screen, screen_x_size, screen_y_size, edgeSrcID, edgeDestID, colour):
        src_node = self.graph.get_graph().getNode(edgeSrcID)
        src_node_x = src_node.get_x()
        src_node_y = src_node.get_y()
        dest_node = self.graph.get_graph().getNode(edgeDestID)
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

        pg.draw.line(screen, colour, (src_node_x, src_node_y), (dest_node_x, dest_node_y), 2)
        drawArrowForEdge(screen, screen_x_size, screen_y_size, src_node_x, src_node_y, dest_node_x, dest_node_y, colour)

    def draw_graph_edges(self, screen, screen_x_size, screen_y_size):
        for edgeSrcID in self.graph.get_graph().get_all_v().keys():
            for edgeDestID in self.graph.get_graph().all_out_edges_of_node(edgeSrcID).keys():
                self.draw_one_edge(screen, screen_x_size, screen_y_size, edgeSrcID, edgeDestID, (0, 0, 0))

                # x1 = abs(src_node_x + dest_node_x)/2
                # y1 = abs(src_node_y + dest_node_y)/2
                #
                # if m >= 0:
                #     x1 -= 50
                #     y1 -= 50
                #     x1, y1 = get_away_from_edge_of_screen(x1, y1, screen_x_size, screen_y_size)
                # else:
                #     x1 += 50
                #     y1 += 50
                #     x1, y1 = get_away_from_edge_of_screen(x1, y1, screen_x_size, screen_y_size)

                # font = pg.font.SysFont('Arial', 12)
                # text = font.render(str(round(self.graph.get_edge_weight(edgeSrcID, edgeDestID), 3)), True, (255, 0, 0))
                # text_rect = text.get_rect()
                # text_rect.center = (x1+15, y1+15)
                # screen.blit(text, text_rect)

    def redraw(self, screen, screen_x_size, screen_y_size):
        screen.fill((255, 255, 255))  # white background
        self.draw_graph_edges(screen, screen_x_size, screen_y_size)
        self.draw_graph_nodes(screen, screen_x_size, screen_y_size)
        self.button_load.show(screen)
        self.button_center.show(screen)
        self.button_short_path.show(screen)
        self.button_TSP.show(screen)
        pg.display.update()

    def init_gui(self):
        pg.init()
        clock = pg.time.Clock()
        pg.display.set_caption('Graph UI')
        screen_x_size = 800
        screen_y_size = 600
        screen = pg.display.set_mode((screen_x_size, screen_y_size), HWSURFACE | DOUBLEBUF | RESIZABLE)
        screen.fill((255, 255, 255))  # white background
        self.button_load = Button("Load", (0, 0))
        self.button_center = Button("Center Point", ((self.button_load.size[0] + self.button_load.x + 3), 0))
        self.button_short_path = Button("Shortest Path", ((self.button_center.size[0] + self.button_center.x + 3), 0))
        self.button_TSP = Button("TSP", ((self.button_short_path.size[0] + self.button_short_path.x + 3), 0))
        self.redraw(screen, screen_x_size, screen_y_size)
        start_timer = sys.maxsize
        input_box_short_path = InputField(self.button_load.x, self.button_load.y + self.button_load.size[1], 140, 32)
        input_box_tsp = InputField(self.button_load.x, self.button_load.y + self.button_load.size[1], 140, 32)
        short_path_clicked = False
        tsp_clicked = False
        pg.display.update()

        running = True
        while running:  # main pygame loop, always include this
            for event in pg.event.get():  # required for OS events
                if event.type == pg.QUIT:  # user closed window
                    running = False
                elif event.type == VIDEORESIZE:
                    self.redraw(screen, pg.display.Info().current_w, pg.display.Info().current_h)
                    clock.tick(30)
                    pg.display.update()
                elif self.button_load.click(event):  # Load Button functionality
                    tk_root = tk.Tk()
                    tk_root.withdraw()
                    string = askopenfilename(filetypes=[("json", "*.json")])
                    self.graph.load_from_json(string)
                    self.redraw(screen, pg.display.Info().current_w, pg.display.Info().current_h)
                elif self.button_center.click(event):
                    self.redraw(screen, pg.display.Info().current_w, pg.display.Info().current_h)
                    center = self.graph.centerPoint()
                    id = center[0]
                    node = self.graph.get_graph().getNode(id)
                    x = normalize_x(pg.display.Info().current_w, node.get_x())
                    y = normalize_y(pg.display.Info().current_h, node.get_y())
                    pg.draw.circle(screen, (255, 0, 0), (x, y), GUI.circle_rad + 2)
                    string = "The center point with ID: " + str(
                        id) + " has been coloured red, its maximal distance from other nodes is: " + str(center[1])
                    start_timer = self.display_temp_text(screen, string, (
                        self.button_load.x, self.button_load.y + self.button_load.size[1] + 25))
                    pg.display.update()
                elif self.button_short_path.click(event):
                    self.display_temp_text(screen, "Enter two IDs of nodes to calculate, separated by space",
                                           (input_box_short_path.x,
                                            input_box_short_path.y + input_box_short_path.h * 1.5))
                    short_path_clicked = True
                    input_box_short_path.draw(screen)
                    pg.display.update()

                elif self.button_TSP.click(event):
                    self.display_temp_text(screen, "Enter IDs of nodes to calculate TSP, separated by spaces",
                                           (input_box_tsp.x,
                                            input_box_tsp.y + input_box_tsp.h * 1.5))
                    tsp_clicked = True
                    input_box_tsp.draw(screen)
                    pg.display.update()

                input_box_short_path.handle_event(screen, event)
                input_box_tsp.handle_event(screen, event)

            if short_path_clicked:
                input_box_short_path.draw(screen)
            if tsp_clicked:
                input_box_tsp.draw(screen)

            input_box_short_path.update()
            input_box_tsp.update()

            if input_box_short_path.final_text != "":
                string_lst = input_box_short_path.final_text.split(' ')
                input_box_short_path.final_text = ""
                self.redraw(screen, pg.display.Info().current_w, pg.display.Info().current_h)
                if len(string_lst) != 2:
                    start_timer = self.display_temp_text(screen, "Incorrect input!",
                                                         (input_box_short_path.x,
                                                          input_box_short_path.y + input_box_short_path.h * 1.5))
                else:
                    short_path_result = self.graph.shortest_path(int(string_lst[0]), int(string_lst[1]))
                    if short_path_result[0] == float('inf'):
                        string = "A path between the two nodes was not found"
                    else:
                        for i in range(1, len(short_path_result[1])):
                            self.draw_one_edge(screen, pg.display.Info().current_w, pg.display.Info().current_h,
                                               int(short_path_result[1][i - 1]), int(short_path_result[1][i]),
                                               (255, 0, 0))
                        string = "The shortest path between the two nodes was coloured red, its weight is: " + str(
                            short_path_result[0])
                    start_timer = self.display_temp_text(screen, string, (
                        input_box_short_path.x, input_box_short_path.y + input_box_short_path.h * 1.5))

            if input_box_tsp.final_text != "":
                string_lst = input_box_tsp.final_text.split(' ')
                id_lst = []
                for i in range(len(string_lst)):
                    id_lst.append(int(string_lst[i]))
                input_box_tsp.final_text = ""
                self.redraw(screen, pg.display.Info().current_w, pg.display.Info().current_h)
                tsp_result = self.graph.TSP(id_lst)
                if float(tsp_result[1]) == float('inf'):
                    string = "A path between the nodes was not found"
                else:
                    for i in range(1, len(tsp_result[0])):
                        self.draw_one_edge(screen, pg.display.Info().current_w, pg.display.Info().current_h,
                                           int(tsp_result[0][i - 1]), int(tsp_result[0][i]), (255, 0, 0))
                    string = "The shortest path between the list of nodes was coloured red, its weight is: " + str(
                        tsp_result[1])
                start_timer = self.display_temp_text(screen, string,
                                                     (input_box_tsp.x, input_box_tsp.y + input_box_tsp.h * 1.5))
            pg.display.update()

            seconds = (pg.time.get_ticks() - start_timer) / 1000  # calculate how many seconds
            if seconds > 4:
                self.redraw(screen, pg.display.Info().current_w, pg.display.Info().current_h)
