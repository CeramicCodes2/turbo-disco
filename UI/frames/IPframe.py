
from asciimatics.widgets import Frame, Layout, Label, ListBox, Divider,TextBox
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import StopApplication, NextScene
from asciimatics.scene import Scene
class IPFrame(Frame):
    def __init__(self, screen,model):
        super(IPFrame, self).__init__(screen, 30, screen.width, has_border=True, name="IP Selector")
        self.selected_index = 0
        self.model = model

        layout = Layout([1])
        self.add_layout(layout)
        self.msj = Label("Selecciona una IP (O para ver protocolos, I para submenu)")
        layout.add_widget(self.msj)
        layout.add_widget(Divider())
        layout_body = Layout([1, 1])
        self.add_layout(layout_body)

        self.ip_list = ListBox(
            height=4,
            options=[(ip,idx) for idx,ip in enumerate(self.split_ip([ip for ip, _, _ in self.model.cachered_ips]))],
            name="ip_list",
            add_scroll_bar=True,
            on_change=self._on_select
        )
        self.parent_list = ListBox(
            height=4,
            options=[(parent, idx) for idx, (_, parent, _) in enumerate(self.model.cachered_ips)],
            name="parent_list",
            add_scroll_bar=True,
            on_change=self._on_select
        )
        layout_body.add_widget(self.ip_list, column=0)
        layout_body.add_widget(self.parent_list, column=1)

        self.protocol_list = ListBox(
            height=3,
            options=[],
            name="protocol_list",
            add_scroll_bar=True
        )
        layout_body.add_widget(self.protocol_list)
        self.protocol_list.disabled = True
        self.protocols_visible = False
        self.fix()
    @staticmethod
    def Quickshort(req:list[int]):
        fin = []
        if len(req) <= 1:
            return req
        
        pivot = req[-1]
        req.pop(req.index(pivot))    
        left = IPFrame.Quickshort([x for x in req if x <= pivot])
        right = IPFrame.Quickshort([x for x in req if x > pivot])
        fin.extend(left)
        fin.extend([pivot])
        fin.extend(right)
        return fin
    def split_ip(self, ip_str_lst:list[str]) -> list[int]:
        mp = {}
        for ip_str in ip_str_lst:
            lst = [int(octet) for octet in ip_str.split('.')]
            if lst[-1] in list(mp.keys()):
                ip_direction = mp[lst[-1]]
                ip_direction.append(lst)
                continue
                # [[192,168,1,5],[192,168,1,5],...] # si termina con el mismo key (que es el ultimo octeto)
            mp[lst[-1]] = [lst]
            organized_keys = IPFrame.Quickshort(list(mp.keys()))
        final_list = []
        for x in organized_keys:
            for ip in mp[x]:
                # print(f"Joining IP: {ip}")
                final_list.append('.'.join([ str(e) for e in ip ]))
        return final_list
    def on_principal_ip_selected(self):
        # XXX BUG BUSCAR Y ACOPLAR LA IP CON LOS PUERTOS
        self.selected_index = self.ip_list.value
        #self.ip_list.value = f"* {self.ip_list.value}" 
        if self.protocols_visible:
            protocols = ()
            for ip,_,protocols in self.model.cachered_ips:
                if ip == self.ip_list.options[self.selected_index][0]:
                    protocols = protocols
                    break
            self.protocol_list.options = [(protocol, i) for i, protocol in enumerate(protocols)]
    def on_parent_ip_selected(self):
        self.protocol_list.options = []# reseteamos
        self.selected_index = self.parent_list.value
        if self.protocols_visible:
            # search for the parent protocols list
            ...
            #self.protocol_list.options = ['nimpl']
            #_, _, protocols = parent_ips.index(self.parent_list.value)
            self.protocol_list.options = [('nimpl',1)]
            #self.protocol_list.options = [(protocol, i) for i, protocol in enumerate(protocols)]
    def get_focused_layout(self):
        focused_widget = self.focussed_widget
        for layout in self.layouts:
            for column in layout._columns:
                if focused_widget in column:
                    return layout
        return None


    def _on_select(self):
        if self.focussed_widget == self.parent_list:
            return self.on_parent_ip_selected()
        return self.on_principal_ip_selected()
        
    def reload_from_directory(self):
        self.msj.text = "[+] Reloading from directory..."
        self.msj.update(self.screen)
        self.model.cmd.commands.reload_from_directory()
        self.model.mapper.from_core(self.model.repo.repository)
        self.ip_list.options = [(ip,idx) for idx,ip in enumerate(self.split_ip([ip for ip, _, _ in self.model.cachered_ips]))]
        self.parent_list.options = [(parent, idx) for idx, (_, parent, _) in enumerate(self.model.cachered_ips)]
        self.msj.text = "[+] Reloaded. Select an IP (O to view protocols, I for submenu)"
        self.msj.update(self.screen)

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('O'), ord('o')]:
                self.model.cachered_ips
                self.protocols_visible = not self.protocols_visible
                if self.protocols_visible:
                    _, _, protocols = self.model.cachered_ips[self.selected_index]
                    self.protocol_list.options = [(protocol, i) for i, protocol in enumerate(protocols)]
                          
                else:
                    self.protocol_list.options = []
            elif event.key_code in [ord('r'), ord('R')]:
                # reload data from the directory
                self.reload_from_directory()

            elif event.key_code in [ord('I'), ord('i')]:
                raise NextScene("protocols")
            elif event.key_code in [ord('Q'), ord('q')]:
                raise StopApplication("Exit")

                
            elif event.key_code in [ord('S'),ord('s')]:
                raise NextScene("search")
        return super(IPFrame, self).process_event(event)