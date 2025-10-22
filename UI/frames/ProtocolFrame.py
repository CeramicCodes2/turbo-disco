
from asciimatics.widgets import Frame, Layout, Label, ListBox, Divider,TextBox
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import StopApplication, NextScene
from asciimatics.scene import Scene
class ProtocolFrame(Frame):
    def __init__(self, screen, model,ip_index=0):
        # parents y protocols frame
        super(ProtocolFrame, self).__init__(screen, 20, screen.width, has_border=True, name="Protocol Submenu")
        self.model = model
        self.ip_index = ip_index
        ip, parent, protocols = self.model.cachered_ips[ip_index]
        self.selection_item:int|None = None
        layout = Layout([1])
        self.add_layout(layout)
        layout.add_widget(Label(f"Protocolos para IP: {ip}"))
        layout.add_widget(Divider())
        self.items = ListBox(
            height=6,
            options=[(protocol, i) for i, protocol in enumerate(protocols)],
            name="protocols",
            add_scroll_bar=True
        )
        layout.add_widget(self.items)
        layout.add_widget(Divider())
        layout.add_widget(Label("Presiona Q para regresar"))
        self.fix()
    def _on_select(self):
        # logica de si es una direccion ip o puerto
        ...
    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('Q'), ord('q')]:
                raise NextScene("main")
            if event.key_code == 10:
                # enter
                self.selection_item =  self.items.value
        return super(ProtocolFrame, self).process_event(event)