"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
import calendar
from datetime import datetime,date



class State(rx.State):

    columns: list[str] = ["Mon", "Tue","Wen","Thu","Fri","Sat","Sun"]

    months:dict[int,str]={
                    1: "January", 2: "February", 3: "March", 4: "April",
                    5: "May", 6: "June", 7: "July", 8: "August",
                    9: "September", 10: "October", 11: "November", 12: "December"
                }

            
    current_year: int = datetime.today().year
    current_month: int = datetime.today().month
    

    def next_month(self):
        """Increment the month and update the state"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1

    def prev_month(self):
        """Decrement the month and update the state"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1

    def next_year(self):
        self.current_year += 1

    def prev_year(self):
        self.current_year -= 1

    def open_popover(self):
        return

    def change_month(self, month_num:int):
        self.current_month=int(month_num)


    @rx.var(cache=True)
    def current_month_str(self)->str:
        return f'{calendar.month_name[self.current_month]} {self.current_year}'

    @rx.var(cache=True)
    def months_days_range(self,)->list[int]:
        cal=calendar.Calendar()
        days_of_the_month = [int(day.day) for day in cal.itermonthdates(self.current_year, self.current_month)]
        return days_of_the_month


    # def get_datetime(self,)->str:
    #     yearmonth = str(self.current_year) + str(self.current_month)
    #     return yearmonth

    
def display_months(month:list):
    return rx.card(
                rx.link(month[1]),
                on_click=State.change_month(month[0])
            )

def display_days(days:list):
    return rx.card(
                open_drawer(rx.link(days[0]),days[1])
                ,height="10vh"
            )

def open_dialog(button:rx.Component,date:str)->rx.Component:

    return rx.dialog.root(
            rx.dialog.trigger(button),
            rx.dialog.content(
                rx.dialog.title(date),
                rx.text_area(
                    placeholder="Enter your task",
                ),
            rx.dialog.close(
                rx.button("Add", size="3",color_scheme="mint",padding_top="2px"),
            ),
            spacing="3",
            justify="end",
        ),
    )


def open_drawer(link:rx.Component, day:int)->rx.Component:

    render_text = rx.text(f'{day}-{State.current_month}-{State.current_year}')

    return rx.drawer.root(
                rx.drawer.trigger(link),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(                 
                            rx.vstack(
                                rx.box(
                                    rx.drawer.close(
                                        rx.button("Close",color_scheme="mint")
                                    )
                                ),
                                rx.box(open_dialog(rx.button(
                                                    "+ Add Schedule",
                                                    color_scheme="mint",
                                                    width="10em"),render_text)
                                    ),
                            ),
      
                        top="auto",
                        right="auto",
                        height="100%",
                        width="15em",
                        padding="2em",
                        background_color="#F7F9F2"
                    ),
                    
                ),
                direction="left",
            )

def mycalendar() -> rx.Component:
    # Calendar Page
    return rx.container(
     
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.popover.root(
                rx.popover.trigger(
                    rx.link(
                        rx.heading(State.current_month_str, color="#91DDCF", size="6"),
                        on_click=State.open_popover),  
                ),
                rx.popover.content(
                    rx.flex(
                        rx.grid(
                            rx.foreach(
                                    State.months,
                                    display_months
                                ),
                            columns="3",
                            spacing="4",
                            width="100%",
                        )
                    ),
                ),
            ),
            rx.hstack(
               rx.button(
                "<< Previous Month ", on_click=State.prev_month,
                                    color_scheme="mint"
            ),
                rx.button(
                "Next Month >>", on_click=State.next_month,
                                color_scheme="mint"
            ),
             rx.button(
                "<< Previous Year ", on_click=State.prev_year,
                color_scheme="mint"
            ),
                rx.button(
                "Next Year >>", on_click=State.next_year,
                color_scheme="mint"
            ),
            id="box-button"
            ),
              #Weeks Day
            rx.grid(
                rx.foreach(
                    State.columns,
                    lambda i: rx.box(rx.card(i,background_color="#F7F9F2"))
                    ),
                columns="7",  # 7 columns for days of week
                spacing="4",
                width="100%",
                gap=0,
            ),
            #Month Days
            rx.grid(
                rx.foreach(
                    State.months_days_range,  # For days in a month
                    lambda i: rx.box(
                                    rx.card(
                                            open_drawer(rx.link(i,
                                                                size="5",
                                                                color_scheme="mint")
                                                                ,i
                                                        ),  # Extract only the day number
                                            height="10vh",
                                            background_color="#F7F9F2",
                                        ), 
                                ),
                        ),
                        columns="7",  # 7 columns for days of week
                        spacing="4",
                        width="100%",
                        gap=0,
            ),
            id="vstack-box",
            spacing="5",
            justify="start",
            min_height="85vh",
            padding_top ="50px",
        ),
    )


def index() -> rx.Component:
    # Welcome Page (Index)
    return mycalendar()
    

app = rx.App()
app.add_page(index)
