import justpy as jp

class Cytoscape(jp.JustpyBaseComponent):

    vue_type = 'cytoscapejs'

    def __init__(self, **kwargs):

        self.options = jp.Dict()
        self.classes = ''
        self.style = ''
        self.width = 400
        self.height = 200
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

    def convert_object_to_dict(self):
        d = {}
        d['vue_type'] = self.vue_type
        d['id'] = self.id
        d['show'] = self.show
        d['classes'] = self.classes
        d['style'] = self.style
        d['event_propagation'] = self.event_propagation
        d['def'] = self.options
        d['events'] = self.events
        d['width'] = self.width
        d['height'] = self.height
        d['clear'] = self.clear
        d['options'] = self.options
        return d

