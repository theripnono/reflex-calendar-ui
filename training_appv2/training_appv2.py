"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
import calendar
from datetime import datetime
obj=calendar.Calendar()


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
    def get_calendar(self) -> list[list]:  
        weeks = obj.monthdatescalendar(self.current_year, self.current_month)
        month_rows = [[day.day for day in week] for week in weeks]
        return month_rows
    

    @rx.var(cache=True)
    def current_month_str(self)->str:
        return f'{calendar.month_name[self.current_month]} {self.current_year}'

    @rx.var(cache=True)
    def months_days_range(self,)->int:
        days_of_month = calendar.monthrange(self.current_year,self.current_month)[1]

        return days_of_month

def display_months(month:list):
    return rx.card(
                rx.link(month[1]),
                on_click=State.change_month(month[0])
            )


def open_drawer(link:rx.Component)->rx.Component:
    return  rx.drawer.root(
                rx.drawer.trigger(link),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.flex(
                            rx.drawer.close(rx.box(rx.button("Close"))),
                            align_items="start",
                            direction="column",
                        ),
                        top="auto",
                        right="auto",
                        height="100%",
                        width="20em",
                        padding="2em",
                        background_color="teal"
                        # background_color=rx.color("green", 3)
                    )
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
                        rx.heading(State.current_month_str, size="6"),
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
            ),
                rx.button(
                "Next Month >>", on_click=State.next_month,
            ),
             rx.button(
                "<< Previous Year ", on_click=State.prev_year,
            ),
                rx.button(
                "Next Year >>", on_click=State.next_year,
            ),
            id="box-button"
            ),
            rx.grid(
                rx.foreach(
                    rx.Var.range(30),  # For days in a month
                    lambda i: rx.box(
                                    rx.card(
                                            open_drawer(rx.link(f"{i + 1}")),
                                            height="10vh"
                                        ),
                                ),
                        ),
                        columns="7",  # 7 columns for days of week
                        spacing="4",
                        width="100%",
            ),
           
            id="vstack-box",
            spacing="5",
            justify="center",
            min_height="85vh",
            
        ),
        
    )


def index() -> rx.Component:
    # Welcome Page (Index)
    return mycalendar()
    

app = rx.App()
app.add_page(index)
