Vue.component('cytoscapejp', {
    template:
    `<div  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style"></div>`,
    methods: {
        graph_create() {
            this.elements = this.$props.jp_props.elements;
            cyto = new cytoscape({
                container: document.getElementById(this.$props.jp_props.id.toString()), // container to render in
                elements: this.$props.jp_props.elements,
                style: this.$props.jp_props.graphstyle,
                layout: this.$props.jp_props.layout
            });
            // Register component
            comp_dict[this.$props.jp_props.id] = cyto;

            // Bind events
            // console.log('events:',this.$props.jp_props.events);
            var events = this.$props.jp_props.events;
            var props = this.$props;
            events.forEach(function(ename){
                // console.log('Binding event:',ename);
                cyto.on(ename, function(ev){
                    var target = ev.target;
                    // console.log('sending cyto event:', ev.type, target, ev);
                    const edata = {
                        'event_type': ename,
                        'target_id': null,
                        'id': props.jp_props.id,
                        'page_id': page_id,
                        'websocket_id': websocket_id
                    };
                    // Add target_id if it exists
                    try { edata.target_id = target.id() }
                    catch (err) {}
                    send_to_server(edata, 'event');
                });
            });

            this.$props.jp_props.plugins.forEach(function(plugin_config){
                //try { edata.target_id = target.id() }
                //console.log('plugin_config:',plugin_config);
                eval(plugin_config);
                //}
                // catch (err) {}
            });
        }
    },
    mounted() {
        var cyto; // create a global variable to debug on console
        this.graph_create();
    },
    updated() {
    },
    props: {
        jp_props: Object
    }
});
