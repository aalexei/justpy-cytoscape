import justpy as jp

class Cytoscape(jp.JustpyBaseComponent):

    vue_type = 'cytoscapejp'

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
        self.allowed_events = ['onEnd', 'onBegin']
        if type(self.options) != jp.Dict:
            self.options = jp.Dict(self.options)
        self.initialize(**kwargs)

    def add_to_page(self, wp: jp.WebPage):
        wp.add_component(self)

    def react(self, data):
        pass

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
