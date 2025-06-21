import reflex as rx
from rxconfig import config
from .header import header
from .main_content import main_content_area

def index() -> rx.Component:
    return rx.box(
        rx.vstack(
            header(),
            main_content_area(),
            width="90vw",
            height="90vh",
            border="2px solid #4A90E2",
            border_radius="15px",
            spacing="1",
            overflow="hidden",
        ),
        width="100vw",
        height="100vh",
        display="flex",
        align_items="center",
        justify_content="center",
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        margin="0",
        padding="0",
    )

app = rx.App(
    theme=rx.theme(
        accent_color="violet",
        gray_color="slate",
        styles={
            "*": {
                "margin": "0",
                "padding": "0",
                "boxSizing": "border-box",
            },
            "html, body": {
                "height": "100%",
                "width": "100%",
                "overflow": "hidden",
                "fontFamily": "system-ui, -apple-system, sans-serif",
            },
            "body": {
                "&::-webkit-scrollbar": {
                    "display": "none",
                },
                "scrollbarWidth": "none",
                "msOverflowStyle": "none",
            },
        },
    ),
)
app.add_page(index) 