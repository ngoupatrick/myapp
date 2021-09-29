from _imports._config import *

def cmp_choose_menu(component, title = "Navigation: ", list_menu = LIST_MENU, key_component = "main_menu"):    
    return component.radio(title, list_menu, key = key_component)

def cmp_choose_dist(component, title = "Choose a Distance", list_distance = LIST_DISTANCE, key_component = "choix_distance"):    
    return component.radio(title, list_distance, key = key_component)

def cmp_choose_number(component, title = "How many pics to compare", min_val = 2, max_val = 5, val = 3, step = 1, key_component = "choix_number"):
    return component.number_input(
            label = title,
            min_value = min_val,
            max_value = max_val,
            value = val,
            step = step,
            key = key_component
        )

def cmp_choose_graph(component, title = "Choose a plot style", list_plot = LIST_GRAPH, key_component = "choix_plot"):
    return component.radio(title, list_plot, key = key_component)

def cmp_btn_pic(component):
    btn_start = component[0].button("Start", key = "_start")
    btn_stop = component[1].button("Stop", key = "_stop")
    btn_take = component[2].button("Take Picture", key = "_take")
    btn_clear_pict = component[3].button("Clear Picture", key = "_clear")
    return btn_start, btn_stop, btn_take, btn_clear_pict