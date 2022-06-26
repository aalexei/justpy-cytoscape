import justpy as jp
import asyncio

class Cytoscape(jp.JustpyBaseComponent):

    vue_type = 'cytoscapejp'
    req_id=0
    futures={}

    def __init__(self, **kwargs):
        self.options = jp.Dict()
        self.classes = ''
        self.style = ''
        self.elements = []
        self.graphstyle = []
        self.plugins = []
        self.layout = {}
        self.clear = False
        self.show = True
        self.event_propagation = True
        self.pages = {}
        kwargs['temp'] = False  # Force an id to be assigned
        super().__init__(**kwargs)
        self.allowed_events = ['free','tap']
        if type(self.options) != jp.Dict:
            self.options = jp.Dict(self.options)
        self.initialize(**kwargs)

    def add_to_page(self, wp: jp.WebPage):
        wp.add_component(self)

    def react(self, data):
        pass

    async def run_method_get_output(self, method, websocket):
        # adapted from https://github.com/elimintz/justpy/discussions/240
        self.req_id += 1
        req_id = f'cyto_{self.req_id}'
        self.futures[req_id]= asyncio.get_running_loop().create_future()

        await websocket.send_json(
            {'type': 'run_javascript',
             'data':f"Object(comp_dict['{self.id}'].{method})",
             'request_id': req_id,
             'send':True}
        )

        return await self.futures[req_id]

    async def handle_page_event(self, msg):
        # adapted from https://github.com/elimintz/justpy/discussions/240
        if msg.event_type != 'result_ready':
            return False
        if not msg.request_id in self.futures:
            return False
        fut = self.futures[msg.request_id]
        self.futures.pop(msg.request_id)
        if not fut.cancelled():
            fut.set_result(msg.result.copy())
        return True

    async def add(self, websocket, data):
        '''Add elements to the graph'''
        return await self.run_method(f'add({data})', websocket)

    def convert_object_to_dict(self):
        d = {}
        d['vue_type'] = self.vue_type
        d['id'] = self.id
        d['show'] = self.show
        d['classes'] = self.classes
        d['style'] = self.style
        d['elements'] = self.elements
        d['graphstyle'] = self.graphstyle
        d['layout'] = self.layout
        d['plugins'] = self.plugins
        d['event_propagation'] = self.event_propagation
        d['def'] = self.options
        d['events'] = self.events
        d['clear'] = self.clear
        d['options'] = self.options
        return d
