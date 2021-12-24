import math
import sys
import tkinter as tk
from tkinter.filedialog import askopenfilename

import pygame as pg
from pygame.locals import *

from src.GUI.Button import Button
from src.GUI.InputField import InputField
from src.GraphAlgo import GraphAlgo
from src.NodeData import NodeData


def init(g: GraphAlgo):
    """Initializing GUI to be called from outside the class"""
    gui = GUI(g)
    gui.init_gui()


def normalize_x(screen_x_size, currNodeVal) -> float:
    """Normalize the x value according to the current size of the screen"""
    return (currNodeVal - NodeData.min_value['x']) / (
            NodeData.max_value['x'] - NodeData.min_value['x']) * (screen_x_size - 20) + 10


def normalize_y(screen_y_size, currNodeVal) -> float:
    """Normalize the y value according to the current size of the screen"""
    return (currNodeVal - NodeData.min_value['y']) / (
            NodeData.max_value['y'] - NodeData.min_value['y']) * (screen_y_size - 20) + 10


def distance(point1, point2) -> float:
    """Calculate distance between the two points"""
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def get_away_from_edge_of_screen(x, y, screen_x_size, screen_y_size):
    """If a point is too close to one of the edges of the screen, we transfer the values slightly further from the edge,
     so that a value can be presented in a visually pleasant way"""
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
    """Method to calculate the results of a quadratic equation (2 values)"""
    x1 = ((-b) + math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    x2 = ((-b) - math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    return x1, x2


class GUI:
    circle_rad = 5  # a constant radius of most of the nodes

    def __init__(self, gr: GraphAlgo):
        """Basic constructor"""
        self.graph = gr

    def display_temp_text(self, screen, text: str, pos):
        """Display a text received, at a given position (x,y). The text shall always be black, on white background
        (can easily be adapted to any other values). The function returns a timestamp of the time when the text was
        displayed"""
        font = pg.font.SysFont('Arial', 15)
        text_out = font.render(text, True, (0, 0, 0), (255, 255, 255))  # font used
        textRect = text_out.get_rect()  # creating frame box for the text
        textRect.bottomleft = pos  # bottom left corner of the text box
        screen.blit(text_out, textRect)  # print to screen
        pg.display.update()  # update the window
        return pg.time.get_ticks()  # start time

    def draw_graph_nodes(self, screen, screen_x_size, screen_y_size):
        """Plot the nodes of the graph, using normalization mentioned above. """
        for node in self.graph.g.get_all_v().values():
            x = node.get_x()
            y = node.get_y()

            # Normalizing values to be between the size of the canvas
            x = normalize_x(screen_x_size, x)
            y = normalize_y(screen_y_size, y)

            pg.draw.circle(screen, (0, 0, 0), (x, y), GUI.circle_rad)  # drawing the nodes themselves

            # printing the id of the node beside it on the graph
            y -= 15
            x, y = get_away_from_edge_of_screen(x, y, screen_x_size, screen_y_size)
            font = pg.font.SysFont('Arial', 20)
            text = font.render(str(node.get_id()), True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            screen.blit(text, text_rect)

    def draw_one_edge(self, screen, screen_x_size, screen_y_size, edgeSrcID, edgeDestID, colour):
        """Function to plot a single edge according to all the data received by the function."""
        # Setting variables for readability and for effectiveness of the code
        src_node = self.graph.get_graph().getNode(edgeSrcID)
        src_node_x = src_node.get_x()
        src_node_y = src_node.get_y()
        dest_node = self.graph.get_graph().getNode(edgeDestID)
        dest_node_x = dest_node.get_x()
        dest_node_y = dest_node.get_y()

        # Normailizing
        src_node_x = normalize_x(screen_x_size, src_node_x)
        src_node_y = normalize_y(screen_y_size, src_node_y)
        dest_node_x = normalize_x(screen_x_size, dest_node_x)
        dest_node_y = normalize_y(screen_y_size, dest_node_y)

        # Below we find the point on the edge that ends at the circles' circumference, so that the arrow does not
        # seem "inside" the node
        m = (dest_node_y - src_node_y) / (dest_node_x - src_node_x)  # m in the linear function y = mx + b
        b = dest_node_y - (m * dest_node_x)  # b in the linear function y = mx + b

        # After calculations, the needed values to be passed to the quadratic equations
        a1 = ((m ** 2) + 1)
        b1 = ((-2) * dest_node_x - (2 * dest_node_y * m) + (2 * m * b))
        c1 = ((dest_node_x ** 2) + (dest_node_y ** 2) - (2 * b * dest_node_y) + (b ** 2) - (
                (GUI.circle_rad + 5) ** 2))
        x1, x2 = quadratic(a1, b1, c1)

        # Correlating y values to each of the x values
        y1 = (m * x1) + b
        y2 = (m * x2) + b
        point1 = [x1, y1]
        point2 = [x2, y2]

        # Finding the wanted node out of the 2 received
        if distance([src_node_x, src_node_y], point1) < distance([src_node_x, src_node_y], point2):
            dest_node_x = point1[0]
            dest_node_y = point1[1]
        else:
            dest_node_x = point2[0]
            dest_node_y = point2[1]

        # Drawing the line of the arrow
        pg.draw.line(screen, colour, (src_node_x, src_node_y), (dest_node_x, dest_node_y), 2)
        # Drawing the arrowhead
        drawArrowForEdge(screen, screen_x_size, screen_y_size, src_node_x, src_node_y, dest_node_x, dest_node_y, colour)

    def draw_graph_edges(self, screen, screen_x_size, screen_y_size):
        """Function to iterate and plot all edges of the graph """
        for edgeSrcID in self.graph.get_graph().get_all_v().keys():
            try:
                for edgeDestID in self.graph.get_graph().all_out_edges_of_node(edgeSrcID).keys():
                    self.draw_one_edge(screen, screen_x_size, screen_y_size, edgeSrcID, edgeDestID, (0, 0, 0))
            except:
                continue

    def redraw(self, screen, screen_x_size, screen_y_size):
        """After a change has been made, a method to replot the graph and the buttons"""
        screen.fill((255, 255, 255))  # white background
        self.draw_graph_edges(screen, screen_x_size, screen_y_size)
        self.draw_graph_nodes(screen, screen_x_size, screen_y_size)

        # Buttons
        self.button_load.show(screen)
        self.button_center.show(screen)
        self.button_short_path.show(screen)
        self.button_TSP.show(screen)
        pg.display.update()
        return sys.maxsize  # Initializing timer

    def init_gui(self):
        pg.init()
        clock = pg.time.Clock()
        pg.display.set_caption('Graph UI')
        screen_x_size = 800  # Default size of the window
        screen_y_size = 600
        screen = pg.display.set_mode((screen_x_size, screen_y_size), HWSURFACE | DOUBLEBUF | RESIZABLE)
        screen.fill((255, 255, 255))  # white background

        # Initializing buttons
        self.button_load = Button("Load", (0, 0))
        self.button_center = Button("Center Point", ((self.button_load.size[0] + self.button_load.x + 3), 0))
        self.button_short_path = Button("Shortest Path", ((self.button_center.size[0] + self.button_center.x + 3), 0))
        self.button_TSP = Button("TSP", ((self.button_short_path.size[0] + self.button_short_path.x + 3), 0))
        start_timer = self.redraw(screen, screen_x_size, screen_y_size)

        # Initializing input fields
        input_box_short_path = InputField(self.button_load.x, self.button_load.y + self.button_load.size[1], 140, 32)
        input_box_tsp = InputField(self.button_load.x, self.button_load.y + self.button_load.size[1], 140, 32)

        # Initializing flags for future use
        short_path_clicked = False
        tsp_clicked = False
        pg.display.update()

        running = True
        while running:  # main pygame loop
            for event in pg.event.get():  # for each event
                if event.type == pg.QUIT:  # user closed window
                    running = False
                elif event.type == VIDEORESIZE:  # If the window was resized
                    start_timer = self.redraw(screen, pg.display.Info().current_w, pg.display.Info().current_h)
                    clock.tick(30)  # plays up to 30 fps
                    pg.display.update()
                elif self.button_load.click(event):  # Load Button functionality
                    tk_root = tk.Tk()
                    tk_root.withdraw()
                    string = askopenfilename(filetypes=[("json", "*.json")])
                    self.graph.load_from_json(string)
                    start_timer = self.redraw(screen, pg.display.Info().current_w, pg.display.Info().current_h)
                elif self.button_center.click(event):  # Center button functionality
                    start_timer = self.redraw(screen, pg.display.Info().current_w, pg.display.Info().current_h)
                    center = self.graph.centerPoint()  # Calling the function to calculate the center point
                    id = center[0]
                    node = self.graph.get_graph().getNode(id)
                    x = normalize_x(pg.display.Info().current_w, node.get_x())  # Normalizing to plot
                    y = normalize_y(pg.display.Info().current_h, node.get_y())
                    pg.draw.circle(screen, (255, 0, 0), (x, y), GUI.circle_rad + 5)  # plot red circle to represent node
                    string = "The center point with ID: " + str(
                        id) + " has been coloured red, its maximal distance from other nodes is: " + str(center[1])
                    start_timer = self.display_temp_text(screen, string, (
                        self.button_load.x, self.button_load.y + self.button_load.size[1] + 25))
                    pg.display.update()
                elif self.button_short_path.click(event):  # Shortest path functionality
                    self.display_temp_text(screen, "Enter two IDs of nodes to calculate, separated by space",
                                           (input_box_short_path.x,
                                            input_box_short_path.y + input_box_short_path.h * 1.5))
                    short_path_clicked = True
                    input_box_short_path.draw(screen)
                    pg.display.update()

                elif self.button_TSP.click(event):  # TSP button functionality
                    self.display_temp_text(screen, "Enter IDs of nodes to calculate TSP, separated by spaces",
                                           (input_box_tsp.x,
                                            input_box_tsp.y + input_box_tsp.h * 1.5))
                    tsp_clicked = True
                    input_box_tsp.draw(screen)
                    pg.display.update()

                input_box_short_path.handle_event(screen, event)
                input_box_tsp.handle_event(screen, event)

            # If one of the input boxes is clicked
            if short_path_clicked:
                input_box_short_path.draw(screen)
            if tsp_clicked:
                input_box_tsp.draw(screen)

            # Update input boxes
            input_box_short_path.update()
            input_box_tsp.update()

            # if the input box of the short path has ended its loop, and it is not empty
            if input_box_short_path.final_text != "":
                string_lst = input_box_short_path.final_text.split(' ')
                input_box_short_path.final_text = ""
                start_timer = self.redraw(screen, pg.display.Info().current_w, pg.display.Info().current_h)

                # If the user input something invalid, print a corresponding error to the screen
                if len(string_lst) != 2:
                    start_timer = self.display_temp_text(screen, "Incorrect input!",
                                                         (input_box_short_path.x,
                                                          input_box_short_path.y + input_box_short_path.h * 1.5))
                else:
                    # Printing the results if all input is OK
                    short_path_result = self.graph.shortest_path(int(string_lst[0]), int(string_lst[1]))
                    if short_path_result[0] == float('inf'):
                        string = "A path between the two nodes was not found"
                    else:
                        for i in range(1, len(short_path_result[1])):  # plotting edges in red colour
                            self.draw_one_edge(screen, pg.display.Info().current_w, pg.display.Info().current_h,
                                               int(short_path_result[1][i - 1]), int(short_path_result[1][i]),
                                               (255, 0, 0))
                        string = "The shortest path between the two nodes was coloured red, its weight is: " + str(
                            short_path_result[0])
                    start_timer = self.display_temp_text(screen, string, (
                        input_box_short_path.x, input_box_short_path.y + input_box_short_path.h * 1.5))

            # if the input box of the TSP has ended its loop, and it is not empty
            if input_box_tsp.final_text != "":
                string_lst = input_box_tsp.final_text.split(' ')  # Split the string received
                id_lst = []
                for i in range(len(string_lst)):  # Convert string list to int list
                    id_lst.append(int(string_lst[i]))
                input_box_tsp.final_text = ""  # Revert changes made to the input field
                start_timer = self.redraw(screen, pg.display.Info().current_w, pg.display.Info().current_h)
                tsp_result = self.graph.TSP(id_lst)

                # There is no viable path
                if float(tsp_result[1]) == float('inf'):
                    string = "A path between the nodes was not found"
                else:
                    for i in range(1, len(tsp_result[0])):  # Plotting edges in different colour
                        self.draw_one_edge(screen, pg.display.Info().current_w, pg.display.Info().current_h,
                                           int(tsp_result[0][i - 1]), int(tsp_result[0][i]), (255, 0, 0))
                    string = "The shortest path between the list of nodes was coloured red, its weight is: " + str(
                        tsp_result[1])
                start_timer = self.display_temp_text(screen, string,
                                                     (input_box_tsp.x, input_box_tsp.y + input_box_tsp.h * 1.5))
            pg.display.update()

            # Display all texts for 4 seconds
            seconds = (pg.time.get_ticks() - start_timer) / 1000  # calculate how many seconds
            if seconds > 4:
                start_timer = self.redraw(screen, pg.display.Info().current_w, pg.display.Info().current_h)
