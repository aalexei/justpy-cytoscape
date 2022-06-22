import justpy as jp

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
        self.layout = {}
        self.clear = False
        self.show = True
        self.event_propagation = True
        self.pages = {}
        kwargs['temp'] = False  # Force an id to be assigned
        super().__init__(**kwargs)
        self.allowed_events = ['onEnd', 'onBegin', 'onJson']
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

        #await webpage.run_javascript(method,request_id=req_id,send=True)
        await websocket.send_json(
            {'type': 'run_javascript',
             'data':f"Object({{value:comp_dict['{self.id}'].{method}}})",
             'request_id': req_id,
             'send':True}
        )

        result = await self.futures[req_id]
        return result['value']

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

    async def reset(self, websocket):
        '''Reset the graph to the default zoom level and panning position.'''
        return await self.run_method('reset()', websocket)

    async def fit(self, websocket):
        '''Pan and zooms the graph to fit to a collection.'''
        return await self.run_method('fit()', websocket)

    async def center(self, websocket):
        '''Centre on all elements in the graph.'''
        return await self.run_method('center()', websocket)

    async def pan(self, x, y, websocket):
        '''Set the current panning position to (x,y)'''
        return await self.run_method(f'pan({{x:{x}, y:{y}}})', websocket)

    async def panBy(self, x, y, websocket):
        '''Shift rendered position by vector (x,y)'''
        return await self.run_method(f'panBy({{x:{x}, y:{y}}})', websocket)

    async def add(self, data, websocket):
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
        d['event_propagation'] = self.event_propagation
        d['def'] = self.options
        d['events'] = self.events
        d['clear'] = self.clear
        d['options'] = self.options
        return d
