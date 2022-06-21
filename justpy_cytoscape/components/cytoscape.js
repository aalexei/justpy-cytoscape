Vue.component('cytoscapejp', {
    template:
    `<div  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style"></div>`,
    data: function () {
        return {
            graph: null
        }
    },
    methods: {
        graph_create() {
            var cy = new cytoscape({
                container: document.getElementById(this.$props.jp_props.id.toString()), // container to render in
                elements: this.$props.jp_props.elements,
                style: this.$props.jp_props.graphstyle,
                layout: this.$props.jp_props.layout
            });
            // Register component
            comp_dict[this.$props.jp_props.id] = cy;

            var events = this.$props.jp_props.events;
            var props = this.$props;
            function onJson() {
                    if (events.includes('onJson')) {
                        var data = cy.json();
                        var e = {
                            'event_type': 'onJson',
                            'id': props.jp_props.id,
                            'class_name': props.jp_props.class_name,
                            'html_tag': props.jp_props.html_tag,
                            'vue_type': props.jp_props.vue_type,
                            'page_id': page_id,
                            'websocket_id': websocket_id,
                            'data': data
                        };
                        send_to_server(e, 'event');
                    }
            };

            cy.onJson = onJson;
        }
    },
    mounted() {
        this.graph_create();
    },
    updated() {
        if (this.graph != this.$props.jp_props.graph) {
            this.graph_create();
        }
    },
    props: {
        jp_props: Object
    }
});
